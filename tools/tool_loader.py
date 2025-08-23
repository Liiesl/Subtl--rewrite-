# tool_loader.py

import sys
import traceback

# Import the list of registered tools from the auto-generated registry.
# This is the Nuitka-friendly way.
from .tool_registry import REGISTERED_TOOL_MODULES

def load_tools():
    """
    Loads all available tools that have been explicitly registered in tool_registry.py.

    This approach is compatible with compilers like Nuitka because it relies on
    explicit imports, allowing the compiler to trace and include all necessary files.
    """
    loaded_tools = {}

    # Iterate through the explicitly imported modules, not the filesystem.
    for module in REGISTERED_TOOL_MODULES:
        try:
            # The tool_id is derived from the module's name (e.g., 'tools.renamer.renamer' -> 'renamer')
            tool_id = module.__name__.split('.')[-1]

            if hasattr(module, 'TOOL_DEFINITION'):
                definition = module.TOOL_DEFINITION
                widget_class = getattr(module, definition['widget_class_name'])

                loaded_tools[tool_id] = {
                    "display_name": definition['display_name'],
                    "widget_class": widget_class,
                    "description": definition.get('description', ''),
                    "can_open_file": definition.get('can_open_file', False),
                    "stylesheet_module": definition.get('stylesheet_module', None),
                }
            else:
                print(f"Warning: Tool module '{module.__name__}' is missing a 'TOOL_DEFINITION'.")

        except (AttributeError, KeyError) as e:
            print(f"Warning: Tool module '{module.__name__}' has a misconfigured definition: {e}")
            traceback.print_exc()

    if not loaded_tools:
        print("Warning: No tools were loaded. Run build_tool_registry.py to generate the tool registry.")

    return loaded_tools

# The single source of truth, now populated at runtime from the static registry.
AVAILABLE_TOOLS = load_tools()