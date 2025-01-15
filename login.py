import time
from playwright.sync_api import Playwright, sync_playwright, expect
"""
@2024年12月09日14:31:24
@获取cookie 写 cookie.json
@2025年01月14日14:12:45 换域名

"""
def fill_user_pwd(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://zblxbf.com/?login")
    page.get_by_placeholder("用户名").fill("dx875419982")
    page.get_by_placeholder("密码").fill("dx875419982")
    page.get_by_placeholder("输入验证码").click()
    time.sleep(10)
    # page.get_by_placeholder("输入验证码").fill("93229")# OCR
    page.get_by_role("button", name="登 录").click()

    time.sleep(200)
    storage_state = context.storage_state(path='./zblxbf_cookie.jsonn')
    # cookie_dict = {}
    # for item in cookies:
    #     cookie_dict[item['name']] = item['value']

    # print(storage_state)
    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    fill_user_pwd(playwright)
