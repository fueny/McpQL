# 代码助手 (Code Assistant)

这是一个基于MCP (Model Context Protocol)和OpenAI API的代码助手工具，可以帮助生成、优化和解释代码。

## 功能

- **代码生成**：根据自然语言描述生成代码
- **代码优化**：根据特定目标优化现有代码
- **代码解释**：解释代码的功能和工作原理

## 系统要求

- Python 3.7+
- OpenAI API密钥

## 安装

1. 克隆此仓库
2. 安装依赖：
   ```
   pip install openai mcp modelcontextprotocol python-dotenv
   ```
3. 设置OpenAI API密钥：
   ```
   export OPENAI_API_KEY=your_api_key_here
   ```
   或者创建一个`.env`文件，添加：
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## 使用方法

### 启动代码助手

```
python start_code_assistant.py
```

这将显示一个菜单，您可以选择：
1. 启动交互式界面
2. 启动MCP服务器
3. 运行命令行客户端

### 直接使用交互式界面

```
python code_assistant_ui.py
```

### 直接启动MCP服务器

```
python mcp_server.py
```

### 使用命令行客户端

生成代码：
```
python mcp_client.py --action generate --language python --description "创建一个简单的HTTP服务器"
```

优化代码：
```
python mcp_client.py --action optimize --language python --code "def factorial(n): if n == 0: return 1 else: return n * factorial(n-1)" --goal "性能"
```

解释代码：
```
python mcp_client.py --action explain --language python --code "def factorial(n): if n == 0: return 1 else: return n * factorial(n-1)"
```

## 架构

该项目使用MCP (Model Context Protocol)实现了服务器-客户端架构：

1. **MCP服务器** (`mcp_server.py`)：提供代码生成、优化和解释的工具
2. **MCP客户端** (`mcp_client.py`)：连接到服务器并使用工具
3. **交互式界面** (`code_assistant_ui.py`)：提供用户友好的界面
4. **启动脚本** (`start_code_assistant.py`)：简化启动过程

## 自定义

您可以通过修改`mcp_server.py`中的工具函数来自定义代码生成、优化和解释的行为。
