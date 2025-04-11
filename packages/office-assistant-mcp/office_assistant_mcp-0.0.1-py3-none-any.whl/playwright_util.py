import os
from playwright.async_api import async_playwright, Locator, Frame, Page, expect
import re

from log_util import log_debug, log_info, log_error

# 浏览器路径
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# 浏览器用户数据目录
CHROME_USER_DATA_DIR = "/Users/kamous/Library/Application Support/Google/Chrome/playwright1"

# 全局变量用于缓存playwright实例
_playwright_instance = None
_browser_instance = None
_page_instance = None

async def reset_playwright_cache():
    log_info("reset playwright cache")
    global _playwright_instance, _browser_instance, _page_instance
    _playwright_instance = None
    _browser_instance = None
    _page_instance = None


async def create_playwright():
    await remove_lock_files()
    p = await async_playwright().start()
    browser = await p.chromium.launch_persistent_context(
        user_data_dir=CHROME_USER_DATA_DIR,
        executable_path=CHROME_PATH,
        headless=False,  # 显示浏览器界面
        args=['--start-maximized']  # 浏览器最大化启动（可选）
    )
    return p, browser


async def get_playwright():
    """获取playwright对象,如果没有则新建，有则返回全局缓存的对象"""
    global _playwright_instance, _browser_instance, _page_instance

    if _playwright_instance is None or _browser_instance is None:
        log_debug(f"create playwright")
        _playwright_instance, _browser_instance = await create_playwright()
        _page_instance = await _browser_instance.new_page()
    return _playwright_instance, _browser_instance, _page_instance


async def close_playwright():
    """关闭并清除缓存的playwright和browser实例"""
    log_debug(f"close playwright")
    global _playwright_instance, _browser_instance, _page_instance

    if _browser_instance:
        await _browser_instance.close()
        _browser_instance = None

    if _playwright_instance:
        await _playwright_instance.stop()
        _playwright_instance = None

    _page_instance = None
    
async def remove_lock_files():
    """删除浏览器用户数据目录下的锁文件，防止浏览器打不开"""
    lock_files_to_remove = ["SingletonLock", "SingletonCookie", "SingletonSocket"]
    if os.path.exists(CHROME_USER_DATA_DIR):
        for file_name in lock_files_to_remove:
            file_path = os.path.join(CHROME_USER_DATA_DIR, file_name)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    log_info(f"Successfully removed lock file: {file_path}")
                except OSError as e:
                    log_info(f"Error removing lock file {file_path}: {e}")
            # No need to log if file doesn't exist during cleanup
    else:
        log_info(f"User data directory not found, skipping lock file cleanup: {CHROME_USER_DATA_DIR}")



async def login_sso():
    """处理飞书SSO登录流程"""
    _, _, page = await get_playwright()

    # 检查页面是否包含"飞书登录"文本
    # 打印当前页面url
    log_info(f"当前页面url:{page.url}")
    if "sso.yunjiglobal.com/?backUrl=" in page.url:
        # 点击飞书登录按钮
        await page.get_by_text("飞书登录").click()
        log_info(f"等待飞书授权登录")
        # 等待"授权"按钮出现
        try:
            await page.wait_for_selector('button:has-text("授权")', timeout=30000)
            # 点击授权按钮
            log_debug("点击授权")
            await page.get_by_role("button", name="授权", exact=True).click()
            log_debug("登录成功")
            return "登录成功"
        except Exception as e:
            log_error(f"等待授权按钮出现时发生错误: {e}")
            return "登录失败"
    else:
        # 页面不包含"飞书登录"文本，无需登录
        log_info(f"无需登录")
        return "无需登录"


async def open_customer_group_page():
    """打开客群列表页面并点击新建客群按钮"""
    _, _, page = await get_playwright()

    open_url = "https://portrait.yunjiglobal.com/customersystem/customerList?identify=cgs-cgm-customerList&d=1744176806057"
    # 打开客群列表页面
    await page.goto(open_url)

    login_result = await login_sso()
    if login_result == "登录成功":
        # 等待两秒
        await asyncio.sleep(2)
        log_debug(f"重新打开页面")
        await page.goto(open_url)

    log_debug(f"开始新建客群")
    content = page.frame_locator("iframe")
    await content.get_by_role("button", name="新建客群").click()
    # await page.pause()

    return "已进入新建客群页面"


async def fill_customer_group_info(group_name: str, business_type: str):
    """填写客群基本信息

    Args:
        group_name: 客群名称
        business_type: 业务类型
    """
    _, _, page = await get_playwright()
    content = page.frame_locator("iframe")

    # 填写客群名称
    await content.get_by_role("textbox", name="请输入字母、数字、下划线和汉字格式的客群名称，最多20字").click()
    await content.get_by_role("textbox", name="请输入字母、数字、下划线和汉字格式的客群名称，最多20字").fill(group_name)

    # 选择业务类型
    await content.get_by_role("textbox", name="请选择").click()
    await content.get_by_text(business_type).click()

    # 选择动态客群
    await content.get_by_role("radio", name="动态客群（每日0点重新按照筛选条件更新客群用户）").click()

    # 点击预估客群人数
    await content.get_by_role("button", name="点我预估客群人数").click()

    return f"已填写客群基本信息：名称={group_name}，业务类型={business_type}"


async def print_iframe_snapshot(page):
    iframe = page.frame_locator("iframe")
    body = iframe.locator('body')
    snapshot = await body.aria_snapshot()
    log_debug(f"snapshot:{snapshot}")

    # log_debug(f"page accessibility:{await page.accessibility.snapshot()}")


async def fill_customer_group_user_tag_set_basic_info():
    """
    新增客群，填写"用户标签"下的"基础信息"
    :return:
    """
    _, _, page1 = await get_playwright()
    content = page1.frame_locator("iframe")
    log_debug(f"start set basic info:{content}")
    snapshot = await page1.locator('body').aria_snapshot()
    # log_debug(f"snapshot:{snapshot}")
    # iframe_locator = page1.locator("iframe")
    # # 获取 iframe 的 frame 对象
    # content_snapshot = await iframe_locator.aria_snapshot()
    await print_iframe_snapshot(page1)

    await content.get_by_role("tab", name="基础信息").click()
    await content.get_by_role("tab", name="基础信息").click()
    await content.get_by_role("tab", name="云集属性").click()
    await content.locator("label").filter(has_text="～59天").locator("span").nth(1).click()
    await content.locator("label").filter(has_text="正常渠道").locator("span").nth(1).click()
    await content.locator("label").filter(has_text="H5基础场景").locator("span").nth(1).click()
    await content.locator("label").filter(has_text="0~100").locator("span").nth(1).click()
    await content.locator("label").filter(has_text="他购型").locator("span").nth(1).click()

    # await content.get_by_label("云集属性").get_by_text("否", exact=True).first.click()
    # await content.locator(':text("否"):right-of(:text("是否优质会员"))').click()
    # await content.locator('.form-item:has-text("是否优质会员")').get_by_text("否", exact=True).click()
    # 这个 XPath 尝试匹配更具体的结构：
    # 找到一个 div，它下面直接有 label/span/button...结构包含"是否优质会员"
    # 然后从这个 div 出发，找到嵌套路径下的 label[2]/span 且文本为"否"
    specific_xpath = '//div[label/span/button/span/span[contains(text(), "是否优质会员")]]/div/div/label[2]/span[contains(text(), "否")]'

    # 或者，更精确匹配文本 (如果 "是否优质会员" 和 "否" 文本是完全匹配的)
    specific_xpath_exact = '//div[label/span/button/span/span[text()="是否优质会员"]]/div/div/label[2]/span[text()="否"]'

    # 使用这个更精确的 XPath
    # await content.locator(f'xpath={specific_xpath_exact}').click()  # 推荐使用 exact text 匹配

    await content.get_by_text("正常", exact=True).click()
    await content.get_by_label("云集属性").get_by_text("否", exact=True).nth(1).click()
    await content.get_by_label("云集属性").get_by_text("0", exact=True).click()
    await content.get_by_label("云集属性").get_by_text("否", exact=True).nth(2).click()
    await content.get_by_text("普通店主").click()
    await content.get_by_label("云集属性").get_by_text("否", exact=True).nth(3).click()
    await content.get_by_text("P1").click()
    await content.get_by_label("云集属性").get_by_text("否", exact=True).nth(4).click()
    await content.get_by_label("云集属性").get_by_text("-7").click()

    return "已完成用户标签基础信息填写"


async def add_user_behavior_search_tags_old():
    """添加一个搜索主题的用户行为标签"""
    _, _, page = await get_playwright()
    content = page.frame_locator("iframe")
    await page.pause()
    # await print_iframe_snapshot(page)

    # 添加第一个行为标签
    await content.get_by_role("button", name=" 添加").click()

    # 填写第一个过滤条件，过滤条件均位于sql-item的div内
    row_class_name = ".sql-item"

    item_count = await content.locator(row_class_name).count()
    log_debug(f"当前sql-item元素数量: {item_count}")

    item = content.locator(row_class_name).nth(item_count - 1)
    log_debug(f"textbox的数量:{await item.locator('textbox').count()}")

    await item.locator(".el-select__caret").first.click()  #
    await content.get_by_role("listitem").filter(has_text="最近").click()

    await item.get_by_role("textbox", name="天数").last.fill("10")

    await item.get_by_role("textbox", name="请选择").nth(0).click()
    await content.get_by_role("listitem").filter(has_text="没做过").click()

    await item.get_by_role("textbox", name="选择主题").last.click()
    await content.get_by_role("listitem").filter(has_text="搜索").click()

    await item.get_by_role("textbox", name="选择维度").last.click()
    await content.get_by_role("listitem").filter(has_text=re.compile(r"^搜索词$")).click()

    await item.get_by_role("textbox", name="请选择").nth(1).click()  # 包含，大小于
    await content.get_by_role("listitem").filter(has_text=re.compile(r"^包含$")).click()

    await item.get_by_role("textbox", name="请输入").nth(0).click()
    await item.get_by_role("textbox", name="请输入").nth(0).wait_for(state="visible", timeout=500)
    await item.get_by_role("textbox", name="请输入").nth(0).fill("轻姿养")

    await item.get_by_role("textbox", name="选择指标").click()
    await content.get_by_role("listitem").filter(has_text=re.compile(r"^搜索次数$")).click()

    await item.get_by_role("textbox", name="请选择").nth(2).click()
    await content.get_by_role("listitem").filter(has_text=">=").click()

    # # 添加第二个行为标签（购买行为）
    # await content.locator(".add-icon > .el-icon-circle-plus").click()
    # await content.locator("div:nth-child(2) > div > .sql-row > div >
    # .el-input > .el-input__suffix > .el-input__suffix-inner >
    # .el-select__caret").first.click()  # 右侧添加按钮

    return "已添加用户行为标签"


async def add_user_behavior_search_tags_test():
    """添加一个搜索主题的用户行为标签"""
    return await add_user_behavior_common_tags(
        time_range_type="最近",
        time_range_value="10",
        action_type="没做过",
        theme="搜索",
        dimension="搜索词",
        dimension_condition="包含",
        dimension_value="轻姿养",
        metric="搜索次数",
        metric_condition=">=",
        metric_value="1"
    )


async def add_user_behavior_common_tags(
    time_range_type: str = "最近",
    time_range_value: str = "7",
    action_type: str = "做过",
    theme: str = "购买", 
    dimension: str = None, 
    dimension_condition: str = None,
    dimension_value: str = None,
    metric: str = None,
    metric_condition: str = None,
    metric_value: str = None 
):
    """添加一个通用的用户行为标签

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
        metric_condition: 指标条件：=, >=, <=, <, >
        metric_value: 指标值：数字类型
    """
    _, _, page = await get_playwright()
    content = page.frame_locator("iframe")

    # 添加新的行为标签
    await content.get_by_role("button", name=" 添加").click()

    # 定位最新添加的行
    row_class_name = ".sql-item"
    item_count = await content.locator(row_class_name).count()
    item = content.locator(row_class_name).nth(item_count - 1)

    # 选择时间范围类型
    await item.locator(".el-select__caret").first.click()
    await content.get_by_role("listitem").filter(has_text=time_range_type).click()

    # 填写时间范围值
    await item.get_by_role("textbox", name="天数").last.fill(time_range_value)

    # 选择行为类型（做过/没做过）
    await item.get_by_role("textbox", name="请选择").nth(0).click()
    await content.get_by_role("listitem").filter(has_text=re.compile(f"^{action_type}$")).click()

    # 选择主题
    await item.get_by_role("textbox", name="选择主题").last.click()
    await content.get_by_role("listitem").filter(has_text=theme).click()

    # 根据是否有维度来确定指标的位置
    textbox_index = 1  # 初始值，用于追踪当前到了第几个"请选择"框
    input_index = 0    # 初始值，用于追踪当前到了第几个"请输入"框

    # 设置维度（如果有）
    if dimension:
        # 选择维度
        await item.get_by_role("textbox", name="选择维度").last.click()
        await content.get_by_role("listitem").filter(has_text=re.compile(f"^{dimension}$")).click()

        # 设置维度条件
        if dimension_condition:
            await item.get_by_role("textbox", name="请选择").nth(textbox_index).click()
            await content.get_by_role("listitem").filter(has_text=re.compile(f"^{dimension_condition}$")).click()
            textbox_index += 1

            # 填写维度值
            if dimension_value:
                await item.get_by_role("textbox", name="请输入").nth(input_index).click()
                await item.get_by_role("textbox", name="请输入").nth(input_index).fill(dimension_value)
                input_index += 1

    # 设置指标（如果有）
    if metric:
        # 如果没有选择维度，则从维度选项框里选择指标
        metric_title = "选择指标"
        if not dimension:
            metric_title = "选择维度"
        
        await item.get_by_role("textbox", name=metric_title).click()
        await content.get_by_role("listitem").filter(has_text=re.compile(f"^{metric}$")).click()

        # 设置指标条件
        if metric_condition:
            await item.get_by_role("textbox", name="请选择").nth(textbox_index).click()
            await content.get_by_role("listitem").filter(has_text=re.compile(f"^{metric_condition}$")).click()

            # 填写指标值
            if metric_value:
                await item.get_by_role("textbox", name="请输入").nth(input_index).click()
                await item.get_by_role("textbox", name="请输入").nth(input_index).fill(metric_value)

    return f"已添加{theme}用户行为标签"


async def add_user_behavior_purchase_tags_test():
    """添加一个购买主题的用户行为标签"""
    return await add_user_behavior_common_tags(
        time_range_type="最近",
        time_range_value="10",
        action_type="做过",
        theme="购买",
        dimension="商品id",
        dimension_condition="=",
        dimension_value="123",
        metric="购买件数", # 购买件数
        metric_condition=">=",
        metric_value="1"
    )


async def add_user_behavior_purchase_tags_no_dimension_test():
    """添加一个购买主题的用户行为标签"""
    return await add_user_behavior_common_tags(
        time_range_type="最近",
        time_range_value="10",
        action_type="做过",
        theme="购买",
        # dimension=None,
        # dimension_condition=None,
        # dimension_value=None,
        metric="购买金额",
        metric_condition=">",
        metric_value="100"
    )


async def start_test():
    await open_customer_group_page()
    # await asyncio.sleep(10)
    # await fill_customer_group_info("测试客群1", "用户运营")
    # await fill_customer_group_user_tag_set_basic_info()
    # await add_user_behavior_search_tags_test()
    # await add_user_behavior_purchase_tags_test()
    await add_user_behavior_purchase_tags_no_dimension_test()


if __name__ == "__main__":
    import asyncio
    asyncio.run(start_test())
    import time
    while True:
        pass
        time.sleep(1)
