import feedparser
import json
import re
import os
import requests
from bs4 import BeautifulSoup
from loguru import logger
from art import *

# ロガーの設定
logger.remove()
logger.add(lambda msg: print(msg, end=""), colorize=True, format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>")

class PaperScraper:
    def __init__(self, output_path='./papers.json'):
        self.output_path = output_path
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def extract_urls(self, text):
        github_pattern = r'https?://github\.com/\S+'
        huggingface_pattern = r'https?://huggingface\.co/\S+'

        github_urls = re.findall(github_pattern, text)
        huggingface_urls = re.findall(huggingface_pattern, text)

        return github_urls, huggingface_urls

    def scrape_arxiv(self):
        logger.info("arXivからの論文スクレイピングを開始します")
        url = 'http://export.arxiv.org/rss/cs.CV'
        feed = feedparser.parse(url)

        papers = []
        for entry in feed.entries:
            full_text = entry.title + ' ' + entry.summary
            github_urls, huggingface_urls = self.extract_urls(full_text)
            if github_urls or huggingface_urls:
                paper = {
                    'title': entry.title,
                    'summary': entry.summary,
                    'link': entry.link,
                    'published': entry.published,
                    'github_urls': github_urls,
                    'huggingface_urls': huggingface_urls,
                    'source': 'arXiv'
                }
                papers.append(paper)
                logger.debug(f"論文を追加しました: {entry.title}")

            if len(papers) >= 30:
                break

        logger.success(f"arXivから{len(papers)}件の論文を取得しました")
        return papers

    def scrape_huggingface(self):
        logger.info("Hugging Faceからの論文スクレイピングを開始します")
        url = 'https://rsshub.app/huggingface/daily-papers'
        
        response = requests.get(url, headers=self.headers)
        logger.debug(f"ステータスコード: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'lxml-xml')
        items = soup.find_all('item')
        logger.info(f"見つかったアイテム数: {len(items)}")

        papers = []
        for item in items:
            title = item.find('title').text if item.find('title') else 'タイトルなし'
            description = item.find('description').text if item.find('description') else '説明なし'
            link = item.find('link').text if item.find('link') else 'リンクなし'
            published = item.find('pubDate').text if item.find('pubDate') else '日付なし'
            authors = item.find('author').text if item.find('author') else '著者なし'

            full_text = title + ' ' + description
            github_urls, huggingface_urls = self.extract_urls(full_text)
            paper = {
                'title': title,
                'summary': description,
                'link': link,
                'published': published,
                'authors': authors,
                'github_urls': github_urls,
                'huggingface_urls': huggingface_urls,
                'source': 'Hugging Face'
            }
            papers.append(paper)
            logger.debug(f"論文を追加しました: {title}")

        logger.success(f"Hugging Faceから{len(papers)}件の論文を取得しました")
        return papers

    def scrape(self):
        tprint(">>  PaperScraper", font="rnd-large")
        logger.info("論文スクレイピングを開始します")
        arxiv_papers = self.scrape_arxiv()
        huggingface_papers = self.scrape_huggingface()

        # all_papers = arxiv_papers + huggingface_papers
        all_papers = huggingface_papers

        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(all_papers, f, ensure_ascii=False, indent=2)

        logger.success(f"合計{len(all_papers)}件の論文を抽出しました")
        logger.info(f"arXiv: {len(arxiv_papers)}件")
        logger.info(f"Hugging Face: {len(huggingface_papers)}件")
        logger.info(f"結果を {self.output_path} に保存しました")

if __name__ == '__main__':
    scraper = PaperScraper()
    scraper.scrape()
