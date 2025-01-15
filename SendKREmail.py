import asyncio
import json
import yaml
from playwright.async_api import async_playwright
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import logging


# 配置日志记录
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('sendEmail.log', mode='a')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


async def singleweburl(url):
    async with async_playwright() as p:
        # 启动浏览器，这里使用 Chromium
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            # 从本地文件读取 cookies 数据
            with open('zblxbf_cookie.json', 'r') as file:
                cookies = json.load(file)['cookies']
            # 添加 cookies 到页面
            await page.context.add_cookies(cookies)
            # 打开网页
            await page.goto(url)
            # 等待页面加载完成
            await page.wait_for_load_state('networkidle')
            # 查找并点击 "点击查看" 按钮
            await page.get_by_role("link", name="点击查看").click()
            # 正确使用 async with 并等待 popup 事件
            async with page.expect_popup() as page2_info:
                await page.get_by_role("link", name="点击进入百度网盘共享文件夹").click()
            # 等待并获取弹出页面
            page2 = await page2_info.value
            # 获取页面标题
            pagetitle = await page.title()
            # 隐藏或替换页面标题中的 "直播录像备份" 文案
            pagetitle = pagetitle.replace('直播录像备份-', '').replace('合集', '')
            videostext = f"[YGQS]{pagetitle}的百度网盘链接:  "
            videourl = page2.url
            logger.info(f"{videostext} {videourl}")
            # print(videostext, videourl)
            return videostext, videourl
        except Exception as e:
            logger.error(f"在处理 {url} 时发生错误: {e}")
        finally:
            try:
                await page.close()  # 关闭页面
            except Exception as e:
                logger.error(f"关闭页面时发生错误: {e}")
            try:
                await browser.close()  # 关闭浏览器
            except Exception as e:
                logger.error(f"关闭浏览器时发生错误: {e}")


async def config_video(labels, receiver_emails, email_config):
    # 读取 zblxbf_config.yml 文件
    with open('zblxbf_config.yml', 'r') as file:
        config = yaml.safe_load(file)
    urls = config.get('urls', [])
    tasks = []
    results = []
    for url_info in urls:
        if url_info.get('label') in labels:
            url = url_info['url']
            tasks.append(singleweburl(url))
    results = await asyncio.gather(*tasks)
    # 处理结果，组合信息
    email_content = "<html><body>"
    for result in results:
        if result:
            videostext, videourl = result
            email_content += f"{videostext}<a href='{videourl}'>立即加入Join</a><br>"
    email_content += f"<p>Send Time: {time.strftime('%Y-%m-%d %H:%M:%S')}</p></body></html>"
    # 发送邮件，配置发送邮件地址
    sender_email = "ygqsmaster@yeah.net"  # 发送邮箱
    sender_password = "VZijknszwkgmF89b"  # SMTP授权码
    logger.info(f'发送邮件的开关：{email_config}')

    if email_config:
        message = MIMEMultipart()
        message['Subject'] = "[YGQS]Video Add Link"  # 邮件发送标题
        message['From'] = sender_email
        message.attach(MIMEText(email_content, 'html'))
        for receiver_email in receiver_emails:
            message['To'] = receiver_email
            try:
                with smtplib.SMTP_SSL('smtp.yeah.net', 465) as server:  # SMTP 服务器地址和端口
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
                logger.info(f"邮件发送给 {receiver_email} 成功")
            except smtplib.SMTPAuthenticationError:
                logger.error(f"邮件发送给 {receiver_email} 时登录失败，请检查用户名和密码")
            except smtplib.SMTPConnectError:
                logger.error(f"邮件发送给 {receiver_email} 时连接失败，请检查网络或 SMTP 服务器地址")
            except Exception as e:
                logger.error(f"邮件发送给 {receiver_email} 失败: {e}")


# 运行异步函数
labels = ["KR10", "KR12", "KR14", "KR16"]  # 可根据需要修改此列表
receiver_emails = ["3935833140@qq.com"]  # 可添加多个接收者邮箱"1131161935@qq.com",
email_config = False  # 可修改为True / False 来关闭邮件发送功能
asyncio.run(config_video(labels, receiver_emails, email_config))