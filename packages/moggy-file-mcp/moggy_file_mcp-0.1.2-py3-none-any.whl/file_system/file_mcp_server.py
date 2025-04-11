import os
import shutil
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import TextContent
from pydantic import BaseModel
from typing import List, Optional

class FileOperationServer(FastMCP):
    def __init__(self, work_dir: str = "", server_name="file-operation-server"):
        super().__init__(server_name)
        self.mcp = self
        # 初始化根目录为当前工作目录
        self.root_dir = ""
        # 确保根目录存在
        os.makedirs(self.root_dir, exist_ok=True)
        self.screenshots = dict()
        self.register_tools()
        self.register_resources()
        # self.register_prompts()

    def _set_work_dir(self, work_dir: str):
        self.root_dir = work_dir

    def register_tools(self):
        @self.mcp.tool(description="列出指定目录下的所有文件和文件夹")
        async def list_directory(path: str="") -> List[str]:
            """列出指定目录的内容"""
            try:
                if path == "":
                    full_path = self.root_dir
                else:
                    full_path = os.path.join(self.root_dir, path)
                    
                items = os.listdir(full_path)
                return [os.path.join(full_path, item) for item in items]
            except Exception as e:
                raise ValueError(f"列出目录失败: {e}")

        @self.mcp.tool(description="读取文件内容")
        async def read_file(file_path: str) -> str:
            """读取文件内容"""
            try:
                full_path = os.path.join(self.root_dir, file_path)
                with open(full_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                raise ValueError(f"读取文件失败: {e}")

        @self.mcp.tool(description="写入文件内容")
        async def write_file(file_path: str, content: str) -> str:
            """写入文件内容"""
            try:
                full_path = os.path.join(self.root_dir, file_path)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"成功写入文件: {full_path}"
            except Exception as e:
                raise ValueError(f"写入文件失败: {e}")

        @self.mcp.tool(description="复制文件")
        async def copy_file(source: str, destination: str) -> str:
            """复制文件"""
            try:
                full_source = os.path.join(self.root_dir, source)
                full_dest = os.path.join(self.root_dir, destination)
                shutil.copy2(full_source, full_dest)
                return f"成功复制文件从 {full_source} 到 {full_dest}"
            except Exception as e:
                raise ValueError(f"复制文件失败: {e}")

        @self.mcp.tool(description="移动文件")
        async def move_file(source: str, destination: str) -> str:
            """移动文件"""
            try:
                full_source = os.path.join(self.root_dir, source)
                full_dest = os.path.join(self.root_dir, destination)
                shutil.move(full_source, full_dest)
                return f"成功移动文件从 {full_source} 到 {full_dest}"
            except Exception as e:
                raise ValueError(f"移动文件失败: {e}")

        @self.mcp.tool(description="删除文件或目录")
        async def delete_item(path: str) -> str:
            """删除文件或目录"""
            try:
                full_path = os.path.join(self.root_dir, path)
                if os.path.isfile(full_path):
                    os.remove(full_path)
                    return f"成功删除文件: {full_path}"
                elif os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                    return f"成功删除目录: {full_path}"
                else:
                    return f"路径不存在: {full_path}"
            except Exception as e:
                raise ValueError(f"删除失败: {e}")

        @self.mcp.tool(description="创建目录")
        async def create_directory(path: str) -> str:
            """创建新目录"""
            try:
                full_path = os.path.join(self.root_dir, path)
                os.makedirs(full_path, exist_ok=True)
                return f"成功创建目录: {full_path}"
            except Exception as e:
                raise ValueError(f"创建目录失败: {e}")

    def register_resources(self):
        @self.mcp.resource("file://{path}")
        async def get_file_content(path: str) -> TextContent:
            """获取文件内容作为资源"""
            try:
                full_path = os.path.join(self.root_dir, path)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return TextContent(type="text", text=content)
            except Exception as e:
                raise ValueError(f"读取文件资源失败: {e}")

app = FileOperationServer()

def main():
    work_dir = os.environ.get("work_dir", "")
    if work_dir == '':
        raise ValueError("work_dir不能为空")

    app._set_work_dir(work_dir)
    app.run(transport="stdio")
