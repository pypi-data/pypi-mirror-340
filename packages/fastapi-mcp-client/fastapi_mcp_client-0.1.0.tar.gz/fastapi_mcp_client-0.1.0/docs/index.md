# FastAPI MCP Client

A modern, efficient client library for interacting with FastAPI services that implement the Model Context Protocol (MCP).

## Overview

FastAPI MCP Client is a Python library that provides a clean and intuitive interface for connecting to and interacting with APIs that implement the Model Context Protocol (MCP). It supports both regular HTTP requests and streaming via Server-Sent Events (SSE).

## Key Features

- **Async-First Design**: Built from the ground up with async/await support
- **Streaming Support**: Built-in support for Server-Sent Events (SSE) streaming
- **Flexible Configuration**: Highly configurable for different environments and use cases
- **Error Handling**: Comprehensive error handling and recovery strategies
- **Type Annotations**: Full type hints for better IDE integration and validation
- **Context Managers**: Proper resource management with async context managers

## Installation

```bash
# Install with pip
pip install fastapi-mcp-client

# Or with UV (recommended)
uv install fastapi-mcp-client
```

## Quick Example

```python
import asyncio
from fastapi_mcp_client import MCPClient

async def main():
    # Connect to an MCP-enabled API
    async with MCPClient("http://localhost:8000") as client:
        # Make a simple request
        result = await client.call_operation("GET:/health")
        print(f"API Health: {result}")
        
        # Make a request with parameters
        search_result = await client.call_operation(
            "ground_query", 
            {"query": "What is machine learning?", "top_k": 3}
        )
        print(f"Found {len(search_result.get('context', []))} results")

# Run the example
asyncio.run(main())
```

## Next Steps

- Check out the [Getting Started](guide/getting-started.md) guide for more examples
- Learn about [Streaming](guide/streaming.md) to handle real-time data
- Explore the [API Reference](api/client.md) for detailed documentation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/your-username/fastapi-mcp-client/blob/main/LICENSE) file for details. 