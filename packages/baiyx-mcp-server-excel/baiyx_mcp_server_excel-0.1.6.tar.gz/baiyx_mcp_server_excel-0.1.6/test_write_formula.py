from mcp_server_excel.server import ExcelServer

def test_write_formula():
    server = ExcelServer()
    
    # 测试参数
    params = {
        "file_path": "/Users/baiyx/Desktop/MCP.xlsx",
        "sheet_name": "Sheet1",
        "range": "E2",
        "formulas": [
            "=SUM(C2:D2)"
        ]
    }
    
    try:
        # 获取工具函数
        write_sheet_formula = server._tools.get("write_sheet_formula")
        if write_sheet_formula:
            result = write_sheet_formula(**params)
            print(f"写入公式成功: {result}")
        else:
            print("工具函数未找到")
    except Exception as e:
        print(f"写入公式失败: {str(e)}")

if __name__ == "__main__":
    test_write_formula() 