import argparse
import os
import webbrowser
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.WebCrawler import WebCrawler
from map.draw_map import draw_map

# configure required arguments
parser = argparse.ArgumentParser()
parser.add_argument('depth', type=int, help='Crawl depth')
parser.add_argument('root_link', help='Start Url of web crawler')
args = parser.parse_args()


def main():
    # collect data to data.jsonl
    start_crawl()
    # generate map.html that can be used to view the data
    draw_map('exported_results.jsonl')
    print(f'Opening file://{os.path.realpath("./map.html")}')
    webbrowser.open(f'file://{os.path.realpath("./map.html")}')


def start_crawl():
    # configure scrapy crawler
    settings = get_project_settings()
    settings['DEPTH_LIMIT'] = args.depth
    print(settings['DEPTH_LIMIT'])
    process = CrawlerProcess(settings)
    WebCrawler.start_urls = [args.root_link]
    process.crawl(WebCrawler)
    # start crawl
    process.start()


if __name__ == '__main__':
    main()
