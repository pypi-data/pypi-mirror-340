# src/genbase_agent_client/base_agent.py

import rpyc
import os
import json
import uuid
import inspect
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Literal, Optional, Tuple, Union, Callable, TypeVar, Type
from pydantic import BaseModel, ValidationError
from functools import wraps
import dataclasses




# Import from local types module
from .types import (
    AgentContext,
    IncludeOptions,
    ProfileStoreFilter,
    ProfileStoreInfo,
    ProfileStoreRecord, # Assuming you keep this dataclass client-side
)

# Define dummy interfaces based on expected engine service contracts
# These help with type hinting but don't need full implementations here.
class RepoServiceInterface: pass
class ProfileStoreServiceInterface: pass
class AgentUtilsInterface: pass

# Import necessary types from litellm (ensure listed in dependencies)
try:
    from litellm import ModelResponse, ChatCompletionMessageToolCall
except ImportError:
    # Provide dummy types if litellm isn't installed
    ModelResponse = dict # type: ignore
    ChatCompletionMessageToolCall = dict # type: ignore

# Define ResponseType for create_structured
ResponseType = TypeVar('ResponseType', bound=BaseModel)

# Import from other libraries (ensure listed in dependencies)
from loguru import logger

# --- Tool Decorator & Collector ---
def tool(func):
    """Decorator to mark agent methods as callable tools for the LLM."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper._is_tool = True # Mark the function
    return wrapper

def collect_tools(instance) -> Dict[str, Callable]:
    """Collects methods decorated with @tool from an agent instance."""
    tools = {}
    for name in dir(instance):
        if name.startswith('_'):
            continue
        try:
            attr = getattr(instance, name)
            # Check if it's a callable method marked by our decorator
            if callable(attr) and hasattr(attr, '_is_tool') and attr._is_tool:
                tools[name] = attr
        except Exception:
            # Ignore attributes that might raise errors on access
            continue
    return tools

# --- Internal Tool Manager (Runs Locally in Client Container) ---
class FunctionMetadata(BaseModel):
    """Basic metadata for a function (tool)."""
    name: str
    description: str
    parameters: Dict[str, Any] # Simplified: JSON Schema for parameters
    is_async: bool

class InternalToolManager:
    """Manages @tool decorated methods WITHIN the agent class."""
    def __init__(self):
        self._internal_tools: Dict[str, Callable] = {}
        self._internal_tool_metadata: Dict[str, FunctionMetadata] = {}
        logger.debug("InternalToolManager initialized.")

    def register_tool(self, name: str, func: Callable, description: Optional[str] = None):
        """Registers a single tool."""
        if name in self._internal_tools:
            # Allow re-registration for potential hot-reloading scenarios? Or raise error?
            logger.warning(f"Re-registering tool: {name}")
            # raise ValueError(f"Tool '{name}' already registered")
        self._internal_tools[name] = func
        try:
            # Extract metadata (can be simple or complex)
            self._internal_tool_metadata[name] = self._extract_function_metadata(func, name, description)
            logger.debug(f"Registered internal tool: {name}")
        except Exception as e:
            logger.error(f"Failed to extract metadata for tool '{name}': {e}", exc_info=True)
            # Rollback registration if metadata extraction fails
            if name in self._internal_tools:
                del self._internal_tools[name]
            raise

    def clear_tools(self):
        """Clears all registered tools."""
        logger.debug("Clearing all internal tools.")
        self._internal_tools = {}
        self._internal_tool_metadata = {}

    def register_tools(self, functions: Dict[str, Callable]):
        """Registers multiple tools, clearing existing ones first."""
        self.clear_tools()
        for name, func in functions.items():
            try:
                self.register_tool(name, func, inspect.getdoc(func))
            except Exception as e:
                # Log error but continue registering other tools
                logger.error(f"Failed to register tool '{name}': {e}", exc_info=True)

    def get_tool_metadata(self, tool_name: str) -> Optional[FunctionMetadata]:
        """Gets metadata for a specific tool."""
        return self._internal_tool_metadata.get(tool_name)

    def get_tool_function(self, tool_name: str) -> Optional[Callable]:
        """Gets the callable function for a tool."""
        return self._internal_tools.get(tool_name)

    def get_all_tools(self) -> List[str]:
        """Gets a list of names of all registered tools."""
        return list(self._internal_tools.keys())

    def has_tool(self, tool_name: str) -> bool:
        """Checks if a tool with the given name is registered."""
        return tool_name in self._internal_tools

    def get_tool_definitions(self, tool_names: Optional[Union[List[str], Literal["all", "none"]]] = None) -> List[Dict[str, Any]]:
        """Gets OpenAI-compatible tool definitions for specified tools."""
        names_to_process = []
        if tool_names == "all" or tool_names is None:
            names_to_process = self.get_all_tools()
        elif tool_names == "none":
            return []
        elif isinstance(tool_names, list):
            names_to_process = [name for name in tool_names if self.has_tool(name)]
        else: # Should not happen with IncludeOptions validation, but handle defensively
             logger.warning(f"Invalid value for tool_names in get_tool_definitions: {tool_names}")
             return []

        tools_definitions = []
        for name in names_to_process:
            metadata = self.get_tool_metadata(name)
            if metadata:
                tools_definitions.append({
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": metadata.description,
                        "parameters": metadata.parameters # Assumes schema is already correct
                    }
                })
            else:
                 logger.warning(f"Metadata not found for registered tool: {name}")
        return tools_definitions

    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Executes the specified tool with given parameters."""
        if not self.has_tool(tool_name):
            raise ValueError(f"Internal tool '{tool_name}' not found.")
        func = self._internal_tools[tool_name]
        try:
            if inspect.iscoroutinefunction(func):
                return await func(**parameters)
            else:
                # Consider running sync functions in a thread pool if they are blocking
                return func(**parameters)
        except Exception as e:
            logger.error(f"Error executing internal tool '{tool_name}': {e}", exc_info=True)
            raise # Re-raise the original exception

    def _extract_function_metadata(self, func: Callable, name: str, description: Optional[str] = None) -> FunctionMetadata:
        """Extracts metadata from a function signature and docstring."""
        # Using inspect for more robust extraction than the previous simplified version
        sig = inspect.signature(func)
        type_hints = inspect.get_annotations(func, eval_str=True) # Use eval_str for forward refs

        params_properties = {}
        required_params = []

        for param_name, param in sig.parameters.items():
            if param_name in ('self', 'cls'): # Skip self/cls
                continue

            param_type = type_hints.get(param_name, Any)
            schema = self._type_to_jsonschema(param_type) # Convert type hint to JSON schema segment

            # Extract description from docstring (simplified example)
            # A more robust parser would handle different docstring styles (RST, Google, Numpy)
            docstring = inspect.getdoc(func)
            param_desc = f"Parameter {param_name}"
            if docstring:
                 # Basic search for :param or @param
                 match = inspect.cleandoc(f""":param {param_name}:""").join(docstring.splitlines()) # Poor man's search
                 # More robust parsing needed here...
                 pass # Placeholder for real docstring parsing

            schema['description'] = param_desc # Add description to schema

            params_properties[param_name] = schema
            if param.default is param.empty:
                required_params.append(param_name)

        final_params_schema = {
            "type": "object",
            "properties": params_properties,
        }
        if required_params:
            final_params_schema["required"] = required_params

        doc = description or inspect.getdoc(func) or f"Executes the {name} tool."
        # Use first line of docstring if multi-line
        final_description = doc.split('\n', 1)[0]

        return FunctionMetadata(
            name=name,
            description=final_description,
            parameters=final_params_schema,
            is_async=inspect.iscoroutinefunction(func)
        )

    def _type_to_jsonschema(self, py_type: Type) -> Dict[str, Any]:
        """Converts basic Python types to JSON Schema components."""
        # This is a simplified converter. A library like Pydantic's schema generation
        # or 'python-jsonschema-objects' would be more robust for complex types.
        origin = getattr(py_type, "__origin__", None)
        args = getattr(py_type, "__args__", [])

        if py_type is str: return {"type": "string"}
        if py_type is int: return {"type": "integer"}
        if py_type is float: return {"type": "number"}
        if py_type is bool: return {"type": "boolean"}
        if py_type is list or origin is list:
            items_schema = self._type_to_jsonschema(args[0]) if args else {}
            return {"type": "array", "items": items_schema}
        if py_type is dict or origin is dict:
            # Assuming string keys, convert value type
            additional_props_schema = self._type_to_jsonschema(args[1]) if len(args) > 1 else {}
            return {"type": "object", "additionalProperties": additional_props_schema}
        if origin is Union:
            # Handle Optional[T] -> T + nullable or oneOf for Union[T, U]
            types = [self._type_to_jsonschema(arg) for arg in args if arg is not type(None)]
            if type(None) in args: # Optional[T]
                 if len(types) == 1:
                      schema = types[0]
                      # Add nullable - either by adding "null" to type array or using oneOf
                      if isinstance(schema.get("type"), list):
                           if "null" not in schema["type"]: schema["type"].append("null")
                      elif "type" in schema:
                           schema["type"] = [schema["type"], "null"]
                      else: # Handle complex cases like oneOf/anyOf within Optional
                           schema = {"oneOf": [schema, {"type": "null"}]}
                      return schema
                 else: # Optional[Union[T, U]]
                      return {"oneOf": types + [{"type": "null"}]}
            else: # Union[T, U]
                 return {"oneOf": types}
        if hasattr(py_type, 'model_json_schema'): # Pydantic model
             try: return py_type.model_json_schema()
             except Exception: pass # Fallback if schema generation fails

        # Default fallback for unknown types
        return {"type": "object", "description": f"Type: {getattr(py_type, '__name__', str(py_type))}"}


# --- Client-Side Facades using RPyC ---
class RemoteAgentUtilsRPyC(AgentUtilsInterface):
    """Facade for AgentUtils methods, making RPyC calls to the engine."""
    def __init__(self, rpyc_root: Any, context: AgentContext):
        self._root = rpyc_root
        self._context = context
        # Store context info needed for calls
        self.module_id = context.module_id
        self.profile = context.profile
        # These are not directly used client-side but satisfy the interface
        self.repo_path = None
        self.module_service = None
        self.repo_service = None

    def read_file(self, relative_path: str) -> Optional[str]:
        try:
            return self._root.exposed_read_file(self.module_id, self.profile, relative_path)
        except Exception as e:
            logger.error(f"RPyC read_file failed: {e}"); raise RuntimeError from e

    def write_file(self, relative_path: str, content: str) -> bool:
        try:
            return self._root.exposed_write_file(self.module_id, self.profile, relative_path, content)
        except Exception as e:
            logger.error(f"RPyC write_file failed: {e}"); raise RuntimeError from e

    def list_files(self, relative_path: str = "") -> List[str]:
        try:
            return self._root.exposed_list_files(self.module_id, self.profile, relative_path)
        except Exception as e:
            logger.error(f"RPyC list_files failed: {e}"); raise RuntimeError from e

    def get_repo_tree(self, path_str: Optional[str] = None) -> str:
        try:
            return self._root.exposed_get_repo_tree(self.module_id, self.profile, path_str)
        except Exception as e:
            logger.error(f"RPyC get_repo_tree failed: {e}"); raise RuntimeError from e

    def read_files(self, relative_paths: List[str]) -> Dict[str, Optional[str]]:
        # Client-side loop calling the single-file method
        results = {}
        for path in relative_paths:
            try:
                results[path] = self.read_file(path)
            except Exception:
                results[path] = None # Or re-raise?
        return results


class RemoteProfileStoreRPyC(ProfileStoreServiceInterface):
    """Facade for ProfileStoreService methods via RPyC."""
    def __init__(self, rpyc_root: Any, context: AgentContext, collection: str):
        self._root = rpyc_root
        # Store context info needed for calls
        self.storeInfo = ProfileStoreInfo( # Use the actual dataclass if imported
             module_id=context.module_id,
             profile=context.profile,
             collection=collection
        )

    def find(self, filter_: ProfileStoreFilter) -> List[ProfileStoreRecord]:
        try:
            filter_dict = dataclasses.asdict(filter_)
            results_dict_list = self._root.exposed_profile_store_find(
                self.storeInfo.module_id, self.storeInfo.profile, self.storeInfo.collection, filter_dict
            )
            return [ProfileStoreRecord(**r_dict) for r_dict in results_dict_list]
        except Exception as e: logger.error(f"RPyC find failed: {e}"); raise RuntimeError from e

    def set_value(self, value: Dict[str, Any]) -> ProfileStoreRecord:
        try:
            result_dict = self._root.exposed_profile_store_set_value(
                 self.storeInfo.module_id, self.storeInfo.profile, self.storeInfo.collection, value
            )
            return ProfileStoreRecord(**result_dict)
        except Exception as e: logger.error(f"RPyC set_value failed: {e}"); raise RuntimeError from e

    def delete(self, filter_: ProfileStoreFilter) -> int:
        try:
            filter_dict = dataclasses.asdict(filter_)
            return self._root.exposed_profile_store_delete(
                self.storeInfo.module_id, self.storeInfo.profile, self.storeInfo.collection, filter_dict
            )
        except Exception as e: logger.error(f"RPyC delete failed: {e}"); raise RuntimeError from e

    def get_by_id(self, record_id: uuid.UUID) -> Optional[ProfileStoreRecord]:
        try:
            result_dict = self._root.exposed_profile_store_get_by_id(
                self.storeInfo.module_id, self.storeInfo.profile, self.storeInfo.collection, str(record_id)
            )
            return ProfileStoreRecord(**result_dict) if result_dict else None
        except Exception as e: logger.error(f"RPyC get_by_id failed: {e}"); raise RuntimeError from e

    def set_many(self, values: List[Dict[str, Any]]) -> List[ProfileStoreRecord]:
        try:
            results_list = self._root.exposed_profile_store_set_many(
                self.storeInfo.module_id, self.storeInfo.profile, self.storeInfo.collection, values
            )
            return [ProfileStoreRecord(**r_dict) for r_dict in results_list]
        except Exception as e: logger.error(f"RPyC set_many failed: {e}"); raise RuntimeError from e

    def update(self, filter_: ProfileStoreFilter, value: Dict[str, Any]) -> int:
        try:
            filter_dict = dataclasses.asdict(filter_)
            return self._root.exposed_profile_store_update(
                self.storeInfo.module_id, self.storeInfo.profile, self.storeInfo.collection, filter_dict, value
            )
        except Exception as e: logger.error(f"RPyC update failed: {e}"); raise RuntimeError from e


# --- RPyC Client BaseAgent ---
class BaseAgent(ABC):
    """
    Client-side BaseAgent using RPyC to communicate OUT to the PlatformRPyCService.
    Runs inside the Kit's container. Base class for user-defined agents in kits.
    """
    _conn: Optional[rpyc.Connection] = None # RPyC connection OUT to engine

    def __init__(self, context: AgentContext):
        """Initializes the agent, connects to the engine's RPyC service."""
        if not isinstance(context, AgentContext):
            raise TypeError("RPyC Client BaseAgent requires an instance of AgentContext")
        self.context = context
        self._connect_rpyc() # Connect OUT to the engine on initialization

        # Local agent state / managers
        self.system_prompt: Optional[str] = None
        self.tools_schemas: List[Dict[str, Any]] = [] # Combined (local @tool + remote profile tool) schemas
        self.tool_manager = InternalToolManager() # Manages local @tool methods
        self._utils: Optional[RemoteAgentUtilsRPyC] = None # Facade for utils
        self.remote_profile_tools: Dict[str, Dict] = {} # Holds metadata dict for remote tools
        self.current_model: Optional[str] = None # Stores model override for 'create' calls

        logger.info(f"RPyC Client BaseAgent initialized for {self.context.module_id}/{self.context.profile}")

    def _connect_rpyc(self):
        """Establishes the RPyC connection OUT to the Engine."""
        # Read config from environment variables set by the AgentRunnerService
        rpyc_host = os.getenv("RPYC_HOST")
        rpyc_port = int(os.getenv("INTERNAL_RPYC_PORT", 18862)) # Engine's RPyC Port

        if not rpyc_host:
            raise ConnectionError("RPYC_HOST environment variable not set inside the container.")

        # Reuse connection if already established and open
        if self._conn and not self._conn.closed:
            # Optional: Add a quick ping check here to ensure it's really alive
            try:
                self._conn.ping(timeout=1) # RPyC's built-in ping
                logger.debug("Reusing existing RPyC connection OUT to Engine.")
                return
            except Exception:
                logger.warning("Existing RPyC connection failed ping test. Reconnecting.")
                self._conn = None # Force reconnect

        logger.info(f"Agent client connecting OUT to Engine RPyC at {rpyc_host}:{rpyc_port}...")
        try:
            self._conn = rpyc.connect(
                rpyc_host, rpyc_port, service=rpyc.VoidService, # Client doesn't expose services back
                config={
                    "allow_public_attrs": False, # Security setting
                    "allow_pickle": False,       # Security setting
                    "sync_request_timeout": 300, # Timeout for RPyC calls (in seconds)
                }
            )
            # Verify connection with the exposed ping method on the server
            pong = self._conn.root.exposed_ping()
            if pong != "pong_rpyc":
                raise ConnectionError("Ping to PlatformRPyCService failed (unexpected response).")
            logger.info("Agent client successfully connected OUT to Engine PlatformRPyCService.")
        except ConnectionRefusedError as e:
             logger.error(f"RPyC connection OUT refused by {rpyc_host}:{rpyc_port}. Is the engine RPyC server running?")
             raise ConnectionError(f"Connection refused by Engine RPyC server: {e}") from e
        except Exception as e:
            logger.error(f"Agent client failed to connect OUT to Engine RPyC: {e}", exc_info=True)
            self._conn = None # Ensure connection is None on failure
            raise ConnectionError(f"Failed to connect OUT to Engine RPyC: {e}") from e

    @property
    def root(self) -> Any:
        """Provides access to the remote engine service root, ensuring connection."""
        if not self._conn or self._conn.closed:
            logger.warning("RPyC connection OUT closed or not established. Reconnecting...")
            self._connect_rpyc()
        # Add extra ping check on access if needed, but might add overhead
        # try: self._conn.ping(timeout=1) except Exception: self._connect_rpyc()
        return self._conn.root

    @property
    def utils(self) -> RemoteAgentUtilsRPyC:
        """Gets the facade for remote AgentUtils."""
        if self._utils is None:
            self._utils = RemoteAgentUtilsRPyC(self.root, self.context)
        return self._utils

    def get_store(self, collection: str) -> RemoteProfileStoreRPyC:
        """Gets the facade for a specific remote ProfileStore collection."""
        # Consider caching these facade instances if needed
        return RemoteProfileStoreRPyC(self.root, self.context, collection)

    # --- Core Methods Making RPyC Calls OUT ---

    def add_message(self, role: str, content: Optional[str], message_type: str = "text",
                    tool_calls: Optional[List[ChatCompletionMessageToolCall]] = None,
                    tool_call_id: Optional[str] = None, name: Optional[str] = None):
        """Adds a message to the central chat history via RPyC."""
        if not self.context: raise ValueError("Agent context not set")
        # Serialize complex objects like tool_calls before sending
        tool_calls_serializable = [tc.model_dump(mode='json') for tc in tool_calls] if tool_calls else None
        try:
            self.root.exposed_add_message(
                module_id=self.context.module_id,
                profile=self.context.profile,
                session_id=self.context.session_id or str(uuid.UUID(int=0)), # Ensure session_id
                role=role,
                content=content,
                message_type=message_type,
                tool_calls_serializable=tool_calls_serializable,
                tool_call_id=tool_call_id,
                name=name
            )
        except Exception as e:
            logger.error(f"RPyC call failed for add_message: {e}", exc_info=True)
            # Decide on error handling: raise, log, or return status?
            raise RuntimeError(f"Failed to add message to remote history: {e}") from e

    def get_messages(self) -> List[Dict[str, Any]]:
        """Gets the chat history from the engine via RPyC."""
        if not self.context: raise ValueError("Agent context not set")
        try:
            # Server returns JSON serializable list of dicts
            return self.root.exposed_get_messages(
                module_id=self.context.module_id,
                profile=self.context.profile,
                session_id=self.context.session_id or str(uuid.UUID(int=0))
            )
        except Exception as e:
            logger.error(f"RPyC call failed for get_messages: {e}", exc_info=True)
            raise RuntimeError(f"Failed to get remote history: {e}") from e

    async def set_context(
        self,
        agent_instructions: Optional[str] = None,
        include: IncludeOptions = IncludeOptions(tools="all", provided_tools=False, elements="all"),
        model: Optional[str] = None
    ) -> tuple[str, List[Dict[str, Any]]]:
        """
        Builds the system prompt and tool schemas for LLM calls.
        Collects local @tool methods and fetches remote profile tool metadata via RPyC.
        """
        if not self.context: raise ValueError("Agent context not set")
        self.current_model = model # Store model override for subsequent 'create' calls

        # 1. Collect and register local @tool methods
        local_agent_tools = collect_tools(self)
        self.tool_manager.register_tools(local_agent_tools)
        local_tool_schemas = self.tool_manager.get_tool_definitions(include.tools)

        # 2. Fetch Remote Profile Metadata via RPyC
        remote_meta_dict: Optional[Dict] = None
        remote_profile_tool_schemas: List[Dict] = []
        self.remote_profile_tools = {} # Reset map for remote tools
        try:
            logger.debug(f"Fetching remote profile metadata via RPyC for {self.context.profile}...")
            remote_meta_dict = self.root.exposed_get_profile_metadata(
                self.context.module_id, self.context.profile, include.provided_tools
            )
            logger.debug(f"Received remote metadata dict: {bool(remote_meta_dict)}")

            # Process tools from the received metadata dict
            if remote_meta_dict and remote_meta_dict.get('tools'):
                 for tool_dict in remote_meta_dict['tools']: # It's already a list of dicts
                     # Safely access potentially missing keys
                     tool_info = tool_dict.get('tool', {})
                     tool_name = tool_info.get('name')
                     metadata = tool_dict.get('metadata') # This should contain parameters schema etc.

                     if not tool_name: continue # Skip if name is missing

                     # Determine if this remote tool should be included based on 'include.tools'
                     should_include = (include.tools == "all" or
                                       (isinstance(include.tools, list) and tool_name in include.tools))

                     if should_include:
                         if metadata and metadata.get('parameters') is not None:
                             remote_profile_tool_schemas.append({
                                 "type": "function",
                                 "function": {
                                     "name": tool_name,
                                     "description": tool_info.get('description') or metadata.get('description', ''),
                                     "parameters": metadata.get('parameters') # Use the schema from metadata
                                 }
                             })
                             # Store the full dict for later use in _execute_remote_tool
                             self.remote_profile_tools[tool_name] = tool_dict
                         else:
                             logger.warning(f"Remote profile tool '{tool_name}' included but missing required metadata (parameters). Skipping schema.")
                             # Store info even without schema if needed, but LLM can't call it effectively
                             # self.remote_profile_tools[tool_name] = tool_dict

        except Exception as e:
            logger.error(f"RPyC failed to get or parse remote profile metadata: {e}", exc_info=True)
            remote_meta_dict = None # Ensure it's None on error

        # 3. Combine Tool Schemas (Local @tool take precedence over remote profile tools)
        final_tool_schemas_dict = {tool['function']['name']: tool for tool in local_tool_schemas}
        for schema in remote_profile_tool_schemas:
            name = schema['function']['name']
            if name not in final_tool_schemas_dict:
                final_tool_schemas_dict[name] = schema
            else:
                logger.warning(f"Tool name collision: Local @tool '{name}' overrides remote profile tool '{name}'.")
        self.tools_schemas = list(final_tool_schemas_dict.values()) # Store combined schemas

        # 4. Construct System Prompt
        parts: Dict[str, str] = {}
        if agent_instructions: parts["Agent Instructions"] = agent_instructions

        # Add profile instructions if fetched
        if remote_meta_dict and remote_meta_dict.get('instructions'):
             # Extract instruction content or description
             profile_instructions_text = "\n".join(
                 f"- {instr.get('name')}: {instr.get('description') or instr.get('content', '')[:100]+'...'}"
                 for instr in remote_meta_dict['instructions']
             )
             if profile_instructions_text: parts["Profile Instructions"] = profile_instructions_text

        # Add descriptions of available tools (both local and remote)
        tool_descriptions = [
            f"- {s['function']['name']}: {s['function']['description']}"
            for s in self.tools_schemas # Use the combined list
        ]
        if tool_descriptions:
            parts["Available Tools"] = "\n".join(tool_descriptions)

        # Add element formatting docs (if requested)
        # This part might need adjustment if get_element_format_documentation isn't available client-side
        # Option 1: Fetch from server? Option 2: Include basic version in client library?
        # For now, using a placeholder.
        if include.elements != "none":
             # element_docs = get_element_format_documentation(include.elements) # Requires function here
             element_docs = "Use <element format='markdown|html|json|etc'>...</element> tags for rich output." # Placeholder
             if element_docs: parts["Generative Elements Formatting"] = element_docs

        # Assemble the final prompt string
        final_prompt = ""
        for key, value in parts.items():
             if value:
                 final_prompt += f"\n\n## {key}:\n{value}"
        self.system_prompt = final_prompt.strip()

        logger.info(f"RPyC Context set. System Prompt length: {len(self.system_prompt)}. Tools available: {len(self.tools_schemas)}")
        return self.system_prompt, self.tools_schemas

    async def run_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Executes a LOCAL @tool decorated method."""
        if not self.context: raise ValueError("Agent context not set")
        logger.info(f"Attempting LOCAL tool execution: {tool_name}")
        if self.tool_manager.has_tool(tool_name):
            try:
                # Use the InternalToolManager to handle async/sync execution
                result = await self.tool_manager.execute_tool(tool_name, parameters)
                logger.info(f"Local tool '{tool_name}' executed successfully.")
                return result
            except Exception as e:
                # Error already logged by execute_tool
                raise RuntimeError(f"Local tool '{tool_name}' failed: {e}") from e
        else:
            logger.error(f"Local tool '{tool_name}' not found by tool manager.")
            raise ValueError(f"Local tool '{tool_name}' not defined or registered.")

    async def _execute_remote_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Executes a REMOTE profile tool (defined in kit.yaml) via RPyC."""
        if not self.context: raise ValueError("Agent context not set")
        logger.info(f"Attempting REMOTE tool execution via RPyC: {tool_name}")

        # Get the metadata dict stored during set_context
        remote_tool_dict = self.remote_profile_tools.get(tool_name)
        if not remote_tool_dict:
            raise ValueError(f"Unknown remote tool '{tool_name}' or metadata not available.")

        # Extract necessary info from the stored dict
        module_id_to_run = remote_tool_dict.get('module_id') or self.context.module_id
        is_provided = remote_tool_dict.get('is_provided', False)

        try:
            # Call the exposed RPyC method on the engine server
            result = self.root.exposed_run_tool(
                module_id=module_id_to_run,
                profile=self.context.profile, # Profile context remains the receiver's profile
                tool_name=tool_name,
                parameters=parameters,
                is_provided=is_provided
            )
            logger.info(f"Remote tool '{tool_name}' executed successfully via RPyC.")
            return result # RPyC handles serialization of basic return types
        except Exception as e:
            logger.error(f"RPyC failed executing remote tool '{tool_name}': {e}", exc_info=True)
            # Propagate error clearly indicating it was a remote execution failure
            raise RuntimeError(f"Remote profile tool '{tool_name}' execution failed: {e}") from e

    async def create(
        self,
        messages: List[Dict[str, Any]],
        stream: bool = False, # Note: Streaming is overridden to False for RPyC call
        tool_choice: Optional[str] = "auto",
        save_messages: bool = True,
        run_tools: bool = True,
        use_history: bool = True,
        max_tool_iterations: int = 5,
        **kwargs
    ) -> ModelResponse:
        """
        Main interaction loop: fetches history, calls LLM (via RPyC),
        handles local and remote tool calls, and saves history.
        """
        if not self.context: raise ValueError("Agent context not set")

        # --- Message Preparation ---
        history = self.get_messages() if use_history else []
        # Ensure system prompt is first if it exists
        all_messages = ([{"role": "system", "content": self.system_prompt}] if self.system_prompt else []) + history + messages

        # Save initial user messages to history (if requested)
        if save_messages:
            for msg in messages:
                 # Typically only save user messages from the input list here
                 if msg.get("role") == "user":
                     self.add_message(msg["role"], msg.get("content"))

        logger.debug(f"RPyC Client calling create. Total messages: {len(all_messages)}")

        # --- Tool Execution Loop ---
        tool_iterations = 0
        current_llm_response: Optional[ModelResponse] = None # Store last LLM response

        while tool_iterations < max_tool_iterations:
            # --- Call LLM via RPyC ---
            try:
                # Force stream=False for RPyC call
                if stream: logger.warning("Streaming not supported in RPyC create, using non-streaming.")
                response_dict = self.root.exposed_chat_completion(
                    messages=all_messages,
                    model=self.current_model, # Use model set during set_context
                    stream=False, # RPyC limitation
                    tools=self.tools_schemas or None, # Use combined schemas
                    tool_choice=tool_choice if self.tools_schemas else None,
                    **kwargs
                )
                # Validate/parse the response dictionary
                current_llm_response = ModelResponse.model_validate(response_dict)
            except Exception as e:
                logger.error(f"RPyC chat completion call failed: {e}", exc_info=True)
                raise RuntimeError(f"LLM call failed via RPyC: {e}") from e

            # --- Process LLM Response ---
            if not current_llm_response or not current_llm_response.choices:
                 logger.warning("LLM response missing choices.")
                 if save_messages: self.add_message("assistant", "[LLM response empty]")
                 return current_llm_response or ModelResponse() # Return empty if None

            assistant_message = current_llm_response.choices[0].message

            # --- Check for Tool Calls ---
            # Validate tool_calls structure before proceeding
            tool_calls_list = []
            if run_tools and assistant_message.tool_calls:
                try:
                    # Ensure tool_calls is a list of valid ChatCompletionMessageToolCall objects
                    tool_calls_list = [ChatCompletionMessageToolCall.model_validate(tc) for tc in assistant_message.tool_calls]
                except (ValidationError, TypeError) as val_err:
                    logger.error(f"Invalid tool_calls structure received from LLM: {val_err} - Data: {assistant_message.tool_calls}")
                    # Decide how to handle - stop loop, add error message?
                    if save_messages: self.add_message("assistant", assistant_message.content or "[Received invalid tool calls]")
                    return current_llm_response # Return the response with invalid calls

            if run_tools and tool_calls_list:
                tool_iterations += 1
                logger.info(f"Processing tool calls (Iteration: {tool_iterations}/{max_tool_iterations})")

                # Save assistant message with tool calls to history
                if save_messages:
                    self.add_message(
                        role="assistant",
                        content=assistant_message.content, # Can be None
                        message_type="tool_calls",
                        tool_calls=tool_calls_list # Pass validated list
                    )

                # --- Execute Tools (Local or Remote) ---
                tool_results_for_next_call = []
                execution_tasks = []

                # Prepare tasks for concurrent execution if desired (using asyncio.gather)
                for tool_call in tool_calls_list:
                    tool_name = tool_call.function.name
                    tool_call_id = tool_call.id
                    try:
                        parameters = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        logger.error(f"Failed to parse arguments for tool '{tool_name}': {tool_call.function.arguments}")
                        # Add error result and continue to next tool call
                        result_str = json.dumps({"error": f"Invalid JSON arguments received for tool '{tool_name}'."})
                        if save_messages: self.add_message("tool", result_str, "tool_result", tool_call_id=tool_call_id, name=tool_name)
                        tool_results_for_next_call.append({ "role": "tool", "tool_call_id": tool_call_id, "name": tool_name, "content": result_str})
                        continue

                    # Determine if local or remote and create an awaitable task
                    if self.tool_manager.has_tool(tool_name):
                        execution_tasks.append(self.run_tool(tool_name, parameters))
                    elif tool_name in self.remote_profile_tools:
                        execution_tasks.append(self._execute_remote_tool(tool_name, parameters))
                    else:
                        logger.error(f"Tool '{tool_name}' requested by LLM but not found locally or in remote profile.")
                        result_str = json.dumps({"error": f"Tool '{tool_name}' is not available."})
                        if save_messages: self.add_message("tool", result_str, "tool_result", tool_call_id=tool_call_id, name=tool_name)
                        tool_results_for_next_call.append({ "role": "tool", "tool_call_id": tool_call_id, "name": tool_name, "content": result_str})
                        # No task to add for unknown tool

                # Execute tasks concurrently (optional, can run sequentially if needed)
                # Note: RPyC calls (_execute_remote_tool) are synchronous from client perspective,
                # but local async tools (run_tool) will run concurrently.
                results = await asyncio.gather(*execution_tasks, return_exceptions=True)

                # Process results and prepare for next LLM call
                result_index = 0
                for tool_call in tool_calls_list: # Iterate again to match results
                    tool_name = tool_call.function.name
                    tool_call_id = tool_call.id

                    # Skip if this tool wasn't found/executed
                    if not (self.tool_manager.has_tool(tool_name) or tool_name in self.remote_profile_tools):
                        continue

                    result_obj = results[result_index]
                    result_index += 1
                    result_content_str = ""

                    if isinstance(result_obj, Exception):
                        logger.error(f"Tool call '{tool_name}' failed during execution: {result_obj}", exc_info=result_obj)
                        result_content_str = json.dumps({"error": f"Tool execution failed: {result_obj}"})
                    else:
                        try:
                            # Attempt to serialize result to JSON
                            result_content_str = json.dumps(result_obj)
                        except TypeError:
                            logger.warning(f"Result for tool '{tool_name}' is not JSON serializable. Converting to string.")
                            result_content_str = json.dumps(str(result_obj)) # Fallback to string conversion

                    # Save tool result message to history
                    if save_messages:
                        self.add_message(
                            role="tool",
                            content=result_content_str,
                            message_type="tool_result",
                            tool_call_id=tool_call_id,
                            name=tool_name
                        )
                    # Add result for the next LLM query
                    tool_results_for_next_call.append({
                         "role": "tool",
                         "tool_call_id": tool_call_id,
                         "name": tool_name,
                         "content": result_content_str,
                    })

                # Add results to messages for the next iteration
                all_messages.extend(tool_results_for_next_call)

                # Check if max iterations reached
                if tool_iterations >= max_tool_iterations:
                     logger.warning(f"Reached max tool iterations ({max_tool_iterations}). Returning last LLM response.")
                     return current_llm_response # Return the response that requested the tools

            else:
                # No tool calls requested, this is the final response
                logger.info("LLM interaction finished, no further tool calls requested.")
                if save_messages and assistant_message.content:
                    self.add_message("assistant", assistant_message.content)
                return current_llm_response # End loop and return final response

        # Should not be reached if loop logic is correct, but acts as a fallback
        logger.warning(f"Exiting create loop unexpectedly after {tool_iterations} iterations.")
        return current_llm_response or ModelResponse()


    async def create_structured(
        self,
        messages: List[Dict[str, Any]],
        response_model: Type[ResponseType],
        save_messages: bool = True,
        use_history: bool = True,
        **kwargs
    ) -> Tuple[ResponseType, ModelResponse]:
        """Gets structured output from the LLM via RPyC, handling history."""
        if not self.context: raise ValueError("Agent context not set")

        # --- Message Preparation ---
        history = self.get_messages() if use_history else []
        all_messages = ([{"role": "system", "content": self.system_prompt}] if self.system_prompt else []) + history + messages

        # Save user messages if requested
        if save_messages:
            for msg in messages:
                 if msg.get("role") == "user":
                     self.add_message(msg["role"], msg.get("content"))

        logger.debug(f"RPyC Client calling create_structured. Response model: {response_model.__module__}.{response_model.__name__}")

        # --- Call RPyC Service ---
        try:
            # Generate JSON schema from the Pydantic model client-side
            model_schema = response_model.model_json_schema()

            # Call the RPyC method, passing the schema dict
            structured_dict, raw_response_dict = self.root.exposed_structured_output_with_schema(
                messages=all_messages,
                response_model_schema=model_schema, # Pass schema, not type
                model=self.current_model, # Use model set during set_context
                **kwargs
            )

            # --- Process Response ---
            # Reconstruct Pydantic model from the returned dict
            # Server should have validated against the schema (or implement validation here)
            structured_response = response_model.model_validate(structured_dict)
            # Reconstruct the raw ModelResponse object
            raw_response = ModelResponse.model_validate(raw_response_dict)

            # Save assistant message to history if requested
            if save_messages and raw_response.choices:
                assistant_message = raw_response.choices[0].message
                # Decide what to save: raw text or serialized structured data?
                content_to_save = assistant_message.content # Prefer raw text if available
                if not content_to_save and structured_response:
                     try:
                         # Fallback to saving the JSON representation
                         content_to_save = structured_response.model_dump_json(indent=2)
                     except Exception:
                         content_to_save = "[Structured Response Received - Serialization Error]"
                if content_to_save:
                    self.add_message("assistant", content_to_save)
                else: # Handle case where there's neither text nor structure
                    self.add_message("assistant", "[Empty Assistant Response]")


            return structured_response, raw_response

        except Exception as e:
            logger.error(f"RPyC structured output call failed: {e}", exc_info=True)
            raise RuntimeError(f"Structured output failed via RPyC: {e}") from e

    # --- Abstract Methods (Must be implemented by Kit developers) ---
    @property
    @abstractmethod
    def agent_type(self) -> str:
        """Return the unique type identifier for this agent."""
        pass

    @abstractmethod
    async def process_request(self) -> Dict[str, Any]:
        """
        The main entry point for the agent's logic.
        It receives user input via self.context.user_input and should
        return a dictionary, typically containing 'response' and 'results'.
        """
        pass

    # --- Cleanup ---
    def close(self):
        """Closes the RPyC connection OUT to the engine."""
        if hasattr(self,'_conn') and self._conn and not self._conn.closed:
            logger.info(f"Closing RPyC connection OUT for {self.context.module_id}/{self.context.profile}")
            try:
                self._conn.close()
            except Exception as e:
                logger.error(f"Error closing RPyC connection OUT: {e}")
            finally:
                self._conn = None

    def __del__(self):
        """Destructor attempts to close the connection."""
        self.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit, ensures connection closure."""
        self.close()