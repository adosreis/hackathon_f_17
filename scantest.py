import urllib.request
from bs4 import BeautifulSoup

page = urllib.request.urlopen('https://www.wired.com/story/have-a-high-tech-halloween-with-your-own-haunted-smart-home/')
x = (page.read())

soup = BeautifulSoup(x, "html.parser")
words = []
for string in soup.strings:
	if(len(string) < 100):
		if not any(x in string for x in '<>/|\}{^*&%\\'):
				words.append(string)
print(words)
