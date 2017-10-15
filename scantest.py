import pickle
from newspaper import Article
tech_urls = []
nontech_urls = []
# l1 = 0
# with open('TECHDATA.txt') as f:
# 	for line in f:
# 		tech_urls.append(str(line))
# 		l1+=1
# 		if 'str' in line:
# 			break
# #print(tech_urls)
# l2 = 0
# with open('NONTECH.txt') as fil:
# 	for line in fil:
# 		nontech_urls.append(str(line))
# 		l2 += 0
# 		if 'str' in line:
# 			break
#print(nontech_urls)
with open('TECHDATA.txt', 'r') as myfile:
    tech_urls=myfile.read().split()
with open('NONTECH.txt', 'r') as myfile:
    nontech_urls=myfile.read().split()
tech_docs = []
l = len(tech_urls)

x = 0
for tech in tech_urls:
	try:
		a = Article(url = str(tech), language = 'en')
		a.download()
		a.parse()
		tech_docs.append(a.text)
	except:
		print("error")
		x+=1
print(x, "websites failed out of ", l)
non_tech_docs = []
l = len(nontech_urls)
x = 0
for nontech in nontech_urls:
	try:
		a = Article(url = str(nontech), language = 'en')
		a.download()
		a.parse()
		non_tech_docs.append(a.text)
	except:
		print("error")
		x+=1


print(x, "websites failed out of ", l)

tech_file = open('techdocs.pickle','wb')
pickle.dump(tech_docs, tech_file)
tech_file.close()

nontech_file = open('nontechdocs.pickle','wb')
pickle.dump(non_tech_docs, nontech_file)
nontech_file.close()
