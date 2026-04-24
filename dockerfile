FROM python:3.10-slim

# 安装系统依赖：JDK（Allure 需要）、curl、wget
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-jre-headless \
        curl \
        wget \
        && rm -rf /var/lib/apt/lists/*

# 安装 Allure 命令行工具（版本 2.30.0）
RUN wget -qO- https://github.com/allure-framework/allure2/releases/download/2.30.0/allure-2.30.0.tgz | \
    tar xz -C /opt/ && \
    ln -s /opt/allure-2.30.0/bin/allure /usr/local/bin/allure

# 设置工作目录（代码将通过卷挂载到此路径）
WORKDIR /tests

# 预装 Python 依赖（把 requirements.txt 先复制进来）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 默认命令：直接运行 pytest
CMD ["pytest", "-s", "-v", "--alluredir=allure-results"]