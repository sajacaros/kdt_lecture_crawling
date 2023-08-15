import configparser
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def login(web, id, passwd):
    web.find_element(By.ID, 'user-email').send_keys(id)
    web.find_element(By.ID, 'user-password').send_keys(passwd)
    web.find_element(By.XPATH, '//*[@id="main"]/section/section/form/button').click()
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


def extend_accordion(web):
    accordion_close_elements = web.find_elements(
        By.CSS_SELECTOR,
        'div.common-accordion-menu:not(.common-accordion-menu--open) > .common-accordion-menu__header'
    )
    for element in accordion_close_elements:
        web.execute_script("arguments[0].click();", element)


def travel_lecture(web):
    lecture_len = int(web.find_element(By.CSS_SELECTOR, 'em.sc-66c26572-1').text)
    print(lecture_len)
    for idx in range(lecture_len):
        web.execute_script("arguments[0].click();", web.find_elements(By.CSS_SELECTOR, '.sc-eb2000db-3')[idx])
        time.sleep(3)

        # part 아코디언 펼치기
        extend_accordion(web)
        # chapter 아코디언 펼치기
        extend_accordion(web)

        # 사이트 정보 획득
        retrieve_lecture_info(BeautifulSoup(web.page_source, 'html.parser'))

        # 뒤로가기
        web.back()
        time.sleep(3)


def retrieve_lecture_info(lecture_html):
    # part로 나누기
    parts = lecture_html.select('div.classroom-sidebar-clip__chapter')
    for part in parts:
        part_title = get_part_title(part)
        print(part_title)
        # part내 chapter로 나누기
        chapters = part.select('div.classroom-sidebar-clip__chapter__part')
        record_chapter_info(chapters)


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    path = config['chrome-driver']['path']
    user_id = config['auth']['id']
    user_pw = config['auth']['passwd']
    driver = webdriver.Chrome(
        service=Service(executable_path=r"{}".format(path))
    )
    url = r'https://kdt.fastcampus.co.kr'

    driver.get(url)
    driver.implicitly_wait(30)  # load

    login(driver, user_id, user_pw)

    travel_lecture(driver)


if __name__ == '__main__':
    main()
