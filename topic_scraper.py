import requests
from bs4 import BeautifulSoup
import re
import csv


# collects urls for each research topic and adds them to a dictionary. Get the link by selecting years and running a
# search by research topics in AKA's searchable database
def get_topic_links():
    url = 'https://akareport.aka.fi/ibi_apps/WFServlet?ekaLataus=0&IBIF_ex=x_RahPaatYht_report2&UILANG=en&SANAHAKU' \
          '=&ETUNIMI=&SUKUNIMI=&SUKUPUOLI=FOC_NONE&HAKU=FOC_NONE&ORGANIS=FOC_NONE&TUTKDI=FOC_NONE&TMK=FOC_NONE' \
          '&PAATVUOSI_A=2018&PAATVUOSI_L=2020&LAJITTELU=TUTALA&TULOSTE=HTML '
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    dictionary = {}
    for link_element in soup.find_all('a')[1:]:
        dictionary.update({link_element.text: link_element.get("href")})
    return dictionary


# Iterates through the dictionary values which are urls. Grabs all the matching tags and the refs are filtered out
# with regex. Each reference is matched with a corresponding research topic and added to a list
def get_data():
    data = []
    for k, v in get_topic_links().items():
        topic_page = requests.get(v)
        soup2 = BeautifulSoup(topic_page.text, 'lxml')
        tags_list = []
        for correct_tags in soup2.find_all('td', align="RIGHT")[1:]:
            tags_list.append(correct_tags.text.strip())
        regex = re.compile(r'\d\d\d\d\d\d|\d\d\d\d\d')
        okay_items = [x for x in tags_list if regex.match(x)]
        for i in okay_items:
            data.append([i, k])
    return data


headers = ['reference', 'topics']

with open('aka_topics.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(get_data())


