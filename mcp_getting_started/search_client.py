import asyncio

from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

# 为 stdio 连接创建服务器参数
server_params = StdioServerParameters(
    # 服务器执行的命令，这里我们使用 uv 来运行 web_search.py
    command='uv',
    # 运行的参数
    args=['run', 'web_search.py'],
    # 环境变量，默认为 None，表示使用当前环境变量
    # env=None
)


async def search_web(query):
    """
    执行网络搜索并返回结果
    
    Args:
        query: 搜索查询
        
    Returns:
        搜索结果
    """
    # 创建 stdio 客户端
    async with stdio_client(server_params) as (stdio, write):
        # 创建 ClientSession 对象
        async with ClientSession(stdio, write) as session:
            # 初始化 ClientSession
            await session.initialize()
            
            try:
                # 调用 web_search 工具
                response = await session.call_tool('web_search', {'query': query})
                return response
            except Exception as e:
                return f"搜索出错: {str(e)}"


async def interactive_search():
    """
    交互式搜索界面
    """
    print("=== 网络搜索客户端 ===")
    print("输入 'exit' 或 'quit' 退出程序")
    
    while True:
        # 获取用户输入
        query = input("\n请输入搜索内容: ")
        
        # 检查是否退出
        if query.lower() in ['exit', 'quit']:
            print("感谢使用，再见！")
            break
            
        if not query.strip():
            print("请输入有效的搜索内容")
            continue
            
        print("正在搜索，请稍候...")
        
        # 执行搜索
        result = await search_web(query)
        
        # 显示结果
        print("\n=== 搜索结果 ===")
        print(result)
        print("===============")


async def main():
    await interactive_search()


if __name__ == '__main__':
    asyncio.run(main())
