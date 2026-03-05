import csv

from selenium import webdriver
from selenium.webdriver.common.by import By


FILENAME = "data.csv"
driver = webdriver.Firefox()
driver.get('https://www.podkablukom.ru/catalog1c/men-botinki/')

with open(FILENAME, "w", newline="") as file:
    writer = csv.writer(file)
    while True:
        elements = driver.find_elements(By.CSS_SELECTOR, ".col-xs-6.col-sm-4.col-md-4.col-lg-3.unproduct-item.js-item")
        for element in elements:
            title_element = element.find_element(By.CSS_SELECTOR, "[title]")
            title = title_element.get_attribute("title")
            try:
                price_element = element.find_element(By.CLASS_NAME, "price")
                price = price_element.text
            except:
                price = "No info"
            try:
                old_price_element = element.find_element(By.CLASS_NAME, "old-price")
                old_price = old_price_element.text
            except:
                old_price = "No info"
            try:
                credit_info_element = element.find_element(By.CLASS_NAME, "credit-ttl-section")
                credit_info = credit_info_element.text
            except:
                credit_info = "No info"
            data = [title, price, old_price, credit_info]
            writer.writerow(data)
        try:
            button = driver.find_element(By.CLASS_NAME, "bx-pag-next")
        except:
            print("Кнопка не найдена")
            break
        span = button.find_element(By.TAG_NAME, "span")
        if(span.get_attribute("class") == "btn disabled"):
            print("Конец")
            break
        else:
            driver.execute_script("arguments[0].scrollIntoView();", button)
            driver.find_element(By.CLASS_NAME, "bx-pag-next").click()
driver.close()
