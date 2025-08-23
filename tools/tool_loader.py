# tool_loader.py

import os
import importlib

def load_tools():
    """
    Dynamically discovers and loads all available tools from the 'tools' directory.

    This script resides within the 'tools' directory and scans its sibling folders.
    Each tool is expected to be in its own subdirectory and contain a Python file
    that defines a 'TOOL_DEFINITION' dictionary. The manager reads this definition
    to get the display name, description, and widget class for the tool.

    This approach makes the system plug-and-play: to add a new tool, simply
    add a new folder with the required files, and it will be loaded automatically.
    """
    loaded_tools = {}
    # Since this script is inside the 'tools' directory, its dirname is the directory
    # we want to scan.
    tools_dir = os.path.dirname(__file__)

    # Iterate through items in the 'tools' folder
    for tool_id in os.listdir(tools_dir):
        tool_path = os.path.join(tools_dir, tool_id)
        
        # We must ensure we're looking at a directory for a tool, not this file,
        # __init__.py, __pycache__, etc.
        if os.path.isdir(tool_path) and not tool_id.startswith('__'):
            try:
                # The module name is assumed to be the same as the folder name (tool_id).
                # The import path must be relative to the project root for importlib.
                module_name = f"tools.{tool_id}.{tool_id}"
                module = importlib.import_module(module_name)
                
                # Each tool module must provide its own definition
                if hasattr(module, 'TOOL_DEFINITION'):
                    definition = module.TOOL_DEFINITION
                    
                    # Get the widget class from the loaded module
                    widget_class = getattr(module, definition['widget_class_name'])
                    
                    # Populate the dictionary entry for the tool
                    loaded_tools[tool_id] = {
                        "display_name": definition['display_name'],
                        "widget_class": widget_class,
                        "description": definition.get('description', ''),
                        # NEW: Check for the 'can_open_file' flag, defaulting to False
                        "can_open_file": definition.get('can_open_file', False),
                    }
                else:
                    print(f"Warning: Tool '{tool_id}' is missing a 'TOOL_DEFINITION'.")

            except ImportError as e:
                print(f"Warning: Could not import module for tool '{tool_id}': {e}")
            except (AttributeError, KeyError) as e:
                print(f"Warning: Tool '{tool_id}' has a misconfigured definition: {e}")

    return loaded_tools

# The single source of truth, now populated entirely at runtime.
AVAILABLE_TOOLS = load_tools()