import requests 
import json
import urllib.parse
import xlsxwriter
import io
from bs4 import BeautifulSoup
import json
 
appids = ['1234520', '1038450', '465100', '230820', '46500', '1321230', '244430', '221810', '1258480', '1225070', '919410', '31800', '714120', '1304640', '232790', '327220']
appnames = ['The_Escaper', 'Nancy_Drew_Midnight_in_Salem', 'LUNA_The_Shadow_Dust', 'The_Night_of_the_Rabbit', 'Syberia', 'Angels_of_Death_EpisodeEddie', 'realMyst_Masterpiece_Edition',
            'The_Cave', 'Aladdin__Hidden_Objects_Game', 'Family_Mysteries_Poisonous_Promises', 'Felix_The_Reaper', 'Nancy_Drew_Danger_by_Design', 'Little_Misfortune', 'Related', 
            'Broken_Age', 'Annas_Quest']
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
			if l > 150 and (nr > 5 or up > 1):
				worksheet.write(row, col,     line['author']['steamid'])
				worksheet.write(row, col + 1, profile_url)
				worksheet.write(row, col + 2, line['author']['num_reviews'])
				worksheet.write(row, col + 3, line['language'])
				worksheet.write(row, col + 4, line['review'])
				worksheet.write(row, col + 5, line['votes_up'])
				worksheet.write(row, col + 6, str(l))
				worksheet.write(row, col + 6, appnames[i])
				row += 1
		print(row)
		print(data['cursor'])
		cursor=data['cursor']
	#csvFile.close()	
	workbook.close()
	print("{} done".format(appids[i]))
	i+=1
