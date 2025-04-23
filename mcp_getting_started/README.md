# MCP 网络搜索客户端

这是一个基于 MCP (Model Control Protocol) 的客户端实现，它允许用户通过命令行界面与大语言模型进行交互，并支持网络搜索功能。

## 功能特点

- 使用 OpenAI 兼容 API 进行语言模型调用
- 通过 MCP 协议与后端服务器通信
- 支持网络搜索功能
- 交互式命令行界面

## 安装

### 前提条件

- Python 3.12 或更高版本
- uv 包管理器

### 安装步骤

1. 克隆此仓库：

```bash
git clone https://github.com/您的用户名/mcp-getting-started.git
cd mcp-getting-started
```

2. 使用 uv 安装依赖：

```bash
uv venv
uv pip install -e .
```

3. 复制环境变量示例文件并填入您的 API 密钥：

```bash
cp .env.example .env
# 编辑 .env 文件，填入您的 API 密钥
```

## 使用方法

1. 启动 McpClient：

```bash
python McpClient.py
```

2. 在提示符下输入您的问题：

```
Query: 今天的天气怎么样？
```

3. 输入 `quit` 退出程序。

更多详细信息，请参阅 [McpClient.md](McpClient.md)。

## 项目结构

- `McpClient.py`: 主客户端实现
- `web_search.py`: 网络搜索工具实现
- `search_client.py`: 搜索客户端实现

## 使用 uv 打包项目

### 什么是 uv

uv 是一个快速的 Python 包安装器和解析器，它可以替代传统的 pip 和 virtualenv 工具。uv 提供了更快的依赖解析和安装速度，以及更好的缓存机制。

### 安装 uv

```bash
pip install uv
```

### 使用 uv 创建虚拟环境

```bash
uv venv
```

这将在当前目录下创建一个 `.venv` 目录作为虚拟环境。

### 使用 uv 安装依赖

```bash
uv pip install -e .
```

这将以可编辑模式安装当前项目及其依赖。

### 使用 uv 打包项目

1. **确保 pyproject.toml 文件配置正确**

   项目使用 `pyproject.toml` 文件来定义项目的元数据和依赖。确保该文件包含正确的信息：

   ```toml
   [project]
   name = "mcp-getting-started"
   version = "0.1.0"
   description = "MCP 网络搜索客户端实现"
   readme = "README.md"
   requires-python = ">=3.12"
   license = {text = "MIT"}
   authors = [
       {name = "您的名字", email = "您的邮箱"}
   ]
   dependencies = [
       "httpx>=0.28.1",
       "mcp[cli]>=1.6.0",
       "openai>=1.75.0",
       "python-dotenv>=1.1.0",
   ]

   [project.urls]
   "Homepage" = "https://github.com/您的用户名/mcp-getting-started"
   "Bug Tracker" = "https://github.com/您的用户名/mcp-getting-started/issues"

   [tool.setuptools]
   py-modules = ["McpClient", "web_search", "search_client", "main"]
   ```

2. **构建项目**

   使用以下命令构建项目：

   ```bash
   uv build
   ```

   这将在 `dist` 目录下生成两个文件：
   - `.tar.gz` 文件：源代码分发包
   - `.whl` 文件：Python wheel 包

3. **安装构建的包**

   您可以使用以下命令安装构建的包：

   ```bash
   uv pip install dist/mcp_getting_started-0.1.0-py3-none-any.whl
   ```

## 许可证

[MIT](LICENSE)

## 贡献

欢迎提交 Pull Request 或创建 Issue 来改进此项目。