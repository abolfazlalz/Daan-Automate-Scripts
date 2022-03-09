import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv


class Daan:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://iauctb.daan.ir/")
        self.login()

    def login(self):
        username = ''
        password = ''

        self.driver.find_element(
            by=By.XPATH, value='//*[@id="welcomAlarm"]/div/div/div[3]/button').click()

        self.driver.find_element(
            by=By.XPATH, value='/html/body/main/div/div[3]/div[1]/section/div[2]/div[2]/a[2]').click()

        self.driver.find_element(
            by=By.XPATH, value='//*[@id="identificationNumber"]').send_keys(username)
        self.driver.find_element(
            by=By.XPATH, value='//*[@id="password"]').send_keys(password)

        self.driver.find_element(
            by=By.XPATH, value='//*[@id="signinform"]/button').click()

        self.driver.find_element(
            by=By.XPATH, value='/html/body/main/section[3]/div/div/div[2]/a').click()

    def load_lessons(self):
        lesson_tag_path = '/html/body/main/div[1]/div/div[3]/div[1]/div'

        i = 0
        lessons = []

        days = {
            'شنبه': 'Saturday',
            'یک شنبه': 'Sunday',
            'دوشنبه': 'Monday',
            'سه شنبه': 'Tuesday',
            'چهارشنبه': 'Wednesday',
            'پنج شنبه': 'Thursday',
            'جمعه': 'Friday'
        }

        while True:
            try:
                i += 1
                lesson_tag = lesson_tag_path + ('[%d]' % i)
                lesson = self.driver.find_element(
                    by=By.XPATH, value=lesson_tag)
                lesson_full_name: list[str] = lesson.find_element(
                    by=By.TAG_NAME, value='h4').text.split('-')
                lesson_id = lesson_full_name[1].strip()
                lesson_name = lesson_full_name[0].strip()
                lesson_full_time = self.driver.find_element(
                    by=By.XPATH, value='/html/body/main/div[1]/div/div[3]/div[1]/div[%d]/div[2]/div[1]/div[2]/h6' % i).text

                lesson_time_regex = re.search(
                    r"(.*) \( (\d*\:\d*) \w* (\d*:\d*) \)", lesson_full_time)

                lesson_day = days[lesson_time_regex.group(1)]
                lesson_start_time = lesson_time_regex.group(2)
                lesson_end_time = lesson_time_regex.group(3)

                lessons.append({'id': lesson_id, 'name': lesson_name, 'endtime': lesson_end_time,
                               'starttime': lesson_start_time, 'day': lesson_day})
            except NoSuchElementException:
                break

        with open('lessons.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(
                f, fieldnames=['id', 'name', 'starttime', 'endtime', 'day'])
            writer.writeheader()
            writer.writerows(lessons)

    def close(self):
        self.driver.find_element(
            by=By.CLASS_NAME, value='logout').click()
        self.driver.close()


def main():
    d = Daan()
    d.load_lessons()
    d.close()


if __name__ == '__main__':
    main()
