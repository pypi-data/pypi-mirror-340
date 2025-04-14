#!/usr/bin/env python3
"""
Simple test script to debug JSON output with mcp-registry
"""
import asyncio
import json
import sys
from mcp_registry.compound import MCPServerSettings, ServerRegistry, MCPAggregator
from mcp_registry.utils.config import load_config

async def main():
    # Load config and create registry
    config = load_config()
    
    # Just use memory server for testing
    server_name = "memory"
    if server_name not in config["mcpServers"]:
        print(f"Server '{server_name}' not found in config", file=sys.stderr)
        return
        
    settings = MCPServerSettings(**config["mcpServers"][server_name])
    registry = ServerRegistry({server_name: settings})
    
    # Use the context manager for aggregator to ensure connections are fully established
    async with MCPAggregator(registry) as aggregator:
        # Get tools with server mapping
        server_tools = await aggregator.list_tools(return_server_mapping=True)
        
        # Convert tools to a JSON-friendly format
        json_result = {}
        for server_name, tools in server_tools.items():
            json_result[server_name] = []
            for tool in tools:
                # Extract basic info
                tool_info = {
                    "name": tool.name,
                    "description": getattr(tool, "description", "")
                }
                
                # Extract parameter information if available
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
                        
                json_result[server_name].append(tool_info)
        
        # Print the JSON result
        print(json.dumps(json_result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())