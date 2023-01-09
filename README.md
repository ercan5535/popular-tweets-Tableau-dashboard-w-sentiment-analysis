- In this project I want to create a user friendly dashboard is used for popular tweets for given keywords.
- get_data.py will search tweets for given keywords, do some process and write into PostgreSQL database.
- Tweepy is used for getting tweets and TextBlob is used for sentiment analysis.
- All operations are handled from helper.py so execution of get_data.py is enough to write data into PostgreSQL database.
- Tableau public doesnt support to connect PostgreSQL server. So I imported data from PostgreSQL database and convert it to excel file to upload Tabluea. Tweets.xlsx is a sample of uploaded data.
- Before executing get_data.py, You have to fill credentials.py for Twitter API, PostgreSQL database and keywords for twitter search.

Tableau Dashboard
<img src="https://user-images.githubusercontent.com/67562422/211403092-81ef63c6-b98d-4bba-828a-821095a9ba4b.png" width="1000" height="500" >

You may experience dashboard [here](https://public.tableau.com/app/profile/ercan2027/viz/final_dashboard_16732929443320/TweetsDashboard2?publish=yes)

