import os
import requests
from bs4 import BeautifulSoup
import re
from PIL import Image, ImageFile
import io
from io import BytesIO
from time import sleep
from PIL import Image
import urllib3
urllib3.disable_warnings()

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) '
        'Gecko/20100101 Firefox/45.0'
      }

base_url = "https://tekstpesni.ru"
artist = ["kaleo"]

carl_url = []
for i in artist:
    url = f"{base_url}/search?q={i}"
    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all(
        'a',
        class_="link-primary link-offset-1 link-offset-1-hover "
                "link-underline link-underline-opacity-0 "
                "link-underline-opacity-75-hover"
                )
    for i in data:
        song_url = i.get("href")
        carl_url.append(f"{base_url}{song_url}")

count = 0
for i_url in carl_url:
    if count >= 3:
        break
    else:
        sleep(5)
        count += 1
        response = requests.get(i_url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        link = soup.find(
            'a',
            class_="d-inline-flex align-items-center gap-1 me-2 link-primary "
            "link-offset-1 link-offset-1-hover link-underline "
            "link-underline-opacity-0 link-underline-opacity-75-hover"
            )
        artist_name = link.text
        print("Имя исполнителя:", artist_name)

        link = soup.find('h1')
        song_title = link.text
        print("Название песни:", song_title)

        lyrics = soup.find('meta', itemprop="description")
        lyrics = str(lyrics).replace('<meta content=', '').replace('itemprop="description"/>', '')
        print(lyrics)
        results_3 = soup.find('img', class_="rounded border").get("src")
        url_img = f"{base_url}{results_3}"
        response = requests.get(url_img, headers=headers, verify=False)
        img = Image.open(io.BytesIO(response.content))
        display(img)
        # Сохранение изображений в папку
        image_filename = os.path.join('images', f'{song_title}.jpg')
        with open(image_filename, 'wb') as img_file:
            img_file.write(response.content)
