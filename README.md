# Steam-review-scraper
Python scripts to extract customer reviews of games from steam. The extracted reviews along with the users's steam id, language, upvotes and No. of reviews by the user are written into an excel sheet.
There are 5 scripts which can be used to get the output in 5 different formats.

- steam_review.py - Input the genre, start page and end page queries. Get the reviews of all the games in the inputted pages in seperate excel sheets.
- similar_games.py - Input the genre, start page and end page queries. Specify the tags for the game for which you want to find the similar games in the code. Get lists of similar games and their app ids as output.
- steam_review_modified.py - Same as steam_review.py but here you can give the lists obtained from similar_games.py as input to process by editing the code.
- steam_review_merged.py - Same as steam_review.py but the extracted reviews are stored in a single excel sheet.
- steam_review_multiprocessing.py - Same as steam_review_merged.py but uses the multiprocessing module in python to increase execution speed.
