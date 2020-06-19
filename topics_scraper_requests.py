from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import re

driver = webdriver.Chrome('/Users/heinipartanen/Downloads/chromedriver')
driver.implicitly_wait(30)

url = 'https://akareport.aka.fi/ibi_apps/WFServlet?ekaLataus=0&IBIF_ex=x_RahPaatYht_report2&UILANG=en&SANAHAKU' \
      '=&ETUNIMI=&SUKUNIMI=&SUKUPUOLI=FOC_NONE&HAKU=FOC_NONE&ORGANIS=FOC_NONE&TUTKDI=FOC_NONE&TMK=FOC_NONE' \
      '&PAATVUOSI_A=2001&PAATVUOSI_L=2019&LAJITTELU=TUTALA&TULOSTE=HTML'

driver.get(url)

links = []
names = []
for link_element in driver.find_elements_by_tag_name("a")[1:]:
    links.append(link_element.get_attribute("href"))
    names.append(link_element.text)

data = []
for link in links:
    driver.get(link)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    ref_list = []
    for table in soup.find_all('tbody'):
        references = table.find_all('td', align="RIGHT")[1:]
        for reference in references:
            ref_list.append(reference.text.strip())
    data.append(ref_list)

driver.quit()

filtered_result = []
for i in data:
    regex = re.compile(r'\s\d\d\d|^\d\d\d$|^\d\d$|^\d$')
    filtered = filter(lambda x: not regex.search(x), i)
    filtered = [x for x in i if not regex.search(x)]
    filtered_result.append(filtered)

df = pd.DataFrame(filtered_result, index=names).transpose()

print(df)

df.to_csv('aka_topics.csv')
