import requests 
import json
import urllib.parse
import xlsxwriter
import io
from bs4 import BeautifulSoup
from multiprocessing import Pool
from functools import partial

def get_reviews(tag, filename, p):
	# '''Given the range of pages and genre of the game, get an excel sheet of all game reviews present in the given pages filtered using number of reviews by a person, upvotes for the
	#    review and length of the review. Python's Beautifulsoup library is used to scrape the steam webpages. 
	#    step 1 : Traverse all the pages for the givrn game genre and extract all the appids and appnames present
	#             An api call is required to load each page
	#    step 2 : for each appid the corresponding page url is generated and stored
	#    step 3 : Open an empty excel workbook and write the column headers
	#    step 4 : Traverse each app url and write all the reviews to the excel worksheet
	#    step 5 : Close the excel workbook'''
	
	appids = []
	appnames = []
	# for p_no in range(start_page, end_page):
		#api call to load the required pages
	url = "https://store.steampowered.com/contenthub/querypaginated/tags/TopSellers/render/?query=&start=" + str(p * 15) + "&count=15&cc=IN&l=english&v=4&tag=" + str(tag)
	response = requests.get(url)
	html_soup = BeautifulSoup(response.content, 'html.parser')
	ids = html_soup.find_all('a', href=True)
		#store app ids and app names in each page to list
	for i in ids:
		appids.append(i['href'].split('\/')[4])
		appnames.append(i['href'].split('\/')[5])

	URLS = []
	for appid in appids:
		#Add the url of each app to a list
		url = "http://store.steampowered.com/appreviews/" +str(appid) + "?json=1&num_per_page=100&review_type=positive&purchase_type=steam&day_range=9223372036854775807&language=all&cursor="
		URLS.append(url)

	i = 0
	#Create an excel workbook to write the data
	fname = str(filename) + str(p) + '.xlsx'
	workbook = xlsxwriter.Workbook(fname)
	worksheet = workbook.add_worksheet()
	row = 1
	col = 0
	#write the header
	worksheet.write(0, col, "Steam_id")
	worksheet.write(0, col + 1, "Steam_url")
	worksheet.write(0, col + 2, "Num_reviews")
	worksheet.write(0, col + 3, "Language")
	worksheet.write(0, col + 4, "Review")
	worksheet.write(0, col + 5, "Upvotes")
	worksheet.write(0, col + 6, "Length")
	worksheet.write(0, col + 7, "Game_name")
	for url in URLS:
		col = 0
		#cursor to load the next set of reviews for a game
		cursor="*" 
		cursor_lst=[]
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
			for line in reviews:
				l = len(line['review'])
				nr = line['author']['num_reviews']
				up = line['votes_up']
				profile_url = "http://steamcommunity.com/profiles/" + line['author']['steamid']
				#Writing data to excel worksheet using filters
				if l > 400 and (nr > 15 or up > 2):
					worksheet.write(row, col,     line['author']['steamid'])
					worksheet.write(row, col + 1, profile_url)
					worksheet.write(row, col + 2, line['author']['num_reviews'])
					worksheet.write(row, col + 3, line['language'])
					worksheet.write(row, col + 4, line['review'])
					worksheet.write(row, col + 5, line['votes_up'])
					worksheet.write(row, col + 6, str(l))
					worksheet.write(row, col + 7, appnames[i])
					row += 1
			print(data['cursor'])
			print(row)
			cursor=data['cursor']
		print("{} done".format(appids[i]))
		i+=1
	workbook.close()

if __name__ =='__main__':
	tag = urllib.parse.quote_plus(input("Genre: "))
	start_page = int(input("Start page: "))
	end_page = int(input("End page: "))
	filename = input("Filename: ")
	p = list(range(start_page, end_page))
	pool = Pool()
	func = partial(get_reviews, tag, filename)
	pool.map(func, p)
	pool.close()
	pool.join()