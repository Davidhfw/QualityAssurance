import re

import allure
import pytest
from playwright.sync_api import sync_playwright, expect


# 定义浏览器 fixture，将其作为每个测试用例执行前和执行后的公共步骤
@allure.step("打开退出浏览器")
@pytest.fixture()
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


@allure.epic("UI测试项目-百度百科")
@allure.severity("P0")
@allure.feature("搜索")
@allure.testcase("用例链接")
@allure.issue("缺陷管理平台链接")
class TestBaike:
    @allure.step("搜索测试")
    @pytest.mark.parametrize("city", ["北京", "上海", "天津", "重庆"])
    def test_city_search(self, browser, city):
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.baidu.com/")
        page.wait_for_timeout(5000)
        page.locator("#kw").fill(city)
        page.get_by_role("button", name="百度一下").click()

        context.close()

    @allure.step("测试Playwright标题")
    def test_has_title(self, browser):
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://playwright.dev/")

        # Expect a title "to contain" a substring.
        expect(page).to_have_title(re.compile("Playwright"))

    @allure.step("测试Playwright开始链接")
    def test_get_started_link(self, browser):
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://playwright.dev/")
        # Click the get started link.
        page.get_by_role("link", name="Get started").click()

        # Expects page to have a heading with the name of Installation.
        expect(page.get_by_role("heading", name="Installation")).to_be_visible()


if __name__ == "__main__":
    pytest.main(["--alluredir", "allure-result"])
