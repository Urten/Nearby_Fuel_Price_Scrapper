from selenium import webdriver

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from crawlers.indian_oil import crawler_indian_oil
import asyncio

options_firefox = FirefoxOptions()
options_chrome = ChromeOptions()

localhost = "http://192.168.1.5:4444"

options_firefox.headless = True
# options_firefox.add_experimental_option("detach", True)
options_firefox.add_argument("--headless")
options_chrome.headless = True

driver1 = webdriver.Remote(command_executor=localhost,
                           options=options_firefox)
# driver2 = webdriver.Remote(command_executor=localhost, options=options_chrome)


def crawl(lat: float | int, lon: float | int):
    """This function will store all the function data"""

    data = {"indian_oil": crawler_indian_oil(lat=lat, lon=lon, driver=driver1)}
    return data


if __name__ == '__main__':
    # async def run():
    #     res = await crawl(26.344146, 92.721522)
    #     print(res)

    # asyncio.run(run())
    print(crawl(26.344146, 92.721522))
