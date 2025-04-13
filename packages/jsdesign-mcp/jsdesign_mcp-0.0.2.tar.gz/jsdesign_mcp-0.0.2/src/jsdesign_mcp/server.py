from typing import Any, Optional, Dict, Union, List
import httpx
import os
import argparse
import json
from mcp.server.fastmcp import FastMCP

# 初始化FastMCP服务器
mcp = FastMCP("jsdesign")

# 从环境变量或默认值获取API基础地址
def get_api_base():
    api_base = os.environ.get("JSDESIGN_API_BASE")
    if api_base:
        return api_base
    
    # 默认使用本地服务器
    return "http://localhost:8080/api/connections"

# 常量
JS_DESIGN_API_BASE = get_api_base()

# 全局变量存储连接代码
CURRENT_CONNECTION_CODE = None

async def make_jsdesign_request(connection_code: str, endpoint: str, method: str = "GET", data: dict = None) -> Dict[str, Any]:
    """向jsdesign API发出请求
    
    Args:
        connection_code (str): 连接代码
        endpoint (str): API端点
        method (str, optional): 请求方法. 默认为 "GET"
        data (dict, optional): 请求数据
        
    Returns:
        Dict[str, Any]: 响应数据
    
    Raises:
        HTTPError: 当HTTP请求失败时
        TimeoutError: 当请求超时时
        ValueError: 当参数无效时
    """
    if not connection_code:
        raise ValueError("连接代码不能为空")
    
    url = f"{JS_DESIGN_API_BASE}/{connection_code}/{endpoint}"
    print(f"发送请求到URL: {url}, 方法: {method}")
    
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, timeout=30.0)
            elif method == "POST":
                response = await client.post(url, json=data, timeout=30.0)
            elif method == "PATCH":
                response = await client.patch(url, json=data, timeout=30.0)
            elif method == "DELETE":
                response = await client.delete(url, timeout=30.0)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            print(f"收到响应: 状态码 {response.status_code}")
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            print(f"请求超时: {url}")
            return {"success": False, "error": "请求超时"}
        except httpx.HTTPError as e:
            print(f"HTTP错误: {str(e)}, URL: {url}")
            return {"success": False, "error": f"HTTP错误: {str(e)}"}
        except Exception as e:
            print(f"请求错误: {str(e)}, URL: {url}")
            return {"success": False, "error": str(e)}

async def verify_connection(connection_code: str) -> bool:
    """验证连接码是否有效
    
    Args:
        connection_code (str): 要验证的连接码
        
    Returns:
        bool: 连接码是否有效
    """
    if not connection_code:
        return False
        
    result = await make_jsdesign_request(connection_code, "check")
    if result and result.get("success"):
        return result["data"]["connected"]
    return False

# 连接到jsdesign
@mcp.tool()
async def join_channel(connection_code: str) -> str:
    """连接到一个指定的频道，并保存连接代码供后续使用
    
    此工具用于建立与jsdesign的连接。在使用其他工具之前，必须先调用此工具进行连接。
    
    Args:
        connection_code (str): jsdesign提供的连接代码
        
    Returns:
        str: 连接结果信息
    """
    if not connection_code:
        return "连接失败：连接代码不能为空"
    
    global CURRENT_CONNECTION_CODE
    
    # 验证连接码是否有效
    is_valid = await verify_connection(connection_code)
    if not is_valid:
        return "连接失败：无效的连接代码"
    
    CURRENT_CONNECTION_CODE = connection_code
    return f"已成功连接到频道，连接代码：{connection_code}"

# 获取文档信息
@mcp.tool()
async def get_document(depth: int = 1, connection_code: str = None) -> str:
    """获取文档信息
    
    此工具用于获取当前jsdesign文档的信息，包括页面、图层等结构。
    
    Args:
        depth (int, optional): 获取文档结构的深度。默认为1
        connection_code (str, optional): 连接代码。如果不提供则使用当前连接
        
    Returns:
        str: 文档信息的字符串表示
    """
    # 如果未提供connection_code，则使用全局存储的
    code = connection_code or CURRENT_CONNECTION_CODE
    if not code:
        return "错误：未提供连接代码且未连接到任何频道"
    
    if depth < 1:
        return "错误：depth必须大于0"
    
    data = await make_jsdesign_request(code, f"document?depth={depth}")
    if not data or not data.get("success"):
        return f"无法获取文档信息: {data.get('error', '未知错误')}"
    return str(data["data"])

# 获取当前选择的节点信息
@mcp.tool()
async def get_selection(depth: int = 2, connection_code: str = None) -> str:
    """获取当前选择的节点信息
    
    此工具用于获取用户在jsdesign中当前选中的节点的详细信息。
    
    Args:
        depth (int, optional): 获取节点信息的深度。默认为2
        connection_code (str, optional): 连接代码。如果不提供则使用当前连接
        
    Returns:
        str: 选中节点的信息
    """
    code = connection_code or CURRENT_CONNECTION_CODE
    if not code:
        return "错误：未提供连接代码且未连接到任何频道"
    
    if depth < 1:
        return "错误：depth必须大于0"
    
    data = await make_jsdesign_request(code, f"selection?depth={depth}")
    if not data or not data.get("success"):
        return f"无法获取选择信息: {data.get('error', '未知错误')}"
    return str(data["data"])

# 创建矩形节点
@mcp.tool()
async def create_rectangle(x: float, y: float, width: float, height: float, name: str = None, connection_code: str = None) -> str:
    """创建矩形节点
    
    此工具用于在jsdesign中创建一个新的矩形图形。
    
    Args:
        x (float): 矩形左上角的X坐标
        y (float): 矩形左上角的Y坐标
        width (float): 矩形的宽度
        height (float): 矩形的高度
        name (str, optional): 矩形的名称
        connection_code (str, optional): 连接代码。如果不提供则使用当前连接
        
    Returns:
        str: 操作结果信息
    """
    code = connection_code or CURRENT_CONNECTION_CODE
    if not code:
        return "错误：未提供连接代码且未连接到任何频道"
    
    # 参数验证
    if width <= 0 or height <= 0:
        return "错误：宽度和高度必须大于0"
    
    data = {
        "x": x,
        "y": y,
        "width": width,
        "height": height
    }
    if name:
        data["name"] = name
    
    result = await make_jsdesign_request(code, "rectangles", "POST", data)
    if not result or not result.get("success"):
        return f"创建矩形失败: {result.get('error', '未知错误')}"
    return "矩形创建成功"

# 创建文本节点
@mcp.tool()
async def create_text(x: float, y: float, text: str, fontSize: int = 24, fontWeight: int = 400, connection_code: str = None) -> str:
    """创建文本节点
    
    此工具用于在jsdesign中创建一个新的文本元素。
    
    Args:
        x (float): 文本左上角的X坐标
        y (float): 文本左上角的Y坐标
        text (str): 要显示的文本内容
        fontSize (int, optional): 字体大小。默认为24
        fontWeight (int, optional): 字体粗细。默认为400
        connection_code (str, optional): 连接代码。如果不提供则使用当前连接
        
    Returns:
        str: 操作结果信息
    """
    code = connection_code or CURRENT_CONNECTION_CODE
    if not code:
        return "错误：未提供连接代码且未连接到任何频道"
    
    # 参数验证
    if not text:
        return "错误：文本内容不能为空"
    if fontSize <= 0:
        return "错误：字体大小必须大于0"
    if fontWeight < 100 or fontWeight > 900:
        return "错误：字体粗细必须在100-900之间"
    
    data = {
        "x": x,
        "y": y,
        "text": text,
        "fontSize": fontSize,
        "fontWeight": fontWeight
    }
    
    result = await make_jsdesign_request(code, "texts", "POST", data)
    if not result or not result.get("success"):
        return f"创建文本失败: {result.get('error', '未知错误')}"
    return "文本创建成功"

# 移动节点到新位置
@mcp.tool()
async def move_node(node_id: str, x: float, y: float, connection_code: str = None) -> str:
    """移动节点到新位置
    
    此工具用于移动jsdesign中的任何节点到新的位置。
    
    Args:
        node_id (str): 要移动的节点ID
        x (float): 新位置的X坐标
        y (float): 新位置的Y坐标
        connection_code (str, optional): 连接代码。如果不提供则使用当前连接
        
    Returns:
        str: 操作结果信息
    """
    code = connection_code or CURRENT_CONNECTION_CODE
    if not code:
        return "错误：未提供连接代码且未连接到任何频道"
    
    if not node_id:
        return "错误：节点ID不能为空"
    
    data = {
        "x": x,
        "y": y
    }
    
    result = await make_jsdesign_request(code, f"nodes/{node_id}/position", "PATCH", data)
    if not result or not result.get("success"):
        return f"移动节点失败: {result.get('error', '未知错误')}"
    return "节点移动成功"

# 调整节点尺寸
@mcp.tool()
async def resize_node(node_id: str, width: float, height: float, connection_code: str = None) -> str:
    """调整节点尺寸
    
    此工具用于调整jsdesign中节点的尺寸。
    
    Args:
        node_id (str): 要调整的节点ID
        width (float): 新的宽度
        height (float): 新的高度
        connection_code (str, optional): 连接代码。如果不提供则使用当前连接
        
    Returns:
        str: 操作结果信息
    """
    code = connection_code or CURRENT_CONNECTION_CODE
    if not code:
        return "错误：未提供连接代码且未连接到任何频道"
    
    if not node_id:
        return "错误：节点ID不能为空"
    
    if width <= 0 or height <= 0:
        return "错误：宽度和高度必须大于0"
    
    data = {
        "width": width,
        "height": height
    }
    
    result = await make_jsdesign_request(code, f"nodes/{node_id}/size", "PATCH", data)
    if not result or not result.get("success"):
        return f"调整节点尺寸失败: {result.get('error', '未知错误')}"
    return "节点尺寸调整成功"

# 设置节点填充颜色
@mcp.tool()
async def set_fill_color(node_id: str, r: float, g: float, b: float, a: float = 1.0, connection_code: str = None) -> str:
    """设置节点填充颜色
    
    此工具用于设置jsdesign中节点的填充颜色。
    
    Args:
        node_id (str): 要设置颜色的节点ID
        r (float): 红色分量 (0-1)
        g (float): 绿色分量 (0-1)
        b (float): 蓝色分量 (0-1)
        a (float, optional): 透明度 (0-1)。默认为1.0
        connection_code (str, optional): 连接代码。如果不提供则使用当前连接
        
    Returns:
        str: 操作结果信息
    """
    code = connection_code or CURRENT_CONNECTION_CODE
    if not code:
        return "错误：未提供连接代码且未连接到任何频道"
    
    if not node_id:
        return "错误：节点ID不能为空"
    
    # 验证颜色值
    if not all(0 <= c <= 1 for c in [r, g, b, a]):
        return "错误：颜色分量必须在0-1之间"
    
    data = {
        "r": r,
        "g": g,
        "b": b,
        "a": a
    }
    
    result = await make_jsdesign_request(code, f"nodes/{node_id}/fill-color", "PATCH", data)
    if not result or not result.get("success"):
        return f"设置填充颜色失败: {result.get('error', '未知错误')}"
    return "填充颜色设置成功"

# 批量移动多个节点到各自新位置
@mcp.tool()
async def batch_move_nodes(nodes, connection_code: str = None) -> str:
    """批量移动多个节点到各自新位置
    
    此工具用于一次性移动多个节点到各自的新位置。
    
    Args:
        nodes (list): 包含节点移动信息的列表，格式为[{'nodeId': 'id1', 'x': 100, 'y': 200}, ...]
        connection_code (str, optional): 连接代码。如果不提供则使用当前连接
        
    Returns:
        str: 操作结果信息
    """
    code = connection_code or CURRENT_CONNECTION_CODE
    if not code:
        return "错误：未提供连接代码且未连接到任何频道"
    
    # 参数验证
    if isinstance(nodes, str):
        try:
            nodes = json.loads(nodes)
        except json.JSONDecodeError:
            return "错误：nodes参数必须是有效的JSON字符串"
    
    if not nodes or not isinstance(nodes, list):
        return "错误：必须提供节点列表"
    
    for node in nodes:
        if not all(key in node for key in ['nodeId', 'x', 'y']):
            return "错误：每个节点必须包含nodeId、x和y字段"
    
    # 修正API路径，使用正确的批量移动节点端点
    result = await make_jsdesign_request(
        code, 
        "nodes/batch-move",  # 确保这里不包含具体节点ID
        method="PATCH", 
        data={"nodes": nodes}
    )
    
    if not result or not result.get("success"):
        return f"批量移动节点失败: {result.get('error', '未知错误')}"
    
    # 统计成功和失败数量
    success_count = len(result.get("data", {}).get("success", []))
    error_count = len(result.get("data", {}).get("errors", []))
    
    if error_count > 0:
        return f"批量移动节点部分成功: {success_count}个成功, {error_count}个失败"
    
    return f"成功移动了{success_count}个节点"

# 批量调整多个节点尺寸
@mcp.tool()
async def batch_resize_nodes(nodes, connection_code: str = None) -> str:
    """批量调整多个节点尺寸
    
    此工具用于一次性调整多个节点的尺寸。
    
    Args:
        nodes (list): 包含节点尺寸信息的列表，格式为[{'nodeId': 'id1', 'width': 200, 'height': 150}, ...]
        connection_code (str, optional): 连接代码。如果不提供则使用当前连接
        
    Returns:
        str: 操作结果信息
    """
    code = connection_code or CURRENT_CONNECTION_CODE
    if not code:
        return "错误：未提供连接代码且未连接到任何频道"
    
    # 参数验证
    if isinstance(nodes, str):
        try:
            nodes = json.loads(nodes)
        except json.JSONDecodeError:
            return "错误：nodes参数必须是有效的JSON字符串"
    
    if not nodes or not isinstance(nodes, list):
        return "错误：必须提供节点列表"
    
    for node in nodes:
        if not all(key in node for key in ['nodeId', 'width', 'height']):
            return "错误：每个节点必须包含nodeId、width和height字段"
        if node.get('width', 0) <= 0 or node.get('height', 0) <= 0:
            return "错误：宽度和高度必须大于0"
    
    # 修正API路径，使用正确的批量调整尺寸端点
    result = await make_jsdesign_request(
        code, 
        "nodes/batch-resize",  # 确保这里不包含具体节点ID
        method="PATCH", 
        data={"nodes": nodes}
    )
    
    if not result or not result.get("success"):
        return f"批量调整节点尺寸失败: {result.get('error', '未知错误')}"
    
    # 统计成功和失败数量
    success_count = len(result.get("data", {}).get("success", []))
    error_count = len(result.get("data", {}).get("errors", []))
    
    if error_count > 0:
        return f"批量调整节点尺寸部分成功: {success_count}个成功, {error_count}个失败"
    
    return f"成功调整了{success_count}个节点的尺寸"

# 批量设置多个节点的填充颜色
@mcp.tool()
async def batch_set_fill_colors(nodes, connection_code: str = None) -> str:
    """批量设置多个节点的填充颜色
    
    此工具用于一次性设置多个节点的填充颜色。
    
    Args:
        nodes (list): 包含节点颜色信息的列表，格式为[{'nodeId': 'id1', 'r': 1, 'g': 0, 'b': 0, 'a': 1}, ...]
        connection_code (str, optional): 连接代码。如果不提供则使用当前连接
        
    Returns:
        str: 操作结果信息
    """
    code = connection_code or CURRENT_CONNECTION_CODE
    if not code:
        return "错误：未提供连接代码且未连接到任何频道"
    
    # 参数验证
    if isinstance(nodes, str):
        try:
            nodes = json.loads(nodes)
        except json.JSONDecodeError:
            return "错误：nodes参数必须是有效的JSON字符串"
    
    if not nodes or not isinstance(nodes, list):
        return "错误：必须提供节点列表"
    
    for node in nodes:
        if not all(key in node for key in ['nodeId', 'r', 'g', 'b']):
            return "错误：每个节点必须包含nodeId、r、g和b字段"
        # 验证颜色值
        for color_key in ['r', 'g', 'b']:
            if color_key in node and not 0 <= node[color_key] <= 1:
                return f"错误：颜色分量必须在0-1之间，节点{node['nodeId']}的{color_key}值无效"
        if 'a' in node and not 0 <= node['a'] <= 1:
            return f"错误：透明度必须在0-1之间，节点{node['nodeId']}的a值无效"
    
    # 修正API路径，使用正确的批量设置颜色端点
    result = await make_jsdesign_request(
        code, 
        "nodes/fill-colors",  # 确保这里不包含具体节点ID
        method="PATCH", 
        data={"nodes": nodes}
    )
    
    if not result or not result.get("success"):
        return f"批量设置填充颜色失败: {result.get('error', '未知错误')}"
    
    # 统计成功和失败数量
    success_count = len(result.get("data", {}).get("success", []))
    error_count = len(result.get("data", {}).get("errors", []))
    
    if error_count > 0:
        return f"批量设置填充颜色部分成功: {success_count}个成功, {error_count}个失败"
    
    return f"成功设置了{success_count}个节点的填充颜色"

# 使用JSON格式创建复杂的设计元素
@mcp.tool()
async def create_from_json(elements, connection_code: str = None) -> str:
    """使用JSON格式创建复杂的设计元素
    
    此工具用于从自定义JSON结构创建设计元素，支持嵌套关系和复杂布局。
    非Frame元素如果有子元素会自动转换为Frame类型。
    
    Args:
        elements (list): 元素定义列表
        connection_code (str, optional): 连接代码。如果不提供则使用当前连接
        
    Returns:
        str: 操作结果信息
    """
    code = connection_code or CURRENT_CONNECTION_CODE
    if not code:
        return "错误：未提供连接代码且未连接到任何频道"
    
    # 参数验证
    if isinstance(elements, str):
        try:
            elements = json.loads(elements)
        except json.JSONDecodeError:
            return "错误：elements参数必须是有效的JSON字符串"
    
    if not elements or not isinstance(elements, list):
        return "错误：必须提供元素列表"
    
    data = {
        "elements": elements
    }
    
    # 调用 API 中的 create_from_json 命令
    result = await make_jsdesign_request(
        code,
        "create-from-json",  # 这个端点需要在后端实现
        method="POST",
        data=data
    )
    
    if not result or not result.get("success"):
        return f"从JSON创建元素失败: {result.get('error', '未知错误')}"
    
    result_data = result.get("data", {})
    elements_created = len(result_data.get("elements", []))
    
    return f"成功从JSON创建了{elements_created}个元素"

# 获取简化版的文档信息
@mcp.tool()
async def get_simplified_document(connection_code: str = None) -> str:
    """获取简化版文档信息
    
    此工具用于获取当前jsdesign文档的简化版信息，只包含节点的基本属性（ID、类型、名称和坐标）。
    
    Args:
        connection_code (str, optional): 连接代码。如果不提供则使用当前连接
        
    Returns:
        str: 包含文档简化信息的字符串
    """
    # 如果未提供connection_code，则使用全局存储的
    code = connection_code or CURRENT_CONNECTION_CODE
    if not code:
        return "错误：未提供连接代码且未连接到任何频道"
    
    data = await make_jsdesign_request(code, "document/simplified")
    if not data or not data.get("success"):
        return f"无法获取简化文档信息: {data.get('error', '未知错误')}"
    return str(data["data"])

def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description='JSDesign MCP Server')
    parser.add_argument('--server', type=str, default="localhost:8080",
                      help='服务器地址，格式为 host:port')
    parser.add_argument('--use-https', action='store_true',
                      help='使用HTTPS协议连接服务器')
    args = parser.parse_args()
    
    # 设置API基础地址
    global JS_DESIGN_API_BASE
    server_host = args.server.split(':')[0].lower()
    is_local = server_host == "localhost" or server_host == "127.0.0.1"
    protocol = "http" if is_local and not args.use_https else "https"
    JS_DESIGN_API_BASE = f"{protocol}://{args.server}/api/connections"
    
    # 运行MCP服务器
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main() 