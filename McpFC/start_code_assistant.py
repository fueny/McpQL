#!/usr/bin/env python3
import os
import sys
import asyncio
import subprocess
import shutil
from pathlib import Path
from dotenv import load_dotenv

def check_dependencies():
    """检查依赖项是否已安装"""
    try:
        import openai
        import mcp
        import modelcontextprotocol
        return True
    except ImportError as e:
        print(f"错误: 缺少依赖项 - {e}")
        print("请使用以下命令安装依赖:")

        # 检查是否有uv
        if shutil.which("uv"):
            print("    uv pip install -e .")
        else:
            print("    python setup_env.py")
            print("或者:")
            print("    pip install -e .")
        return False

async def main():
    """主函数"""
    # 检查依赖项
    if not check_dependencies():
        return

    # 加载环境变量
    load_dotenv()

    # 确保output目录存在
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    print(f"输出目录: {os.path.abspath(output_dir)}")

    # 检查OpenAI API密钥
    if not os.environ.get("OPENAI_API_KEY"):
        api_key = input("请输入OpenAI API密钥: ")
        os.environ["OPENAI_API_KEY"] = api_key

    # 检查OpenAI API基础URL
    api_base = os.environ.get("OPENAI_API_BASE")
    if not api_base:
        use_custom = input("是否使用自定义API基础URL? (y/n): ").lower() == 'y'
        if use_custom:
            api_base = input("请输入OpenAI API基础URL (默认: https://api.openai.com/v1): ")
            if api_base:
                os.environ["OPENAI_API_BASE"] = api_base

    # 显示API配置信息
    print(f"OpenAI API密钥: {'已设置' if os.environ.get('OPENAI_API_KEY') else '未设置'}")
    print(f"OpenAI API基础URL: {os.environ.get('OPENAI_API_BASE', 'https://api.openai.com/v1')}")

    # 显示菜单
    print("\n===== 代码助手 =====")
    print("1. 启动交互式界面")
    print("2. 启动MCP服务器")
    print("3. 运行命令行客户端")
    print("0. 退出")

    choice = input("请选择操作 (0-3): ")

    if choice == "0":
        return

    elif choice == "1":
        # 启动交互式界面
        print("启动交互式界面...")
        subprocess.run([sys.executable, "code_assistant_ui.py"])

    elif choice == "2":
        # 启动MCP服务器
        print("启动MCP服务器...")
        subprocess.run([sys.executable, "mcp_server.py"])

    elif choice == "3":
        # 运行命令行客户端
        print("运行命令行客户端...")

        # 获取参数
        action = input("请选择操作 (generate/optimize/explain): ")
        language = input("请输入编程语言: ")

        if action == "generate":
            description = input("请描述代码功能: ")
            subprocess.run([
                sys.executable, "mcp_client.py",
                "--action", action,
                "--language", language,
                "--description", description
            ])

        elif action == "optimize":
            code_file = input("请输入代码文件路径: ")
            goal = input("请输入优化目标: ")

            with open(code_file, "r") as f:
                code = f.read()

            subprocess.run([
                sys.executable, "mcp_client.py",
                "--action", action,
                "--language", language,
                "--code", code,
                "--goal", goal
            ])

        elif action == "explain":
            code_file = input("请输入代码文件路径: ")

            with open(code_file, "r") as f:
                code = f.read()

            subprocess.run([
                sys.executable, "mcp_client.py",
                "--action", action,
                "--language", language,
                "--code", code
            ])

        else:
            print("无效的操作")

    else:
        print("无效的选择")

if __name__ == "__main__":
    asyncio.run(main())
