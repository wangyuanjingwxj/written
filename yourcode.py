import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_forex_rate(date, currency):
    # 设置 Chrome 选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口
    service = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")  # 请替换为您的 ChromeDriver 路径
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 打开中国银行外汇牌价网站
        driver.get('https://www.boc.cn/sourcedb/whpj/')

        # 等待页面加载
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'pjbjTable')))

        # 输入日期
        date_input = driver.find_element(By.ID, 'erectDate')
        date_input.clear()
        date_input.send_keys(date)

        # 选择货币
        currency_select = driver.find_element(By.NAME, 'pjname')
        currency_select.send_keys(currency)

        # 点击查询按钮
        driver.find_element(By.CLASS_NAME, 'search').click()

        # 等待查询结果加载
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'pjbjTable')))

        # 获取现汇卖出价
        forex_rate = driver.find_element(By.XPATH, '//table[@id="pjbjTable"]//tr[2]/td[5]').text

        # 将结果写入文件
        with open('result.txt', 'w') as f:
            f.write(driver.page_source)

        return forex_rate

    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.quit()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 yourcode.py <date> <currency>")
        sys.exit(1)

    date = sys.argv[1]
    currency = sys.argv[2]

    forex_rate = get_forex_rate(date, currency)
    if forex_rate:
        print(f"The forex rate on {date} for {currency} is: {forex_rate}")
