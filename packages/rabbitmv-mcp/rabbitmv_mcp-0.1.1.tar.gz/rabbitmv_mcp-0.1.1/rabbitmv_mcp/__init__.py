#!/usr/bin/env python3
"""
RabbitMV MCP Service - 基于 Model Context Protocol 的视频、文章、演员等数据服务

此模块实现了RabbitMV的MCP服务，提供视频、文章、演员等数据的访问接口。
可以通过uvx直接执行，或者作为Python包导入使用。

使用方法：
    1. 直接执行: uvx run rabbitmv-mcp
    2. 作为包导入: from rabbitmv_mcp import mcp
"""

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, AsyncIterator, Dict, List, Optional
import sys

import httpx
import uvloop
from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel
from dotenv import load_dotenv

from .config import API_BASE_URL

# 加载环境变量
load_dotenv()

# 配置uvloop
uvloop.install()

# 配置日志
def log_debug(msg: str) -> None:
    """输出调试日志"""
    print(f"[DEBUG] {msg}", file=sys.stderr, flush=True)

def log_info(msg: str) -> None:
    """输出信息日志"""
    print(f"[INFO] {msg}", file=sys.stderr, flush=True)

def log_error(msg: str) -> None:
    """输出错误日志"""
    print(f"[ERROR] {msg}", file=sys.stderr, flush=True)

# 数据模型
class VodData(BaseModel):
    """视频数据模型"""
    vod_id: int
    vod_name: str
    type_id: int
    type_name: str
    vod_time: str
    vod_remarks: Optional[str] = None
    vod_play_from: Optional[str] = None
    vod_play_url: Optional[str] = None
    vod_pic: Optional[str] = None

class ArtData(BaseModel):
    """文章数据模型"""
    art_id: int
    art_name: str
    type_id: int
    type_name: str
    art_time: str
    art_en: Optional[str] = None
    art_author: Optional[str] = None
    art_from: Optional[str] = None
    art_remarks: Optional[str] = None
    art_pic: Optional[str] = None
    art_content: Optional[str] = None

class ActorData(BaseModel):
    """演员数据模型"""
    actor_id: int
    actor_name: str
    type_id: int
    type_name: str
    actor_time: str
    actor_en: Optional[str] = None
    actor_alias: Optional[str] = None
    actor_sex: Optional[str] = None
    actor_area: Optional[str] = None
    actor_pic: Optional[str] = None
    actor_content: Optional[str] = None

class AppContext:
    """应用上下文"""
    def __init__(self):
        self.cache = {}
        self.http_client = httpx.AsyncClient()

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """管理应用生命周期"""
    log_info("MCP服务正在启动...")
    context = AppContext()
    try:
        yield context
    finally:
        log_info("MCP服务正在关闭...")
        await context.http_client.aclose()

# 错误处理
def handle_error(error: Exception) -> None:
    """全局错误处理"""
    log_error(str(error))
    if isinstance(error, httpx.HTTPError):
        log_error("HTTP请求失败")
    elif isinstance(error, ValueError):
        log_error("参数验证失败")

# 创建 MCP 服务
mcp = FastMCP(
    name="rabbitmv-mcp",
    tools=[
        "search_vod",
        "search_articles",
        "search_actors"
    ],
    resources=[
        "vod://{vod_id}",
        "article://{art_id}",
        "actor://{actor_id}"
    ],
    version="0.1.0",
    lifespan=app_lifespan,
    error_handler=handle_error,
)

# 资源定义
@mcp.resource("vod://{vod_id}")
async def get_vod(vod_id: str) -> VodData:
    """
    获取视频详情

    Args:
        vod_id: 视频ID

    Returns:
        视频详细信息
    """
    # TODO: 实现数据库查询
    return VodData(
        vod_id=int(vod_id),
        vod_name="示例视频",
        type_id=1,
        type_name="电影",
        vod_time=datetime.now().isoformat()
    )

@mcp.resource("article://{art_id}")
async def get_article(art_id: str) -> ArtData:
    """
    获取文章详情

    Args:
        art_id: 文章ID

    Returns:
        文章详细信息
    """
    # TODO: 实现数据库查询
    return ArtData(
        art_id=int(art_id),
        art_name="示例文章",
        type_id=1,
        type_name="新闻",
        art_time=datetime.now().isoformat()
    )

@mcp.resource("actor://{actor_id}")
async def get_actor(actor_id: str) -> ActorData:
    """
    获取演员详情

    Args:
        actor_id: 演员ID

    Returns:
        演员详细信息
    """
    # TODO: 实现数据库查询
    return ActorData(
        actor_id=int(actor_id),
        actor_name="示例演员",
        type_id=1,
        type_name="明星",
        actor_time=datetime.now().isoformat()
    )

# 工具定义
@mcp.tool()
async def search_vod(
    ctx: Context,
    query: str = '',
    type_id: Optional[int] = None,
    year: Optional[str] = None,
    ids: Optional[str] = None,
    h: Optional[int] = None,
    from_: Optional[str] = None,
    isend: Optional[int] = None,
    page: int = 1,
    page_size: int = 20,
    ac: Optional[str] = None
) -> Dict[str, Any]:
    """
    搜索视频内容

    Args:
        ctx: MCP上下文
        query: 关键词搜索(wd参数)
        type_id: 分类ID(t参数)
        year: 年份，支持年份范围(如:2020或2020-2023)
        ids: 视频ID,多个用逗号分隔
        h: 几小时内的数据
        from_: 播放器组标识
        isend: 是否完结:1完结,0未完结
        page: 页码(pg参数)
        page_size: 每页数量,默认20,最大100
        ac: 是否获取详情:videolist/detail获取详情

    Returns:
        搜索结果列表
    """
    log_debug(f"收到视频搜索请求: query={query}")
    log_debug(f"搜索参数: type_id={type_id}, year={year}, ids={ids}, h={h}, from={from_}, isend={isend}, page={page}, page_size={page_size}, ac={ac}")
    
    try:
        # 构建API请求参数
        params = {
            "wd": query,
            "t": type_id,
            "pg": page,
            "pagesize": min(page_size, 100),
            "ac": ac
        }
        
        if year:
            params["year"] = year
        if ids:
            params["ids"] = ids
        if h:
            params["h"] = h
        if from_:
            params["from"] = from_
        if isend is not None:
            params["isend"] = isend

        # 发送API请求
        async with ctx.app.http_client as client:
            response = await client.get(
                f"{API_BASE_URL}/api.php/provide/vod",
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

            # 处理返回数据
            vod_list = []
            for item in data.get("list", []):
                vod = {
                    "vod_id": item["vod_id"],
                    "vod_name": item["vod_name"],
                    "type_id": item["type_id"],
                    "type_name": item["type_name"],
                    "vod_time": item["vod_time"],
                    "vod_remarks": item.get("vod_remarks"),
                    "vod_play_from": item.get("vod_play_from"),
                    "vod_play_url": item.get("vod_play_url"),
                    "vod_pic": item.get("vod_pic")
                }
                vod_list.append(vod)

            result = {
                "list": vod_list,
                "page": data.get("page", page),
                "pagesize": data.get("pagesize", page_size),
                "total": data.get("total", len(vod_list))
            }
            
            log_debug(f"搜索结果: {result}")
            return result

    except httpx.HTTPError as e:
        log_error(f"API请求失败: {e}")
        raise
    except Exception as e:
        log_error(f"搜索失败: {e}")
        raise

@mcp.tool()
async def search_articles(
    ctx: Context,
    query: str = '',
    type_id: Optional[int] = None,
    h: Optional[int] = None,
    ids: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    ac: Optional[str] = None
) -> Dict[str, Any]:
    """
    搜索文章

    Args:
        ctx: MCP上下文
        query: 关键词搜索(wd参数)
        type_id: 分类ID(t参数)
        h: 几小时内的数据
        ids: 文章ID,多个用逗号分隔
        page: 页码(pg参数)
        page_size: 每页数量,默认20,最大100
        ac: detail:获取详情

    Returns:
        搜索结果列表
    """
    log_debug(f"收到文章搜索请求: query={query}")
    log_debug(f"搜索参数: type_id={type_id}, h={h}, ids={ids}, page={page}, page_size={page_size}, ac={ac}")

    try:
        # 构建API请求参数
        params = {
            "wd": query,
            "t": type_id,
            "pg": page,
            "pagesize": min(page_size, 100),
            "ac": ac
        }
        
        if ids:
            params["ids"] = ids
        if h:
            params["h"] = h

        # 发送API请求
        async with ctx.app.http_client as client:
            response = await client.get(
                f"{API_BASE_URL}/api.php/provide/art",
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

            # 处理返回数据
            article_list = []
            for item in data.get("list", []):
                article = {
                    "art_id": item["art_id"],
                    "art_name": item["art_name"],
                    "type_id": item["type_id"],
                    "type_name": item["type_name"],
                    "art_time": item["art_time"],
                    "art_en": item.get("art_en"),
                    "art_author": item.get("art_author"),
                    "art_from": item.get("art_from"),
                    "art_remarks": item.get("art_remarks"),
                    "art_pic": item.get("art_pic"),
                    "art_content": item.get("art_content") if ac == "detail" else None
                }
                article_list.append(article)

            result = {
                "list": article_list,
                "page": data.get("page", page),
                "pagesize": data.get("pagesize", page_size),
                "total": data.get("total", len(article_list))
            }
            
            log_debug(f"搜索结果: {result}")
            return result

    except httpx.HTTPError as e:
        log_error(f"API请求失败: {e}")
        raise
    except Exception as e:
        log_error(f"搜索失败: {e}")
        raise

@mcp.tool()
async def search_actors(
    ctx: Context,
    query: str = '',
    type_id: Optional[int] = None,
    h: Optional[int] = None,
    ids: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    ac: Optional[str] = None
) -> Dict[str, Any]:
    """
    搜索演员

    Args:
        ctx: MCP上下文
        query: 关键词搜索(wd参数)
        type_id: 分类ID(t参数)
        h: 几小时内的数据
        ids: 演员ID,多个用逗号分隔
        page: 页码(pg参数)
        page_size: 每页数量,默认20,最大100
        ac: detail:获取详情

    Returns:
        搜索结果列表
    """
    log_debug(f"收到演员搜索请求: query={query}")
    log_debug(f"搜索参数: type_id={type_id}, h={h}, ids={ids}, page={page}, page_size={page_size}, ac={ac}")

    try:
        # 构建API请求参数
        params = {
            "wd": query,
            "t": type_id,
            "pg": page,
            "pagesize": min(page_size, 100),
            "ac": ac
        }
        
        if ids:
            params["ids"] = ids
        if h:
            params["h"] = h

        # 发送API请求
        async with ctx.app.http_client as client:
            response = await client.get(
                f"{API_BASE_URL}/api.php/provide/actor",
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

            # 处理返回数据
            actor_list = []
            for item in data.get("list", []):
                actor = {
                    "actor_id": item["actor_id"],
                    "actor_name": item["actor_name"],
                    "type_id": item["type_id"],
                    "type_name": item["type_name"],
                    "actor_time": item["actor_time"],
                    "actor_en": item.get("actor_en"),
                    "actor_alias": item.get("actor_alias"),
                    "actor_sex": item.get("actor_sex"),
                    "actor_area": item.get("actor_area"),
                    "actor_pic": item.get("actor_pic"),
                    "actor_content": item.get("actor_content") if ac == "detail" else None
                }
                actor_list.append(actor)

            result = {
                "list": actor_list,
                "page": data.get("page", page),
                "pagesize": data.get("pagesize", page_size),
                "total": data.get("total", len(actor_list))
            }
            
            log_debug(f"搜索结果: {result}")
            return result

    except httpx.HTTPError as e:
        log_error(f"API请求失败: {e}")
        raise
    except Exception as e:
        log_error(f"搜索失败: {e}")
        raise

if __name__ == "__main__":
    # 运行 MCP 服务
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"[ERROR] Failed to start MCP service: {e}", file=sys.stderr)
        raise
