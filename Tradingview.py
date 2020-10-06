import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime 
import time as t
import os
from smtplib import SMTP
#PATH = 'C:\chromedriver.exe'
#driver = webdriver.Chrome(PATH)
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
name = input('Enter stock symbol\n')
driver.get('https://in.tradingview.com/')
search = driver.find_element_by_class_name('tv-header-search__input')
search.send_keys('{}'.format(name))
search.send_keys(Keys.RETURN)
t.sleep(3)
price = []
timeseries = []
while True: 
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    date = now.strftime("%d/%m/%y")
    if time >= '09:15:00' and time < '15:30:00':
        live_price = driver.find_element_by_class_name('tv-symbol-price-quote__value')  
        initial_price = live_price.text
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        price.append(initial_price)
        timeseries.append(time)
        print('Appending initial price at the start')
        while True:
            now = datetime.now()
            time = now.strftime("%H:%M:%S")
            if time == '15:30:00':
                break
            live_price = driver.find_element_by_class_name('tv-symbol-price-quote__value') 
            current_price = live_price.text
            if current_price == initial_price:
                print('Same Price '+current_price)
                t.sleep(1)
                continue
            else:
                print('Appending '+current_price)
                t.sleep(1)
                price.append(current_price)
                timeseries.append(time)
                initial_price = current_price
    else :
        mailserver = smtplib.SMTP('smtp.gmail.com',587)
        # identify ourselves to smtp gmail client
        mailserver.ehlo()
        # secure our email with tls encryption
        mailserver.starttls()
        # re-identify ourselves as an encrypted connection
        mailserver.ehlo()
        mailserver.login('studentgrievance69@gmail.com', 'admin6969')
        from_addr = "studentgrievance69@gmail.com"
        to_addr = "sanayshah2@gmail.com"
        subj = "hello"
        date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )

        message_text = "Hello\nThis is a mail from your server\n\nBye\n"

        msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" 
                % ( from_addr, to_addr, subj, date, message_text )
        mailserver.sendmail(from_addr,to_addr,msg)
        mailserver.quit()
        continue
#df = pd.DataFrame({'Time':timeseries, 'Price':price})
#df.to_csv('{}_{} {}.csv'.format(name, now.strftime('%b'), now.strftime('%d')), index = False)
print('Excel sheet prepared and yet to be mailed')
driver.quit()
