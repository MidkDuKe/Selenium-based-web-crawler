import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设置Edge选项
edge_options = Options()
# 设置Edge服务
service = Service('edgedriver_win64/msedgedriver.exe')  # 替换为msedgedriver.exe的实际路径
# 创建浏览器对象
driver = webdriver.Edge(service=service, options=edge_options)
# 访问网页
driver.get('https://movie.douban.com/explore/')
# 获取电视剧列表元素
# 使用显式等待来等待<ul class="explore-list">下的第一个<li>元素变得可见

wait = WebDriverWait(driver, 10)  # 设置等待时间为10秒
region_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "地区")]')))
region_button.click()

chinese_option = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="app"]/div/div[1]/div/div[1]/div[2]/div/div[2]/div/div/ul/li[2]/span')))
chinese_option.click()
try:
    item_count = 0
    max_items_per_click = 20
    total_count = 0
    for _ in range(3):
        time.sleep(2)
        try:
            load_more_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/div/div[2]/div/button'))
            )
            load_more_button.click()
        except:
            break
    # 等待页面上所有可见的 <li> 元素（或根据您的需求调整）
    lis = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="app"]/div/div[2]/ul/li'))
                     )
    # 遍历当前页面上的 <li> 元素
    parsed_data = []
    for li in lis:
        # 提取和处理数据（例如，打印文本）
        data = li.text.strip()
        dataN=data.split('\n')
        name = dataN[0]
        info_str = dataN[1]
        rate = dataN[2]
        # 分割info_str来获取type, director, actor
        parts = info_str.split('/')
        year=parts[0].strip()
        type_ = parts[2].strip()  # 获取类型
        director = parts[3].strip()  # 获取导演
        try:
            actors = parts[4].strip()  # 获取演员列表（可能有多位）
        except:
            actors = ''
        # 构建字典并添加到parsed_data列表中
        parsed_item = {
            'name': name,
            'year':year,
            'type': type_,
            'director': director,
            'actor': actors,
            'rate': rate
        }
        parsed_data.append(parsed_item)
    df = pd.DataFrame(parsed_data)

    # 将DataFrame保存到Excel文件
    df.to_excel('result.xlsx', index=False)
finally:
    driver.quit()
