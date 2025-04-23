# McpClient 使用指南

## 简介

`McpClient.py` 是一个基于 MCP (Model Control Protocol) 的客户端实现，它允许用户通过命令行界面与大语言模型进行交互，并支持网络搜索功能。该客户端使用 OpenAI API 进行语言模型调用，并通过 MCP 协议与后端服务器通信。

## 前提条件

在使用 `McpClient.py` 之前，您需要确保以下条件已满足：

1. 安装所需的依赖包：
   ```bash
   pip install openai python-dotenv mcp
   ```

2. 创建 `.env` 文件，并设置以下环境变量：
   ```
   OPENAI_API_KEY=您的OpenAI API密钥
   OPENAI_MODEL=您要使用的模型名称（例如：gpt-3.5-turbo）
   ```

3. 确保 `web_search.py` 文件在当前目录中可用。

## 代码结构

`McpClient.py` 主要包含以下组件：

1. `MCPClient` 类：实现与 MCP 服务器的通信和大语言模型的调用。
   - `connect_to_server()`: 连接到 MCP 服务器
   - `process_query()`: 处理用户查询并调用大语言模型
   - `chat_loop()`: 实现交互式聊天循环
   - `cleanup()`: 清理资源

2. `main()` 函数：程序的入口点，负责初始化客户端并启动聊天循环。

## 使用方法

### 基本使用

1. 确保您已经设置好环境变量和安装了所需依赖。

2. 运行 `McpClient.py` 文件：
   ```bash
   python McpClient.py
   ```

3. 程序启动后，您将看到一个提示符 `Query:`，您可以在此输入您的问题。

4. 输入 `quit` 可以退出程序。

### 示例交互

```
Query: 今天的天气怎么样？

[Calling tool web_search with args {'query': '今天的天气怎么样'}]

根据我的搜索，我无法确定您所在位置的具体天气情况。天气是特定于地理位置的，需要知道您的具体位置才能提供准确的天气信息。

如果您想了解特定城市或地区的天气，请提供具体的位置信息，例如"北京今天的天气怎么样？"或"上海今天的天气如何？"，这样我才能为您提供相关的天气预报信息。

Query: quit
```

## 自定义配置

### 修改服务器启动命令

默认情况下，客户端使用 `uv run web_search.py` 命令启动后端服务器。如果您需要修改此命令，请编辑 `connect_to_server()` 方法中的 `server_params` 变量：

```python
server_params = StdioServerParameters(
    command='您的命令',
    args=['您的参数1', '您的参数2'],
    env=None
)
```

### 修改系统提示词

您可以通过编辑 `process_query()` 方法中的 `system_prompt` 变量来自定义系统提示词，以控制大语言模型的行为：

```python
system_prompt = (
    "您的自定义提示词"
)
```

## 故障排除

1. **连接错误**：如果出现连接错误，请确保 `web_search.py` 文件存在并且可以正常运行。

2. **API 错误**：如果出现 API 错误，请检查您的 OpenAI API 密钥是否正确设置，以及是否有足够的额度。

3. **模型错误**：如果出现模型相关错误，请确保您指定的模型名称正确，并且您有权限访问该模型。

## 注意事项

- 该客户端依赖于外部服务和 API，因此需要稳定的网络连接。
- 使用 OpenAI API 可能会产生费用，请注意控制使用量。
- 确保您的 `.env` 文件不会被提交到公共代码库中，以保护您的 API 密钥安全。
