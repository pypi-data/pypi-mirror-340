# Copyright 2025 TigerGraph Inc.
# Licensed under the Apache License, Version 2.0.
# See the LICENSE file or https://www.apache.org/licenses/LICENSE-2.0
#
# Permission is granted to use, copy, modify, and distribute this software
# under the License. The software is provided "AS IS", without warranty.

from typing import Optional, Dict
from pydantic import Field
from mcp.types import Tool, TextContent

from tigergraphx import Graph

from tigergraph_mcp.tools import TigerGraphToolNames
from tigergraph_mcp.tools.base_tool_input import (
    BaseToolInput,
    TIGERGRAPH_CONNECTION_CONFIG_DESCRIPTION,
)


class AddNodeToolInput(BaseToolInput):
    """Input schema for adding a node to a TigerGraph graph."""

    graph_name: str = Field(
        ..., description="The name of the graph where the node will be added."
    )
    node_id: str = Field(..., description="The unique identifier of the node.")
    node_type: Optional[str] = Field(
        None, description="The type of the node (optional)."
    )
    attributes: Optional[Dict] = Field(
        default_factory=dict, description="Additional attributes for the node."
    )


tools = [
    Tool(
        name=TigerGraphToolNames.ADD_NODE,
        description="""Adds a node to a TigerGraph database using TigerGraphX.

Example input:
```python
graph_name = "SocialGraph"
node_id = "Alice"
node_type = "Person"
attributes = {"age": 30, "gender": "Female"}
```

**`tigergraph_connection_config`** must also be provided to establish the connection to TigerGraph.

### Configuration Options:
The `tigergraph_connection_config` is required to authenticate and configure the connection to the TigerGraph instance. It can either be explicitly provided or populated via environment variables (recommended). Do not mix both methods.

For more details on configuring `tigergraph_connection_config`, please refer to the following:
"""
        + "\n\n"
        + TIGERGRAPH_CONNECTION_CONFIG_DESCRIPTION.strip(),
        inputSchema=AddNodeToolInput.model_json_schema(),
    )
]


async def add_node(
    graph_name: str,
    node_id: str,
    node_type: Optional[str] = None,
    attributes: Optional[Dict] = None,
    tigergraph_connection_config: Optional[Dict] = None,
) -> list[TextContent]:
    try:
        attributes = attributes or {}
        graph = Graph.from_db(graph_name, tigergraph_connection_config)
        graph.add_node(node_id, node_type, **attributes)
        result = f"✅ Node '{node_id}' (Type: {node_type or 'default'}) added successfully to graph '{graph_name}'."
    except Exception as e:
        result = f"❌ Failed to add node '{node_id}' to graph '{graph_name}': {str(e)}"
    return [TextContent(type="text", text=result)]
