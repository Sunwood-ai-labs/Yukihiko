import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from services.llm_service import LLMService
from services.github_service import GitHubService
from config import get_settings  # 新しく追加
from art import *

class IssueSummarizer:
    def __init__(self):
        self.llm_service = LLMService()
        self.github_service = GitHubService()
        self.settings = get_settings()  # 新しく追加

    def summarize_paper(self, issue_title: str, issue_body: str) -> str:
        prompt = f"""
以下のarXiv論文を知識がない初心者で分かるような論文要約を日本語で記述してください。論文要約のみをください。箇条書きやマークダウンを活用して可読性を高めてください：

タイトル: {issue_title}

本文:
{issue_body}

## 論文要約

        """
        return self.llm_service.get_response(prompt)

    def process_issue(self):  # issue_number パラメータを削除
        tprint(">>  IssueSummarizer", font="rnd-large")
        issue_number = self.settings.ISSUE_NUMBER  # 設定から ISSUE_NUMBER を取得
        issue = self.github_service.get_issue(issue_number)
        logger.info(f"#{issue.number} の要約を処理しています: {issue.title}")

        paper_summary = self.summarize_paper(issue.title, issue.body)
        comment = f"## 論文要約\n\n{paper_summary}"
        self.github_service.add_comment(issue, comment)
        logger.info("論文要約を生成し、コメントとして追加しました。")
        
if __name__ == "__main__":
    summarizer = IssueSummarizer()
    summarizer.process_issue()
