import urllib.request
from bs4 import BeautifulSoup

page = urllib.request.urlopen('https://stackoverflow.com/questions/14694482/converting-html-to-text-with-python')
x = (page.read())

soup = BeautifulSoup(x)
print(soup.get_text('\n'))