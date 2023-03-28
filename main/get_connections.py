from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import json

import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui



#driver = webdriver.Chrome(path)
#driver = webdriver.Edge()
driver = webdriver.firefox()

# Login
def login():

    email = "haxtor001@gmail.com"
    password = "H@axtor111"

    driver.get("https://www.linkedin.com/login")
    time.sleep(1)

    eml = driver.find_element(by=By.ID, value="username")
    eml.send_keys(email)
    passwd = driver.find_element(by=By.ID, value="password")
    passwd.send_keys(password)
    loginbutton = driver.find_element(by=By.XPATH, value="//*[@id=\"organic-div\"]/form/div[3]/button")
    loginbutton.click()
    time.sleep(3)


if __name__ == "__main__":
    login()
    print(">>>>Logged in!!!")
    # test = input("Waiting for the security process - Press Enter to continue")
    # print('Security check passed!!!')


    url = "https://www.linkedin.com/mynetwork/invite-connect/connections/"
    driver.get(url)
    time.sleep(5)


    soup = BeautifulSoup(driver.page_source, "html.parser")
    connection_count = soup.find("h1", class_="t-18 t-black t-normal").get_text().split(' ')
    connection_count = [t for t in connection_count if t not in ['', ' ', '\n']]
    connection_count = int(connection_count[0])
    print('connection_count >> ', connection_count)


    count_prev = 0
    count = 0
    btn_flg = False
    con_counter = 0

    while count != connection_count:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        soup = soup.body
        main = soup.find("main", id="main", class_="scaffold-layout__main")
        div = main.find("div", class_="scaffold-finite-scroll__content")
        li = div.findChildren('li')

        count = len(li)
        print(count)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        #input('paused!!')

        if count_prev == count:
            if not btn_flg:
                time.sleep(5)
                btn = driver.find_element(By.XPATH, '//button[normalize-space()="Show more results"]')
                btn.click()
                time.sleep(2)
                btn_flg = True
            else:
                con_counter += 1

        count_prev = count

        if con_counter>3:
            break

    print('>>>>Finish Scrolling')

    # write txt file
    txt_to_write = ''

    for a in li:
        link = a.find_all('a', href=True)[0]['href']
        txt_to_write += link + '\n'

    f = open('test.txt', 'w')
    f.writelines(txt_to_write)
    f.close()

    # write json file
    json_out = {}
    all_link = [l.find_all('a', href=True)[0]['href'] for l in li]
    json_out['connection'] = all_link
    with open('connection.json', 'w') as f:
        json.dump(json_out, f)

    time.sleep(2)
    driver.quit()



