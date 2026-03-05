FROM python:3.13-slim

# 安装 SSH 服务和必要的工具
RUN apt-get update && apt-get install -y \
    openssh-server \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/* \
    && echo 'root:123456' | chpasswd \
    && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && mkdir -p /var/run/sshd

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露 SSH 端口
EXPOSE 22

# 启动 SSH 和 FastAPI 应用
CMD service ssh start && python src/main.py