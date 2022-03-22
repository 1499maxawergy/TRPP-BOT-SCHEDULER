from bs4 import BeautifulSoup
import requests

url = 'https://www.mirea.ru/schedule/'
links = []

def parse_mirea():
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    links = soup.findAll('a', class_='uk-link-toggle', href=True)

    for link in links:
        if link['href'].endswith(".xlsx"):
            print(link['href'])

parse_mirea()

#ИИТ ИИИ ИРЭА ИТХТ