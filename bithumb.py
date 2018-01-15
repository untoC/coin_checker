from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from termcolor import colored
import time
import re
import os
from datetime import datetime

def do_nothing():
    i = 1

if __name__ == '__main__':
    my_order = [
        {'title': "리플", 'price':2000, 'quantity':100000}
    ]

    chrome_options = Options()
    chrome_options.add_argument('--headless')

    while True:
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get('https://www.bithumb.com')
        try :
            table = driver.find_element_by_id('tableAsset')

            trs = table.find_elements_by_css_selector('tbody tr')

            current = {}
            not_loading = False
            for tr in trs:
                tds = tr.find_elements_by_tag_name('td')
                if len(tds) > 3:
                    current[tds[0].text] = int(re.sub('[\s원,]', '', tds[2].text))
                else:
                    not_loading = True
                    break

            if not_loading:
                driver.quit()
                time.sleep(3)
                continue

            os.system('clear')
            
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            sum = 0
            for order in my_order:
               current_price = current[order['title']] * order['quantity']
               earn = current_price - order['price'] * order['quantity'] 
               sum = sum + earn 
               
               color = 'green'
               if earn < 0 :
                   color = 'red'

               print("%s[%s] : %s"%(order['title'], colored("{:,}".format(current[order['title']]), "yellow"), colored("{:,}".format(int(earn)), color))) 
               
            color = 'green' 
            if sum < 0 : 
                color = 'red' 
                
            print("total : %s"%(colored("{:,}".format(int(sum)), color)))

        except:
            do_nothing()

        driver.quit()
        time.sleep(3)

