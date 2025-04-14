#!/usr/bin/env python3
"""
RabbitMV MCP Service - 入口文件

这个文件作为uvx执行的入口点，启动MCP服务
"""

from rabbitmv_mcp import mcp


def main():
    """主函数，启动MCP服务"""
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        import sys
        print(f"[ERROR] Failed to start MCP service: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()