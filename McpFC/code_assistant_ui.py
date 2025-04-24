#!/usr/bin/env python3
import os
import sys
import asyncio
import tempfile
import subprocess
from typing import Dict, Any, List, Optional

# 检查是否安装了必要的库
try:
    from modelcontextprotocol.client import McpClient, ServerParameters, StdioClientTransport
except ImportError:
    print("错误: 未安装modelcontextprotocol库")
    print("请运行: pip install modelcontextprotocol")
    sys.exit(1)

class CodeAssistantUI:
    def __init__(self, server_path: str):
        """初始化代码助手UI

        Args:
            server_path: MCP服务器脚本的路径
        """
        self.server_path = server_path
        self.client = None
        self.tools = {}

    async def connect(self):
        """连接到MCP服务器"""
        print("正在连接到代码助手服务器...")

        # 设置服务器参数
        server_params = ServerParameters.builder("python")
        server_params.args(self.server_path)

        # 创建传输层
        transport = StdioClientTransport(server_params.build())

        # 创建客户端
        self.client = McpClient.sync(transport).build()

        # 初始化连接
        self.client.initialize()

        # 获取可用工具列表
        tools_list = self.client.list_tools()

        # 存储工具信息
        for tool in tools_list.tools:
            self.tools[tool.name] = {
                "description": tool.description,
                "input_schema": tool.input_schema
            }

        print(f"已连接到服务器，可用工具: {', '.join(self.tools.keys())}")
        return True

    def generate_code(self, language: str, description: str) -> str:
        """生成代码

        Args:
            language: 编程语言
            description: 代码功能描述

        Returns:
            生成的代码
        """
        if not self.client:
            print("错误: 未连接到服务器")
            return ""

        print(f"正在生成{language}代码...")

        # 调用工具
        result = self.client.call_tool({
            "name": "generate_code",
            "arguments": {
                "language": language,
                "description": description
            }
        })

        # 提取结果
        if result.content and len(result.content) > 0:
            return result.content[0].text

        return "生成代码失败"

    def optimize_code(self, language: str, code: str, optimization_goal: str) -> str:
        """优化代码

        Args:
            language: 编程语言
            code: 需要优化的代码
            optimization_goal: 优化目标

        Returns:
            优化后的代码
        """
        if not self.client:
            print("错误: 未连接到服务器")
            return ""

        print(f"正在优化{language}代码...")

        # 调用工具
        result = self.client.call_tool({
            "name": "optimize_code",
            "arguments": {
                "language": language,
                "code": code,
                "optimization_goal": optimization_goal
            }
        })

        # 提取结果
        if result.content and len(result.content) > 0:
            return result.content[0].text

        return "优化代码失败"

    def explain_code(self, language: str, code: str) -> str:
        """解释代码

        Args:
            language: 编程语言
            code: 需要解释的代码

        Returns:
            代码解释
        """
        if not self.client:
            print("错误: 未连接到服务器")
            return ""

        print(f"正在解释{language}代码...")

        # 调用工具
        result = self.client.call_tool({
            "name": "explain_code",
            "arguments": {
                "language": language,
                "code": code
            }
        })

        # 提取结果
        if result.content and len(result.content) > 0:
            return result.content[0].text

        return "解释代码失败"

    def close(self):
        """关闭客户端连接"""
        if self.client:
            self.client.close_gracefully()
            print("已断开与服务器的连接")

    def save_to_file(self, content: str, extension: str = "py") -> str:
        """将内容保存到output目录

        Args:
            content: 要保存的内容
            extension: 文件扩展名

        Returns:
            文件路径
        """
        # 确保output目录存在
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        # 生成文件名
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/code_{timestamp}.{extension}"

        # 保存文件
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        return filename

    def display_menu(self):
        """显示主菜单"""
        print("\n===== 代码助手 =====")
        print("1. 生成代码")
        print("2. 优化代码")
        print("3. 解释代码")
        print("0. 退出")
        return input("请选择操作 (0-3): ")

    async def run(self):
        """运行交互式界面"""
        # 连接到服务器
        await self.connect()

        while True:
            choice = self.display_menu()

            if choice == "0":
                break

            elif choice == "1":
                # 生成代码
                language = input("请输入编程语言 (例如 python, javascript): ")
                description = input("请描述代码功能: ")

                result = self.generate_code(language, description)
                print("\n" + result)

                # 询问是否保存
                if input("\n是否保存到文件? (y/n): ").lower() == "y":
                    file_path = self.save_to_file(result, language)
                    print(f"已保存到文件: {file_path}")

            elif choice == "2":
                # 优化代码
                language = input("请输入编程语言 (例如 python, javascript): ")
                print("请输入需要优化的代码 (输入完成后按Ctrl+D结束):")

                code_lines = []
                while True:
                    try:
                        line = input()
                        code_lines.append(line)
                    except EOFError:
                        break

                code = "\n".join(code_lines)
                optimization_goal = input("请输入优化目标 (例如 性能, 可读性): ")

                result = self.optimize_code(language, code, optimization_goal)
                print("\n" + result)

                # 询问是否保存
                if input("\n是否保存到文件? (y/n): ").lower() == "y":
                    file_path = self.save_to_file(result, language)
                    print(f"已保存到文件: {file_path}")

            elif choice == "3":
                # 解释代码
                language = input("请输入编程语言 (例如 python, javascript): ")
                print("请输入需要解释的代码 (输入完成后按Ctrl+D结束):")

                code_lines = []
                while True:
                    try:
                        line = input()
                        code_lines.append(line)
                    except EOFError:
                        break

                code = "\n".join(code_lines)

                result = self.explain_code(language, code)
                print("\n" + result)

            else:
                print("无效的选择，请重试")

            input("\n按Enter继续...")

        # 关闭客户端
        self.close()

async def main():
    # 检查环境变量
    if not os.environ.get("OPENAI_API_KEY"):
        api_key = input("请输入OpenAI API密钥: ")
        os.environ["OPENAI_API_KEY"] = api_key

    # 创建UI
    ui = CodeAssistantUI("mcp_server.py")

    # 运行UI
    await ui.run()

if __name__ == "__main__":
    asyncio.run(main())
