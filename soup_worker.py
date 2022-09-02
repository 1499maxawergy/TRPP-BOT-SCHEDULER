"""Загрузка файлов с расписанием с mirea.ru/schedule через модуль BeautifulSoup4"""
import os

import requests
from bs4 import BeautifulSoup

url = 'https://www.mirea.ru/schedule/'


# parse_mirea() - удаление предыдущих и скачивание новый .xlsx файлов с расписанием
def parse_mirea():
    """Обновление файлов расписания

    Удаляет старые файлы с расписанием и загружает новые
     для последующей работы с ними"""
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in files:
        if file.endswith(".xlsx"):
            os.remove(file)

    page = requests.get(url, timeout=3)
    soup = BeautifulSoup(page.text, "html.parser")
    links = soup.findAll('a', class_='uk-link-toggle', href=True)

    for link in links:
        if link['href'].endswith(".xlsx"):
            if (link['href'].split("/")[-1].find("IIT") != -1 or
                link['href'].split("/")[-1].find("III") != -1 or
                link['href'].split("/")[-1].find("IRI") != -1 or
                link['href'].split("/")[-1].find("ITKHT") != -1) and \
                    link['href'].split("/")[-1].find("mag") == -1:
                open(link['href'].split("/")[-1], 'wb').write(requests.get(link['href']).content)
