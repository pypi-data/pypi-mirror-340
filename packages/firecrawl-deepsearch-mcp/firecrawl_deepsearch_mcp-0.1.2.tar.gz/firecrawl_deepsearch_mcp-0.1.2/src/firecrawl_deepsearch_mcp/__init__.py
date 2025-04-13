from . import mcp
import asyncio

def main():
    """Main entry point for the package."""
    asyncio.run(mcp.mcp.run())

# Optionally expose other important items at package level
__all__ = ['main', 'mcp']