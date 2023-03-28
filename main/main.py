from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json

import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui

options = webdriver.FirefoxOptions()
options.add_argument('--headless')

# driver = webdriver.Chrome(path)
# driver = webdriver.Edge()
driver = webdriver.Firefox(options=options)


# Login
def login():
    print("Logging in!!!")

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


def scrap(profile_url):
    wt_after = 10 # >>> make this random 10-20 sec

    user_info = {'url': profile_url}

    # get main page info -------------------------------------------------
    url = profile_url
    driver.get(url)
    time.sleep(wt_after)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    # time.sleep(1)

    main_profile = soup.find('div', class_='mt2 relative')
    user_info['name'] = main_profile.find('h1',
                                          class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip()
    user_info['title'] = main_profile.find('div', class_='text-body-medium break-words').get_text().lstrip().strip()
    user_info['location'] = main_profile.find('span',
                                              class_='text-body-small inline t-black--light break-words').get_text().lstrip().strip()

    # get summary

    # print(user_info)
    # print("-" * 50)
    time.sleep(2)
    # --------------------------------------------------------------------------
    k = 'experience'
    url = profile_url + '/details/' + k
    driver.get(url)
    time.sleep(wt_after)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    soup = soup.body

    # get main -> 1st ul -> its li
    main = soup.find("main", id="main", class_="scaffold-layout__main")
    ul = main.findChildren("ul", class_="pvs-list")[0]
    li = ul.findChildren("li", recursive=False)

    tmp = []
    if "Nothing to see for now" in main.getText():
        # print("NONE !!!!")
        user_info['experience'] = None
        pass
    else:
        for lst in li:
            div = lst.findChildren("div", class_="display-flex flex-row justify-space-between")

            # dot means the person do multiple role at one comp
            dot = lst.findChildren("span", class_="pvs-entity__path-node")
            dot_flg = False

            for idx, e in enumerate(div):
                row = [t for t in e.getText().split('\n') if t not in ['', ' ']]
                row = [t[:int(len(t) / 2)] for t in row]

                if dot and not dot_flg:
                    # print("Found the dots!!!")
                    tmp.append(row)
                    dot_flg = True
                elif dot and dot_flg:
                    tmp[-1].append(row)
                else:
                    tmp.append(row)

        user_info[k] = tmp

    print(" " * 3, k, user_info[k])
    time.sleep(2)
    # --------------------------------------------------------------------------
    keys = ['skills', 'education', 'languages']

    for k in keys:

        refresh_count = 0
        tmp = []

        # repeat if tmp is [] empty
        while tmp is not None and not tmp:

            url = profile_url + '/details/' + k
            driver.get(url)
            time.sleep(wt_after)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            soup = soup.body
            main = soup.find("main", id="main", class_="scaffold-layout__main")
            div = main.findChildren("div", class_="display-flex flex-row justify-space-between")

            if "Nothing to see for now" in main.getText():
                tmp = None
                pass
            else:
                for idx, e in enumerate(div):
                    row = [t for t in e.getText().split('\n') if t not in ['', ' ']]
                    row = [t[:int(len(t) / 2)] for t in row]

                    if k == 'skills':
                        tmp += row
                    else:
                        tmp.append(row)

            refresh_count += 1
            if refresh_count > 3: raise Exception("Refresh count exceeded")

        if k == 'skills': tmp = list(set(tmp))
        user_info[k] = tmp

        print(" " * 3, k, user_info[k])
        time.sleep(2)


    # get as much as we can
    # # awards --------------------------------------------------------
    # url = profile_url + '/details/awards/'
    # li = get_li(url)
    #
    # tmp = []
    # for i, e in enumerate(li):
    #     # print(e.getText())
    #     row = [t for t in e.getText().split('\n') if t not in ['', ' ']]
    #     row = [t[:int(len(t) / 2)] for t in row]
    #     if len(row) > 1:
    #         tmp.append(row)
    #         print(row[:2])
    #         print("-" * 50)
    #
    # user_info['awards'] = tmp
    #
    # # cert --------------------------------------------------------
    # url = profile_url + '/details/cert/'
    # li = get_li(url)
    #
    # tmp = []
    # for i, e in enumerate(li):
    #     # print(e.getText())
    #     row = [t for t in e.getText().split('\n') if t not in ['', ' ']]
    #     row = [t[:int(len(t) / 2)] for t in row]
    #     if len(row) > 2:
    #         tmp.append(row[:3])
    #         print(row[:3])
    #         print("-" * 50)
    #
    # user_info['cert'] = tmp

    print(" " * 3, 'done !!!\n')
    return user_info


if __name__ == "__main__":

    t_start = time.time()

    # read txt file
    f = open('test.txt', 'r')
    con_lst = f.readlines()
    f.close()

    # # read json file
    # f = open('connection.json', 'r')
    # con_lst_json = f.readline()
    # con_lst_json = json.loads(con_lst_json)['connection']
    # f.close()

    login()
    print("Logged in!!!")
    # print(driver.current_url)
    # test = input("Waiting for the security process - Press Enter to continue")
    # print('Security check passed!!!')

    data = {'data': []}

    count = len(con_lst)
    base_url = "https://www.linkedin.com"

    start = 150
    end = 170
    print(f"Start {start} - {end}!!!")


    err_count = 0
    err_user_lst = []

    # fix_lst = ['https://www.linkedin.com/in/zana-mahim-a69529235/',
    #            'https://www.linkedin.com/in/dr-mehmet-k%C4%B1l%C4%B1%C3%A7-4b28411b3/',
    #            'https://www.linkedin.com/in/%E6%94%BF%E8%BC%9D-%E9%99%B3-13533b219/',
    #            'https://www.linkedin.com/in/ayse-mine-evren/',
    #            'https://www.linkedin.com/in/naterkuor/',
    #            'https://www.linkedin.com/in/albert-storey-567b1a173/']

    for i, p in enumerate(con_lst[start:end]):
        user_url = base_url + p
    # for i, p in enumerate(fix_lst):
    #     user_url = p

        print(f">>>> {start + i + 1}/{end}  -- {user_url}")

        try:
            user = scrap(user_url)
            data['data'].append(user)
        except Exception as e:
            print(e)
            err_count += 1
            err_user_lst.append(p)
            print('err_count:', err_count, '\n')

        time.sleep(2)

    print("Finished!!!")
    print(f"total error : {err_count} !!!")

    f_name = 'fix_list.txt'
    with open(f_name, 'w') as f:
        f.writelines(err_user_lst)

    f_name = f'scraped-{start}-{end}.json'
    with open(f_name, 'w') as f:
        json.dump(data, f)

    print(f"Saved to {f_name}!!!")

    time.sleep(2)
    driver.quit()

    t_end = time.time()
    print("total time >>", (end-start)/60, "min")
