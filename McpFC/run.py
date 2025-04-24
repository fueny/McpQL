#!/usr/bin/env python3
"""
代码助手启动脚本 - 使用uv管理的环境
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_environment():
    """检查环境是否已正确设置"""
    # 检查虚拟环境
    venv_path = Path(".venv")
    if not venv_path.exists():
        print("未检测到虚拟环境。正在设置...")
        setup_environment()
        return False
    
    # 检查是否在虚拟环境中运行
    if not os.environ.get("VIRTUAL_ENV"):
        print("警告: 未在虚拟环境中运行。")
        print("请先激活虚拟环境:")
        if sys.platform == "win32":
            print("    .venv\\Scripts\\activate")
        else:
            print("    source .venv/bin/activate")
        return False
    
    return True

def setup_environment():
    """设置环境"""
    # 检查是否安装了uv
    if not shutil.which("uv"):
        print("未检测到uv。正在安装...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
            print("uv安装成功！")
        except subprocess.CalledProcessError:
            print("安装uv失败。请手动安装: pip install uv")
            return False
    
    # 运行setup_env.py
    try:
        subprocess.run([sys.executable, "setup_env.py"], check=True)
        print("环境设置成功！")
        return True
    except subprocess.CalledProcessError:
        print("环境设置失败。请检查错误信息。")
        return False

def main():
    """主函数"""
    # 检查环境
    if not check_environment():
        return 1
    
    # 运行代码助手
    try:
        subprocess.run([sys.executable, "start_code_assistant.py"])
        return 0
    except Exception as e:
        print(f"运行代码助手时出错: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
