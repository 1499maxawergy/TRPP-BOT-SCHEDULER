import os
import random

from bs4 import BeautifulSoup
import requests

url = 'https://www.mirea.ru/schedule/'
url_floppa1 = "https://memepedia.ru/wp-content/uploads/2020/10/big-floppa-meme.png"
url_floppa2 = "https://i.kym-cdn.com/photos/images/original/002/028/716/ef3.jpg"

# parse_mirea() - удаление предыдущих и скачивание новый .xlsx файлов с расписанием
def parse_mirea():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in files:
        if file.endswith(".xlsx"):
            os.remove(file)

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    links = soup.findAll('a', class_='uk-link-toggle', href=True)

    for link in links:
        if link['href'].endswith(".xlsx"):
            if (link['href'].split("/")[-1].find("ИИТ") != -1 or
                link['href'].split("/")[-1].find("ИИИ") != -1 or
                link['href'].split("/")[-1].find("ИРЭИ") != -1 or
                link['href'].split("/")[-1].find("ИТХТ") != -1) and \
                    link['href'].split("/")[-1].find("маг") == -1:
                open(link['href'].split("/")[-1], 'wb').write(requests.get(link['href']).content)


def download_floppa():
    rand = random.randint(0, 10)
    if rand == 0:
        open("floppa.png", 'wb').write(requests.get(url_floppa2).content)
    else:
        open("floppa.png", 'wb').write(requests.get(url_floppa1).content)


def delete_floppa():
    os.remove("floppa.png")
