import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import time
import json
from datetime import datetime
from collections import defaultdict

# ARGS (optional): takes the url of the livetiming, number of queries, and the time between queries (seconds)
url = 'https://livetiming.alkamelsystems.com/imsa'# sys.argv[1] if (len(sys.argv) > 1) else 'https://livetiming.alkamelsystems.com/lcsc'
max_hits = 1#int(sys.argv[2]) if (len(sys.argv) > 2) else 3
interval = 1#int(sys.argv[3]) if (len(sys.argv) > 3) else 5

chromedriver_path = '../chromedriver'

options = webdriver.ChromeOptions()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)


driver.delete_all_cookies()
driver.implicitly_wait(10)

driver.get(url)
driver.refresh()

driver.find_element_by_css_selector('#accept').click()
pit_times = defaultdict(list)
driver_pit_num = defaultdict(int)
start_time = '1:40:00'
FMT1 = '%H:%M:%S'
FMT2 = '%M:%S'
# test_time = '2:15:00'
# test_times = []

# test_times.append(str(datetime.strptime(start_time, FMT) - datetime.strptime(test_time, FMT)))
# print(test_times)
while True:
    
    table_sample = []
    for ele in driver.find_elements_by_xpath("//table/tbody/tr"):
        row = [field.text for field in ele.find_elements_by_css_selector("*") if field.text]
        table_sample.append(row)

    current_time = driver.find_element_by_class_name('hour-title').text
    
    for t in table_sample:
        if driver_pit_num[t[2]] != t[-1]:
#             if(t[-1]!= '0'):
            pit_times[t[2]].append((datetime.strptime(start_time, FMT1) - datetime.strptime(current_time, FMT1 if len(current_time) > 5 else FMT2)).total_seconds())
            driver_pit_num[t[2]] = t[-1]

            
    for k in driver_pit_num:
        if driver_pit_num[k] == '0':
            pit_times[k] = [0]
        
    
    
    
    
    temp = {0: (datetime.strptime(start_time, FMT1) - datetime.strptime(current_time, FMT1 if len(current_time) > 5 else FMT2)).total_seconds()}
    with open('current_time.json', 'w') as fp:
        json.dump(dict(temp), fp)
    fp.close()
    with open('result.json', 'w') as fp:
        json.dump(dict(pit_times), fp)
    fp.close()
    print('pass')
    time.sleep(interval)

# print(weather_samples)
# print(current_time)
# print(driver_pit_num)
# print(pit_times)
driver.quit()