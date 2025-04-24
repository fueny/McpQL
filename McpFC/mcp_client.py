#!/usr/bin/env python3
import os
import sys
import json
import asyncio
import subprocess
import datetime
from typing import Dict, Any, List, Optional
import argparse

# 检查是否安装了modelcontextprotocol库
try:
    from modelcontextprotocol.client import McpClient, ServerParameters, StdioClientTransport
except ImportError:
    print("错误: 未安装modelcontextprotocol库")
    print("请运行: pip install modelcontextprotocol")
    sys.exit(1)

class CodeAssistantClient:
    def __init__(self, server_path: str):
        """初始化代码助手客户端

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

    def save_to_file(self, content: str, language: str) -> str:
        """将内容保存到output目录

        Args:
            content: 要保存的内容
            language: 编程语言，用于确定文件扩展名

        Returns:
            文件路径
        """
        # 确保output目录存在
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        # 确定文件扩展名
        extension_map = {
            "python": "py",
            "javascript": "js",
            "typescript": "ts",
            "java": "java",
            "c#": "cs",
            "csharp": "cs",
            "c++": "cpp",
            "cpp": "cpp",
            "go": "go",
            "rust": "rs",
            "ruby": "rb",
            "php": "php",
            "html": "html",
            "css": "css"
        }
        extension = extension_map.get(language.lower(), "txt")

        # 生成文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/code_{timestamp}.{extension}"

        # 保存文件
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        return filename

    def close(self):
        """关闭客户端连接"""
        if self.client:
            self.client.close_gracefully()
            print("已断开与服务器的连接")

async def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="代码助手客户端")
    parser.add_argument("--server", default="mcp_server.py", help="MCP服务器脚本路径")
    parser.add_argument("--action", choices=["generate", "optimize", "explain"], required=True, help="要执行的操作")
    parser.add_argument("--language", required=True, help="编程语言")
    parser.add_argument("--description", help="代码功能描述 (用于生成代码)")
    parser.add_argument("--code", help="代码 (用于优化或解释)")
    parser.add_argument("--goal", help="优化目标 (用于优化代码)")

    args = parser.parse_args()

    # 创建客户端
    client = CodeAssistantClient(args.server)

    try:
        # 连接到服务器
        await client.connect()

        # 根据操作类型执行相应功能
        if args.action == "generate":
            if not args.description:
                print("错误: 生成代码需要提供--description参数")
                return

            result = client.generate_code(args.language, args.description)
            print("\n" + result)

            # 保存到文件
            file_path = client.save_to_file(result, args.language)
            print(f"\n已保存到文件: {file_path}")

        elif args.action == "optimize":
            if not args.code:
                print("错误: 优化代码需要提供--code参数")
                return

            if not args.goal:
                print("错误: 优化代码需要提供--goal参数")
                return

            result = client.optimize_code(args.language, args.code, args.goal)
            print("\n" + result)

            # 保存到文件
            file_path = client.save_to_file(result, args.language)
            print(f"\n已保存到文件: {file_path}")

        elif args.action == "explain":
            if not args.code:
                print("错误: 解释代码需要提供--code参数")
                return

            result = client.explain_code(args.language, args.code)
            print("\n" + result)

    finally:
        # 关闭客户端
        client.close()

if __name__ == "__main__":
    asyncio.run(main())
