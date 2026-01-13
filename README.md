# Time MCP

一个时间处理的 MCP (Model Context Protocol) 工具，基于 Python + FastMCP 构建。

## 功能特性

| 工具               | 说明                              |
| ------------------ | --------------------------------- |
| `get_current_time` | 获取当前时间                      |
| `time_calculate`   | 时间计算（加减年/月/日/时/分/秒） |
| `timezone_convert` | 时区转换                          |
| `list_timezones`   | 列出可用时区                      |

### 核心特性

- 🕐 默认使用北京时间（Asia/Shanghai）
- 🔢 时间戳自动识别（10 位秒级 / 13 位毫秒级）
- 📅 支持多种时间输入格式
- 🌍 支持全球时区转换

## 安装

### 使用 uv（推荐）

```bash
git clone https://github.com/xbsheng/time-mcp.git
cd time-mcp
uv sync
```

### 使用 pip

```bash
pip install fastmcp python-dateutil pytz
```

## 使用方法

### 启动 MCP 服务

服务默认使用 HTTP 方式运行在 8000 端口：

```bash
uv run python src/server.py
```

启动后，MCP 服务将在 `http://localhost:8000` 上监听。

### 在 Cursor 中配置

在 `~/.cursor/mcp.json` 中添加：

```json
{
  "mcpServers": {
    "time-mcp": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

或者使用命令行方式（无需单独启动服务）：

```json
{
  "mcpServers": {
    "time-mcp": {
      "command": "uv",
      "args": ["--directory", "/path/to/time-mcp", "run", "python", "src/server.py"]
    }
  }
}
```

### 在 Claude Desktop 中配置

在 Claude Desktop 配置文件中添加：

```json
{
  "mcpServers": {
    "time-mcp": {
      "command": "uv",
      "args": ["--directory", "/path/to/time-mcp", "run", "python", "src/server.py"]
    }
  }
}
```

## 工具详细说明

### get_current_time

获取当前时间，返回多种格式。

**参数：**

| 参数       | 类型   | 默认值        | 说明           |
| ---------- | ------ | ------------- | -------------- |
| `timezone` | string | Asia/Shanghai | 时区           |
| `format`   | string | -             | 自定义输出格式 |

**返回示例：**

```json
{
  "datetime": "2026-01-12 22:00:00",
  "date": "2026-01-12",
  "time": "22:00:00",
  "timestamp": 1768226400,
  "timestamp_ms": 1768226400000,
  "timezone": "Asia/Shanghai",
  "iso": "2026-01-12T22:00:00+08:00",
  "weekday": "Monday",
  "weekday_cn": "周一"
}
```

### time_calculate

时间计算，对指定时间进行加减运算。

**参数：**

| 参数        | 类型       | 默认值        | 说明                           |
| ----------- | ---------- | ------------- | ------------------------------ |
| `base_time` | string/int | 当前时间      | 基准时间（时间戳或日期字符串） |
| `years`     | int        | 0             | 加减年数                       |
| `months`    | int        | 0             | 加减月数                       |
| `days`      | int        | 0             | 加减天数                       |
| `hours`     | int        | 0             | 加减小时数                     |
| `minutes`   | int        | 0             | 加减分钟数                     |
| `seconds`   | int        | 0             | 加减秒数                       |
| `timezone`  | string     | Asia/Shanghai | 时区                           |

**使用示例：**

```
# 当前时间加7天
time_calculate(days=7)

# 指定时间减1个月
time_calculate(base_time="2026-01-01", months=-1)

# 时间戳加8小时
time_calculate(base_time=1704067200, hours=8)
```

### timezone_convert

时区转换，将时间转换为指定时区。

**参数：**

| 参数      | 类型       | 默认值        | 说明     |
| --------- | ---------- | ------------- | -------- |
| `time`    | string/int | -             | 输入时间 |
| `from_tz` | string     | Asia/Shanghai | 源时区   |
| `to_tz`   | string     | -             | 目标时区 |

**使用示例：**

```
# 北京时间转纽约时间
timezone_convert(time="2026-01-12 12:00:00", to_tz="America/New_York")
```

### list_timezones

列出可用时区。

**参数：**

| 参数     | 类型   | 默认值 | 说明                                   |
| -------- | ------ | ------ | -------------------------------------- |
| `region` | string | -      | 按区域筛选（如 Asia, America, Europe） |

## 项目结构

```
time-mcp/
├── src/
│   ├── __init__.py
│   └── server.py      # MCP 服务主文件
├── pyproject.toml     # 项目配置
├── uv.lock            # 依赖锁定
├── LICENSE
└── README.md
```

## 技术栈

- Python 3.11+
- [FastMCP](https://github.com/jlowin/fastmcp) >= 2.0.0 - MCP 服务框架
- [python-dateutil](https://github.com/dateutil/dateutil) - 时间解析
- [pytz](https://pythonhosted.org/pytz/) - 时区支持

## 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。
