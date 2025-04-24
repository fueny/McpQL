# 代码助手 (Code Assistant)

这是一个基于MCP (Model Context Protocol)和OpenAI API的代码助手工具，可以帮助生成、优化和解释代码。该工具使用服务器-客户端架构，通过MCP协议实现组件间通信。

## 功能特点

- **代码生成**：根据自然语言描述生成代码
- **代码优化**：根据特定目标优化现有代码
- **代码解释**：解释代码的功能和工作原理
- **MCP服务器-客户端架构**：使用Model Context Protocol实现组件间通信
- **交互式界面**：提供用户友好的操作方式

## 系统要求

- Python 3.10+
- OpenAI API密钥

## 文件结构

- **mcp_server.py** - MCP服务器，提供代码生成、优化和解释工具
- **mcp_client.py** - MCP客户端，连接到服务器并使用工具
- **code_assistant_ui.py** - 交互式界面
- **start_code_assistant.py** - 启动脚本
- **run.py** - 简化的启动脚本，自动检查和设置环境
- **pyproject.toml** - 项目配置和依赖管理（使用uv）
- **setup_env.py** - 环境设置脚本，使用uv管理依赖
- **.gitignore** - Git忽略文件配置
- **output/** - 生成的代码输出目录

## 安装步骤

1. 克隆仓库：
   ```
   git clone 
   cd code-assistant
   ```
2. 安装uv（如果尚未安装）：
   ```
   pip install uv
   ```
3. 设置环境：
   ```
   python setup_env.py
   ```
4. 激活虚拟环境：
   ```
   # Windows
   .venv\Scripts\activate

   # Linux/Mac
   source .venv/bin/activate
   ```
5. 准备OpenAI API密钥（可以在运行时输入）

### 开发环境设置

如果您想安装开发依赖（如测试工具），请使用：
```
python setup_env.py --dev
```

如果需要清理并重新创建环境，请使用：
```
python setup_env.py --clean
```

### 配置环境变量

您可以通过以下方式设置OpenAI API密钥和基础URL：

1. 编辑`.env`文件：
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_API_BASE=https://api.openai.com/v1
   ```

2. 或者在命令行中设置环境变量：
   ```
   # Windows
   set OPENAI_API_KEY=your_openai_api_key_here
   set OPENAI_API_BASE=https://api.openai.com/v1

   # Linux/Mac
   export OPENAI_API_KEY=your_openai_api_key_here
   export OPENAI_API_BASE=https://api.openai.com/v1
   ```

3. 或者在运行时通过交互式提示输入

## 使用方法

### 输出目录

所有生成的代码都会自动保存在`output`目录中，文件名格式为`code_YYYYMMDD_HHMMSS.扩展名`。扩展名根据编程语言自动确定。

### 方法1：使用启动脚本（推荐）

启动脚本提供了一个简单的菜单，可以选择不同的操作模式：

```
python start_code_assistant.py
```

运行后，您将看到以下菜单：
```
===== 代码助手 =====
1. 启动交互式界面
2. 启动MCP服务器
3. 运行命令行客户端
0. 退出
```

### 方法2：直接使用交互式界面

交互式界面提供了用户友好的操作方式：

```
python code_assistant_ui.py
```

运行后，您将看到以下菜单：
```
===== 代码助手 =====
1. 生成代码
2. 优化代码
3. 解释代码
0. 退出
```

## 使用示例

### 示例1：生成一个简单的Python HTTP服务器

1. 运行 `python start_code_assistant.py`
2. 选择 `1` 启动交互式界面
3. 选择 `1` 生成代码
4. 输入编程语言 `python`
5. 输入描述 `创建一个简单的HTTP服务器，提供一个API端点，返回当前时间`
6. 查看生成的代码
7. 输入 `y` 保存代码
8. 代码将被保存到 `output` 目录中，文件名类似 `code_20250424_235959.py`
9. 可以直接运行生成的代码：`python output/code_20250424_235959.py`

### 示例2：优化代码

1. 运行 `python start_code_assistant.py`
2. 选择 `1` 启动交互式界面
3. 选择 `2` 优化代码
4. 输入编程语言 `python`
5. 输入需要优化的代码（输入完成后按Ctrl+D结束）
6. 输入优化目标 `性能`
7. 查看优化后的代码
8. 输入 `y` 保存代码
9. 优化后的代码将被保存到 `output` 目录中
10. 可以直接运行优化后的代码：`python output/code_20250424_235959.py`

### 示例3：解释代码

1. 运行 `python start_code_assistant.py`
2. 选择 `1` 启动交互式界面
3. 选择 `3` 解释代码
4. 输入编程语言 `python`
5. 输入需要解释的代码（输入完成后按Ctrl+D结束）
6. 查看代码解释

## 架构说明

该项目使用MCP (Model Context Protocol)实现了服务器-客户端架构：

1. **MCP服务器**：提供代码生成、优化和解释的工具
2. **MCP客户端**：连接到服务器并使用工具
3. **交互式界面**：提供用户友好的界面
4. **启动脚本**：简化启动过程

MCP协议允许客户端和服务器之间进行标准化通信，使得工具可以在不同环境中使用。

## 自定义和扩展

您可以通过以下方式自定义和扩展代码助手：

1. 修改 `mcp_server.py` 中的工具函数，调整代码生成、优化和解释的行为
2. 在 `mcp_server.py` 中添加新的工具函数，提供更多功能
3. 修改 `code_assistant_ui.py` 中的用户界面，改进用户体验
4. 创建新的客户端，连接到MCP服务器并使用工具

## 故障排除

### 常见问题

1. **无法连接到服务器**
   - 确保服务器已启动
   - 检查端口是否被占用

2. **API密钥错误**
   - 确保已正确设置OpenAI API密钥
   - 检查API密钥是否有效

3. **API基础URL错误**
   - 如果使用自定义API基础URL，确保URL格式正确
   - 确保URL末尾不包含斜杠
   - 标准格式：`https://api.openai.com/v1`

4. **依赖项错误**
   - 确保已正确设置环境：`python setup_env.py`
   - 确保已激活虚拟环境
   - 检查Python版本是否为3.10或更高版本

## 使用uv管理项目

本项目使用uv包管理工具来管理依赖和环境。以下是一些常用的uv命令和操作：

### 常用uv命令

```bash
# 查看依赖树
uv pip list --tree

# 更新所有依赖
uv pip sync

# 添加新依赖
uv pip install package_name

# 添加新依赖并更新pyproject.toml
uv pip install package_name --update-pyproject

# 运行带有虚拟环境的命令
uv run python start_code_assistant.py

# 构建分发包
uv build
```

### 快速启动

克隆仓库后，可以使用以下命令快速启动：

```bash
# 一键设置环境并运行
pip install uv && python setup_env.py && .venv\Scripts\activate && python run.py  # Windows
pip install uv && python setup_env.py && source .venv/bin/activate && python run.py  # Linux/Mac
```

### 使用run.py脚本

项目提供了一个简化的`run.py`脚本，它会自动检查环境并在必要时设置环境：

```bash
# 直接运行
python run.py
```

这个脚本会检查是否已安装uv，是否已创建虚拟环境，并在需要时自动设置。

## 注意事项

- 代码生成和优化功能依赖于OpenAI API，需要有效的API密钥
- 生成的代码可能需要根据具体需求进行调整
- 优化建议仅供参考，实际效果可能因具体情况而异
- 本项目使用uv管理依赖，确保使用最新版本的uv以获得最佳体验
