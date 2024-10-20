# EyeAiApp

## 概要

眼底検査で撮影した画像を機械学習を用いて病状判定するwebアプリケーション
参考にした動画
https://www.youtube.com/watch?v=ydpoMxwWNA8&t=522s

### デモ・スクリーンショット
none

## 実装状況
- 1:MySQLとの接続、ログイン、ユーザー登録機能の実装

### 前提条件
- config.iniを以下の形式で同じ階層に作成し、DBの接続先を指定する
```bash
[MySQL]
host=
port = 3306
database=aidb
user=
password=
```

- MySQLで次のようなusersテーブル作成
```bash
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
```


### 実行方法
```bash
streamlit run main.py
```