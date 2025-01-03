import re
import os
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from ..custom_downloader_middleware import CustomDownloaderMiddleware
from ..js_executor import JsExecutor


class BrowserHandler:
    @staticmethod
    def conf_need_browser(config_original_content, js_render):
        group_regex = re.compile(r'\(\?P<(.+?)>.+?\)')
        results = re.findall(group_regex, config_original_content)

        return len(results) > 0 or js_render

    @staticmethod
    def init(config_original_content, js_render, user_agent):
        driver = None

        if BrowserHandler.conf_need_browser(config_original_content,
                                            js_render):
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('user-agent={0}'.format(user_agent))
            chrome_options.add_argument('--ignore-certificate-errors')  # SSL 인증서 오류 무시
            chrome_options.add_argument('--disable-web-security')       # 웹 보안 비활성화
            chrome_options.add_argument('--allow-insecure-localhost')   # 로컬 호스트 SSL 인증서 무시

            CHROMIUMDRIVER_PATH = os.environ.get('CHROMIUMDRIVER_PATH', "/usr/bin/chromedriver")

            if os.path.isfile(CHROMIUMDRIVER_PATH):
                webdriver_service = Service(executable_path=CHROMIUMDRIVER_PATH)
                driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
            else:
                webdriver_service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

            CustomDownloaderMiddleware.driver = driver
            JsExecutor.driver = driver
        return driver

    @staticmethod
    def destroy(driver):
        # Start browser if needed
        if driver is not None:
            driver.quit()
            driver = None

        return driver
