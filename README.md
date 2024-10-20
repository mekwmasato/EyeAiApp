# EyeAiApp

## 概要

眼底検査で撮影した画像を機械学習を用いて病状判定するwebアプリケーション
参考にした動画
https://www.youtube.com/watch?v=ydpoMxwWNA8&t=522s

### デモ・スクリーンショット
none

## 実装状況
- 1:MySQLとの連携、ログイン、ユーザー登録機能の実装

### 前提条件
- config.iniを作成し、
```bash
[MySQL]
host=
port = 3306
database=aidb
user=
password=

```bash
# 例: 必要なライブラリのインストール
pip install -r requirements.txt

### 実行方法
```bash
streamlit run main.py