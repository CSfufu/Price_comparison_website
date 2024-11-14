# 使用官方 Python 作为基础镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 修改镜像源为阿里云的镜像（如果文件不存在则创建）
RUN echo "deb http://mirrors.aliyun.com/debian/ bookworm main non-free contrib" > /etc/apt/sources.list \
    && echo "deb-src http://mirrors.aliyun.com/debian/ bookworm main non-free contrib" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制并安装依赖文件
COPY ./requirements.txt /app/

# 创建虚拟环境并激活
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装 Gunicorn 和 django-cors-headers（确保它们被包含在 requirements.txt 中，避免重复安装）
RUN pip install gunicorn django-cors-headers

# 复制后端代码
COPY . /app/

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 暴露端口
EXPOSE 8000

# 运行 Django 服务，确保 gunicorn 启动路径正确
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
