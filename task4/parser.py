from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def parse_site(url):
    driver = webdriver.Chrome()
    driver.get(url)
    results = []
    while True:
        elements = driver.find_elements(By.CSS_SELECTOR, ".col-xs-6.col-sm-4.col-md-4.col-lg-3.unproduct-item.js-item")
        for element in elements:
            item = {}
            item['title'] = element.find_element(By.CSS_SELECTOR, "[title]").get_attribute("title")
            try:
                item['price'] = element.find_element(By.CLASS_NAME, "price").text
            except NoSuchElementException:
                item['price'] = "No info"
            try:
                item['old_price'] = element.find_element(By.CLASS_NAME, "old-price").text
            except NoSuchElementException:
                item['old_price'] = "No info"
            try:
                item['credit_info'] = element.find_element(By.CLASS_NAME, "credit-ttl-section").text
            except NoSuchElementException:
                item['credit_info'] = "No info"
            
            results.append(item)
        try:
            button = driver.find_element(By.CLASS_NAME, "bx-pag-next")
            span = button.find_element(By.TAG_NAME, "span")
            
            if span.get_attribute("class") == "btn disabled":
                break
            else:
                driver.execute_script("arguments[0].scrollIntoView();", button)
                driver.find_element(By.CLASS_NAME, "bx-pag-next").click()
        except NoSuchElementException:
            break
    driver.quit()
    return {"items": results}
