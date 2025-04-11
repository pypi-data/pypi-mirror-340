# Xiyan Table MCP Server

这是一个基于 MCP (Model Control Protocol) 的表格数据查询服务器。它允许用户配置本地表格数据，并通过自然语言进行查询。

## 功能特点

- 支持本地 CSV 文件的配置和读取
- 提供表格数据的预览功能（前20行）
- 支持自然语言查询
- 基于大语言模型的智能解答
- 使用 YAML 进行灵活配置
- 简单易用的 MCP 工具和资源

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/xiyan-table-mcp-server.git
cd xiyan-table-mcp-server
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置

1. 复制配置文件模板：
```bash
cp config.yml.example config.yml
```

2. 编辑 `config.yml` 文件：
```yaml
table:
  path: "data/example.csv"  # CSV文件路径
  encoding: "utf-8"         # 文件编码
  preview_rows: 20          # 预览行数

model:
  type: "openai"           # 模型类型
  api_key: ""             # API密钥
  model_name: "gpt-4"     # 模型名称
  temperature: 0.1        # 温度参数

server:
  name: "xiyan-table"     # 服务名称
  version: "0.1.0"        # 版本号
```

## 使用方法

1. 启动服务器：
```bash
python server.py
```

2. 使用 MCP 客户端连接服务器：
```python
from mcp.client import MCPClient

# 连接服务器
client = MCPClient()

# 获取表格预览
preview = client.get_table_preview()
print(f"表格列名：{preview['columns']}")
print(f"预览行数：{preview['preview_rows']}")

# 查询数据
result = client.query_table("表格中总共有多少行数据？")
print(f"查询结果：{result}")
```

## API 说明

### 资源

#### get_table_preview
获取表格数据预览。

返回格式：
```python
{
    "columns": List[str],        # 列名
    "data": List[List[Any]],     # 表格数据
    "total_rows": int,           # 总行数
    "preview_rows": int          # 预览行数
}
```

### 工具

#### query_table
使用自然语言查询表格。

参数：
- `question` (str)：自然语言查询问题

返回：
- 包含查询答案的字符串

## 开发

### 环境要求
- Python 3.8+
- pandas
- pyyaml
- openai
- mcp-core

### 项目结构
```
xiyan-table-mcp-server/
├── config.yml          # 配置文件
├── server.py          # 主服务器实现
├── requirements.txt   # 项目依赖
└── README.md         # 文档
```

## 许可证

MIT License

## 贡献

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request 