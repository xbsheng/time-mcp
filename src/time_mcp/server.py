"""Time MCP Server - 时间处理 MCP 工具服务."""

from datetime import datetime
from typing import Optional, Union

import pytz
from dateutil.relativedelta import relativedelta
from fastmcp import FastMCP

# 创建 MCP 服务实例
mcp = FastMCP(
    "time-mcp", instructions="时间处理 MCP 工具，提供时间计算、时区转换等功能"
)

# 默认时区
DEFAULT_TIMEZONE = "Asia/Shanghai"


def parse_timestamp(value: Union[str, int, float]) -> datetime:
    """解析时间戳，自动识别秒级或毫秒级.

    Args:
        value: 时间戳值，10位为秒级，13位为毫秒级

    Returns:
        datetime: UTC 时间对象
    """
    if isinstance(value, str):
        value = int(value)

    # 自动识别：13位为毫秒，10位为秒
    if value > 9999999999:  # 毫秒级时间戳
        value = value / 1000

    return datetime.fromtimestamp(value, tz=pytz.UTC)


def parse_time_input(
    time_input: Optional[Union[str, int, float]], timezone: str = DEFAULT_TIMEZONE
) -> datetime:
    """解析时间输入，支持时间戳或日期时间字符串.

    Args:
        time_input: 时间输入，可以是时间戳、日期时间字符串或 None（使用当前时间）
        timezone: 时区

    Returns:
        datetime: 带时区的时间对象
    """
    tz = pytz.timezone(timezone)

    if time_input is None:
        return datetime.now(tz)

    # 尝试解析为时间戳
    if isinstance(time_input, (int, float)):
        dt = parse_timestamp(time_input)
        return dt.astimezone(tz)

    # 尝试解析为时间戳字符串
    if isinstance(time_input, str) and time_input.isdigit():
        dt = parse_timestamp(int(time_input))
        return dt.astimezone(tz)

    # 尝试解析为日期时间字符串
    from dateutil import parser

    try:
        dt = parser.parse(time_input)
        if dt.tzinfo is None:
            dt = tz.localize(dt)
        return dt
    except Exception as e:
        raise ValueError(f"无法解析时间输入: {time_input}, 错误: {e}")


def format_time_result(dt: datetime, timezone: str = DEFAULT_TIMEZONE) -> dict:
    """格式化时间结果为统一的 JSON 结构.

    Args:
        dt: datetime 对象
        timezone: 时区

    Returns:
        dict: 包含多种时间格式的字典
    """
    tz = pytz.timezone(timezone)
    dt_tz = dt.astimezone(tz)

    return {
        "datetime": dt_tz.strftime("%Y-%m-%d %H:%M:%S"),
        "date": dt_tz.strftime("%Y-%m-%d"),
        "time": dt_tz.strftime("%H:%M:%S"),
        "timestamp": int(dt_tz.timestamp()),
        "timestamp_ms": int(dt_tz.timestamp() * 1000),
        "timezone": timezone,
        "iso": dt_tz.isoformat(),
        "weekday": dt_tz.strftime("%A"),
        "weekday_cn": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][
            dt_tz.weekday()
        ],
    }


@mcp.tool()
def get_current_time(
    timezone: str = DEFAULT_TIMEZONE, format: Optional[str] = None
) -> dict:
    """获取当前时间.

    Args:
        timezone: 时区，默认为 Asia/Shanghai（北京时间）
        format: 自定义输出格式，如 "%Y-%m-%d %H:%M:%S"，默认返回多种格式

    Returns:
        dict: 包含当前时间的多种格式
    """
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)

    result = format_time_result(now, timezone)

    if format:
        result["formatted"] = now.strftime(format)

    return result


@mcp.tool()
def time_calculate(
    base_time: Optional[Union[str, int]] = None,
    years: int = 0,
    months: int = 0,
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
    timezone: str = DEFAULT_TIMEZONE,
) -> dict:
    """时间计算，对指定时间进行加减运算.

    Args:
        base_time: 基准时间，支持时间戳（秒/毫秒自动识别）或日期时间字符串，默认为当前时间
        years: 加减年数，正数为加，负数为减
        months: 加减月数，正数为加，负数为减
        days: 加减天数，正数为加，负数为减
        hours: 加减小时数，正数为加，负数为减
        minutes: 加减分钟数，正数为加，负数为减
        seconds: 加减秒数，正数为加，负数为减
        timezone: 时区，默认为 Asia/Shanghai（北京时间）

    Returns:
        dict: 包含计算结果的多种时间格式

    Examples:
        - time_calculate(days=7): 当前时间加7天
        - time_calculate(base_time="2026-01-01", months=-1): 2026-01-01 减1个月
        - time_calculate(base_time=1704067200, hours=8): 时间戳加8小时
    """
    # 解析基准时间
    base_dt = parse_time_input(base_time, timezone)

    # 计算时间差
    delta = relativedelta(
        years=years,
        months=months,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )

    result_dt = base_dt + delta

    # 构建结果
    result = format_time_result(result_dt, timezone)
    result["base_time"] = format_time_result(base_dt, timezone)
    result["operation"] = {
        "years": years,
        "months": months,
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
    }

    return result


@mcp.tool()
def timezone_convert(
    time: Union[str, int], to_tz: str, from_tz: str = DEFAULT_TIMEZONE
) -> dict:
    """时区转换，将时间转换为指定时区.

    Args:
        time: 输入时间，支持时间戳（秒/毫秒自动识别）或日期时间字符串
        to_tz: 目标时区，如 "America/New_York", "Europe/London", "UTC"
        from_tz: 源时区，默认为 Asia/Shanghai（北京时间）

    Returns:
        dict: 包含转换前后时间的多种格式

    Examples:
        - timezone_convert(time="2026-01-12 12:00:00", to_tz="America/New_York")
        - timezone_convert(time=1704067200000, to_tz="UTC")  # 毫秒时间戳
    """
    # 解析源时间
    source_dt = parse_time_input(time, from_tz)

    # 转换到目标时区
    target_tz = pytz.timezone(to_tz)
    target_dt = source_dt.astimezone(target_tz)

    return {
        "source": format_time_result(source_dt, from_tz),
        "target": format_time_result(target_dt, to_tz),
        "from_timezone": from_tz,
        "to_timezone": to_tz,
    }


@mcp.tool()
def list_timezones(region: Optional[str] = None) -> dict:
    """列出可用的时区.

    Args:
        region: 可选，按区域筛选，如 "Asia", "America", "Europe"

    Returns:
        dict: 包含时区列表
    """
    all_timezones = pytz.all_timezones

    if region:
        timezones = [tz for tz in all_timezones if tz.startswith(region)]
    else:
        # 返回常用时区
        common_timezones = [
            "Asia/Shanghai",
            "Asia/Tokyo",
            "Asia/Seoul",
            "Asia/Singapore",
            "Asia/Hong_Kong",
            "America/New_York",
            "America/Los_Angeles",
            "America/Chicago",
            "Europe/London",
            "Europe/Paris",
            "Europe/Berlin",
            "Australia/Sydney",
            "Pacific/Auckland",
            "UTC",
        ]
        timezones = common_timezones

    return {
        "timezones": timezones,
        "count": len(timezones),
        "hint": "使用 region 参数筛选特定区域，如 'Asia', 'America', 'Europe'",
    }


if __name__ == "__main__":
    mcp.run()
