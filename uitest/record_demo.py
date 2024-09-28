import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    page.locator("#kw").fill("北京")
    page.get_by_role("button", name="百度一下").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="北京市(中华人民共和国首都、... - 百度百科").click()
    page1 = page1_info.value
    with page1.expect_popup() as page2_info:
        page1.get_by_role("link", name="北京市各区示意图").click()
    page2 = page2_info.value
    page2.locator("img").click()
    page2.locator("img").click()
    page2.locator("img").click()
    page2.close()
    with page1.expect_popup() as page3_info:
        page1.get_by_role("link", name="丰台街道").click()
    page3 = page3_info.value
    page3.close()

    # ---------------------
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
