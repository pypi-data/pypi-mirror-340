# === File: act/execution_manager.py ===

import importlib
import traceback
import logging
import json
from typing import Callable, Dict, Any, List, Optional, Type, Tuple, Union # Added Union
import asyncio
from datetime import datetime, timedelta
import re
import os
from pathlib import Path
import inspect
import sys
import copy # Import copy for deep copying if needed later

# Third-party libraries
try:
    from colorama import init, Fore, Style
    init(autoreset=True) # Autoreset style after each print
except ImportError:
    print("Warning: colorama not found. Colors will not be used in output.")
    # Define dummy Fore/Style if needed
    class DummyStyle:
        def __getattr__(self, name): return ""
    Fore = DummyStyle()
    Style = DummyStyle()

try:
    from tabulate import tabulate
except ImportError:
    print("Warning: tabulate not found. Status tables will be basic.")
    # Dummy tabulate function if library is missing
    def tabulate(table_data, headers, tablefmt):
        # Basic non-library formatting
        if not table_data: return "No data to display."
        # Get column widths based on headers and data
        widths = [len(h) for h in headers]
        for row in table_data:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))
        # Create separator line
        sep = "+".join("-" * (w + 2) for w in widths)
        # Format header
        header_line = "|" + "|".join(f" {h:<{widths[i]}} " for i, h in enumerate(headers)) + "|"
        # Format data rows
        data_lines = [
            "|" + "|".join(f" {str(cell):<{widths[i]}} " for i, cell in enumerate(row)) + "|"
            for row in table_data
        ]
        return "\n".join([sep, header_line, sep] + data_lines + [sep])


# --- Custom Exception Definitions ---
# Define the missing exception classes that inherit from Exception
class NodeExecutionError(Exception):
    """Custom exception for errors during node execution."""
    pass

class NodeValidationError(Exception):
    """Custom exception for errors during node validation or parameter issues."""
    pass

# --- End Custom Exception Definitions ---


# Relative imports (assuming package structure)
try:
    from .actfile_parser import ActfileParser, ActfileParserError
    # Import BaseNode if needed for type checking during discovery
    from .nodes.base_node import BaseNode
    # Import GenericNode if fallback is desired
    # from .nodes.GenericNode import GenericNode
except ImportError as e:
    # Handle cases where script might be run standalone or package isn't set up
    print(f"Warning: Relative import failed ({e}). Attempting direct imports or using placeholders.")
    # Add sys.path manipulation or alternative import strategies if necessary
    # Or define dummy classes for basic functionality:
    class ActfileParserError(Exception): pass # Keep this dummy definition as fallback
    class ActfileParser:
        def __init__(self, path): self.path = path; logger.warning("Using dummy ActfileParser.")
        def parse(self): logger.warning("Using dummy ActfileParser.parse()"); return {'workflow': {'start_node': None, 'name': 'DummyFlow'}, 'nodes': {}, 'edges': {}}
        def get_start_node(self): return None
        def get_node_successors(self, node_name): return []
        def get_workflow_name(self): return "DummyFlow"
    class BaseNode: pass
    # class GenericNode(BaseNode): pass


# Configure logging
# Use DEBUG level to see detailed fetch_value/resolve logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s [%(levelname)s] - %(message)s') # Changed to INFO for less noise usually
logger = logging.getLogger(__name__) # Logger specific to this module

# --- ExecutionManager Class ---

class ExecutionManager:
    """
    Manages the loading, resolution, and execution of workflows defined in Actfiles.
    Handles node discovery, placeholder resolution (including initial input),
    and sequential execution based on defined edges (with placeholder for conditional logic).
    """
    def __init__(self, actfile_path: Union[str, Path] = 'Actfile', sandbox_timeout: int = 600):
        """
        Initializes the ExecutionManager.

        Args:
            actfile_path: Path to the Actfile definition.
            sandbox_timeout: Maximum execution time for the workflow in seconds (0 for no timeout).
        """
        logger.info(f"Initializing ExecutionManager with Actfile: {actfile_path}")
        self.actfile_path = Path(actfile_path) # Ensure it's a Path object
        self.sandbox_timeout = sandbox_timeout
        self.node_results: Dict[str, Any] = {}
        self.sandbox_start_time: Optional[datetime] = None
        self.node_loading_status: Dict[str, Dict[str, str]] = {}

        # Track node execution status
        self.node_execution_status: Dict[str, Dict[str, Any]] = {}
        self.current_execution_id: Optional[str] = None
        self.status_callbacks: List[Callable] = []

        # Store initial workflow input data (will be populated by execute_workflow)
        self.initial_input_data: Dict[str, Any] = {}

        # Store parsed workflow data and the parser instance
        self.workflow_data: Dict[str, Any] = {}
        self.actfile_parser: Optional[ActfileParser] = None
        self.node_executors: Dict[str, Any] = {} # Stores instantiated node objects

        # Load workflow data and node executors during initialization
        try:
            self.load_workflow()
        except (FileNotFoundError, ActfileParserError) as e:
            logger.error(f"Failed to initialize ExecutionManager: {e}")
            # Decide if initialization should fail completely or continue in a degraded state
            raise # Re-raise the error to prevent using a non-functional manager

    # --- Status Reporting ---

    def register_status_callback(self, callback: Callable):
        """Registers a callback function to receive status updates during execution."""
        if callable(callback):
            self.status_callbacks.append(callback)
            logger.debug(f"Registered status callback: {getattr(callback, '__name__', 'anonymous')}")
        else:
            logger.warning("Attempted to register a non-callable status callback.")

    def update_node_status(self, node_name: str, status: str, message: str = ""):
        """Updates the status of a node and notifies all registered callbacks."""
        timestamp = datetime.now().isoformat()
        status_entry = {
            "status": status,
            "message": message,
            "timestamp": timestamp
        }
        self.node_execution_status[node_name] = status_entry
        # Use INFO level for status updates for better visibility
        logger.info(f"Node '{node_name}' Status -> {status.upper()}: {message[:100] + ('...' if len(message)>100 else '')}") # Limit message length in log

        # Notify all registered callbacks
        for callback in self.status_callbacks:
            try:
                # Consider if callbacks should be async if they perform I/O
                callback(node_name, status, message, self.node_execution_status)
            except Exception as e:
                logger.error(f"Error in status callback '{getattr(callback, '__name__', 'anonymous')}': {e}", exc_info=True)

    def get_execution_status(self) -> Dict[str, Any]:
        """Returns the current execution status including results and configuration."""
        wf_name = "N/A"
        if self.actfile_parser and hasattr(self.actfile_parser, 'get_workflow_name'):
             wf_name = self.actfile_parser.get_workflow_name() or "N/A"

        return {
            "execution_id": self.current_execution_id,
            "node_status": self.node_execution_status,
            "results": self.node_results,
            "initial_input": self.initial_input_data, # Include for context
            "workflow_name": wf_name
        }

    # --- Workflow Loading and Node Discovery ---

    def load_workflow(self):
        """Loads the workflow data using ActfileParser and loads node executors."""
        logger.info(f"Loading workflow data from: {self.actfile_path}")
        if not self.actfile_path.is_file():
             error_msg = f"Actfile not found at path: {self.actfile_path}"
             logger.error(error_msg)
             raise FileNotFoundError(error_msg)

        try:
            self.actfile_parser = ActfileParser(self.actfile_path)
            self.workflow_data = self.actfile_parser.parse() # Parsing happens here
            logger.info("Actfile parsed successfully.")
            if not self.workflow_data.get('nodes'):
                 logger.warning("Actfile parsed but contains no 'nodes' section.")

        except ActfileParserError as e:
            logger.error(f"Error parsing Actfile: {e}")
            self.workflow_data = {} # Ensure data is cleared on error
            self.actfile_parser = None
            raise # Re-raise parsing error
        except Exception as e:
            logger.error(f"Unexpected error during Actfile parsing: {e}", exc_info=True)
            self.workflow_data = {}
            self.actfile_parser = None
            raise ActfileParserError(f"Unexpected error during parsing: {e}") # Wrap error

        # Load executors only after successful parsing
        if self.workflow_data:
            self.load_node_executors()
        else:
            logger.warning("Skipping node executor loading due to parsing failure.")


    def discover_node_classes(self) -> Dict[str, Type]:
        """
        Discovers available BaseNode subclasses from the 'act.nodes' package.

        Returns:
            A dictionary mapping discovered node type strings to their class objects.
        """
        node_classes: Dict[str, Type] = {}
        nodes_package_name = "act.nodes" # TODO: Make this configurable?

        try:
            nodes_module = importlib.import_module(nodes_package_name)
            # Find the directory of the nodes package
            package_path = getattr(nodes_module, '__path__', None)
            if not package_path: # Fallback if __path__ isn't available (e.g., single file module)
                 package_file = inspect.getfile(nodes_module)
                 nodes_dir = Path(package_file).parent
            else:
                 nodes_dir = Path(package_path[0]) # Use first path if multiple exist

            logger.info(f"Scanning nodes directory: {nodes_dir}")
        except (ImportError, TypeError, AttributeError, FileNotFoundError) as e:
            logger.error(f"Could not import or find nodes package '{nodes_package_name}' at expected location: {e}", exc_info=True)
            # Attempt fallback relative to this file (less reliable)
            try:
                nodes_dir = Path(__file__).parent / "nodes"
                if not nodes_dir.is_dir(): raise FileNotFoundError
                logger.info(f"Falling back to scanning nodes directory: {nodes_dir}")
            except Exception:
                logger.error("Nodes directory could not be located. Node discovery aborted.")
                return {}

        # --- Node Registry (Optional) ---
        registry_module_name = f"{nodes_package_name}.node_registry"
        try:
            registry_module = importlib.import_module(registry_module_name)
            registry = getattr(registry_module, 'NODES', None) or getattr(registry_module, 'NODE_REGISTRY', None)
            if isinstance(registry, dict):
                logger.info(f"Found node registry '{registry_module_name}' with {len(registry)} nodes")
                node_classes.update(registry)
            else: logger.debug(f"No NODES/NODE_REGISTRY dict found in {registry_module_name}")
        except (ImportError, AttributeError) as e:
            logger.debug(f"Node registry {registry_module_name} not found or error loading: {e}")

        # --- Dynamic Discovery from Files ---
        node_files: Dict[str, Path] = {}
        logger.debug(f"Globbing for Python files in {nodes_dir}")
        for file_path in nodes_dir.glob('*.py'):
            module_name = file_path.stem
            if file_path.name.startswith('__') or module_name.lower() in ('base_node', 'node_registry'):
                logger.debug(f"Skipping file: {file_path.name}")
                continue
            logger.debug(f"Found potential node file: {module_name}")
            node_files[module_name] = file_path

        if node_files: logger.info(f"Found {len(node_files)} potential node files for dynamic loading.")
        else: logger.info("No additional node files found for dynamic loading.")

        # Process each potential node file
        # Make sure BaseNode is imported for issubclass check
        # from .nodes.base_node import BaseNode (already imported above via try/except)

        for module_name, file_path in node_files.items():
            try:
                full_module_name = f"{nodes_package_name}.{module_name}"
                logger.debug(f"Importing module: {full_module_name}")
                module = importlib.import_module(full_module_name)

                for attr_name, attr_value in inspect.getmembers(module, inspect.isclass):
                    # Check if it's a non-abstract subclass of BaseNode
                    if issubclass(attr_value, BaseNode) and attr_value is not BaseNode and not inspect.isabstract(attr_value):
                        node_class = attr_value
                        node_type = self._determine_node_type(node_class, attr_name, module_name)

                        if node_type and node_type not in node_classes:
                             logger.info(f"Discovered node class {attr_name} -> type '{node_type}'")
                             node_classes[node_type] = node_class
                        elif node_type and node_type in node_classes:
                             logger.debug(f"Node type '{node_type}' from {attr_name} already registered, skipping dynamic load.")
                        elif not node_type:
                             logger.warning(f"Could not determine node type for class {attr_name} in {module_name}.")
            except Exception as e:
                logger.error(f"Error processing node file {module_name} ({file_path}): {e}", exc_info=True)

        logger.info(f"Node discovery finished. Total distinct node types found: {len(node_classes)}")
        return node_classes

    def _determine_node_type(self, node_class: Type, class_name: str, module_name: str) -> Optional[str]:
        """Helper to determine the node type string from schema or class name."""
        node_type = None
        # 1. Try getting from schema (assuming schema has 'node_type' attribute or class variable)
        try:
            schema_node_type = getattr(node_class, 'node_type', None) # Check class variable first
            if schema_node_type and isinstance(schema_node_type, str):
                node_type = schema_node_type
                logger.debug(f"Using node_type '{node_type}' from class variable for class {class_name}")
                return node_type

            if hasattr(node_class, 'get_schema'):
                 # Complex logic for calling get_schema if needed, simplified here
                 logger.debug(f"Class {class_name} has get_schema method (not used for type determination currently).")
                 pass # get_schema might be for parameters, not the type itself

        except Exception as e: logger.warning(f"Error checking node_type/schema for {class_name}: {e}")

        # 2. Fallback to class name conversion
        if class_name.endswith('Node'): node_type = self._snake_case(class_name[:-4])
        else: node_type = self._snake_case(class_name)
        logger.debug(f"Using derived node_type '{node_type}' from class name {class_name}")
        return node_type


    def load_node_executors(self):
        """Instantiates node executor classes required by the current workflow."""
        logger.info("Loading node executors for the current workflow...")
        if not self.workflow_data or 'nodes' not in self.workflow_data:
             logger.error("Cannot load node executors: Workflow data is not loaded or empty.")
             return

        node_types_in_workflow = set(
            node_config.get('type') for node_config in self.workflow_data['nodes'].values() if node_config.get('type')
        )
        if not node_types_in_workflow: logger.warning("No node types found in the current workflow definition."); return

        logger.info(f"Workflow requires node types: {', '.join(sorted(list(node_types_in_workflow)))}")
        self.node_executors = {}
        self.node_loading_status = {node_type: {'status': 'pending', 'message': ''} for node_type in node_types_in_workflow}
        all_available_node_classes = self.discover_node_classes()
        logger.info(f"Discovered {len(all_available_node_classes)} potentially available node types.")

        for node_type in node_types_in_workflow:
            node_class = None; load_message = ""; status = "error"
            node_class = all_available_node_classes.get(node_type)
            if node_class: load_message = f"Found exact match: class {node_class.__name__}"; logger.debug(f"Found exact match for '{node_type}': {node_class.__name__}")
            else:
                logger.debug(f"No exact match for '{node_type}', checking case-insensitive...")
                for available_type, klass in all_available_node_classes.items():
                    if available_type.lower() == node_type.lower():
                        node_class = klass; load_message = f"Found case-insensitive match: type '{available_type}' (class {node_class.__name__})"; logger.debug(f"Found case-insensitive match for '{node_type}': Using type '{available_type}' ({node_class.__name__})"); break
                if not node_class: load_message = "No suitable node class found."; logger.warning(f"Could not find class for node type: '{node_type}'.")

            if node_class:
                try:
                    node_instance = self._instantiate_node(node_class)
                    if node_instance: self.node_executors[node_type] = node_instance; status = 'success'; load_message += " -> Instantiated successfully."; logger.info(f"Successfully loaded executor for '{node_type}'.")
                    else: status = 'error'; load_message += " -> Instantiation failed (returned None)."; logger.error(f"Instantiation of {node_class.__name__} for '{node_type}' returned None.")
                except Exception as e: status = 'error'; load_message += f" -> Instantiation error: {e}"; logger.error(f"Error instantiating {node_class.__name__} for '{node_type}': {e}", exc_info=True)

            self.node_loading_status[node_type]['status'] = status; self.node_loading_status[node_type]['message'] = load_message

            # Optional Fallback to GenericNode (Ensure GenericNode is discovered and imported)
            # if status == 'error':
            #     generic_node_type_name = 'generic_node'; # Example type name for GenericNode
            #     generic_node_class = all_available_node_classes.get(generic_node_type_name)
            #     if generic_node_class:
            #          logger.warning(f"Attempting fallback to {generic_node_class.__name__} for type '{node_type}'.")
            #          try:
            #              generic_instance = self._instantiate_node(generic_node_class); self.node_executors[node_type] = generic_instance; self.node_loading_status[node_type]['status'] = 'fallback'; self.node_loading_status[node_type]['message'] += f" | Fallback to {generic_node_class.__name__} successful."; logger.info(f"Using {generic_node_class.__name__} fallback for type '{node_type}'.")
            #          except Exception as e: logger.error(f"Error instantiating {generic_node_class.__name__} fallback for '{node_type}': {e}", exc_info=True); self.node_loading_status[node_type]['status'] = 'error'; self.node_loading_status[node_type]['message'] += f" | Fallback failed: {generic_node_class.__name__} instantiation error: {e}."
            #     else: logger.error(f"GenericNode (type '{generic_node_type_name}') not found for fallback! Node type '{node_type}' will be unavailable."); self.node_loading_status[node_type]['status'] = 'error'; self.node_loading_status[node_type]['message'] += f" | Fallback failed: GenericNode not found."

        self._print_node_loading_status()

    def _print_node_loading_status(self):
        """Prints a formatted table showing the loading status of required nodes."""
        if not self.node_loading_status: print("\nNo nodes required by workflow or loading not performed.\n"); return
        headers = ["Required Node Type", "Loading Status", "Details"]; table_data = []
        for node_type, status_info in sorted(self.node_loading_status.items()):
            status = status_info['status']; message = status_info['message']
            if status == 'success': status_symbol, color = "🟢", Fore.GREEN
            elif status == 'fallback': status_symbol, color = "🟡", Fore.YELLOW
            elif status == 'error': status_symbol, color = "🔴", Fore.RED
            else: status_symbol, color = "⚪", Fore.WHITE
            table_data.append([node_type, f"{color}{status_symbol} {status.upper()}{Style.RESET_ALL}", message])
        try:
            table = tabulate(table_data, headers=headers, tablefmt="grid", maxcolwidths=[None, 15, 80])
        except NameError: # Fallback if tabulate is dummy
             table = self._basic_table(table_data, headers)
        print("\n--- Node Executor Loading Status ---\n" + table + "\n------------------------------------\n")

    def _basic_table(self, data, headers):
         """Minimal text table formatting if tabulate is unavailable."""
         if not data: return "No data."
         widths = [len(h) for h in headers]
         for row in data:
             for i, cell in enumerate(row): widths[i] = max(widths[i], len(str(cell)))
         sep = "+".join("-" * (w + 2) for w in widths)
         header_line = "|" + "|".join(f" {h:<{widths[i]}} " for i, h in enumerate(headers)) + "|"
         data_lines = [ "|" + "|".join(f" {str(cell):<{widths[i]}} " for i, cell in enumerate(row)) + "|" for row in data ]
         return "\n".join([sep, header_line, sep] + data_lines + [sep])


    def _instantiate_node(self, node_class: Type) -> Any:
        """Instantiates a node class, handles sandbox_timeout, sets execution_manager."""
        logger.debug(f"Instantiating node class: {node_class.__name__}")
        try:
            # Simpler instantiation, assuming BaseNode handles common args or uses kwargs
            node_instance = node_class()

            # Set execution manager if method exists
            set_manager_method = getattr(node_instance, 'set_execution_manager', None)
            if callable(set_manager_method):
                logger.debug(f"Setting execution manager for instance of {node_class.__name__}")
                set_manager_method(self)

            # Set sandbox timeout if method exists (optional)
            set_timeout_method = getattr(node_instance, 'set_sandbox_timeout', None)
            if callable(set_timeout_method):
                logger.debug(f"Setting sandbox timeout ({self.sandbox_timeout}s) for instance of {node_class.__name__}")
                set_timeout_method(self.sandbox_timeout)

            return node_instance
        except Exception as e:
            logger.error(f"Failed to instantiate {node_class.__name__}: {e}", exc_info=True)
            raise # Re-raise the instantiation error


    # --- Workflow Execution ---

    def execute_workflow(self,
                         execution_id: Optional[str] = None,
                         initial_input: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes the loaded workflow synchronously. Accepts initial input data.
        Manages the async execution loop internally using asyncio.run().
        """
        self.current_execution_id = execution_id or f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        logger.info(f"Starting synchronous execution wrapper for workflow ID: {self.current_execution_id}")
        self.node_results = {}; self.node_execution_status = {}
        # Store a shallow copy - consider deepcopy if inputs are complex/mutable and modified by nodes
        self.initial_input_data = dict(initial_input) if initial_input else {}
        logger.debug(f"Stored initial input data for run {self.current_execution_id}: {self.log_safe_node_data(self.initial_input_data)}")

        if self.workflow_data and 'nodes' in self.workflow_data:
             for node_name in self.workflow_data['nodes'].keys(): self.update_node_status(node_name, "pending", "Waiting for execution")
        else:
             logger.error("Cannot execute workflow: Workflow data not loaded or missing nodes.")
             # Add status update for a 'workflow' meta-node if desired
             # self.update_node_status("__workflow__", "error", "Workflow data not loaded/invalid.")
             return {"status": "error", "message": "Workflow data not loaded/invalid.", "results": {}, "node_status": self.node_execution_status}

        try:
             result = asyncio.run(self.execute_workflow_async())
             logger.info(f"Workflow {self.current_execution_id} execution finished.")
             self._print_node_execution_results(); return result # Print summary after completion
        except Exception as e:
             logger.error(f"Critical error during workflow execution run: {e}", exc_info=True)
             self._print_node_execution_results() # Print status on error
             # Update status for a 'workflow' meta-node
             # self.update_node_status("__workflow__", "error", f"Workflow execution failed: {e}")
             return {"status": "error", "message": f"Workflow execution failed with unexpected error: {e}", "results": self.node_results, "node_status": self.node_execution_status}

    async def execute_workflow_async(self) -> Dict[str, Any]:
        """
        Asynchronously executes the workflow step-by-step based on Actfile edges.
        Handles node execution, result storage, status updates, and timeout checks.
        Uses the stored `self.initial_input_data` for placeholder resolution context.
        Includes placeholder for conditional logic based on If/Switch nodes.
        """
        exec_id = self.current_execution_id
        logger.info(f"Starting ASYNC execution of workflow ID: {exec_id}")
        logger.debug(f"Initial input data for this run: {self.log_safe_node_data(self.initial_input_data)}")

        if not self.actfile_parser:
            logger.error("Cannot execute async workflow: Actfile parser not available.")
            return {"status": "error", "message": "Actfile parser not initialized.", "results": {}, "node_status": self.node_execution_status}

        self.sandbox_start_time = datetime.now()
        execution_queue: List[Tuple[str, Optional[Dict[str, Any]]]] = []
        executed_nodes = set()

        try:
            start_node_name = self.actfile_parser.get_start_node()
            if not start_node_name:
                logger.error("No start node specified.")
                return {"status": "error", "message": "No start node specified.", "results": {}, "node_status": self.node_execution_status}
            if start_node_name not in self.workflow_data.get('nodes', {}):
                error_msg = f"Start node '{start_node_name}' not defined in workflow nodes."
                logger.error(error_msg)
                return {"status": "error", "message": error_msg, "results": {}, "node_status": self.node_execution_status}

            logger.info(f"Workflow starting at node: {start_node_name}")
            execution_queue.append((start_node_name, None))

            # --- Main Execution Loop ---
            while execution_queue:
                # Check timeout at the beginning of each iteration
                if self.sandbox_timeout > 0 and (datetime.now() - self.sandbox_start_time).total_seconds() > self.sandbox_timeout:
                    timeout_msg = f"Workflow timeout ({self.sandbox_timeout}s) exceeded."
                    logger.error(timeout_msg)
                    # Try to update the status of the node that *would* have run
                    node_about_to_run = execution_queue[0][0] if execution_queue else "N/A"
                    self.update_node_status(node_about_to_run, "error", f"Timeout before execution: {timeout_msg}")
                    return {"status": "error", "message": timeout_msg, "results": self.node_results, "node_status": self.node_execution_status}

                node_name, previous_node_result = execution_queue.pop(0)

                # Skip if already executed (important for loops/merges)
                if node_name in executed_nodes:
                    logger.info(f"Node '{node_name}' already executed. Skipping to avoid cycle issues.")
                    continue

                # Check if node exists before executing (safety check)
                if node_name not in self.workflow_data.get('nodes', {}):
                    logger.error(f"Node '{node_name}' scheduled but not found in workflow definition. Stopping.")
                    return {"status": "error", "message": f"Node '{node_name}' not found in workflow definition.", "results": self.node_results, "node_status": self.node_execution_status}


                logger.info(f"--- Executing Node: {node_name} ---")
                executed_nodes.add(node_name) # Mark as executed *before* await
                self.update_node_status(node_name, "running", "Node execution started")

                # Execute the node
                node_result = await self.execute_node_async(node_name, input_context=previous_node_result)
                self.node_results[node_name] = node_result # Store result immediately

                # --- Handle Node Result ---
                if node_result.get('status') == 'error':
                    error_msg = node_result.get('message', 'Unknown node error')
                    logger.error(f"Node '{node_name}' failed: {error_msg}. Stopping workflow.")
                    # Status already updated by execute_node_async on error
                    return {"status": "error", "message": f"Workflow failed at node '{node_name}': {error_msg}", "results": self.node_results, "node_status": self.node_execution_status}
                else:
                    logger.info(f"Node '{node_name}' finished with status: {node_result.get('status', 'unknown')}")
                    # Status already updated by execute_node_async on success/warning


                # --- Queue Successors (Conditional Logic) ---
                all_successors = self.actfile_parser.get_node_successors(node_name)
                logger.debug(f"Potential successors for '{node_name}': {all_successors}")
                current_node_type = self.workflow_data['nodes'][node_name].get('type')
                nodes_to_queue = []

                # --- >>> START CONDITIONAL LOGIC AREA <<< ---
                # Retrieve result data carefully
                result_data = node_result.get('result', {}) if isinstance(node_result, dict) else {}

                if current_node_type == 'if':
                    # Expect 'result' boolean directly inside 'result' dict
                    condition_outcome = result_data.get('result') if isinstance(result_data, dict) else None
                    if isinstance(condition_outcome, bool):
                        logger.info(f"IfNode '{node_name}' result: {condition_outcome}. Applying conditional branching (Convention: 1st=True, 2nd=False).")
                        true_target = all_successors[0] if len(all_successors) > 0 else None
                        false_target = all_successors[1] if len(all_successors) > 1 else None
                        target_node_name = true_target if condition_outcome else false_target
                        if target_node_name: nodes_to_queue.append(target_node_name)
                        elif condition_outcome and not true_target: logger.warning(f"IfNode '{node_name}' was True, but no 'True' path (1st successor) defined.")
                        elif not condition_outcome and not false_target: logger.warning(f"IfNode '{node_name}' was False, but no 'False' path (2nd successor) defined.")
                        else: logger.info(f"No specific conditional target determined for IfNode '{node_name}'. Path ends.")
                    else:
                        logger.error(f"IfNode '{node_name}' did not return a boolean 'result' in its result data. Cannot branch. Result data: {result_data}")

                elif current_node_type == 'switch':
                     # Expect 'selected_node' string inside 'result' dict
                     target_node_name = result_data.get('selected_node') if isinstance(result_data, dict) else None
                     if isinstance(target_node_name, str) and target_node_name:
                         logger.info(f"SwitchNode '{node_name}' selected target: '{target_node_name}'.")
                         nodes_to_queue.append(target_node_name)
                     elif target_node_name is None or target_node_name == "":
                         logger.info(f"SwitchNode '{node_name}' selected no target (no match/default or empty string). Path ends.")
                     else:
                         logger.error(f"SwitchNode '{node_name}' did not return a valid string 'selected_node' in its result data. Cannot branch. Result data: {result_data}")

                else: # Default: Queue all direct successors
                     logger.debug(f"Queueing all defined direct successors for non-conditional node '{node_name}'")
                     nodes_to_queue.extend(all_successors)
                # --- >>> END CONDITIONAL LOGIC AREA <<< ---

                # Add selected nodes to the queue after filtering out invalid/already queued ones
                for successor_name in nodes_to_queue:
                     if not successor_name: continue # Skip empty target names
                     if successor_name not in self.workflow_data.get('nodes', {}):
                         logger.warning(f"Target node '{successor_name}' from node '{node_name}' branch not defined in workflow. Skipping.")
                         continue
                     # Skip if already executed *unless* loops are explicitly allowed (not handled here)
                     # if successor_name in executed_nodes:
                     #     logger.debug(f"Target node '{successor_name}' already executed. Skipping cycle.")
                     #     continue
                     if any(item[0] == successor_name for item in execution_queue):
                         logger.debug(f"Target node '{successor_name}' already in queue. Skipping.")
                         continue
                     logger.info(f"Queueing next node: '{successor_name}'")
                     execution_queue.append((successor_name, node_result))

            # Loop finished successfully
            logger.info(f"Workflow execution completed successfully for ID: {exec_id}")
            return {"status": "success", "message": "Workflow executed successfully", "results": self.node_results, "node_status": self.node_execution_status}

        except Exception as e:
            logger.error(f"Unexpected error during workflow execution loop for {exec_id}: {e}", exc_info=True)
            # Try to identify the last node being processed if possible
            last_node = locals().get('node_name', 'N/A')
            self.update_node_status(last_node, "error", f"Workflow loop error: {e}")
            return {"status": "error", "message": f"Workflow failed unexpectedly: {e}", "results": self.node_results, "node_status": self.node_execution_status}

    async def execute_node_async(self, node_name: str, input_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Executes a single node: gets config, resolves placeholders, prepares data, calls executor."""
        logger.debug(f"Preparing to execute node: {node_name}")
        try:
            # 1. Get Config & Basic Validation
            if not self.workflow_data or node_name not in self.workflow_data.get('nodes', {}):
                raise NodeExecutionError(f"Node '{node_name}' configuration not found in workflow data.")
            node_config = self.workflow_data['nodes'][node_name].copy() # Use copy to avoid modifying original
            node_type = node_config.get('type')
            if not node_type:
                raise NodeExecutionError(f"Node '{node_name}' definition is missing the required 'type' field.")

            # Add previous result to config temporarily for resolution context if needed
            # if input_context:
            #     node_config['__previous_result'] = input_context # Potential data leak if not careful

            # 2. Resolve Placeholders (More Robustly)
            logger.debug(f"Resolving placeholders for '{node_name}' config (type: {node_type})...")
            try:
                resolved_node_config = self.resolve_placeholders_for_execution(node_config)
                logger.debug(f"'{node_name}' config AFTER resolving: {self.log_safe_node_data(resolved_node_config)}")
            except Exception as resolve_err:
                raise NodeExecutionError(f"Failed to resolve placeholders for node '{node_name}': {resolve_err}") from resolve_err


            # 3. Prepare Data for Executor
            processed_data = self._process_node_parameters(resolved_node_config)
            executor_data = self._structure_data_for_executor(processed_data, node_name)
            logger.debug(f"Final data for executor '{node_name}': {self.log_safe_node_data(executor_data)}")

            # 4. Get Executor Instance
            executor = self.node_executors.get(node_type)
            if not executor:
                # This error should ideally be caught during load_node_executors, but double-check
                raise NodeExecutionError(f"No executor instance loaded for type '{node_type}' (node: '{node_name}'). Check node loading status.")

            # 5. Execute Node Logic
            logger.info(f"Calling {type(executor).__name__}.execute for node '{node_name}'")
            execute_method = getattr(executor, 'execute', None)
            if not callable(execute_method):
                raise NodeExecutionError(f"Executor for node type '{node_type}' (class {type(executor).__name__}) has no callable 'execute' method.")

            node_result = None
            try:
                if inspect.iscoroutinefunction(execute_method):
                    node_result = await execute_method(executor_data)
                else:
                    # Note: Running sync code in async loop can block. Use asyncio.to_thread if needed.
                    logger.warning(f"Executing potentially blocking sync node '{node_name}' ({node_type}). Consider making its execute method async or using asyncio.to_thread.")
                    node_result = execute_method(executor_data)
                # Handle cases where sync function returns awaitable by mistake
                if inspect.iscoroutine(node_result):
                    logger.warning(f"Sync execute for '{node_name}' returned an awaitable. Awaiting it.")
                    node_result = await node_result
            except Exception as exec_err:
                 # Catch errors *during* the node's execute() call
                 raise NodeExecutionError(f"Error during {node_type}.execute(): {exec_err}") from exec_err


            # 6. Process and Validate Result Structure
            logger.info(f"Node '{node_name}' raw result: {self.log_safe_node_data(node_result)}")
            if not isinstance(node_result, dict) or 'status' not in node_result:
                 logger.warning(f"Node '{node_name}' result is not a dict or missing 'status'. Wrapping. Original result: {node_result}")
                 final_result = {
                     "status": "warning",
                     "message": "Node returned unexpected result format (missing dict structure or status key).",
                     "result": node_result # Preserve original result under 'result' key
                 }
            else:
                final_result = node_result # Use the result directly if structure is okay

            node_status = final_result.get('status', 'error') # Default to error if status somehow gets removed
            node_message = final_result.get('message', '')

            # Validate status value
            valid_statuses = ['success', 'error', 'warning']
            if node_status not in valid_statuses:
                 logger.warning(f"Node '{node_name}' returned invalid status '{node_status}'. Treating as warning.")
                 final_result['status'] = 'warning'
                 final_result['message'] = f"Node returned invalid status '{node_status}'. Original message: {node_message}"
                 node_status = 'warning' # Update local variable

            # Update global status based on node result
            self.update_node_status(node_name, node_status, node_message)
            return final_result # Return the potentially wrapped/validated result

        # --- Exception Handling for execute_node_async ---
        # Catch specific, known errors first
        except (NodeExecutionError, NodeValidationError, ActfileParserError) as e:
             error_msg = f"Error executing node {node_name}: {e}"
             logger.error(error_msg, exc_info=False) # Log known errors without full traceback unless debugging
             self.update_node_status(node_name, "error", error_msg)
             return {"status": "error", "message": error_msg, "error_type": type(e).__name__}
        # Catch FileNotFoundError specifically if nodes might access files
        except FileNotFoundError as e:
             error_msg = f"File not found during execution of node {node_name}: {e}"
             logger.error(error_msg, exc_info=True)
             self.update_node_status(node_name, "error", error_msg)
             return {"status": "error", "message": error_msg, "error_type": type(e).__name__}
        # Catch any other unexpected errors
        except Exception as e:
             error_msg = f"Unexpected internal error during execution of node {node_name}: {str(e)}"
             logger.error(error_msg, exc_info=True) # Log full traceback for unexpected errors
             self.update_node_status(node_name, "error", error_msg)
             return {"status": "error", "message": error_msg, "error_type": type(e).__name__}


    def _structure_data_for_executor(self, processed_data: Dict[str, Any], node_name: str) -> Dict[str, Any]:
        """Organizes processed data into the {'params': {...}, ...metadata} structure expected by node execute methods."""
        executor_data = {}
        params = {}
        # Define keys that are considered metadata vs actual parameters for the node logic
        # Convert to set for faster lookup
        metadata_keys = {'type', 'label', 'position_x', 'position_y', 'description', '__previous_result'}

        for k, v in processed_data.items():
            if k in metadata_keys:
                executor_data[k] = v
            else:
                params[k] = v

        executor_data['params'] = params
        # Add context useful for node execution/logging
        executor_data['__node_name'] = node_name
        executor_data['__execution_id'] = self.current_execution_id
        return executor_data

    def _process_node_parameters(self, resolved_node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Attempts basic type conversions on resolved string values (e.g., "true"->True, "5"->5, JSON strings)."""
        processed_data = resolved_node_data.copy() # Work on a copy
        logger.debug(f"Processing parameters for type conversion: {list(processed_data.keys())}")

        for key, value in processed_data.items():
            if isinstance(value, str):
                original_value_repr = repr(value)
                new_value = value # Start with the original string

                # Skip conversion if it still looks like an unresolved placeholder (safety)
                if (value.startswith('{{') and value.endswith('}}')) or (value.startswith('${') and value.endswith('}')):
                    logger.warning(f"Parameter '{key}' seems to contain an unresolved placeholder '{original_value_repr}'. Skipping conversion.")
                    continue

                # 1. Try JSON decoding for specific keys or structural hints
                looks_like_json = (value.strip().startswith(('[', '{')) and value.strip().endswith((']', '}')))
                # List common keys that often contain JSON strings
                is_json_key = key.lower() in ['messages', 'json_body', 'data', 'payload', 'headers', 'items', 'list', 'options', 'config']

                if looks_like_json and is_json_key:
                    try:
                        new_value = json.loads(value)
                        logger.debug(f"Successfully decoded JSON for key '{key}'.")
                    except json.JSONDecodeError:
                        logger.debug(f"Value for key '{key}' looks like JSON but failed to decode. Keeping as string.")
                        pass # Keep as string if decode fails

                # 2. Try boolean conversion if JSON didn't parse
                elif new_value is value and value.lower() in ('true', 'false'):
                    new_value = value.lower() == 'true'

                # 3. Try numeric conversion (int then float) if not boolean
                elif new_value is value:
                    # Try integer first
                    if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                         try: new_value = int(value)
                         except ValueError: pass # Ignore error, keep as string
                    # Try float if not integer (handles ".")
                    elif self._is_float(value):
                         try: new_value = float(value)
                         except ValueError: pass # Ignore error, keep as string

                # Log if conversion happened
                if new_value is not value:
                    processed_data[key] = new_value
                    logger.debug(f"Converted key '{key}': {original_value_repr}({type(value).__name__}) -> {repr(new_value)}({type(new_value).__name__})")

            # Optionally handle non-string values if needed (e.g. already resolved lists/dicts)
            # elif isinstance(value, (list, dict)):
            #     processed_data[key] = self._process_node_parameters(value) # Recurse if needed, ensure dicts/lists are copied

        logger.debug("Finished processing parameters for type conversion.")
        return processed_data


    def _is_float(self, text: str) -> bool:
        """Checks if a string can likely represent a float, handling potential edge cases."""
        if not isinstance(text, str):
            return False
        # Basic check: contains a dot and potentially digits/sign
        if '.' in text and re.match(r'^-?\d*\.?\d+$', text.strip()):
             try:
                 float(text)
                 return True
             except ValueError:
                 return False
        # Also consider scientific notation maybe?
        # if 'e' in text.lower() and re.match(r'^-?\d+(\.\d+)?e[-+]?\d+$', text.strip().lower()):
        #    try: float(text); return True
        #    except ValueError: return False
        return False


    # --- Placeholder Resolution ---

    def resolve_placeholders_for_execution(self, data: Any) -> Any:
        """Recursively resolves placeholders in data structures (dicts, lists, strings)."""
        if isinstance(data, dict):
            # Create new dict to avoid modifying original during iteration if nested
            resolved_dict = {}
            for key, value in data.items():
                resolved_dict[key] = self.resolve_placeholders_for_execution(value)
            return resolved_dict
        elif isinstance(data, list):
            # Create new list
            return [self.resolve_placeholders_for_execution(item) for item in data]
        elif isinstance(data, str):
            # Perform placeholder resolution on the string itself
            return self.resolve_placeholder_string(data)
        else:
            # Return non-container types (int, float, bool, None, etc.) as is
            return data


    def resolve_placeholder_string(self, text: str) -> Any:
        """Resolves ${ENV_VAR} and {{source.path}} / {{key:key_name}} placeholders within a string."""
        if not isinstance(text, str):
            return text # Should not happen if called from resolve_placeholders_for_execution

        # 1. Environment Variables ${...}
        # Use a function for replacement to handle not found cases cleanly
        def replace_env(match):
            var_name = match.group(1)
            env_value = os.environ.get(var_name)
            if env_value is not None:
                logger.debug(f"Resolved env var '${{{var_name}}}'")
                return env_value
            else:
                logger.warning(f"Env var '${{{var_name}}}' not found. Leaving placeholder.")
                return match.group(0) # Return original placeholder if not found

        env_var_pattern = re.compile(r'\$\{([A-Za-z_][A-Za-z0-9_]*)\}')
        resolved_text_env = env_var_pattern.sub(replace_env, text)
        text = resolved_text_env # Update text for next stage


        # 2. Workflow Placeholders {{...}}
        placeholder_pattern = re.compile(r'\{\{(.*?)\}\}')
        matches = list(placeholder_pattern.finditer(text))
        if not matches:
            return text # No workflow placeholders found

        # --- Full String Match Check ---
        # If the entire string is just one placeholder, try to return the actual resolved type
        if len(matches) == 1 and matches[0].group(0) == text.strip(): # Use strip() here
            placeholder_content = matches[0].group(1).strip()
            if not placeholder_content: return text # Empty placeholder {{}}

            logger.debug(f"Attempting full string resolution for: '{{{{{placeholder_content}}}}}'")
            resolved_value = self._resolve_single_placeholder_content(placeholder_content)

            if resolved_value is not None:
                # Success! Return the potentially non-string value
                logger.debug(f"Resolved full placeholder '{{{{{placeholder_content}}}}}' to type {type(resolved_value).__name__}")
                return resolved_value
            else:
                # Resolution failed, return the original placeholder string
                logger.warning(f"Could not resolve full placeholder '{{{{{placeholder_content}}}}}'. Returning original text.")
                return text

        # --- Partial/Multiple Placeholder Replacement ---
        # If placeholders are part of a larger string, the result must be a string
        logger.debug(f"Performing partial/multiple string replacement for: {text}")
        resolved_text_wf = text # Start with the potentially env-resolved string

        offset = 0 # Keep track of index changes due to replacements
        for match in matches:
            start, end = match.span()
            start += offset
            end += offset

            full_placeholder = match.group(0)
            placeholder_content = match.group(1).strip()
            if not placeholder_content: continue

            value = self._resolve_single_placeholder_content(placeholder_content)

            if value is not None:
                str_value = str(value) # Convert resolved value to string
                logger.debug(f"Replacing partial '{{{{{placeholder_content}}}}}' with string: '{str_value[:50]}{'...' if len(str_value)>50 else ''}'")

                # Replace in the accumulating result string using slicing and calculated offsets
                resolved_text_wf = resolved_text_wf[:start] + str_value + resolved_text_wf[end:]
                # Update offset for next iteration
                offset += len(str_value) - len(full_placeholder)
            else:
                logger.warning(f"Could not resolve partial placeholder '{{{{{placeholder_content}}}}}'. Leaving it in the string.")
                # No replacement, offset remains the same for this iteration

        return resolved_text_wf


    def _resolve_single_placeholder_content(self, content: str) -> Any:
         """Resolves the content inside {{...}}, handling 'key:' prefix or 'source.path'."""
         if content.startswith('key:'):
             key_name = content[len('key:'):].strip()
             logger.debug(f"Attempting to fetch value using key: '{key_name}'")
             # Need a mechanism to get keyed values (e.g., from 'set' nodes)
             # Assuming node_results might store them or a dedicated key-value store exists
             # Placeholder: Check node_results for a direct key match first (simplistic)
             if key_name in self.node_results: # This might be wrong depending on 'set' node logic
                 logger.warning(f"Found key '{key_name}' directly in node_results - this might be unexpected.")
                 return self.node_results[key_name]
             # TODO: Implement proper retrieval from where 'set' nodes store data
             # Example: return self.key_value_store.get(key_name)
             logger.error(f"Key-based lookup ('key:{key_name}') is not fully implemented yet.")
             return None # Or raise error?
         else:
             # Assume 'source_id.path.to.value' format
             source_id, path = self._split_placeholder_path(content)
             logger.debug(f"Attempting to fetch value from source: '{source_id}', path: '{path}'")
             return self.fetch_value(source_id, path)


    def _split_placeholder_path(self, content: str) -> Tuple[str, str]:
         """Splits 'source.path.to.value' into ('source', 'path.to.value'). Handles cases with no dot."""
         parts = content.split('.', 1);
         source_id = parts[0].strip() # Strip whitespace from source
         path = parts[1].strip() if len(parts) > 1 else "" # Strip whitespace from path
         # Ensure source_id is not empty
         if not source_id:
            logger.warning(f"Placeholder content '{content}' resulted in empty source_id after splitting.")
            # Decide how to handle this: return None, raise error, or return ('', path)?
            # Returning ('', path) might cause issues in fetch_value
            return ('__invalid_source__', path) # Return a clearly invalid source
         return source_id, path

    def fetch_value(self, source_id: str, path: str) -> Any:
        """
        Fetches a value from initial input ('input' source) or node results (using node name as source).
        Uses a dot-separated path to navigate nested dictionaries and lists.
        """
        logger.debug(f"FETCH_VALUE called for source_id: '{source_id}', path: '{path}'")
        base_value = None

        # --- Determine Base Value Source ---
        if source_id == 'input':
            logger.debug("Fetching from 'input' source.")
            initial_data = getattr(self, 'initial_input_data', None)
            if isinstance(initial_data, dict):
                # If 'input' key exists at the top level, use it directly. Otherwise use the whole dict.
                # This allows passing {'input': {'user_query': 'xyz'}} or just {'user_query': 'xyz'}
                base_value = initial_data.get('input', initial_data)
                logger.debug(f"  Base value source determined from initial_input_data (type: {type(base_value).__name__})")
            else:
                logger.warning("FETCH_VALUE cannot access 'input': self.initial_input_data is missing, None, or not a dict.")
                return None # Cannot proceed without initial data if source is 'input'

        elif source_id in self.node_results:
            logger.debug(f"Fetching from node result: '{source_id}'.")
            base_value = self.node_results[source_id]
            logger.debug(f"  Base value source determined from node_results['{source_id}'] (type: {type(base_value).__name__})")

        # --- Handle cases where source exists but might be None ---
        elif source_id in self.workflow_data.get('nodes', {}):
             # Node exists but hasn't run or returned None?
             logger.warning(f"Source ID '{source_id}' refers to a defined node, but no result is available yet (or it was None).")
             return None
        else:
             logger.warning(f"FETCH_VALUE FAILED: Source ID '{source_id}' not found in initial input ('input') or node results.")
             return None


        # --- Traverse Path ---
        if not path:
            logger.debug(f"No path specified for source '{source_id}'. Returning base value directly.")
            return base_value # Return the entire node result or input dict

        # --- Path Traversal Logic ---
        parts = path.split('.')
        current_value = base_value
        logger.debug(f"Traversing path: {parts} starting from type: {type(current_value).__name__}")

        for i, part in enumerate(parts):
            current_path_log = '.'.join(parts[:i+1]) # Path traversed so far

            if part == '': # Handle potential empty parts from ".." etc.
                logger.warning(f"Empty path part encountered at '{current_path_log}'. Skipping.")
                continue

            if isinstance(current_value, dict):
                if part in current_value:
                    current_value = current_value[part]
                    logger.debug(f"  Path '{current_path_log}': Accessed dict key '{part}'. New value type: {type(current_value).__name__}")
                else:
                    # Key not found - check case-insensitively as a fallback? (Optional)
                    # found_case_insensitive = False
                    # for k in current_value:
                    #    if k.lower() == part.lower():
                    #        current_value = current_value[k]
                    #        logger.debug(f" Path '{current_path_log}': Accessed dict key '{k}' (case-insensitive for '{part}'). New type: {type(current_value).__name__}")
                    #        found_case_insensitive = True
                    #        break
                    # if not found_case_insensitive:
                    logger.warning(f"Path part '{part}' (key) not found in dictionary at path '{current_path_log}'. Available keys: {list(current_value.keys())}")
                    return None # Path traversal failed

            elif isinstance(current_value, list):
                if part.isdigit():
                   try:
                       idx = int(part)
                       # Check bounds
                       if -len(current_value) <= idx < len(current_value): # Allow negative indices
                           actual_index = idx if idx >= 0 else len(current_value) + idx
                           current_value = current_value[actual_index]
                           logger.debug(f"  Path '{current_path_log}': Accessed list index {idx} (actual: {actual_index}). New value type: {type(current_value).__name__}")
                       else:
                           logger.warning(f"Index {idx} out of bounds for list of length {len(current_value)} at path '{current_path_log}'.")
                           return None # Path traversal failed
                   except ValueError: # Should not happen if isdigit() passed, but safety
                       logger.warning(f"Path part '{part}' is digits but failed int conversion at path '{current_path_log}'.")
                       return None
                else:
                    logger.warning(f"Path part '{part}' is not a valid integer index for list access at path '{current_path_log}'.")
                    return None # Path traversal failed

            # Handle case where we try to traverse into a non-container type (string, int, etc.)
            else:
                logger.warning(f"Cannot traverse further. Part '{part}' requested, but current value at path '{'.'.join(parts[:i])}' is of type {type(current_value).__name__} (not a dict or list).")
                return None # Path traversal failed

            # Check if traversal resulted in None (valid if None was stored)
            if current_value is None and i < len(parts) - 1:
                 logger.debug(f"Path traversal encountered None at '{current_path_log}'. Cannot traverse further into path '{'.'.join(parts[i+1:])}'.")
                 # If None is the final value, we return it. If intermediate, traversal fails.
                 return None


        # If loop completes, current_value holds the final result
        logger.debug(f"Successfully fetched value for {source_id}.{path}. Final type: {type(current_value).__name__}")
        return current_value


    # --- Utility Methods ---

    @staticmethod
    def log_safe_node_data(node_data: Any) -> str:
        """Converts data to JSON string for logging, redacting sensitive keys."""
        sensitive_keys = ['api_key', 'token', 'password', 'secret', 'credentials', 'auth', 'apikey', 'access_key', 'secret_key']
        # Add variations if needed

        def redact_recursive(data: Any) -> Any:
            if isinstance(data, dict):
                new_dict = {}
                for k, v in data.items():
                    # Check if key itself is sensitive (case-insensitive)
                    is_sensitive_key = isinstance(k, str) and any(s in k.lower() for s in sensitive_keys)
                    new_dict[k] = '[REDACTED]' if is_sensitive_key else redact_recursive(v)
                return new_dict
            elif isinstance(data, list):
                return [redact_recursive(item) for item in data]
            elif isinstance(data, str):
                # Maybe redact sensitive patterns within strings? (More complex)
                # Example: if re.search(r'AIza[0-9A-Za-z\\-_]{35}', data): return '[REDACTED_PATTERN]'
                return data # Keep strings as-is for now unless the key was sensitive
            else:
                 # Handle non-serializable types gracefully
                try:
                    # Test serializability without actually dumping large data
                    json.dumps(data, default=str)
                    return data
                except (TypeError, OverflowError):
                    return f"[Non-Serializable: {type(data).__name__}]"

        try:
            safe_data = redact_recursive(node_data)
            # Use default=str to handle common non-serializable types like datetime
            return json.dumps(safe_data, indent=2, default=str, ensure_ascii=False, sort_keys=False) # sort_keys=False preserves order
        except Exception as e:
            logger.error(f"Error creating log-safe JSON representation: {e}")
            # Provide a fallback representation
            return f"[Error logging data - Type: {type(node_data).__name__}, Error: {e}]"


    def _snake_case(self, name: str) -> str:
        """Converts PascalCase/CamelCase to snake_case."""
        if not name: return ""
        # Insert underscore before uppercase letters preceded by a lowercase letter or digit
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
        # Insert underscore before uppercase letters preceded by another uppercase letter if followed by lowercase (e.g., HTTPRequest -> HTTP_Request)
        name = re.sub('([A-Z])([A-Z][a-z])', r'\1_\2', name)
        return name.lower()


    def _print_node_execution_results(self):
        """Prints a summary table of final node execution statuses."""
        if not self.node_execution_status:
            print("\n--- Node Execution Summary ---\nNo node statuses recorded.\n------------------------------\n")
            return

        headers = ["Node Name", "Final Status", "Message/Result Summary"]
        table_data = []

        # Ensure nodes are sorted, potentially by execution order if tracked, or alphabetically
        # Alphabetical sort is simpler here:
        sorted_node_names = sorted(self.node_execution_status.keys())

        for node_name in sorted_node_names:
            status_info = self.node_execution_status[node_name]
            status = status_info.get('status', 'unknown')
            message = status_info.get('message', 'N/A')
            # Limit summary length for display
            summary = message[:120] + ('...' if len(message) > 120 else '')

            # Determine color and symbol based on status
            if status == 'success':
                status_symbol, color = "🟢", Fore.GREEN
            elif status == 'error':
                status_symbol, color = "🔴", Fore.RED
            elif status == 'warning' or status == 'fallback': # Group warning/fallback visually
                status_symbol, color = "🟡", Fore.YELLOW
            elif status == 'pending':
                 status_symbol, color = "⚪", Fore.WHITE # Or use Fore.BLUE?
            elif status == 'running': # Should ideally not be the final state
                 status_symbol, color = "🔵", Fore.CYAN
            else: # Unknown status
                status_symbol, color = "❓", Fore.MAGENTA

            # Add row with colored status
            table_data.append([node_name, f"{color}{status_symbol} {status.upper()}{Style.RESET_ALL}", summary])

        try:
            # Use tabulate if available
            table = tabulate(table_data, headers=headers, tablefmt="grid", maxcolwidths=[None, 15, 80])
        except NameError:
            # Use basic fallback if tabulate is missing
            logger.warning("Tabulate not found, using basic table format.")
            table = self._basic_table(table_data, headers)

        print("\n--- Node Execution Summary ---\n" + table + "\n----------------------------\n")