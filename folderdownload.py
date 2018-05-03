linkdl = input('Paste the folder link here:')
getlink = 'http://urlchecker.org/folder'

print('Please wait...')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import requests
from bs4 import BeautifulSoup
import re

options = Options()
options.set_headless(headless=True)
driver = webdriver.Firefox(firefox_options=options, executable_path=r'geckodriver.exe')
driver.get(getlink)
driver.find_element_by_partial_link_text(" FILE SHARING").click()
element = driver.find_element_by_id('fixed-box')
driver.execute_script("""
var element = arguments[0];
element.parentNode.removeChild(element);
""", element)
elem = driver.find_element_by_id("id_urlarea")
elem.send_keys(Keys.CONTROL + "a")
elem.send_keys(Keys.DELETE)
elem.send_keys(linkdl)
driver.find_element_by_id("id_urlform").click()

html = driver.page_source
driver.close()

links = re.findall(r"arrURL[[0-9]*]=.*'",str(html))
for i in range(len(links)):
    links[i] = links[i].split("='")[1][:-1]

nLinks = len(links)

print("Found ",str(nLinks),' links \n')
dlinks = []
for i in range(nLinks):
    print('Loading link..',str(i+1),'/',str(nLinks),'\n',sep='')
    link = links[i]
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    dlink = soup.find_all('a', class_ = 'DownloadButtonAd-startDownload gbtnSecondary', href=True)[0]
    dlinks.append(dlink['href'])    
s = "\n".join(dlinks)
file = open('output.txt','w')
file.write(s)
file.close()
print("Done! Check the file 'output.txt'")
