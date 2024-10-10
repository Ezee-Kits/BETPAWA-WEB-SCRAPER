from func import selenium_init,scrolling,requesting_init,saving_files,drop_duplicate,main_date,saving_path_csv
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from lxml import html
import pandas as pd



def betpawa_func():
    path = f'{saving_path_csv}/BETPAWA.csv'
    driver,wait,EC,By = selenium_init()
    driver.get('https://www.betpawa.ng/upcoming?marketId=_1X2&categoryId=2')
    time.sleep(3)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#view-wrapper > div.view-wrapper-content > div.main-content > div.center-view > div > div.tabs > div > div:nth-child(4) > a > div:nth-child(2) > div > p:nth-child(1)')))

    code_load = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="view-wrapper"]/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div[2]/button')))
    time.sleep(1.5)
    code_load.click()
    time.sleep(1.5)

    for x in range(5):
        elem = wait.until(EC.presence_of_element_located((By.TAG_NAME,'html')))
        elem.send_keys(Keys.END)
        print('\n SCROLLED \n ',x)
        time.sleep(5)


    matches = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="view-wrapper"]/div[1]/div[2]/div[1]/div/div[2]/div')))
    matches = matches.text.replace('\n','!').split('!')
    # print(matches)

    int_vals = [str(x) for x in range(1,3)]
    other_vals = ['X']
    int_vals = int_vals + other_vals

    new_matches = []

    for x in matches:
        x = x.strip()
        if x in int_vals or '+' in x:
            pass
        else:
            new_matches.append(x)

    time_value = []
    time_index = []

    for i,x in enumerate(new_matches):
        if ':' in x:
            indx = new_matches.index(x,i,len(new_matches))
            time_index.append(indx)
            time_value.append(x)

    # print(new_matches)
    # print(time_index)
    # print(time_value)


    for x in time_index:
        try:

            f_elem_indx = time_index.index(x)
            s_elem_indx = time_index.index(x) + 1

            if (time_index[s_elem_indx] - time_index[f_elem_indx]) == 7:
                all_info = new_matches[ time_index[f_elem_indx]:time_index[s_elem_indx] ]
                match_time = all_info[0].split()
                leq_12 = int(match_time[0].split(':')[0])

                if match_time[1] == 'pm' and leq_12 < 12:
                    match_time = match_time[0].split(':')
                    match_time = str(int(match_time[0]) + 12) + f':{match_time[1]}'

                if match_time[1] == 'am'and leq_12 < 12:
                    match_time = '0'+str(match_time[0])

                if match_time[1] == 'am' or match_time[1] == 'pm' and leq_12 == 12:
                    match_time = match_time[0]


                home_team = all_info[1]
                away_team = all_info[2]

                home_odd = float(all_info[4])
                draw_odd = float(all_info[5])
                away_odd = float(all_info[6])
                bookmaker = 'BETPAWA'

                data = {
                    'TIME':match_time,
                    'HOME TEAM':home_team,
                    'AWAY TEAM':away_team,

                    'HOME ODD': home_odd,
                    'DRAW ODD':draw_odd,
                    'AWAY ODD':away_odd,
                    'BOOKMAKER':bookmaker
                }
                saving_files(data=[data],path=path)

        except:
            pass
