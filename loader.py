import requests


def download(link):
    filename = link.split('/')[-1]
    r = requests.get(link, allow_redirects=True)
    open(filename, "wb").write(r.content)


ikbo_2k = "https://webservices.mirea.ru/upload/iblock/25f/oxqk11pdd33p0p5sh9v2jvtc89gs76kw/ИИТ_2%20курс_21-22_" \
          "весна.xlsx "

