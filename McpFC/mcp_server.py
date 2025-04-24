#!/usr/bin/env python3
from typing import Any, Dict, List
import os
import json
import asyncio
from mcp.server.fastmcp import FastMCP
import openai

# 初始化FastMCP服务器
mcp = FastMCP("code-assistant")

# 设置OpenAI API密钥和基础URL
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_api_base = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")

if not openai_api_key:
    print("警告: 未设置OPENAI_API_KEY环境变量")
else:
    print("OpenAI API密钥已设置")

print(f"使用API基础URL: {openai_api_base}")

# 初始化OpenAI客户端
client = openai.OpenAI(api_key=openai_api_key, base_url=openai_api_base)

@mcp.tool()
async def generate_code(language: str, description: str) -> str:
    """根据描述生成代码。

    Args:
        language: 编程语言 (例如 python, javascript, java, c#, etc.)
        description: 代码功能的详细描述
    """
    try:
        # 构建提示词
        prompt = f"""
        请为我生成{language}代码，实现以下功能:
        {description}

        只返回代码，不需要解释。确保代码是完整的、可运行的，并遵循最佳实践。
        """

        # 调用OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的代码生成助手，专注于生成高质量、可运行的代码。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,  # 较低的温度使输出更加确定性
            max_tokens=2000
        )

        # 提取生成的代码
        generated_code = response.choices[0].message.content

        return f"""
# {language}代码 - 基于描述: {description}

{generated_code}
"""
    except Exception as e:
        return f"生成代码时出错: {str(e)}"

@mcp.tool()
async def optimize_code(language: str, code: str, optimization_goal: str) -> str:
    """优化现有代码。

    Args:
        language: 编程语言 (例如 python, javascript, java, c#, etc.)
        code: 需要优化的代码
        optimization_goal: 优化目标 (例如 "性能", "可读性", "内存使用", "简洁性")
    """
    try:
        # 构建提示词
        prompt = f"""
        请优化以下{language}代码，优化目标是: {optimization_goal}

        原始代码:
        ```{language}
        {code}
        ```

        请提供优化后的代码，并简要说明所做的更改。
        """

        # 调用OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的代码优化专家，专注于根据特定目标优化代码。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )

        # 提取优化后的代码
        optimized_result = response.choices[0].message.content

        return f"""
# 优化后的{language}代码 - 优化目标: {optimization_goal}

{optimized_result}
"""
    except Exception as e:
        return f"优化代码时出错: {str(e)}"

@mcp.tool()
async def explain_code(language: str, code: str) -> str:
    """解释代码的功能和工作原理。

    Args:
        language: 编程语言 (例如 python, javascript, java, c#, etc.)
        code: 需要解释的代码
    """
    try:
        # 构建提示词
        prompt = f"""
        请详细解释以下{language}代码的功能和工作原理:

        ```{language}
        {code}
        ```

        请提供清晰、详细的解释，包括:
        1. 代码的整体功能
        2. 关键部分的工作原理
        3. 使用的主要算法或技术
        4. 任何可能的边缘情况或限制
        """

        # 调用OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的代码解释专家，擅长将复杂的代码解释得简单明了。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )

        # 提取解释
        explanation = response.choices[0].message.content

        return f"""
# {language}代码解释

{explanation}
"""
    except Exception as e:
        return f"解释代码时出错: {str(e)}"

if __name__ == "__main__":
    # 初始化并运行服务器
    print("启动代码助手MCP服务器...")
    mcp.run(transport='stdio')
