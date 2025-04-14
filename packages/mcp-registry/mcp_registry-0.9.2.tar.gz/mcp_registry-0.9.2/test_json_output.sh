#!/bin/bash

echo "====== Testing MCP Registry JSON Output Commands ======"

# Test the dedicated JSON command
echo -e "\n== Testing list-tools-json command =="
echo "Command: mcp-registry list-tools-json memory"
JSON_OUTPUT=$(mcp-registry list-tools-json memory 2>/dev/null)
echo "Output size: $(echo "$JSON_OUTPUT" | wc -c) bytes"
echo "First 200 characters:"
echo "$JSON_OUTPUT" | head -c 200
echo -e "\n..."

# Test the --json flag for the list-tools command
echo -e "\n== Testing list-tools --json flag =="
echo "Command: mcp-registry list-tools memory --json"
JSON_OUTPUT=$(mcp-registry list-tools memory --json 2>/dev/null)
echo "Output size: $(echo "$JSON_OUTPUT" | wc -c) bytes"
echo "First 200 characters:"
echo "$JSON_OUTPUT" | head -c 200
echo -e "\n..."

# Compare outputs
echo -e "\n== Comparing the two outputs =="
LIST_TOOLS_OUTPUT=$(mcp-registry list-tools memory --json 2>/dev/null)
LIST_TOOLS_JSON_OUTPUT=$(mcp-registry list-tools-json memory 2>/dev/null)

if [ "$LIST_TOOLS_OUTPUT" == "$LIST_TOOLS_JSON_OUTPUT" ]; then
    echo "✅ The outputs are identical"
else
    echo "❌ The outputs are different"
    
    LIST_TOOLS_HASH=$(echo "$LIST_TOOLS_OUTPUT" | md5sum)
    LIST_TOOLS_JSON_HASH=$(echo "$LIST_TOOLS_JSON_OUTPUT" | md5sum)
    
    echo "list-tools --json hash: $LIST_TOOLS_HASH"
    echo "list-tools-json hash: $LIST_TOOLS_JSON_HASH"
fi

# Example usage with jq
if command -v jq &> /dev/null; then
    echo -e "\n== Example: Filtering tools with jq =="
    echo "Command: mcp-registry list-tools-json | jq '.memory | map(select(.name == \"read_graph\"))'"
    mcp-registry list-tools-json 2>/dev/null | jq '.memory | map(select(.name == "read_graph"))' || echo "jq error"
else
    echo -e "\n== jq not installed, skipping jq examples =="
fi

echo -e "\n====== Test completed ======"