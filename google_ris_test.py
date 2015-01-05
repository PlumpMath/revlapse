import json
import requests
from bs4 import BeautifulSoup
import json

def ris(image_url):
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    r = requests.get('http://www.google.com/searchbyimage?image_url=' + image_url, headers=headers)

    html = r.text

    print html

    soup = BeautifulSoup(html)

    print soup

    text = soup.find("a", class_="_gUb")

    if text:
        text = text.find(text=True)

    matches = soup.find_all("h3", class_="r")

    if (matches):
        output_matches = []
        for match in matches:
            output_matches.append(match.find(href=True)['href'])
        matches = output_matches

    print text
    print matches


print ris("http://vps.provolot.com/GITHUB/revlapse/imgs/example1.jpg");
