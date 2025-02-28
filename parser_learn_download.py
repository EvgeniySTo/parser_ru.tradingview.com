import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd


while True:
    category = input(
        '1. G20\n'
        '2. Северная Америка\n'
        '3. Европа\n'
        '4. Ближний Восток / Африка\n'
        '5. Мексика / Южная Америка\n'
        '6. Азия / Тихоокеанский регион\n'
        'Введите номер категории\n'
    )
    chose_list = [1, 2, 3, 4, 5, 6]
    result = int(category)
    if result in chose_list:
        break
print('Идет выгрузка данных....')
with open(f'data/{result-1}.json', encoding='utf-8') as file:
    countries_in_category = json.load(file)
counter = 0
df = None
for key, value in countries_in_category.items():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(6)
    driver.get(value)
    if counter == 0:
        titles = driver.find_elements(By.CSS_SELECTOR, 'span[class="title-eAllN2Yh"]')
        tit_list = []
        for i in titles:
            tit_list.append(i.text)
        df = pd.DataFrame(columns=[
            'Государство',
            tit_list[0],
            tit_list[1],
            tit_list[2],
            tit_list[3],
            tit_list[4],
            tit_list[5]
        ])
    elements = driver.find_elements(
        By.CSS_SELECTOR,
        'span[class="highlight-maJ2WnzA highlight-eAllN2Yh price-qWcO4bp9 price-eAllN2Yh"]'
    )
    params = [key,]
    for i in elements:
        params.append(i.text)
    if len(params) == 7:
        df.loc[counter] = params
    else:
        print(f'Страница с {key} не прогрузилась')
    driver.close()
    counter += 1
df.to_excel(f'{result}.xlsx', index=False)
print('файл сохранен в текущей папке!')
