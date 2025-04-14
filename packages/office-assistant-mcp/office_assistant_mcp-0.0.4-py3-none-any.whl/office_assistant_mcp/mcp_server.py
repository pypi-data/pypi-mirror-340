from mcp.server.fastmcp import FastMCP
import random
from office_assistant_mcp import playwright_util
from mcp.server.fastmcp.prompts import base
import os
import re

from office_assistant_mcp.log_util import log_info

mcp = FastMCP("mcp_demo_server", port=8088)


async def server_log_info(msg: str):
    """发送信息级别的日志消息"""
    await mcp.get_context().session.send_log_message(
        level="info",
        data=msg,
    )


@mcp.resource("config://app")
def get_config() -> str:
    """Static configuration data"""
    return "这是应用的全部配置"

#  定义动态 Resource


@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    """Dynamic user data"""
    return f"用户全部信息： {user_id}"


@mcp.tool()
def ask_weather(city: str) -> dict[str, str]:
    """返回指定城市的天气"""
    return {"city": city, "weather": "晴天", "temperature": 25}


@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"


@mcp.tool()
async def open_customer_group_page() -> str:
    """打开客群页面并点击新建客群按钮"""
    try:
        await server_log_info("【T】开始打开客群页面")
        result = await playwright_util.open_customer_group_page()
        return f"客群页面已打开: {result}"
    except Exception as e:
        await server_log_info(f"【E】打开客群页面时出错: {str(e)}")
        return f"打开客群页面时出错: {str(e)}"


@mcp.tool()
async def fill_customer_group_info(group_name: str, business_type: str="活动运营") -> str:
    """填写客群基本信息

    Args:
        group_name: 客群名称
        business_type: 业务类型，可选值：社群运营、用户运营、活动运营、商品运营、内容运营、游戏运营
    """
    try:
        await server_log_info(f"【T】开始填写客群信息: {group_name}, {business_type}")
        result = await playwright_util.fill_customer_group_info(group_name, business_type)
        return f"客群信息填写成功: {result}"
    except Exception as e:
        await server_log_info(f"【E】填写客群信息时出错: {str(e)}")
        return f"填写客群信息时出错: {str(e)}"


@mcp.tool()
async def login_sso() -> str:
    """如果需要授权登录，则使用本工具进行飞书SSO登录"""
    try:
        await server_log_info("【T】开始飞书SSO登录")
        result = await playwright_util.login_sso()
        await server_log_info(f"【T】登录结果: {result}")
        return result
    except Exception as e:
        await server_log_info(f"【E】飞书SSO登录出错: {str(e)}")
        return f"登录过程中出错: {str(e)}"


@mcp.tool()
async def fill_customer_group_user_tag_set_basic_info(
    identity_types: list[str] = None,
    v2_unregistered: str = None
) -> str:
    """新增客群时填写客群用户标签中的基础信息，包括用户身份及是否推客用户。
    
    Args:
        identity_types: 新制度用户身份，可多选，例如 ["P1", "V3"]
                       可选值包括: "P1", "P2", "P3", "P4", "V1", "V2", "V3", "VIP"
                       不区分大小写，如"p1"也会被识别为"P1"
        v2_unregistered: V2以上未注册推客用户，可选值: "是", "否"
    """
    try:
        await server_log_info("【T】开始填写客群用户标签基础信息")
        result = await playwright_util.fill_customer_group_user_tag_set_basic_info(
            identity_types=identity_types,
            v2_unregistered=v2_unregistered
        )
        await server_log_info(f"【T】填写基础信息结果: {result}")
        return result
    except Exception as e:
        await server_log_info(f"【E】填写客群用户标签基础信息时出错: {str(e)}")
        return f"填写基础信息时出错: {str(e)}"


@mcp.tool()
async def add_user_behavior_tag(
    time_range_type: str = "最近",
    time_range_value: str = "7",
    action_type: str = "做过",
    theme: str = "购买", 
    dimension: str = None, 
    dimension_condition: str = None,
    dimension_value: str = None,
    metric: str = None,
    metric_condition: str = None,
    metric_value: str = None,
    metric_value_end: str = None
) -> str:
    """添加用户行为标签

    Args:
        time_range_type: 时间范围类型："最近"或"任意时间"
        time_range_value: 时间范围值，天数，如："7"
        action_type: 行为类型："做过"或"没做过"
        theme: 主题："购买"或"搜索"等
        dimension: 维度选项。当theme="购买"时可用：
            - 类目相关：["后台一级类目", "后台二级类目", "后台三级类目", "后台四级类目"]
              (条件均为=或!=，值为字符串，支持下拉列表多选)
            - 商品相关：["商品品牌", "商品名称", "商品id"] 
              (条件均为=或!=，品牌需从下拉列表选择，其他为字符串)
            - 其他："统计日期"
        dimension_condition: 维度条件：通常为=或!=，部分情况支持"包含"等
        dimension_value: 维度值：根据dimension类型提供相应字符串
        metric: 指标名称。当theme="购买"时可用：
            ["购买金额", "购买件数", "购买净金额", "购买订单数"]
            (所有指标条件均支持=, >=, <=, <, >，值均为数字)
        metric_condition: 指标条件：=, >=, <=, <, >, 介于
        metric_value: 指标值：数字类型，当metric_condition="介于"时为范围开始值
        metric_value_end: 指标范围结束值：仅当metric_condition="介于"时使用
    """
    try:
        await server_log_info(f"【T】开始添加{theme}用户行为标签")
        result = await playwright_util.add_user_behavior_common_tags(
            time_range_type=time_range_type,
            time_range_value=time_range_value,
            action_type=action_type,
            theme=theme,
            dimension=dimension,
            dimension_condition=dimension_condition,
            dimension_value=dimension_value,
            metric=metric,
            metric_condition=metric_condition,
            metric_value=metric_value,
            metric_value_end=metric_value_end
        )
        await server_log_info(f"【T】添加用户行为标签结果: {result}")
        return result
    except Exception as e:
        await server_log_info(f"【E】添加用户行为标签时出错: {str(e)}")
        return f"添加用户行为标签时出错: {str(e)}"


@mcp.tool()
async def get_current_version() -> str:
    """获取当前应用的版本号"""
    try:
        await server_log_info("【T】开始获取版本号")
        # 获取pyproject.toml的路径（相对于当前文件的位置）
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        pyproject_path = os.path.join(current_dir, "pyproject.toml")
        
        # 读取pyproject.toml文件
        with open(pyproject_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 使用正则表达式提取版本号
        version_match = re.search(r'version\s*=\s*"([^"]+)"', content)
        if version_match:
            version = version_match.group(1)
            await server_log_info(f"【T】获取版本号成功: {version}")
            return f"当前版本号: {version}"
        else:
            await server_log_info("【E】未找到版本号")
            return "未找到版本号信息"
    except Exception as e:
        await server_log_info(f"【E】获取版本号时出错: {str(e)}")
        return f"获取版本号时出错: {str(e)}"


def main():
    """MCP服务入口函数"""
    log_info(f"服务启动")
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
