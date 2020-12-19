import csv
from selenium import webdriver
from bs4 import BeautifulSoup


def get_url(search_text):
    """Generate a url from search text"""
    template = 'https://www.sastodeal.com/catalogsearch/result/?q={}'
    search_term = search_text.replace(' ', '')

   # add term query to url
    url = template.format(search_term)
    
    # add page query placeholder
    # url += '/index/?p={}&q={}'
        
    return url

def extract_record(product):
    """Extract and return data from a single product"""
    parent_class = product.find('div', 'product details product-item-details')

    title = parent_class.a.text.strip()
    # print(title)
    
    try:
        old_price = parent_class.find('span', 'price').text.strip()
        # print(old_price)
    except AttributeError:
        old_price = 'NA'

    try:
        new_price = parent_class.find('span', 'special-price pricenew').text.strip()
        # print(new_price)
    except AttributeError:
        new_price = 'NA'

    try:
        discount = parent_class.find('span', 'disPrice').text.strip()
        # print(discount)
    except AttributeError:
        discount = 'NA'

    product_url = parent_class.a.get('href')
    # print(product_url)

    result = (title, old_price, discount, new_price, product_url)
    return result


def main(search_term):
    """Run main program"""

    # startup the webdriver
    driver = webdriver.Chrome('./chromedriver')

    records = []
    url = get_url(search_term)

    # looping through multiple pages.
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    products = soup.find_all('li', 'item product product-item')
    for product in products:
        record = extract_record(product)
        if record:
            records.append(record)
    
    driver.close()

    # Savimg extracted data to a csv file
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Old Price', 'Discount', 'New Price', 'URL'])
        writer.writerows(records)

# Run the main program
main('heater')