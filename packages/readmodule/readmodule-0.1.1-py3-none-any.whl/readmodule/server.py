from mcp.server.fastmcp import FastMCP
import os

def create_server():
    """Create and return the MCP server instance"""
    # 创建 MCP server
    mcp = FastMCP("readmodule", "Read the code based on the given path and module name.")

    @mcp.tool()
    def read(path, module_name):
        """
        Read the code from all files in an OpenHarmony module directory, including subdirectories.
        
        Args:
            path (str): The project path
            module_name (str): The name of the module directory to read
            
        Returns:
            dict: A dictionary containing the code content from all files or error message
        """
        try:
            module_path = os.path.join(path, module_name)
            
            # 存储所有文件内容
            all_files_content = []
            files_count = 0
            
            # 需要读取的文件扩展名
            valid_extensions = ('.md', '.ets', '.ts', '.json', '.json5', '.cpp', '.h')
            
            # 检查模块是否存在
            if not os.path.isdir(module_path):
                return {"error": f"Module directory not found: {module_path}"}
            
            # 遍历目录及子目录
            for root, dirs, files in os.walk(module_path):
                # 如果当前目录是模块下的 build 目录，跳过此目录
                rel_dir = os.path.relpath(root, module_path)
                dir_parts = rel_dir.split(os.sep)
                
                # 跳过模块下的 build 目录
                if dir_parts[0] == 'build':
                    continue
                
                for file in files:
                    # 只读取指定类型的文件
                    if file.lower().endswith(valid_extensions):
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, path)
                        
                        try:
                            # 读取文件内容
                            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                                file_content = f.read()
                                
                            # 添加文件标注和内容
                            all_files_content.append(
                                f"# FILE: {relative_path}\n"
                                f"# {'=' * 60}\n"
                                f"{file_content}\n"
                                f"# {'=' * 60}\n"
                            )
                            files_count += 1
                        except Exception as file_error:
                            all_files_content.append(f"# ERROR reading {relative_path}: {str(file_error)}\n")
            
            if files_count == 0:
                return {
                    "warning": f"No relevant files found in module: {module_path}",
                    "module_path": module_path,
                    "success": True
                }
                
            return {
                "content": "\n".join(all_files_content),
                "module_path": module_path,
                "files_count": files_count,
                "success": True
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }

    return mcp

def start_server():
    """Initialize and start the MCP server"""
    mcp = create_server()
    print("MCP Server 'readModule' started and waiting for connections...")
    # 启动服务器
    mcp.run()

