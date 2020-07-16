import requests 
import json
import urllib.parse
import xlsxwriter
import io
from bs4 import BeautifulSoup
import json
 
appids = []
appnames = []
tag = urllib.parse.quote_plus(input("Genre: "))
start_page = int(input("Start page: "))
end_page = int(input("End page: "))
for p_no in range(start_page, end_page):
	url = "https://store.steampowered.com/contenthub/querypaginated/tags/TopSellers/render/?query=&start=" + str(p_no * 15) + "&count=15&cc=IN&l=english&v=4&tag=" + str(tag)
	response = requests.get(url)
	html_soup = BeautifulSoup(response.content, 'html.parser')
	ids = html_soup.find_all('a', href=True)
	for i in ids:
		appids.append(i['href'].split('\/')[4])
		appnames.append(i['href'].split('\/')[5])
URLS = []
for appid in appids:
	url = "http://store.steampowered.com/appreviews/" +str(appid) + "?json=1&num_per_page=100&review_type=positive&purchase_type=steam&day_range=9223372036854775807&language=all&cursor="
	URLS.append(url)

i = 0
for url in URLS:
	cursor="*" 
	cursor_lst=[]
	fname = appnames[i] + '.xlsx'
	workbook = xlsxwriter.Workbook(fname)
	worksheet = workbook.add_worksheet()
	row = 1
	col = 0
	while cursor!= None:
		print(cursor)
		if cursor in cursor_lst:
			print("duplicate cursor")
			break
		cursor_lst.append(cursor)
		r = requests.get(url+urllib.parse.quote_plus(cursor))
		data = r.json()
		data_ = json.dumps(data)
		dataset = json.loads(data_)
		reviews = dataset['reviews']

		worksheet.write(0, col, "Steam_id")
		worksheet.write(0, col + 1, "Steam_url")
		worksheet.write(0, col + 2, "Num_reviews")
		worksheet.write(0, col + 3, "Language")
		worksheet.write(0, col + 4, "Review")
		worksheet.write(0, col + 5, "Upvotes")
		worksheet.write(0, col + 6, "Length")
		worksheet.write(0, col + 6, "Game_name")
		for line in reviews:
			l = len(line['review'])
			nr = line['author']['num_reviews']
			up = line['votes_up']
			profile_url = "http://steamcommunity.com/profiles/" + line['author']['steamid']
			if l > 100 and (nr > 5 or up > 0):
				worksheet.write(row, col,     line['author']['steamid'])
				worksheet.write(row, col + 1, profile_url)
				worksheet.write(row, col + 2, line['author']['num_reviews'])
				worksheet.write(row, col + 3, line['language'])
				worksheet.write(row, col + 4, line['review'])
				worksheet.write(row, col + 5, line['votes_up'])
				worksheet.write(row, col + 6, str(l))
				worksheet.write(row, col + 6, appnames[i])
				row += 1
		print(data['cursor'])
		cursor=data['cursor']
	#csvFile.close()	
	workbook.close()
	print("{} done".format(appids[i]))
	i+=1
