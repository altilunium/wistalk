# wi-stalk
WikiStalk : Analyze Wikipedia User's Activity

## Live Demo
https://replit.com/@rtnf141/wistalk

## How To Use
`pip install beautifulsoup4`
`pip install lxml`
`python3 wistalk.py targetWikipediaUsername wikipediaLanguageCode`\
Supported wikipedia language : `id` (default) and `en` \
Example : \
`python3 wistalk.py someUser en`
`python3 wistalk.py namaPengguna`


## Screenshot
![Screenshot2](https://github.com/altilunium/wistalk/blob/main/Screenshot%20from%202021-03-20%2021-39-21.png?raw=true)
![Screenshot3](https://github.com/altilunium/wistalk/blob/main/Screenshot%20from%202021-03-20%2021-46-34.png?raw=true)

## Dependencies
`pip install beautifulsoup4`
`pip install requests`
`pip install lxml`


### Update : Wistalk2
Now you can directly query to Wikipedia's database to analyze wikipedia user's activity (https://quarry.wmcloud.org/query/59144). It's much faster this way.
* Create a Wikipedia account
* Log in to Quarry
* Fork that SQL query
* Change the target variable with target username
* Submit query
