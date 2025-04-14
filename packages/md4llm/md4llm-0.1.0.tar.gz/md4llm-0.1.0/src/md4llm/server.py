from mcp.server.fastmcp import FastMCP 
import pymupdf4llm


mcp = FastMCP("markdowngiver")


@mcp.tool()
def give_markdown(url:str)->str: 
    """
    This fucntion takes pdf absolute path as input and it outpts the markdown format of the pdf
    """

    text = pymupdf4llm.to_markdown(url)

    return text 
