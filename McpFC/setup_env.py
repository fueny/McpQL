#!/usr/bin/env python3
"""
设置和管理项目环境的脚本，使用uv包管理工具。
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_uv_installed():
    """检查uv是否已安装"""
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_uv():
    """安装uv包管理工具"""
    print("正在安装uv包管理工具...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
        print("uv安装成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"安装uv失败: {e}")
        return False

def create_venv():
    """创建虚拟环境"""
    venv_path = ".venv"
    
    if Path(venv_path).exists():
        print(f"虚拟环境已存在于 {venv_path}")
        return True
    
    print(f"正在创建虚拟环境 {venv_path}...")
    try:
        subprocess.run(["uv", "venv", venv_path], check=True)
        print(f"虚拟环境创建成功: {venv_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"创建虚拟环境失败: {e}")
        return False

def install_dependencies(dev=False):
    """安装项目依赖"""
    print("正在安装项目依赖...")
    cmd = ["uv", "pip", "install", "-e", "."]
    
    if dev:
        cmd.append("--dev")
    
    try:
        subprocess.run(cmd, check=True)
        print("依赖安装成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"安装依赖失败: {e}")
        return False

def activate_venv_command():
    """返回激活虚拟环境的命令"""
    if sys.platform == "win32":
        return ".venv\\Scripts\\activate"
    else:
        return "source .venv/bin/activate"

def main():
    parser = argparse.ArgumentParser(description="设置和管理项目环境")
    parser.add_argument("--dev", action="store_true", help="安装开发依赖")
    parser.add_argument("--clean", action="store_true", help="清理并重新创建虚拟环境")
    
    args = parser.parse_args()
    
    # 检查uv是否已安装
    if not check_uv_installed():
        print("未检测到uv。正在尝试安装...")
        if not install_uv():
            print("无法安装uv。请手动安装: pip install uv")
            return 1
    
    # 如果需要清理，删除现有虚拟环境
    if args.clean and Path(".venv").exists():
        import shutil
        print("正在清理现有虚拟环境...")
        shutil.rmtree(".venv")
    
    # 创建虚拟环境
    if not create_venv():
        return 1
    
    # 安装依赖
    if not install_dependencies(args.dev):
        return 1
    
    # 显示激活命令
    activate_cmd = activate_venv_command()
    print(f"\n设置完成！要激活虚拟环境，请运行:\n\n    {activate_cmd}\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
