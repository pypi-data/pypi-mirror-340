"""
RabbitMV MCP Service 测试用例
"""

import asyncio
from datetime import datetime
from typing import Any, Dict

import pytest
from mcp.server.fastmcp import FastMCP

from rabbitmv_mcp import mcp

@pytest.fixture(scope="function")
async def server():
    """服务测试固定装置"""
    async with mcp._lifespan() as context:
        yield mcp

@pytest.mark.asyncio
class TestResources:
    """资源访问测试"""
    
    async def test_get_vod(self, server):
        """测试获取视频资源"""
        result = await server._read_resource("vod://1")
        assert isinstance(result, dict)
        assert result["vod_id"] == 1
        assert "vod_name" in result
        assert "type_id" in result
        assert "type_name" in result
        assert "vod_time" in result

    async def test_get_article(self, server):
        """测试获取文章资源"""
        result = await server._read_resource("article://1")
        assert isinstance(result, dict)
        assert result["art_id"] == 1
        assert "art_name" in result
        assert "type_id" in result
        assert "type_name" in result
        assert "art_time" in result

    async def test_get_actor(self, server):
        """测试获取演员资源"""
        result = await server._read_resource("actor://1")
        assert isinstance(result, dict)
        assert result["actor_id"] == 1
        assert "actor_name" in result
        assert "type_id" in result
        assert "type_name" in result
        assert "actor_time" in result

    async def test_invalid_resource(self, server):
        """测试无效资源访问"""
        with pytest.raises(Exception):
            await server._read_resource("invalid://1")

@pytest.mark.asyncio
class TestTools:
    """工具调用测试"""

    async def test_search_vod(self, server):
        """测试视频搜索"""
        result = await server._call_tool("search_vod", {
            "query": "测试",
            "page": 1,
            "page_size": 20
        })
        assert isinstance(result, dict)
        assert "list" in result
        assert "page" in result
        assert "pagesize" in result
        assert "total" in result
        assert isinstance(result["list"], list)
        assert len(result["list"]) > 0

    async def test_search_articles(self, server):
        """测试文章搜索"""
        result = await server._call_tool("search_articles", {
            "query": "测试",
            "page": 1,
            "page_size": 20
        })
        assert isinstance(result, dict)
        assert "list" in result
        assert "page" in result
        assert "pagesize" in result
        assert "total" in result
        assert isinstance(result["list"], list)
        assert len(result["list"]) > 0

    async def test_search_actors(self, server):
        """测试演员搜索"""
        result = await server._call_tool("search_actors", {
            "query": "测试",
            "page": 1,
            "page_size": 20
        })
        assert isinstance(result, dict)
        assert "list" in result
        assert "page" in result
        assert "pagesize" in result
        assert "total" in result
        assert isinstance(result["list"], list)
        assert len(result["list"]) > 0

    async def test_invalid_tool(self, server):
        """测试无效工具调用"""
        with pytest.raises(Exception):
            await server._call_tool("invalid_tool", {})

@pytest.mark.asyncio
class TestLifecycle:
    """生命周期管理测试"""

    async def test_startup_shutdown(self, server):
        """测试服务启动和关闭"""
        assert server.lifespan_context is not None
        assert hasattr(server.lifespan_context, "cache")
        assert hasattr(server.lifespan_context, "http_client")
        
        # 验证 HTTP 客户端
        assert not server.lifespan_context.http_client.is_closed

@pytest.mark.asyncio
class TestValidation:
    """输入验证测试"""

    async def test_invalid_page(self, server):
        """测试无效的页码参数"""
        with pytest.raises(Exception):
            await server._call_tool("search_vod", {
                "query": "测试",
                "page": 0
            })

    async def test_invalid_page_size(self, server):
        """测试无效的页大小参数"""
        with pytest.raises(Exception):
            await server._call_tool("search_vod", {
                "query": "测试",
                "page_size": 0
            })

    async def test_missing_required_params(self, server):
        """测试缺少必需参数"""
        with pytest.raises(Exception):
            await server._call_tool("search_vod", {})
