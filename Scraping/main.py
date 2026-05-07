from bs4 import BeautifulSoup
import requests
from time import sleep
from random import random
import csv

with open("teachers.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Contact1", "Contact2"])

    for i in range(1, 55):
        print(f"Парсинг {i} страницы...")
        html = requests.get(f"https://atlas.herzen.spb.ru/teachers?page={i}")
        soup = BeautifulSoup(html.text, 'html.parser')

        table = soup.find("tbody")

        for row in table.find_all('tr'):
            sleep(random())
            link = row.find('td').find('a')

            name = link.get_text(strip=True)
            href = link.get('href')

            profile_page = requests.get(href)
            soup = BeautifulSoup(profile_page.text, 'html.parser')
            container = soup.find(id='home').find('div').find('div')
            divs = container.find_all('div')[1].find_all('div')[:-1]

            contacts = []
            for div in divs:
                contacts.append(div.find('h1').get_text(strip=True))

            contact1 = contacts[0] if len(contacts) > 0 else None
            contact2 = contacts[1] if len(contacts) > 1 else None

            writer.writerow((name, contact1, contact2))
        
        f.flush()
