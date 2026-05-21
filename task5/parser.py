from playwright.sync_api import sync_playwright


def parse_site(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        page = browser.new_page()
        page.goto(url, timeout=60000)
        
        results = []
        page_num = 1
        while True:
            page_num += 1
            elements = page.query_selector_all(".col-xs-6.col-sm-4.col-md-4.col-lg-3.unproduct-item.js-item")
            for element in elements:
                print(page_num)
                item = {}
                title_element = element.query_selector("[title]")
                item['title'] = title_element.get_attribute("title") if title_element else "No title"
                
                price_element = element.query_selector(".price")
                item['price'] = price_element.inner_text() if price_element else "No info"
                
                old_price_element = element.query_selector(".old-price")
                item['old_price'] = old_price_element.inner_text() if old_price_element else "No info"
                
                credit_info_element = element.query_selector(".credit-ttl-section")
                item['credit_info'] = credit_info_element.inner_text() if credit_info_element else "No info"
                
                results.append(item)

            next_button = page.query_selector(".bx-pag-next")
            if next_button:
                span = next_button.query_selector("span")
                if span and "disabled" in (span.get_attribute("class") or ""):
                    break
                page.goto('https://www.podkablukom.ru/catalog1c/men-botinki/?PAGEN_1=' + str(page_num), timeout=60000)
            else:
                break
        
        browser.close()
        return {"items": results}