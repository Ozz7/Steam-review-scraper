import requests 
import json
import urllib.parse
import xlsxwriter
from bs4 import BeautifulSoup
import re

appids = []
appnames = []
tag = urllib.parse.quote_plus(input("Genre: "))
start_page = int(input("Start page: "))
end_page = int(input("End page: "))
limit = int(input("Number of matching tags to look for: "))
for p_no in range(start_page, end_page):
	url = "https://store.steampowered.com/contenthub/querypaginated/tags/TopSellers/render/?query=&start=" + str(p_no * 15) + "&count=15&cc=IN&l=english&v=4&tag=" + str(tag)
	response = requests.get(url)
	html_soup = BeautifulSoup(response.content, 'html.parser')
	ids = html_soup.find_all('a', href=True)
	for i in ids:
		appids.append(i['href'].split('\/')[4])
		appnames.append(i['href'].split('\/')[5])
#Input the tags of the game for which you want to find the similar games
darkarta_tags = ['Adventure', 'Indie', 'Casual', 'Hidden Object', 'Puzzle', 'Point & Click', 'Female Protagonist', 'Fantasy', 'Alternate History', 'Romance',
				 'Historical', 'Atmospheric', 'Classic','Singleplayer']
URLS_rev = []
URLS_app = []
for appid, appname in zip(appids, appnames):
	url_rev = "http://store.steampowered.com/appreviews/" +str(appid) + "?json=1&num_per_page=100&review_type=positive&purchase_type=steam&day_range=9223372036854775807&language=all&cursor="
	url_app = 'https://store.steampowered.com/app/' + str(appid) + '/' + str(appname)
	URLS_rev.append(url_rev)
	URLS_app.append(url_app)
i = 0
similar_apps = []
similar_app_ids =[]
for url in URLS_app:
	response = requests.get(url)
	html_soup = BeautifulSoup(response.content, 'html.parser')
	ids = html_soup.find('div', class_ = 'glance_tags popular_tags')
	z = []
	k = ids.find_all('a', href = True)
	for j in k:
		regex = re.compile(r'[\n\r\t]')
		s = regex.sub("", j.text)
		z.append(s)
	common = list(set(z) & set(darkarta_tags))
	if len(common) >= limit:
		print(appnames[i])
		similar_apps.append(appnames[i])
		similar_app_ids.append(appids[i])
	i+=1
print(similar_apps)
print(similar_app_ids)