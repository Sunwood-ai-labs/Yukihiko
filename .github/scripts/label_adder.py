import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from config import get_settings
from services.llm_service import LLMService
from services.github_service import GitHubService

class LabelAdder:
    def __init__(self):
        self.settings = get_settings()
        logger.debug(f"ISSUE_NUMBER: {self.settings.ISSUE_NUMBER}")
        
        self.llm_service = LLMService()
        self.github_service = GitHubService()
        self.existing_labels = self.load_labels_from_github()
        self.user_name = "@yukihiko-fuyuki"
    def load_labels_from_github(self):
        return self.github_service.get_labels()

    def analyze_issue(self, issue_title: str, issue_body: str) -> str:
        prompt = f"""
        以下のGitHubイシューを分析し、適切なラベルを提案してください：

        タイトル: {issue_title}

        本文:
        {issue_body}

        既存のラベルのリスト:
        {', '.join(self.existing_labels)}

        上記の既存のラベルのリストから、このイシューに最も適切なラベルを最大3つ選んでください。
        もし適切なラベルが既存のリストにない場合は、新しいラベルを提案することもできます。
        選んだラベルをカンマ区切りで提案してください。

        回答は以下の形式でラベルのみを提供してください：
        label1, label2, label3
        """
        return self.llm_service.get_response(prompt)

    def process_issue(self):  # issue_number パラメータを削除
        issue_number = self.settings.ISSUE_NUMBER  # 設定から ISSUE_NUMBER を取得
        issue = self.github_service.get_issue(issue_number)
        logger.info(f"イシュー #{issue.number} のラベル追加を処理しています: {issue.title}")

        suggested_labels_str = self.analyze_issue(issue.title, issue.body)
        suggested_labels = [label.strip().replace("*", "").replace("新しいラベル", "") for label in suggested_labels_str.split(',')]

        applied_labels = []
        new_labels = []

        for label in suggested_labels:
            if label in self.existing_labels:
                applied_labels.append(label)
            else:
                new_labels.append(label)
                self.github_service.create_label(label)
                self.existing_labels.append(label)
                applied_labels.append(label)

        if applied_labels:
            self.github_service.add_labels(issue, applied_labels)
            logger.info(f"ラベルを適用しました: {', '.join(applied_labels)}")

        comment = f"{self.user_name} が以下のラベルを提案し、適用しました：\n\n" + "\n".join([f"- {label}" for label in applied_labels])
        if new_labels:
            comment += f"\n\n以下の新しいラベルが作成され、適用されました：\n\n" + "\n".join([f"- {label}" for label in new_labels])
        self.github_service.add_comment(issue, comment)
        logger.info(f"イシュー #{issue.number} のラベル追加処理が完了しました。")

if __name__ == "__main__":
    label_adder = LabelAdder()
    label_adder.process_issue()
