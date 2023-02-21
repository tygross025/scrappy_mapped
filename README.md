# scrappy_mapped

Description
-----------
A web crawler that maps the locations of crawled ips.


Example output
-------------
map.html
<img width="1564" alt="Screenshot 2023-02-21 at 9 51 03 AM" src="https://user-images.githubusercontent.com/31942911/220394138-6a97fa46-39c3-48c0-a032-ca377e6cbda2.png">


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


