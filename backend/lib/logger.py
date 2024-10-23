# lib/logger.py

import logging
import os
from logging.handlers import RotatingFileHandler

# 创建 logger 对象
logger = logging.getLogger('jd_search_logger')
logger.setLevel(logging.DEBUG)  # 设置全局日志级别

# 创建日志目录（如果不存在）
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

# 创建文件处理器，支持日志轮转
file_handler = RotatingFileHandler(
    os.path.join(log_dir, 'jd_search.log'),
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)  # 文件处理器日志级别

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # 控制台处理器日志级别

# 创建日志格式
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 添加处理器到 logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 避免重复日志记录（特别是在模块多次导入时）
logger.propagate = False
