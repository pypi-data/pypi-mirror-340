#!/usr/bin/env python3
"""
Simple CLI command to output MCP server tools as JSON
"""
import asyncio
import json
import sys
import logging
from typing import Optional, List

from mcp_registry.compound import MCPServerSettings, ServerRegistry, MCPAggregator
from mcp_registry.utils.config import load_config


async def get_tools_json(server_names: Optional[List[str]] = None) -> dict:
    """Get tools from servers as JSON-friendly dictionary"""
    # Load config
    config = load_config()
    
    # Filter servers if specified
    available_servers = {
        name: MCPServerSettings(**settings)
        for name, settings in config["mcpServers"].items()
        if not server_names or name in server_names
    }
    
    if not available_servers:
        return {}
        
    # Create registry
    registry = ServerRegistry(available_servers)
    
    # Use context manager to ensure connections are properly established
    async with MCPAggregator(registry) as aggregator:
        # Get tools with server mapping
        server_tools = await aggregator.list_tools(return_server_mapping=True)

        # Convert to JSON-friendly format
        result = {}
        for server_name, tools in server_tools.items():
            result[server_name] = []
            for tool in tools:
                # Extract basic info
                tool_info = {
                    "name": tool.name,
                    "description": getattr(tool, "description", "")
                }
                
                # Extract parameters if available
                if hasattr(tool, 'inputSchema') and tool.inputSchema:
                    parameters = []
                    props = tool.inputSchema.get("properties", {})
                    required = tool.inputSchema.get("required", [])
                    
                    for name, prop in props.items():
                        param_type = prop.get("type", "any")
                        is_required = name in required
                        description = prop.get("description", "")
                        
                        parameters.append({
                            "name": name,
                            "type": param_type,
                            "required": is_required,
                            "description": description
                        })
                        
                    if parameters:
                        tool_info["parameters"] = parameters
                        
                result[server_name].append(tool_info)
                
        return result


def main():
    # Suppress logging
    logging.getLogger("mcp_registry").setLevel(logging.ERROR)
    
    # Get server names from command line args
    server_names = sys.argv[1:] if len(sys.argv) > 1 else None
    
    try:
        # Run async function
        result = asyncio.run(get_tools_json(server_names))
        
        # Output JSON result
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        # Output empty JSON on error
        print("{}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()