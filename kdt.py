import configparser
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def login(web_driver, id, passwd):
    web_driver.find_element(By.ID, 'user-email').send_keys(id)
    web_driver.find_element(By.ID, 'user-password').send_keys(passwd)
    web_driver.find_element(By.XPATH, '//*[@id="main"]/section/section/form/button').click()
    time.sleep(3)


def get_part_title(part_html):
    return part_html.select_one('p.classroom-sidebar-clip__chapter__title__text').text


# [(title, time), ...]
def get_semi_chapter_list(chapter_html):
    semi_chapter_title = chapter_html.select('span.classroom-sidebar-clip__chapter__clip__title')
    semi_chapter_time = chapter_html.select('span.classroom-sidebar-clip__chapter__clip__time')
    ret = []
    for (c_title, c_time) in zip(semi_chapter_title, semi_chapter_time):
        ret.append((c_title.text, c_time.text))
    return ret


def record_chapter_info(chapters_html):
    for chapter in chapters_html:
        chapter_title = chapter.select_one('p.classroom-sidebar-clip__chapter__part__title')
        print(chapter_title.text)
        semi_chapter_list = get_semi_chapter_list(chapter)
        print(semi_chapter_list)


def extend_accordion(driver):
    accordion_close_btns = driver.find_elements(
        By.CSS_SELECTOR,
        'div.common-accordion-menu:not(.common-accordion-menu--open) > .common-accordion-menu__header'
    )
    for btn in accordion_close_btns:
        driver.execute_script("arguments[0].click();", btn)


config = configparser.ConfigParser()
config.read('config.ini')
path = config['chrome-driver']['path']
user_id = config['auth']['id']
user_pw = config['auth']['passwd']
driver = webdriver.Chrome(
    service=Service(executable_path=r"{}".format(path))
)


def main():
    url = r'https://kdt.fastcampus.co.kr'

    driver.get(url)
    driver.implicitly_wait(30)  # load

    login(driver, user_id, user_pw)
    details_buttons = driver.find_elements(By.CSS_SELECTOR, '.sc-eb2000db-3')
    for idx in range(len(details_buttons)):
        print('page 이동')
        driver.execute_script("arguments[0].click();", driver.find_elements(By.CSS_SELECTOR, '.sc-eb2000db-3')[idx])
        time.sleep(3)

        # part 아코디언 펼치기
        extend_accordion(driver)

        # chapter 아코디언 펼치기
        extend_accordion(driver)

        # bs4
        lecture_html = BeautifulSoup(driver.page_source, 'html.parser')
        # part로 나누기
        parts = lecture_html.select('div.classroom-sidebar-clip__chapter')
        for part in parts:
            part_title = get_part_title(part)
            print(part_title)
            # part내 chapter로 나누기
            chapters = part.select('div.classroom-sidebar-clip__chapter__part')
            record_chapter_info(chapters)

        print('뒤로 가기')
        driver.back()
        time.sleep(3)

    time.sleep(60)  # main wait


if __name__=='__main__':
    main()