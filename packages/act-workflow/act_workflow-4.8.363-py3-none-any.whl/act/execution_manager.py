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
    def tabulate(data, headers, tablefmt): # Dummy tabulate
        header_line = " | ".join(map(str, headers))
        separator = "-+-".join("-" * len(str(h)) for h in headers)
        data_lines = [" | ".join(map(str, row)) for row in data]
        return "\n".join([header_line, separator] + data_lines)


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
    class ActfileParserError(Exception): pass
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
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s [%(levelname)s] - %(message)s')
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
        logger.debug(f"Node '{node_name}' Status -> {status.upper()}: {message[:100] + ('...' if len(message)>100 else '')}") # Limit message length in log

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
        self.load_node_executors()

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
        # 1. Try getting from schema (assuming schema has 'node_type' attribute)
        try:
            if hasattr(node_class, 'get_schema'):
                 schema_func = getattr(node_class, 'get_schema')
                 schema = None
                 if hasattr(schema_func, '__get__') and not inspect.isroutine(schema_func):
                      schema = schema_func.__get__(None, node_class)()
                 else:
                      try: temp_instance = node_class(); schema = temp_instance.get_schema()
                      except Exception as inst_err: logger.warning(f"Could not instantiate {class_name} to get schema: {inst_err}")
                 if schema and hasattr(schema, 'node_type'):
                      node_type = getattr(schema, 'node_type')
                      if node_type: logger.debug(f"Using node_type '{node_type}' from schema for class {class_name}"); return node_type
        except Exception as e: logger.warning(f"Error getting schema from {class_name}: {e}")

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

            # Optional Fallback to GenericNode
            if status == 'error':
                generic_node_type_name = 'GenericNode'; generic_node_class = all_available_node_classes.get(generic_node_type_name)
                if generic_node_class:
                     logger.warning(f"Attempting fallback to {generic_node_type_name} for type '{node_type}'.")
                     try:
                         generic_instance = self._instantiate_node(generic_node_class); self.node_executors[node_type] = generic_instance; self.node_loading_status[node_type]['status'] = 'fallback'; self.node_loading_status[node_type]['message'] += f" | Fallback to {generic_node_type_name} successful."; logger.info(f"Using {generic_node_type_name} fallback for type '{node_type}'.")
                     except Exception as e: logger.error(f"Error instantiating {generic_node_type_name} fallback for '{node_type}': {e}", exc_info=True); self.node_loading_status[node_type]['status'] = 'error'; self.node_loading_status[node_type]['message'] += f" | Fallback failed: {generic_node_type_name} instantiation error: {e}."
                else: logger.error(f"{generic_node_type_name} not found for fallback! Node type '{node_type}' will be unavailable."); self.node_loading_status[node_type]['status'] = 'error'; self.node_loading_status[node_type]['message'] += f" | Fallback failed: {generic_node_type_name} not found."

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
        table = tabulate(table_data, headers=headers, tablefmt="grid", maxcolwidths=[None, 15, 80])
        print("\n--- Node Executor Loading Status ---\n" + table + "\n------------------------------------\n")

    def _instantiate_node(self, node_class: Type) -> Any:
        """Instantiates a node class, handles sandbox_timeout, sets execution_manager."""
        logger.debug(f"Instantiating node class: {node_class.__name__}")
        try:
            sig = inspect.signature(node_class.__init__); node_instance = node_class(sandbox_timeout=self.sandbox_timeout) if 'sandbox_timeout' in sig.parameters else node_class()
            set_manager_method = getattr(node_instance, 'set_execution_manager', None)
            if callable(set_manager_method): logger.debug(f"Setting execution manager for instance of {node_class.__name__}"); set_manager_method(self)
            return node_instance
        except Exception as e: logger.error(f"Failed to instantiate {node_class.__name__}: {e}", exc_info=True); raise

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
             return {"status": "error", "message": "Workflow data not loaded/invalid.", "results": {}, "node_status": {}}

        try:
             result = asyncio.run(self.execute_workflow_async())
             logger.info(f"Workflow {self.current_execution_id} execution finished.")
             self._print_node_execution_results(); return result # Print summary after completion
        except Exception as e:
             logger.error(f"Critical error during workflow execution run: {e}", exc_info=True)
             self._print_node_execution_results() # Print status on error
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
        logger.info(f"Initial input data for this run: {self.log_safe_node_data(self.initial_input_data)}")

        if not self.actfile_parser: logger.error("Cannot execute async workflow: Actfile parser not available."); return {"status": "error", "message": "Actfile parser not initialized.", "results": {}, "node_status": self.node_execution_status}

        self.sandbox_start_time = datetime.now()
        execution_queue: List[Tuple[str, Optional[Dict[str, Any]]]] = []
        executed_nodes = set()

        try:
            start_node_name = self.actfile_parser.get_start_node()
            if not start_node_name: logger.error("No start node specified."); return {"status": "error", "message": "No start node specified.", "results": {}, "node_status": self.node_execution_status}
            if start_node_name not in self.workflow_data.get('nodes', {}): logger.error(f"Start node '{start_node_name}' not defined."); return {"status": "error", message: f"Start node '{start_node_name}' not defined.", "results": {}, "node_status": self.node_execution_status}

            logger.info(f"Workflow starting at node: {start_node_name}")
            execution_queue.append((start_node_name, None))

            # --- Main Execution Loop ---
            while execution_queue:
                # --- >> ADDED LOOP STATE LOGGING << ---
                logger.debug(f"WHILE LOOP TOP - Initial Data ID: {id(self.initial_input_data)}, Content: {self.log_safe_node_data(self.initial_input_data)}")
                # --- >> END LOOP STATE LOGGING << ---

                node_name, previous_node_result = execution_queue.pop(0)

                if node_name in executed_nodes: logger.warning(f"Node '{node_name}' already executed. Skipping cycle."); continue
                executed_nodes.add(node_name)

                # Timeout check
                if self.sandbox_timeout > 0 and (datetime.now() - self.sandbox_start_time).total_seconds() > self.sandbox_timeout:
                    timeout_msg = f"Workflow timeout ({self.sandbox_timeout}s) exceeded at node '{node_name}'."; logger.error(timeout_msg); self.update_node_status(node_name, "error", timeout_msg)
                    return {"status": "error", "message": timeout_msg, "results": self.node_results, "node_status": self.node_execution_status}

                logger.info(f"--- Executing Node: {node_name} ---")
                self.update_node_status(node_name, "running", "Node execution started")
                node_result = await self.execute_node_async(node_name, input_context=previous_node_result)
                self.node_results[node_name] = node_result # Store result immediately

                # --- Handle Node Result ---
                if node_result.get('status') == 'error':
                    error_msg = node_result.get('message', 'Unknown node error'); logger.error(f"Node '{node_name}' failed: {error_msg}. Stopping workflow.")
                    return {"status": "error", "message": f"Workflow failed at node '{node_name}': {error_msg}", "results": self.node_results, "node_status": self.node_execution_status}
                else: logger.info(f"Node '{node_name}' finished with status: {node_result.get('status', 'unknown')}")

                # --- Queue Successors (Conditional Logic Placeholder) ---
                all_successors = self.actfile_parser.get_node_successors(node_name)
                logger.debug(f"Potential successors for '{node_name}': {all_successors}")
                current_node_type = self.workflow_data['nodes'][node_name].get('type')
                nodes_to_queue = []

                # --- >>> START CONDITIONAL LOGIC AREA <<< ---
                if current_node_type == 'if' and 'result' in node_result.get('result', {}):
                    condition_outcome = node_result['result']['result']
                    logger.info(f"IfNode '{node_name}' result: {condition_outcome}. Applying conditional branching (Convention: 1st=True, 2nd=False).")
                    true_target = all_successors[0] if len(all_successors) > 0 else None
                    false_target = all_successors[1] if len(all_successors) > 1 else None
                    target_node_name = true_target if condition_outcome else false_target
                    if target_node_name: nodes_to_queue.append(target_node_name)
                    elif condition_outcome and not true_target: logger.warning(f"IfNode '{node_name}' was True, but no 'True' path (1st successor) defined.")
                    elif not condition_outcome and not false_target: logger.warning(f"IfNode '{node_name}' was False, but no 'False' path (2nd successor) defined.")
                    else: logger.info(f"No specific conditional target determined for IfNode '{node_name}'. Path ends.")

                elif current_node_type == 'switch' and 'selected_node' in node_result.get('result', {}):
                     target_node_name = node_result['result']['selected_node']
                     logger.info(f"SwitchNode '{node_name}' selected target: '{target_node_name}'.")
                     if target_node_name: nodes_to_queue.append(target_node_name)
                     else: logger.info(f"SwitchNode '{node_name}' selected no target (no match/default). Path ends.")

                else: # Default: Queue all successors
                     logger.debug(f"Queueing all successors for non-conditional node '{node_name}'")
                     nodes_to_queue.extend(all_successors)
                # --- >>> END CONDITIONAL LOGIC AREA <<< ---

                # Add selected nodes to the queue after filtering
                for successor_name in nodes_to_queue:
                     if successor_name not in self.workflow_data.get('nodes', {}): logger.warning(f"Target node '{successor_name}' not defined. Skipping."); continue
                     if successor_name in executed_nodes: logger.debug(f"Target node '{successor_name}' already executed. Skipping cycle."); continue
                     if any(item[0] == successor_name for item in execution_queue): logger.debug(f"Target node '{successor_name}' already in queue. Skipping."); continue
                     logger.info(f"Queueing next node: '{successor_name}'")
                     execution_queue.append((successor_name, node_result))

            # Loop finished successfully
            logger.info(f"Workflow execution completed successfully for ID: {exec_id}")
            return {"status": "success", "message": "Workflow executed successfully", "results": self.node_results, "node_status": self.node_execution_status}

        except Exception as e:
            logger.error(f"Unexpected error during workflow execution loop for {exec_id}: {e}", exc_info=True)
            last_node = locals().get('node_name');
            if last_node: self.update_node_status(last_node, "error", f"Workflow loop error: {e}")
            return {"status": "error", "message": f"Workflow failed unexpectedly: {e}", "results": self.node_results, "node_status": self.node_execution_status}

    async def execute_node_async(self, node_name: str, input_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Executes a single node: gets config, resolves placeholders, prepares data, calls executor."""
        logger.debug(f"Preparing to execute node: {node_name}")
        try:
            # 1. Get Config
            if not self.workflow_data or node_name not in self.workflow_data.get('nodes', {}): raise NodeExecutionError(f"Node '{node_name}' configuration not found.")
            node_config = self.workflow_data['nodes'][node_name].copy(); node_type = node_config.get('type')
            if not node_type: raise NodeExecutionError(f"Node '{node_name}' missing 'type'.")
            if input_context: node_config['__previous_result'] = input_context # Add previous result context

            # 2. Log State Before Resolution (DEBUG STEP)
            logger.debug(f"State BEFORE resolving placeholders for '{node_name}':")
            logger.debug(f"  - Initial Data ID: {id(self.initial_input_data)}, Content: {self.log_safe_node_data(self.initial_input_data)}")
            logger.debug(f"  - Node Results So Far: {self.log_safe_node_data(self.node_results)}")
            logger.debug(f"  - Config to Resolve: {self.log_safe_node_data(node_config)}")

            # 3. Resolve Placeholders
            logger.debug(f"Resolving placeholders for '{node_name}' config...")
            resolved_node_config = self.resolve_placeholders_for_execution(node_config)
            logger.debug(f"'{node_name}' config AFTER resolving: {self.log_safe_node_data(resolved_node_config)}")

            # 4. Prepare Data for Executor
            processed_data = self._process_node_parameters(resolved_node_config)
            executor_data = self._structure_data_for_executor(processed_data, node_name)
            logger.debug(f"Final data for executor '{node_name}': {self.log_safe_node_data(executor_data)}")

            # 5. Get Executor
            executor = self.node_executors.get(node_type)
            if not executor: raise NodeExecutionError(f"No executor instance found for type '{node_type}' (node: '{node_name}').")

            # 6. Execute
            logger.info(f"Calling {type(executor).__name__}.execute for node '{node_name}'")
            execute_method = getattr(executor, 'execute', None)
            if not callable(execute_method): raise NodeExecutionError(f"Executor for '{node_type}' has no callable 'execute' method.")
            if inspect.iscoroutinefunction(execute_method): node_result = await execute_method(executor_data)
            else: logger.warning(f"Executing sync node '{node_name}' ({node_type})."); node_result = execute_method(executor_data)
            if inspect.iscoroutine(node_result): logger.warning(f"Sync execute for '{node_name}' returned awaitable."); node_result = await node_result

            # 7. Process Result
            logger.info(f"Node '{node_name}' raw result: {self.log_safe_node_data(node_result)}")
            if not isinstance(node_result, dict) or 'status' not in node_result:
                 logger.warning(f"Node '{node_name}' result invalid. Wrapping."); node_result = {"status": "warning", "message": "Node returned unexpected format.", "original_result": node_result}
            node_status = node_result.get('status', 'error'); node_message = node_result.get('message', '')
            if node_status not in ['success', 'error', 'warning']: logger.warning(f"Node '{node_name}' returned invalid status '{node_status}'. Treating as warning."); node_status = "warning"; node_result['status'] = node_status; node_result['message'] = f"Invalid status '{node_status}'. {node_message}"
            self.update_node_status(node_name, node_status, node_message); return node_result

        except (NodeExecutionError, NodeValidationError, FileNotFoundError, ActfileParserError) as e: # Catch specific known errors
             error_msg = f"Error executing node {node_name}: {e}"; logger.error(error_msg, exc_info=False); self.update_node_status(node_name, "error", error_msg); return {"status": "error", "message": error_msg, "error_type": type(e).__name__}
        except Exception as e: # Catch unexpected errors
             error_msg = f"Unexpected internal error during execution of node {node_name}: {str(e)}"; logger.error(error_msg, exc_info=True); self.update_node_status(node_name, "error", error_msg); return {"status": "error", "message": error_msg, "error_type": type(e).__name__}


    def _structure_data_for_executor(self, processed_data: Dict[str, Any], node_name: str) -> Dict[str, Any]:
        """Organizes processed data into the {'params': {...}, ...metadata} structure."""
        executor_data = {}; metadata_keys = {'type', 'label', 'position_x', 'position_y', 'description', '__previous_result', '__node_name', '__execution_id'}; params = {}
        for k, v in processed_data.items(): (executor_data if k in metadata_keys else params)[k] = v
        executor_data['params'] = params; executor_data.setdefault('__node_name', node_name); executor_data.setdefault('__execution_id', self.current_execution_id)
        return executor_data

    def _process_node_parameters(self, resolved_node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Attempts basic type conversions on resolved string values (e.g., "true"->True, "5"->5)."""
        processed_data = resolved_node_data; logger.debug(f"Processing parameters for type conversion: {list(processed_data.keys())}")
        for key, value in processed_data.items():
            if isinstance(value, str):
                original_value_repr = repr(value); new_value = value
                if (value.startswith('{{') and value.endswith('}}')) or (value.startswith('${') and value.endswith('}')): logger.warning(f"Param '{key}' still contains placeholder '{original_value_repr}'."); continue
                looks_like_json = (value.startswith(('[', '{')) and value.endswith((']', '}'))); is_json_key = key.lower() in ['messages', 'json_body', 'data', 'payload', 'headers']
                if looks_like_json and is_json_key:
                    try: new_value = json.loads(value)
                    except json.JSONDecodeError: pass
                elif new_value is value and value.lower() in ('true', 'false'): new_value = value.lower() == 'true'
                elif new_value is value:
                    if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                         try: new_value = int(value)
                         except ValueError: pass
                    elif self._is_float(value):
                         try: new_value = float(value)
                         except ValueError: pass
                if new_value is not value: processed_data[key] = new_value; logger.debug(f"Converted key '{key}': {original_value_repr}({type(value).__name__}) -> {repr(new_value)}({type(new_value).__name__})")
        logger.debug("Finished processing parameters for type conversion."); return processed_data

    def _is_float(self, text: str) -> bool:
        """Checks if a string can likely represent a float."""
        if not isinstance(text, str): return False
        try: float(text); return True
        except ValueError: return False

    # --- Placeholder Resolution ---

    def resolve_placeholders_for_execution(self, node_data: Any) -> Any: # Accept Any, return Any
        """Recursively resolves placeholders in node data structures (dicts, lists, strings)."""
        if isinstance(node_data, dict): return {key: self.resolve_placeholders_for_execution(value) for key, value in node_data.items()}
        elif isinstance(node_data, list): return [self.resolve_placeholders_for_execution(item) for item in node_data]
        elif isinstance(node_data, str): return self.resolve_placeholder_string(node_data)
        else: return node_data # Return non-container types as is

    def resolve_placeholder_string(self, text: str) -> Any:
        """Resolves ${ENV_VAR} and {{source.path}} placeholders within a string."""
        if not isinstance(text, str): return text

        # 1. Environment Variables ${...}
        env_var_pattern = re.compile(r'\$\{([A-Za-z_][A-Za-z0-9_]*)\}')
        resolved_text_env = text
        for match in env_var_pattern.finditer(text):
            var_name = match.group(1); env_value = os.environ.get(var_name)
            if env_value is not None: resolved_text_env = resolved_text_env.replace(match.group(0), env_value); logger.debug(f"Resolved env var '${{{var_name}}}'")
            else: logger.warning(f"Env var '${{{var_name}}}' not found.")
        text = resolved_text_env

        # 2. Workflow Placeholders {{...}}
        placeholder_pattern = re.compile(r'\{\{(.*?)\}\}')
        matches = list(placeholder_pattern.finditer(text))
        if not matches: return text

        # Check for full string match (return actual type)
        if len(matches) == 1 and matches[0].group(0) == text:
            placeholder_content = matches[0].group(1).strip();
            if not placeholder_content: return text
            logger.debug(f"Attempting full string resolution for: {placeholder_content}")
            source_id, path = self._split_placeholder_path(placeholder_content)
            resolved_value = self.fetch_value(source_id, path)
            if resolved_value is not None: logger.debug(f"Resolved full placeholder '{placeholder_content}' to type {type(resolved_value).__name__}"); return resolved_value
            else: logger.warning(f"Could not resolve full placeholder '{placeholder_content}'."); return text # Return original placeholder

        # Partial/multiple placeholder replacement (always results in string)
        logger.debug(f"Performing partial string replacement for: {text}")
        resolved_text_wf = text # Initialize result with original text
        for match in matches:
            full_placeholder = match.group(0); placeholder_content = match.group(1).strip()
            if not placeholder_content: continue
            source_id, path = self._split_placeholder_path(placeholder_content)
            value = self.fetch_value(source_id, path)
            if value is not None:
                 str_value = str(value); logger.debug(f"Replacing partial '{placeholder_content}' with string: '{str_value[:50]}...'")
                 # --- CORRECTED LINE (Replaces in accumulating string) ---
                 resolved_text_wf = resolved_text_wf.replace(full_placeholder, str_value)
            else: logger.warning(f"Could not resolve partial placeholder '{placeholder_content}'.")
        return resolved_text_wf

    def _split_placeholder_path(self, content: str) -> Tuple[str, str]:
         """Splits 'source.path.to.value' into ('source', 'path.to.value')."""
         parts = content.split('.', 1); source_id = parts[0]; path = parts[1] if len(parts) > 1 else ""
         return source_id, path

    def fetch_value(self, source_id: str, path: str) -> Any:
        """Fetches a value from initial input or node results using a dot-path."""
        # --- >> ADDED DETAILED LOGGING << ---
        logger.debug(f"FETCH_VALUE Start - Initial Data ID: {id(self.initial_input_data)}, Content: {self.log_safe_node_data(self.initial_input_data)}")
        logger.debug(f"FETCH_VALUE called for source_id: '{source_id}', path: '{path}'")
        # --- >> END DETAILED LOGGING << ---
        base_value = None

        if source_id == 'input':
            logger.debug(f"FETCH_VALUE checking 'input' source.")
            initial_data = getattr(self, 'initial_input_data', None)
            if isinstance(initial_data, dict):
                logger.debug(f"  initial_input_data IS present: {self.log_safe_node_data(initial_data)}")
                if 'input' in initial_data and isinstance(initial_data['input'], dict): base_value = initial_data['input']; logger.debug("  Using 'input' key from initial_input_data.")
                else: base_value = initial_data; logger.debug("  Using initial_input_data directly.")
            else: logger.warning(f"FETCH_VALUE FAILED for 'input': self.initial_input_data is missing, None, or not a dict."); return None
        elif source_id in self.node_results: base_value = self.node_results[source_id]; logger.debug(f"Accessing node result for '{source_id}'. Type: {type(base_value).__name__}")
        else: logger.warning(f"FETCH_VALUE FAILED: Source ID '{source_id}' not found."); return None

        if base_value is None: logger.debug(f"Source '{source_id}' resolved to None. Cannot traverse path '{path}'."); return None
        if not path: logger.debug(f"No path for source '{source_id}'. Returning base value."); return base_value

        parts = path.split('.'); current_value = base_value; logger.debug(f"Traversing path: {parts} in source type: {type(current_value).__name__}")
        for i, part in enumerate(parts):
            current_path_log = '.'.join(parts[:i+1])
            if isinstance(current_value, dict):
                if part in current_value: current_value = current_value[part]; logger.debug(f"Path '{current_path_log}' accessed dict key '{part}'. New type: {type(current_value).__name__}")
                else: logger.warning(f"Path part '{part}' (key) not found in dict. Path: {current_path_log}"); return None
            elif isinstance(current_value, list):
                if part.isdigit():
                   try:
                       idx = int(part)
                       if 0 <= idx < len(current_value): current_value = current_value[idx]; logger.debug(f"Path '{current_path_log}' accessed list index {idx}. New type: {type(current_value).__name__}")
                       else: logger.warning(f"Index {idx} out of bounds (len {len(current_value)}). Path: {current_path_log}"); return None
                   except ValueError: logger.warning(f"Path part '{part}' invalid index. Path: {current_path_log}"); return None
                else: logger.warning(f"Path part '{part}' not digit index for list. Path: {current_path_log}"); return None
            else: logger.warning(f"Cannot traverse part '{part}'. Current value type {type(current_value).__name__} not dict/list. Path: {current_path_log}"); return None
            if current_value is None: logger.debug(f"Path traversal resulted in None at part '{part}'. Path: {current_path_log}"); return None

        logger.debug(f"Successfully fetched value for {source_id}.{path}. Final type: {type(current_value).__name__}"); return current_value

    # --- Utility Methods ---

    @staticmethod
    def log_safe_node_data(node_data: Any) -> str:
        """Converts data to JSON string for logging, redacting sensitive keys."""
        sensitive_keys = ['api_key', 'token', 'password', 'secret', 'credentials', 'auth']
        def redact_recursive(data: Any) -> Any:
            if isinstance(data, dict): return {k: ('[REDACTED]' if isinstance(k, str) and any(s in k.lower() for s in sensitive_keys) else redact_recursive(v)) for k, v in data.items()}
            elif isinstance(data, list): return [redact_recursive(item) for item in data]
            else: 
                try:
                    json.dumps(data)
                    return data
                except TypeError:
                    return f"[Non-Serializable: {type(data).__name__}]"
        try: safe_data = redact_recursive(node_data); return json.dumps(safe_data, indent=2, default=str, ensure_ascii=False)
        except Exception as e: logger.error(f"Error creating log-safe JSON: {e}"); return f"[Error logging data: {e}]"

    def _snake_case(self, name: str) -> str:
        """Converts PascalCase/CamelCase to snake_case."""
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name); name = re.sub('__([A-Z])', r'_\1', name); name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name); return name.lower()

    def _print_node_execution_results(self):
        """Prints a summary table of final node execution statuses."""
        if not self.node_execution_status: print("\n--- Node Execution Summary ---\nNo node statuses recorded.\n------------------------------\n"); return
        headers = ["Node Name", "Final Status", "Message/Result Summary"]; table_data = []
        for node_name, status_info in sorted(self.node_execution_status.items()):
            status = status_info.get('status', 'unknown'); message = status_info.get('message', 'N/A'); summary = message[:120] + ('...' if len(message)>120 else '')
            if status == 'success': status_symbol, color = "🟢", Fore.GREEN
            elif status == 'error': status_symbol, color = "🔴", Fore.RED
            elif status == 'warning' or status == 'fallback': status_symbol, color = "🟡", Fore.YELLOW
            else: status_symbol, color = "⚪", Fore.WHITE
            table_data.append([node_name, f"{color}{status_symbol} {status.upper()}{Style.RESET_ALL}", summary])
        try: table = tabulate(table_data, headers=headers, tablefmt="grid", maxcolwidths=[None, 15, 80])
        except NameError: table = "\n".join([", ".join(headers)] + [", ".join(map(str, row)) for row in table_data]) # Basic fallback if tabulate failed import
        print("\n--- Node Execution Summary ---\n" + table + "\n----------------------------\n")

# --- Main Block for Standalone Testing (Example) ---
if __name__ == "__main__":
    print("Executing ExecutionManager main block for testing...")
    script_dir = Path(__file__).parent; actfile_name = "continuous_test_workflow_switch.ini"; actfile_path = script_dir / actfile_name
    print("Ensuring test environment structure..."); act_dir = script_dir / "act"; nodes_dir = act_dir / "nodes"; nodes_dir.mkdir(parents=True, exist_ok=True); (act_dir / "__init__.py").touch(exist_ok=True); (nodes_dir / "__init__.py").touch(exist_ok=True)
    # --- Create Dummy Nodes ---
    base_node_content = """import logging; logger = logging.getLogger(__name__); class NodeValidationError(Exception): pass; class NodeExecutionError(Exception): pass; class NodeParameterType: ANY="any"; STRING="string"; BOOLEAN="boolean"; NUMBER="number"; ARRAY="array"; OBJECT="object"; SECRET="secret"; class NodeParameter: def __init__(self, name, type, description, required=True, default=None, enum=None, case_sensitive=None): pass; class NodeSchema: def __init__(self, node_type, version, description, parameters, outputs, tags=None, author=None): self.node_type=node_type; class BaseNode:
        def __init__(self, sandbox_timeout=None): self.sandbox_timeout=sandbox_timeout; logger.debug(f"Initializing {type(self).__name__}")
        def set_execution_manager(self, manager): self.manager = manager; logger.debug(f"Set execution manager for {type(self).__name__}")
        def get_schema(self): logger.warning(f"Using dummy get_schema for {type(self).__name__}"); return NodeSchema(node_type='dummy_base', version='0.0', description='', parameters=[], outputs={})
        async def execute(self, data): logger.warning(f"Dummy BaseNode execute called for {type(self).__name__}"); return {"status": "warning", "message": f"Dummy execute for {type(self).__name__}"}
        def handle_error(self, error, context=""): logger.error(f"Error in {context}: {error}", exc_info=True); return {"status": "error", "message": f"Error in {context}: {error}", "error_type": type(error).__name__}
        def _check_and_convert_string(self,v): return v # Dummy needed by IfNode example"""
    (nodes_dir / "base_node.py").write_text(base_node_content)
    log_message_node_content = """from .base_node import BaseNode, NodeSchema, NodeParameter, NodeParameterType, NodeValidationError; import logging, json; logger = logging.getLogger(__name__); class LogMessageNode(BaseNode):
        _VALID_LOG_LEVELS = ["debug", "info", "warning", "error", "critical"]
        def get_schema(self): return NodeSchema(node_type='LogMessage', version='1.0', description='', parameters=[NodeParameter(name='message', type=NodeParameterType.STRING, description=''), NodeParameter(name='level', type=NodeParameterType.STRING, description='', default='info', enum=self._VALID_LOG_LEVELS)], outputs={'logged_level': NodeParameterType.STRING})
        async def execute(self, node_data: dict) -> dict:
            params = node_data.get('params', {}); message = params.get('message', 'No message'); level = str(params.get('level', 'info')).lower(); node_name = node_data.get('__node_name', 'LogMessageNode')
            if level not in self._VALID_LOG_LEVELS: level = 'info'
            log_func = getattr(logger, level, logger.info); log_output = f"[{node_name}] {message}"; log_func(log_output)
            return {"status": "success", "message": f"Message logged at level '{level}'.", "result": {"logged_level": level, "logged_message": message}}"""
    (nodes_dir / "log_message_node.py").write_text(log_message_node_content)
    if_node_content = """from .base_node import BaseNode, NodeSchema, NodeParameter, NodeParameterType, NodeValidationError, NodeExecutionError; import logging, numbers; logger = logging.getLogger(__name__); class IfNode(BaseNode): # Using v1.2.0 logic
        def get_schema(self) -> NodeSchema: return NodeSchema(node_type="if", version="1.2.0", description=".", parameters=[ NodeParameter(name="value1", type=NodeParameterType.ANY, description=".", required=True), NodeParameter(name="operator", type=NodeParameterType.STRING, description=".", required=True, enum=["==", "eq", "!=", "ne", ">", "gt", "<", "lt", ">=", "ge", "<=", "le", "contains", "not contains", "starts_with", "ends_with", "is_true", "is_false", "is_empty", "is_not_empty"]), NodeParameter(name="value2", type=NodeParameterType.ANY, description=".", required=False, default=None), NodeParameter(name="case_sensitive", type=NodeParameterType.BOOLEAN, description=".", required=False, default=True) ], outputs={ "result": NodeParameterType.BOOLEAN, "value1_resolved": NodeParameterType.ANY, "value2_resolved": NodeParameterType.ANY, })
        def _check_and_convert_string(self, v): # Simplified version from IfNode v1.2.0
            if isinstance(v, str):
                if v.lower()=='true': return True;
                if v.lower()=='false': return False;
                if v.isdigit() or (v.startswith('-') and v[1:].isdigit()): return int(v)
                try: return float(v)
                except ValueError: pass
            return v
        async def execute(self, node_data: dict) -> dict:
            node_name = node_data.get('__node_name', 'if_node'); logger.debug(f"Executing IfNode: {node_name}")
            try:
                params = node_data.get("params", {}); val1 = params.get("value1"); op = params.get("operator"); val2 = params.get("value2"); case_sensitive = params.get("case_sensitive", True)
                if not op or not isinstance(op, str): raise NodeValidationError("Missing 'operator'")
                logger.info(f"{node_name} - Received: v1='{val1}'({type(val1).__name__}), op='{op}', v2='{val2}'({type(val2).__name__}), cs={case_sensitive}")
                condition_met = False; error_msg = None
                try:
                    str_val1 = str(val1); str_val2 = str(val2) if val2 is not None else None; str_val1_cmp = str_val1.lower() if not case_sensitive and isinstance(val1, str) else str_val1; str_val2_cmp = str_val2.lower() if not case_sensitive and isinstance(val2, str) and str_val2 is not None else str_val2
                    unary_ops = ["is_true", "is_false", "is_empty", "is_not_empty"]; binary_ops_req_val2 = ["==", "eq", "!=", "ne", ">", "gt", "<", "lt", ">=", "ge", "<=", "le","contains", "not contains", "starts_with", "ends_with"]
                    if op in unary_ops: conv_val1 = self._check_and_convert_string(val1); logger.debug(f"{node_name} - Unary op '{op}' using: '{conv_val1}' ({type(conv_val1).__name__})"); condition_met = bool(conv_val1) if op=="is_true" else (not bool(conv_val1) if op=="is_false" else (conv_val1 is None or (hasattr(conv_val1, '__len__') and len(conv_val1) == 0)) if op=="is_empty" else (conv_val1 is not None and (not hasattr(conv_val1, '__len__') or len(conv_val1) > 0)))
                    elif op in binary_ops_req_val2:
                        if val2 is None: raise ValueError(f"Operator '{op}' requires value2")
                        elif op in ["==", "eq"]: condition_met = (str_val1_cmp == str_val2_cmp) if not case_sensitive and isinstance(val1, str) and isinstance(val2, str) else (val1 == val2)
                        elif op in ["!=", "ne"]: condition_met = (str_val1_cmp != str_val2_cmp) if not case_sensitive and isinstance(val1, str) and isinstance(val2, str) else (val1 != val2)
                        elif op in [">", "gt", "<", "lt", ">=", "ge", "<=", "le"]:
                             try: condition_met = (val1 > val2) if op in [">","gt"] else (val1 < val2) if op in ["<","lt"] else (val1 >= val2) if op in [">=","ge"] else (val1 <= val2)
                             except TypeError: logger.debug(f"{node_name} - TypeError on direct numeric compare, attempting conversion..."); conv_val1 = self._check_and_convert_string(val1); conv_val2 = self._check_and_convert_string(val2); logger.debug(f"{node_name} - Converted for fallback: '{conv_val1}'({type(conv_val1).__name__}), '{conv_val2}'({type(conv_val2).__name__})");
                             if isinstance(conv_val1, numbers.Number) and isinstance(conv_val2, numbers.Number): condition_met = (conv_val1 > conv_val2) if op in [">","gt"] else (conv_val1 < conv_val2) if op in ["<","lt"] else (conv_val1 >= conv_val2) if op in [">=","ge"] else (conv_val1 <= conv_val2)
                             else: raise TypeError(f"Numeric compare failed after conversion: {type(val1).__name__} vs {type(val2).__name__}")
                        elif op == "contains": container = str_val1_cmp if isinstance(val1, str) and not case_sensitive else val1; item = str_val2_cmp if isinstance(val1, str) and isinstance(val2, str) and not case_sensitive else val2; condition_met = item in container if isinstance(container,(str,list,tuple,dict)) else False
                        elif op == "starts_with": condition_met = str_val1_cmp.startswith(str_val2_cmp) if isinstance(val1, str) and isinstance(val2, str) else False
                        elif op == "ends_with": condition_met = str_val1_cmp.endswith(str_val2_cmp) if isinstance(val1, str) and isinstance(val2, str) else False
                    else: error_msg = f"Unsupported operator: {op}"
                    if error_msg: raise NodeExecutionError(error_msg)
                except TypeError as e: return self.handle_error(NodeExecutionError(f"Type error on compare for '{op}': {e}. Comparing '{val1}'({type(val1).__name__}) and '{val2}'({type(val2).__name__})"), context=f"{node_name} Comparison")
                except ValueError as e: return self.handle_error(NodeExecutionError(str(e)), context=f"{node_name} Setup")
                except NodeExecutionError as e: return self.handle_error(e, context=f"{node_name} Logic")
                except Exception as e: return self.handle_error(e, context=f"{node_name} Comparison")
                logger.info(f"{node_name} - Condition '{op}' evaluated to: {condition_met}")
                return {"status": "success", "result": {"result": condition_met, "value1_resolved": val1, "value2_resolved": val2}, "message": f"Condition evaluated to {condition_met}"}
            except NodeValidationError as e: return self.handle_error(e, context=f"{node_name} Validation")
            except Exception as e: return self.handle_error(e, context=f"{node_name} Execute")"""
    (nodes_dir / "if_node.py").write_text(if_node_content) # Overwrite with dummy version if needed
    # Add dummy SetNode, GenerateUUIDNode, SwitchNode, OpenAINode if needed for standalone test
    # ... (similar dummy content for other nodes used in the test Actfile) ...

    # --- Dummy Actfile Content ---
    # Using the complex test workflow content
    actfile_content = """
[workflow]
name = "Complex If Test Workflow"
start_node = IfEqualsNumber

[node:IfEqualsNumber]
type     = if; label = "Test: Number == 10"; value1 = "{{input.number_value}}"; operator = "=="; value2 = 10
[node:LogEqualsNumberTrue]
type     = LogMessage; message = "[PASSED] {{input.number_value}} == 10"
[node:LogEqualsNumberFalse]
type     = LogMessage; level = error; message = "[FAILED] {{input.number_value}} == 10"

[node:IfNotEqualsNumber]
type     = if; label = "Test: Number != 5"; value1 = "{{input.number_value}}"; operator = "!="; value2 = 5
[node:LogNotEqualsNumberTrue]
type     = LogMessage; message = "[PASSED] {{input.number_value}} != 5"
[node:LogNotEqualsNumberFalse]
type     = LogMessage; level = error; message = "[FAILED] {{input.number_value}} != 5"

[node:IfGreaterThanNumber]
type     = if; label = "Test: Number > 5"; value1 = "{{input.number_value}}"; operator = ">"; value2 = 5
[node:LogGreaterThanNumberTrue]
type     = LogMessage; message = "[PASSED] {{input.number_value}} > 5"
[node:LogGreaterThanNumberFalse]
type     = LogMessage; level = error; message = "[FAILED] {{input.number_value}} > 5"

[node:IfFinalLog]
type = LogMessage
message = "Complex If Workflow Completed All Possible Paths."

[edges]
IfEqualsNumber = LogEqualsNumberTrue
IfEqualsNumber = LogEqualsNumberFalse
LogEqualsNumberFalse = IfNotEqualsNumber

IfNotEqualsNumber = LogNotEqualsNumberTrue
IfNotEqualsNumber = LogNotEqualsNumberFalse
LogNotEqualsNumberFalse = IfGreaterThanNumber

IfGreaterThanNumber = LogGreaterThanNumberTrue
IfGreaterThanNumber = LogGreaterThanNumberFalse
LogGreaterThanNumberFalse = IfFinalLog
LogGreaterThanNumberTrue = IfFinalLog
"""
    actfile_path.write_text(actfile_content)

    # --- Define Initial Input ---
    initial_test_data = {"input": {"number_value": 10, "other_value": "abc"}}
    print(f"Using Initial Input: {json.dumps(initial_test_data, indent=2)}")

    # --- Execute ---
    try:
        print("\n--- Initializing ExecutionManager ---")
        if not actfile_path.is_file(): raise FileNotFoundError(f"Actfile missing at {actfile_path}")
        execution_manager = ExecutionManager(actfile_path=str(actfile_path))
        print("\n--- Executing Complex Workflow ---")
        workflow_result = execution_manager.execute_workflow(initial_input=initial_test_data) # Pass input!
        print("\n--- Complex Workflow Final Result ---")
        print(execution_manager.log_safe_node_data(workflow_result))
        print("\n--- Review Logs Above for [PASSED]/[FAILED] and Detailed Execution ---")
    except Exception as e:
        print(f"\n--- An error occurred during testing ---"); print(f"Error: {e}"); traceback.print_exc()
    # --- Optional Cleanup ---
    # finally: print("\n--- Cleaning up temporary test files ---"); # Add cleanup logic