from fastmcp import FastMCP
from typing import Dict, Any, List

from src.tools.email import Email

# Create an MCP server
mcp = FastMCP(
    "tdoa-mcp",
    description="Tongda OA integration through the Model Context Protocol",
)

@mcp.tool()
def write_email(subject: str, content: str) -> str:
    """在通达OA中写一封邮件，并将邮件保存到草稿箱中
    
    Args:
        subject: 邮件主题
        content: 邮件内容
        
    Returns:
        str: 邮件保存结果
    """
    email = Email()
    body_id = email.write(subject, content)
    if body_id:
        return f"邮件已保存到草稿箱，ID为：{body_id}"
    else:
        return "邮件保存失败"

def main():
    """Run the MCP server"""
    mcp.run()

if __name__ == "__main__":
    main()