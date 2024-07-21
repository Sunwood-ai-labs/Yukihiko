from github import Github
from loguru import logger
from config import get_settings
import random

def generate_random_color():
    """ランダムな6桁の16進数カラーコードを生成する"""
    return f"{random.randint(0, 0xFFFFFF):06x}"

class GitHubService:
    def __init__(self):
        self.settings = get_settings()
        # self.g = Github(self.settings.GITHUB_TOKEN)
        # self.g = Github(self.settings.YOUR_PERSONAL_ACCESS_TOKEN)
        self.g = Github(self.settings.YOUR_PERSONAL_ACCESS_TOKEN_YUKIHIKO)
        
        self.repo = self.g.get_repo(self.settings.GITHUB_REPOSITORY)
        logger.debug(f"Using token: {self.settings.YOUR_PERSONAL_ACCESS_TOKEN[:5]}...")

    def get_issue(self, issue_number: int = None):
        issue_number = issue_number or self.settings.ISSUE_NUMBER
        logger.debug(f"issue_number : {issue_number}")
        return self.repo.get_issue(number=issue_number)

    def get_comments(self, issue):
        return list(issue.get_comments())

    def add_comment(self, issue, comment):
        issue.create_comment(comment)
        logger.info(f"コメントを追加しました: \n{comment[:200]}...")

    def add_labels(self, issue, labels):
        issue.add_to_labels(*labels)
        logger.info(f"ラベルを追加しました: {', '.join(labels)}")

    def create_pull_request(self, title, body, head, base="main"):
        pr = self.repo.create_pull(title=title, body=body, head=head, base=base)
        logger.info(f"Pull Requestを作成しました: {pr.html_url}")
        return pr

    def get_labels(self):
        """リポジトリの既存のラベルを取得する"""
        labels = self.repo.get_labels()
        return [label.name for label in labels]

    def create_label(self, label_name, description=""):
        """新しいラベルをランダムな色で作成する"""
        color = generate_random_color()
        try:
            self.repo.create_label(name=label_name, color=color, description=description)
            logger.info(f"新しいラベルを作成しました: {label_name} (色: #{color})")
        except Exception as e:
            logger.error(f"ラベルの作成中にエラーが発生しました: {str(e)}")
