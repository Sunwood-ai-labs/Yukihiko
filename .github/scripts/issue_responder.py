import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from config import get_settings
from services.llm_service import LLMService
from services.github_service import GitHubService

class IssueResponder:
    def __init__(self):
        self.llm_service = LLMService()
        self.github_service = GitHubService()
        self.settings = get_settings()

    def generate_response(self, issue_title: str, issue_body: str, comments: list) -> str:
        # issue_bodyとコメントを結合してLLMへの入力を準備
        context = f"## Issue Title:\n{issue_title}\n\n## Issue Body:\n{issue_body}"
        for i, comment in enumerate(comments):
            context += f"\n\n## Comment {i+1}:\n{comment.body}"

        prompt = f"""
あなたは、親切で役に立つAIアシスタントです。

以下のGitHub Issueに対して、新しいコメントを生成してください。
{context}

## 新しいコメント:
"""
        return self.llm_service.get_response(prompt)

    def process_issue(self):
        issue_number = self.settings.ISSUE_NUMBER
        issue = self.github_service.get_issue(issue_number)
        comments = self.github_service.get_comments(issue)

        # 自分以外のコメントがあれば応答を生成
        if comments and comments[-1].user.login != "yukihiko-fuyuki":
            logger.info(f"#{issue.number} {issue.title} に返信します。")
            response = self.generate_response(issue.title, issue.body, comments)
            self.github_service.add_comment(issue, response)
        else:
            logger.info(f"#{issue.number} {issue.title} には、まだ返信する必要はありません。")


if __name__ == "__main__":
    responder = IssueResponder()
    responder.process_issue()
