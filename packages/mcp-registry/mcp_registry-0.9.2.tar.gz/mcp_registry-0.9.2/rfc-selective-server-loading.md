# RFC: Selective Server Loading in MCPRegistry

## Summary

This RFC proposes adding a `filter_servers` method to the ServerRegistry class that creates a new registry containing only specified servers. This enhancement will provide a clean, explicit way to work with subsets of configured servers, improving efficiency and resource usage.

## Background and Motivation

Currently, when using MCPAggregator or the `serve` command, we have two approaches to filtering servers:

1. In the CLI's `serve` command, we load the full registry but pass a list of server_names to the run_registry_server function
2. In the MCPAggregator class, we accept a server_names parameter that filters during operations

Both approaches load all server configurations initially, which can be inefficient, especially with many server configurations. Additionally, in the `serve` command, we filter at the command level but pass the full registry to run_registry_server, which can be confusing.

## Proposal

Add a `filter_servers` method to ServerRegistry that creates a new registry with only the specified servers. This will enable explicit filtering at the registry level, which is more aligned with the single responsibility principle.

## API Changes

### Add `filter_servers` method to ServerRegistry

```python
def filter_servers(self, server_names: list[str]) -> "ServerRegistry":
    """
    Create a new ServerRegistry containing only the specified servers.
    
    Args:
        server_names: List of server names to include in the filtered registry
        
    Returns:
        ServerRegistry: A new registry containing only the specified servers
        
    Raises:
        ValueError: If any of the specified servers are not in the registry
    """
    missing = [name for name in server_names if name not in self.registry]
    if missing:
        raise ValueError(f"Servers not found: {', '.join(missing)}")
        
    filtered = {
        name: settings for name, settings in self.registry.items()
        if name in server_names
    }
    return ServerRegistry(filtered)
```

### Update `run_registry_server` function (Optional)

The `run_registry_server` function could be simplified to remove the server_names parameter, as filtering would happen before calling it:

```python
async def run_registry_server(registry: ServerRegistry):
    """
    Create and run an MCP compound server that aggregates tools from the registry.
    
    Args:
        registry: Registry containing only the servers that should be exposed
    """
    # Create server
    server = Server("MCP Registry Server")

    # Create aggregator - no need to filter since registry is already filtered
    aggregator = MCPAggregator(registry)
    
    # ... rest of the implementation
```

## Implementation Plan

1. Add the `filter_servers` method to ServerRegistry class
2. Update the serve.py command to use this method
3. Consider removing the server_names parameter from run_registry_server (optional)
4. Add tests for the new method
5. Update documentation

## Implementation Considerations

1. **Performance**: The proposed changes reduce memory and CPU usage by only loading configurations for servers that will actually be used.

2. **Clarity**: This approach makes it clearer which servers are being used, as filtering happens explicitly.

3. **Single Responsibility**: Each class maintains a clear responsibility:
   - ServerRegistry handles server configuration management and filtering
   - MCPAggregator focuses on tool aggregation

## Backward Compatibility

The proposed changes maintain backward compatibility:

- Adding a new method to ServerRegistry is non-breaking
- The existing MCPAggregator constructor remains unchanged
- If we keep the server_names parameter in run_registry_server, it remains compatible

## Example Usage

### CLI Implementation

```python
# In serve.py
def serve(servers, project):
    # ... existing code to load available_servers ...
    
    # Determine which servers to use
    server_names = list(servers) if servers else None
    
    # Create registry with all available servers
    registry = ServerRegistry(available_servers)
    
    # If specific servers requested, filter the registry
    if server_names:
        try:
            registry = registry.filter_servers(server_names)
            click.echo(f"Serving {len(registry.registry)} servers: {', '.join(registry.registry.keys())}", err=True)
        except ValueError as e:
            click.echo(f"Error: {str(e)}", err=True)
            return
    else:
        click.echo(f"Serving all {len(registry.registry)} available servers", err=True)
    
    # Run the compound server with pre-filtered registry
    asyncio.run(run_registry_server(registry))
```

### Programmatic Usage

```python
# Create a registry with all servers
full_registry = ServerRegistry.from_config(config_path)

# Create a filtered registry
memory_github_registry = full_registry.filter_servers(["memory", "github"])

# Create an aggregator with the filtered registry
aggregator = MCPAggregator(memory_github_registry)

# Use the aggregator with only the selected servers
tools = await aggregator.list_tools()
result = await aggregator.call_tool("memory__get", {"key": "test"})
```

## Conclusion

Adding a `filter_servers` method to ServerRegistry provides a clean, explicit way to create registry subsets with only specified servers. This approach is more efficient than the current methods, follows the single responsibility principle, and offers a clear API for both CLI and programmatic usage.