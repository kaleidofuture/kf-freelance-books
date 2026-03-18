---
title: kf-freelance-books
emoji: 🚀
colorFrom: green
colorTo: blue
sdk: streamlit
sdk_version: 1.44.1
app_file: app.py
pinned: false
---

# KF-FreelanceBooks

> 銀行CSVを取り込んで、キーワードで経費を自動分類。確定申告の地獄を脱出。

## The Problem

フリーランスの確定申告が毎年地獄。銀行明細を一行ずつ手作業で分類するのに何時間もかかる。キーワードマッチングで自動分類すれば数秒で完了します。

## How It Works

1. 銀行CSV / クレジットカードCSVをアップロード
2. 日付・金額・摘要カラムを自動検出（手動調整可）
3. キーワードベースで経費カテゴリを自動分類（ルールはカスタマイズ可能）
4. 勘定科目別集計を表示
5. 分類済みCSVと確定申告用の集計CSVをダウンロード

## Libraries Used

- **pandas** — データ操作・集計

## Development

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deployment

Hosted on [Hugging Face Spaces](https://huggingface.co/spaces/mitoi/kf-freelance-books).

---

Part of the [KaleidoFuture AI-Driven Development Research](https://kaleidofuture.com) — proving that everyday problems can be solved with existing libraries, no AI model required.
