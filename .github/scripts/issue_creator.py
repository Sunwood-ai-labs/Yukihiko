import sys
import os
import time
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from github import Github
from services.llm_service import LLMService
from loguru import logger
from tqdm import tqdm

from art import *

class IssueCreator:
    def __init__(self, papers_path='./papers.json'):
        self.papers_path = papers_path
        # self.g = Github(os.environ['GITHUB_TOKEN'])
        self.g = Github(os.environ['YOUR_PERSONAL_ACCESS_TOKEN_YUKIHIKO'])
        self.repo = self.g.get_repo(os.environ['GITHUB_REPOSITORY'])
        self.llm_service = LLMService()

    def translate_text(self, text: str, target_language: str = "日本語", max_retries: int = 5) -> Optional[str]:
        logger.info(f"テキストを{target_language}に翻訳中...")
        prompt = f"""
以下のテキストを自然な{target_language}に翻訳してください。翻訳結果のみをください：

{text}
        """
        logger.debug(f"prompt:\n{prompt}")
        with open("prompt.md", 'w', encoding='utf-8') as f:
            f.write(prompt)

        for attempt in range(max_retries):
            try:
                translated_text = self.llm_service.get_response(prompt)
                logger.success(f"翻訳完了:\n{translated_text}")
                return translated_text
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    wait_time = 60  # 1分待機
                    logger.warning(f"レート制限エラーが発生しました。{wait_time}秒待機してリトライします。(アテンプト {attempt + 1}/{max_retries})")
                    for _ in tqdm(range(wait_time)):
                        time.sleep(1)
                else:
                    logger.error(f"翻訳中にエラーが発生しました: {e}")
                    return None

        logger.error(f"最大リトライ回数（{max_retries}回）に達しました。翻訳に失敗しました。")
        return None

    def create_issue(self, paper):
        logger.info(f"論文 '{paper['title']}' のIssueを作成中...")
        
        translated_title = self.translate_text(paper['title'])
        if translated_title is None:
            logger.error(f"論文 '{paper['title']}' のタイトル翻訳に失敗しました。Issueの作成をスキップします。")
            return

        translated_title = translated_title.replace("*", "")
        
        translated_summary = self.translate_text(paper['summary'])
        if translated_summary is None:
            logger.error(f"論文 '{paper['title']}' の概要翻訳に失敗しました。Issueの作成をスキップします。")
            return

        title = f"{translated_title}"
        body = f"""
## タイトル: {translated_title}

## リンク: {paper['link']}

## 概要: \n{translated_summary} 
        """

        self.repo.create_issue(title=title, body=body)
        logger.success(f"論文 '{translated_title}' のIssueを作成しました")

    def create_issues_from_file(self):
        tprint(">>  IssueCreator", font="rnd-large")
        logger.info(f"{self.papers_path} からデータを読み込み中...")
        with open(self.papers_path, 'r') as f:
            papers = json.load(f)
        logger.success(f"{len(papers)}件の論文データを読み込みました")

        debug_start = 1
        n = 1
        for i, paper in enumerate(papers[debug_start:debug_start+n], 1):
            logger.info(f"論文 {i}/{n} を処理中...")
            self.create_issue(paper)

        logger.success("すべての論文のIssue作成が完了しました")

if __name__ == '__main__':
    logger.info("Issue作成プロセスを開始します")
    creator = IssueCreator()
    creator.create_issues_from_file()
    logger.success("Issue作成プロセスが正常に完了しました")
