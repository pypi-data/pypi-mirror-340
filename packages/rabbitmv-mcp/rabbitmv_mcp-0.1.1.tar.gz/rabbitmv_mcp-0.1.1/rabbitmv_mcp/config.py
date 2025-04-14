#!/usr/bin/env python3
"""
RabbitMV MCP Service - 配置模块

此模块提供了RabbitMV MCP服务的配置项管理。
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.rabbitmv.com')

# 日志配置
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# 缓存配置
CACHE_TIME = int(os.getenv('CACHE_TIME', 3600))

# 鉴权配置
NEED_AUTH = os.getenv('NEED_AUTH', 'false').lower() == 'true'
AUTH_KEY = os.getenv('AUTH_KEY', '')

# 图片域名前缀
IMG_URL = os.getenv('IMG_URL', 'https://images.example.com')

# 消息大小限制
MAX_MESSAGE_SIZE = int(os.getenv('MAX_MESSAGE_SIZE', 1048576))

# 数据过滤器配置
DATA_FILTER = os.getenv('DATA_FILTER', '')
TYPE_FILTER = os.getenv('TYPE_FILTER', '').split(',')