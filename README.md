# scrappy_mapped

Description
-----------
A web crawler that maps the locations of crawled ips.


Example output
-------------
map.html
<img width="1200" alt="Screenshot 2023-02-21 at 10 05 41 AM" src="https://user-images.githubusercontent.com/31942911/220397560-92dbae70-f589-49bd-8944-7ca4666d2c34.png">



How to run
----------
Run the following with the desired crawl depth and crawl start url.
 ```
 python scrapy_mapped.py [depth] [root_link]
 ```
The results will be saved as map.html and will be opened automatically in your browser.

>note: Enviornment variable IPINFO_ACCESS_TOKEN with a ipinfo.io api key is needed.

Requirements
------------
All of the required packages can be found in ``requirements.txt``


