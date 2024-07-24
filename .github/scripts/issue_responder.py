import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from config import get_settings
from services.llm_service import LLMService
from services.github_service import GitHubService

class IssueResponder:
    def __init__(self, persona_path="persona.md"):
        self.llm_service = LLMService()
        self.github_service = GitHubService()
        self.settings = get_settings()
        self.persona = self.load_persona(persona_path)

    def load_persona(self, persona_path):
        with open(persona_path, "r", encoding="utf-8") as f:
            persona = f.read()
        return persona

    def generate_response(self, issue_title: str, issue_body: str, comments: list) -> str:
        context = f"## Issue Title:\n{issue_title}\n\n## Issue Body:\n{issue_body}"
        for i, comment in enumerate(comments[:-1]):
            context += f"\n\n## Comment {i+1}:\n{comment.body}"

        last_comment = comments[-1]
        logger.debug(f"last_comment : {last_comment}")
        
        prompt = f"""
あなたは、以下の設定の架空の人物「雪彦」として、下記の質問に対して、これまでのコメントも踏まえて応答してください。
応答のみを出力して

## 雪彦の設定:
```
{self.persona}
```

## Issueのこれまでの流れ:
{context}

## 質問: 
{last_comment.body}

## 雪彦の応答:
"""
        return self.llm_service.get_response(prompt)

    def process_issue(self):
        issue_number = self.settings.ISSUE_NUMBER
        issue = self.github_service.get_issue(issue_number)
        comments = self.github_service.get_comments(issue)

        # 自分以外のコメントがあれば応答を生成
        if comments and comments[-1].user.login != "yukihiko-fuyuki":
            logger.info(f"#{issue.number} {issue.title} の最後のコメントに雪彦として返信します。")
            response = self.generate_response(issue.title, issue.body, comments)
            self.github_service.add_comment(issue, response)
        else:
            logger.info(f"#{issue.number} {issue.title} には、まだ返信する必要はありません。")


if __name__ == "__main__":
    responder = IssueResponder()  # persona.mdを読み込む
    responder.process_issue()
