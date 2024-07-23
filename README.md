## <p align="center">
<img src="https://huggingface.co/datasets/MakiAi/IconAssets/resolve/main/Yukihiko.png" width="100%">
<br>
<h1 align="center">Yukihiko</h1>
<h2 align="center">
  ～ AI-powered research discovery ～
<br>
  <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/Yukihiko">
<img alt="PyPI - Format" src="https://img.shields.io/pypi/format/Yukihiko">
<img alt="PyPI - Implementation" src="https://img.shields.io/pypi/implementation/Yukihiko">
<img alt="PyPI - Status" src="https://img.shields.io/pypi/status/Yukihiko">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dd/Yukihiko">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/Yukihiko">
<a href="https://github.com/Sunwood-ai-labs/Yukihiko" title="Go to GitHub repo"><img src="https://img.shields.io/static/v1?label=Yukihiko&message=Sunwood-ai-labs&color=blue&logo=github"></a>
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Sunwood-ai-labs/Yukihiko">
<a href="https://github.com/Sunwood-ai-labs/Yukihiko"><img alt="forks - Sunwood-ai-labs" src="https://img.shields.io/github/forks/Yukihiko/Sunwood-ai-labs?style=social"></a>
<a href="https://github.com/Sunwood-ai-labs/Yukihiko"><img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/Sunwood-ai-labs/Yukihiko"></a>
<a href="https://github.com/Sunwood-ai-labs/Yukihiko"><img alt="GitHub Top Language" src="https://img.shields.io/github/languages/top/Sunwood-ai-labs/Yukihiko"></a>
<img alt="GitHub Release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/Yukihiko?color=red">
<img alt="GitHub Tag" src="https://img.shields.io/github/v/tag/Sunwood-ai-labs/Yukihiko?sort=semver&color=orange">
<img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/Sunwood-ai-labs/Yukihiko/publish-to-pypi.yml">
<br>
<p align="center">
  <a href="https://hamaruki.com/"><b>[ Website]</b></a> •
  <a href="https://github.com/Sunwood-ai-labs"><b>[ GitHub]</b></a>
  <a href="https://x.com/hAru_mAki_ch"><b>[ Twitter]</b></a> •
  <a href="https://hamaruki.com/"><b>[ Official Blog]</b></a>
</p>

</h2>

</p>

>[!IMPORTANT]
>このリポジトリのリリースノートやREADME、コミットメッセージの9割近くは[claude.ai](https://claude.ai/)や[ChatGPT4](https://chatgpt.com/)を活用した[AIRA](https://github.com/Sunwood-ai-labs/AIRA), [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), [Gaiah](https://github.com/Sunwood-ai-labs/Gaiah), [HarmonAI_II](https://github.com/Sunwood-ai-labs/HarmonAI_II)で生成しています。

# Yukihiko

## はじめに

Yukihikoは、最新の機械学習論文を簡単にキャッチアップできるように設計されたツールです。 毎日自動的に論文を収集し、日本語に翻訳、要約を作成してGitHubのIssueとして投稿します。 忙しい研究者や開発者の方々に、最新の研究動向を効率的に把握するお手伝いをします。

## 機能

* 定期刊行物のWebサイトから論文をスクレイピング
*  スクレイピングした論文を日本語に翻訳
* 翻訳された論文の要約を自動生成
* 翻訳と要約をGitHubのIssueとして投稿
* Issueに自動的にラベルを付与

## 導入方法

1. リポジトリをクローンします。
2. 設定ファイルで、スクレイピングするWebサイト、翻訳先の言語、その他のオプションを設定します。
3. スケジュールされたタスクを設定し、スクリプトを毎日自動的に実行します。

## 更新情報

### v0.1.0 (2024-07-23)

- **新機能:**
    - arXivとHugging Faceから論文情報を自動取得
    - 論文情報を日本語に自動翻訳
    - 翻訳された論文の要約を自動生成
    - 翻訳と要約をGitHubのIssueとして投稿
    - Issueに自動的にラベルを付与
- **改善:**
    - 論文スクレイパーの実行時間の変更
    - ワークフローの効率性と安全性の向上
    - 不要なブランチ作成とプッシュの回避
    - GitHub Actionsワークフローの改善
    - スクリプトのデバッグ開始位置修正
- **バグ修正:**
    - GitHub Actionsの権限エラーを修正
    - IssueCreator スクリプトのデバッグ開始位置を修正
-   **ドキュメント:**
    - SourceSageの使い方を記述したusage.mdを追加
    - リリースノート生成のための設定ファイルを追加

## 貢献

このプロジェクトはオープンソースであり、コントリビューションを歓迎します。 機能のリクエスト、バグレポート、プルリクエストを提出してください。

## ライセンス

MIT License

## 謝辞

このリポジトリは、多くのオープンソースプロジェクトやライブラリを使用しています。 開発者や貢献者に感謝いたします。

## 免責事項

このリポジトリは学術的な目的で作成されています。 翻訳と要約の精度は、使用される機械学習モデルによって異なる場合があります。 情報の正確性については、必ず元の論文を参照してください。
```
