import os

from bs4 import BeautifulSoup
import requests

url = 'https://www.mirea.ru/schedule/'


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


# ИИТ=И ИИИ=K ИРЭИ=Р ИТХТ=Х
