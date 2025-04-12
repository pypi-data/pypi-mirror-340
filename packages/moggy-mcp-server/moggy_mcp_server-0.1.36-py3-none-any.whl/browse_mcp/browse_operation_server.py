import base64
import json
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import TextContent, ImageContent
from playwright.async_api import Page
from browse_mcp.browse_manager import BrowserManager
from pydantic import BaseModel, Field
from browse_mcp.tools.playwright_tools import PlaywrightTools
import pathlib
from browse_mcp.tools.file_tools import FileTools

from autogen_ext.agents.web_surfer._types import InteractiveRegion
from autogen_ext.agents.web_surfer.playwright_controller import PlaywrightController
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    List,
    Optional,
    Sequence,
)

class BrowserNavigationServer(FastMCP):
    def __init__(self, server_name="browser-operation-server"):
        super().__init__(server_name)
        self.mcp = self
        self.browser_manager = BrowserManager()
        # self.llm_config = get_default_llm_config()
        # self.llm_client = LLMClient(self.llm_config)
        self.screenshots = dict()
        self.register_tools()
        self.register_resources()
        self.register_prompts()
        self.file_tools = FileTools()

    def register_tools(self):

        @self.mcp.tool(description="在百度上搜索并获取结果")
        async def baidu_search(query: str, page: int = 1,pageSize: int = 50):
            """在百度上执行搜索查询并返回结果"""
            try:
                self.current_query = query
                self.current_page = page
                
                # 构建百度搜索URL
                search_url = f"https://www.baidu.com/s?wd={query}&pn={(page-1)*10}&rn={pageSize}"
                
                # 导航到搜索页面
                browser_page: Page = await self.browser_manager.ensure_browser()
                await browser_page.goto(url=search_url, wait_until="domcontentloaded", timeout=30000)
                
                # 等待搜索结果加载
                await browser_page.wait_for_selector(".result", timeout=5000)
                
                # 提取搜索结果
                results = await self._extract_search_results(browser_page)
                
                # 提取分页信息
                total_pages = await self._extract_pagination_info(browser_page)
                self.total_pages = total_pages
                
                # 缓存结果
                cache_key = f"{query}_{page}"
                self.search_results_cache[cache_key] = results
                
                # 构建返回信息
                return {
                    "query": query,
                    "page": page,
                    "total_pages": total_pages,
                    "results": [result.dict() for result in results],
                    "result_count": len(results)
                }
            except Exception as e:
                raise ValueError(f"搜索失败: {e}")
        # @self.mcp.tool(description="Navigate to a URL and get makrdown content")
        # async def playwright_navigate(url: str):
        #     """Navigate to a URL."""
        #     try:
        #         page: Page = await self.browser_manager.ensure_browser()
        #         await page.goto(url=url, wait_until="load", timeout=30000)
        #         page: Page = await self.browser_manager.ensure_browser()
        #         playwright_controller = PlaywrightController()
        #         page_markdown: str = await playwright_controller.get_page_markdown(page)
        #         return page_markdown
        #     except Exception as e:
        #         raise ValueError(f"Navigation failed: {e}")


        # async def content_elements_mark_backup():
        #     page: Page = await self.browser_manager.ensure_browser()
        #     mark_elements_css = self.file_tools.get_file_content("src/browse_mcp/css/page_elements_mark.css")
        #     await page.add_style_tag(content=mark_elements_css)
        #     mark_elements_script = self.file_tools.get_file_content("src/browse_mcp/script/page_elements_mark.js")
        #     element_count = await page.evaluate(mark_elements_script)
        #     mark_elements_choose = self.file_tools.get_file_content("src/browse_mcp/script/page_elements_choose.js")
        #     marked_content = await page.evaluate(mark_elements_choose)
        #     return marked_content

        # @self.mcp.tool(description="get markdown from current web page")       
        # async def content_markdown():
        #     page: Page = await self.browser_manager.ensure_browser()
        #     playwright_controller = PlaywrightController()
        #     page_markdown: str = await playwright_controller.get_page_markdown(page)
        #     return page_markdown



        # @self.mcp.tool()
        # async def get_playwright_screenshot(
        #     name: str, selector: str = None, width: int = 800, height: int = 600
        # ):
        #     """Take a screenshot of the current page or a specific element."""
        #     try:
        #         page: Page = await self.browser_manager.ensure_browser()
        #         element = await page.query_selector(selector) if selector else None
        #         screeenshot_options = {
        #             "type": "png",
        #             "full_page": True,
        #             "element": element,
        #             # "mask": True # TODO
        #         }

        #         if element:
        #             screenshot = await page.screenshot(**screeenshot_options)
        #             # Convert the screenshot to a base64 string
        #             screenshot_base64 = base64.b64encode(screenshot).decode("utf-8")
        #             self.screenshots[name] = screenshot_base64
        #             return [
        #                 TextContent(type="text", text=f"Screenshot {name} taken"),
        #                 ImageContent(
        #                     type="image", data=screenshot_base64, mimeType="image/png"
        #                 ),
        #             ]
        #         else:
        #             return f"Element not found: {selector}"
        #     except Exception as e:
        #         raise ValueError(f"Screenshot failed: {e}")

        # async def store_playwright_screenshot(
        #     name: str, selector: str = None, width: int = 800, height: int = 600
        # ):
        #     """Take a screenshot of the current page or a specific element."""
        #     try:
        #         page: Page = await self.browser_manager.ensure_browser()
        #         await page.screenshot(path=os.path.join(self.debug_dir, screenshot_png_name))  # type: igno
        #     except Exception as e:
        #         raise ValueError(f"Screenshot failed: {e}")

        @self.mcp.tool()
        async def playwright_click(selector: str):
            """Click an element on the page."""
            try:
                page: Page = await self.browser_manager.ensure_browser()
                await page.click(selector)
                return f"Clicked on {selector}"
            except Exception as e:
                raise ValueError(f"Failed to click: {e}")

        # @self.mcp.tool()
        # async def playwright_fill(selector: str, value: str):
        #     """Fill out an input field."""
        #     try:
        #         page: Page = await self.browser_manager.ensure_browser()
        #         await page.wait_for_selector(selector)
        #         await page.fill(selector, value)
        #         return f"Filled {selector} with {value}"
        #     except Exception as e:
        #         raise ValueError(f"Failed to fill: {e}")

        # @self.mcp.tool()
        # async def playwright_select(selector: str, value: str):
        #     """Select an element on the page with a Select tag."""
        #     try:
        #         page: Page = await self.browser_manager.ensure_browser()
        #         await page.wait_for_selector(selector)
        #         await page.select_option(selector, value)
        #         return f"Selected {value} in {selector}"
        #     except Exception as e:
        #         raise ValueError(f"Failed to select: {e}")

        # @self.mcp.tool()
        # async def playwright_hover(selector: str):
        #     """Hover over an element on the page."""
        #     try:
        #         page: Page = await self.browser_manager.ensure_browser()
        #         await page.wait_for_selector(selector)
        #         await page.hover(selector)
        #         return f"Hovered over {selector}"
        #     except Exception as e:
        #         raise ValueError(f"Failed to hover: {e}")

        # @self.mcp.tool()
        # async def playwright_evaluate(script: str):
        #     """Execute JavaScript in the browser console."""
        #     try:
        #         page: Page = await self.browser_manager.ensure_browser()
        #         script_result = await page.evaluate(
        #             """
        #         (script) => {
        #             const logs = [];
        #             const originalConsole = { ...console };

        #             ['log', 'info', 'warn', 'error'].forEach(method => {
        #                 console[method] = (...args) => {
        #                     logs.push(`[${method}] ${args.join(' ')}`);
        #                     originalConsole[method](...args);
        #                 };
        #             });

        #             try {
        #                 const result = eval(script);
        #                 Object.assign(console, originalConsole);
        #                 return { result, logs };
        #             } catch (error) {
        #                 Object.assign(console, originalConsole);
        #                 throw error;
        #             }
        #         }
        #         """,
        #             script,
        #         )
        #         # Parentheses allow grouping multiple expressions in one line,
        #         # often used for long strings, tuples, or function arguments
        #         # that span multiple lines.
        #         return_string = (
        #             "Execution result:\n"
        #             + json.dumps(script_result["result"], indent=2)
        #             + "\n\n"
        #             + "Console output:\n"
        #             + "\n".join(script_result["logs"])
        #         )
        #         return return_string
        #     except Exception as e:
        #         raise ValueError(f"Script execution failed: {e}")

        # @self.mcp.tool()
        # async def playwright_get_page_source() -> str:
        #     """获取当前页面的HTML源码"""
        #     try:
        #         page: Page = await self.browser_manager.ensure_browser()
        #         # 获取页面的完整HTML内容
        #         html_content = await page.content()
                
        #         return html_content
        #     except Exception as e:
        #         raise ValueError(f"获取页面源码失败: {e}")
        # @self.mcp.tool()
        # async def extract_selector_by_page_content(user_message: str) -> str:
        #     """Try to find a css selector by current page content."""
        #     # Ensure the browser page is available
        #     page = await self.browser_manager.ensure_browser()

        #     # Get the HTML content of the page
        #     html_content = await page.content()

        #     # Prepare the prompt for the LLM
        #     prompt = (
        #         "Given the following HTML content of a web page:\n\n"
        #         f"{html_content}\n\n"
        #         f"User request: '{user_message}'\n\n"
        #         "Provide the CSS selector that best matches the user's request. Return only the CSS selector."
        #     )

        #     # Use the LLM client to generate the selector
        #     llm_response: LLMResponse = await self.llm_client.invoke_with_prompt(prompt)
        #     selector: str = llm_response["content"]

        #     # Return the selector
        #     return selector.strip()

        # # Long-running example to read all screenshots from a list of file names
        # @self.mcp.tool()
        # async def read_all_screenshots(file_name_list: list[str], ctx: Context) -> str:
        #     """Read all screenshots from a list of file names."""
        #     for i, file_name in enumerate(file_name_list):
        #         ctx.info(f"Processing {file_name}...")
        #         await ctx.report_progress(i, len(file_name_list))

        #         # Read another resource if needed
        #         data = await ctx.read_resource(f"screenshot://{file_name}")

        #     return "Processing complete"

    def register_resources(self):
        @self.mcp.resource("console://logs")
        async def get_console_logs() -> str:
            """Get a personalized greeting"""
            return TextContent(
                type="text", text="\n".join(self.browser_manager.console_logs)
            )

        @self.mcp.resource("screenshot://{name}")
        async def get_screenshot(name: str) -> str:
            """Get a screenshot by name"""
            screenshot_base64 = self.screenshots.get(name)
            if screenshot_base64:
                return ImageContent(
                    type="image",
                    data=screenshot_base64,
                    mimeType="image/png",
                    uri=f"screenshot://{name}",
                )
            else:
                raise ValueError(f"Screenshot {name} not found")

    def register_prompts(self):
        @self.mcp.prompt()
        async def hello_world(code: str) -> str:
            return f"Hello world:\n\n{code}"


""" 
When executing the MCP Inspector in a terminal, use the following command:

```bash
cmd> fastmcp dev ./server/browser_navigator_server.py:app
```

app = BrowserNavigationServer()

- `server/browser_navigator_server.py` specifies the file path.
- `app` refers to the server object created by `BrowserNavigationServer`.

After running the command, the following message will be displayed:

```
> Starting MCP Inspector...
> 🔍 MCP Inspector is up and running at http://localhost:5173 🚀
```

**Important:** Do not use `__main__` to launch the MCP Inspector. This will result in the following error:

    No server object found in **.py. Please either:
    1. Use a standard variable name (mcp, server, or app)
    2. Specify the object name with file:object syntax
"""

app = BrowserNavigationServer()
def main():
    app.run()

print("BrowserNavigationServer is running...")
# print all attributes of the mcp
# print(dir(app))


# if __name__ == "__main__":
#     app = BrowserNavigationServer()
#     app.run()
#     print("BrowserNavigationServer is running...")