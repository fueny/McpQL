
# 使用 npx -y @modelcontextprotocol/inspector uv run web_search.py 运行代码
# 此代码存在问题，关于下边zhipu的api key 不可从.env读取会在用行时报错 记录时间2025.4.22，待后续解决
import httpx
from mcp.server import FastMCP
# # 初始化 FastMCP 服务器
app = FastMCP('web-search')


@app.tool()
async def web_search(query: str) -> str:
    """
    搜索互联网内容

    Args:
        query: 要搜索内容

    Returns:
        搜索结果的总结
    """

    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://open.bigmodel.cn/api/paas/v4/tools',
            headers={'Authorization': '92ca11e676794de485c213c18eab0ea7.fpphoGfEswv9wh9t'},
            json={
                'tool': 'web-search-pro',
                'messages': [
                    {'role': 'user', 'content': query}
                ],
                'stream': False
            }
        )

        res_data = []
        for choice in response.json()['choices']:
            for message in choice['message']['tool_calls']:
                search_results = message.get('search_result')
                if not search_results:
                    continue
                for result in search_results:
                    res_data.append(result['content'])

        return '\n\n\n'.join(res_data)
if __name__ == "__main__":
    app.run(transport='stdio')