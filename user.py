# pip  install mysql-connector-python
import mysql.connector
import streamlit as st
from configparser import ConfigParser
import bcrypt
CNX: mysql.connector.connect = None #DBの接続を保持するために使う。最初はNONEで初期化している


def login(userName: str, password: str) -> bool:
    if not userName or not password:
        return False
    # ユーザーのパスワードハッシュを取得
    query = "SELECT password FROM users WHERE username = %s"
    result = execute_sql_query(query, (userName,))
    
    if not result:
        # ユーザー名が見つからなかった場合
        return False
    
    stored_hashed_password = result[0]  # データベースから取得したハッシュ化されたパスワード

    # bcrypt のハッシュか平文かをチェック
    if stored_hashed_password.startswith('$2b$') or stored_hashed_password.startswith('$2a$'):
        # bcrypt のハッシュの場合
        return bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8'))
    else:
        # 平文のパスワードの場合（古い形式）
        if stored_hashed_password == password:
            # 平文が一致したら、ハッシュ化してデータベースをアップデート
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            query = "UPDATE users SET password = %s WHERE username = %s"
            execute_sql_query(query, (hashed_password, userName))
            CNX.commit()
            return True
        else:
            return False

def execute_sql_query(query, args):
    global CNX
    if (CNX is None):
        config = ConfigParser()
        config. read("config.ini")
        _host = config.get('MySQL', 'host')
        _port = config.get('MySQL', 'port')
        _database = config.get('MySQL', 'database')
        _user = config.get('MySQL', 'user')
        _password = config.get('MySQL', 'password')
        CNX = mysql.connector.connect(host=_host, database=_database,user=_user,passwd=_password,port=_port)

    try:
        with CNX.cursor() as cur:
            cur.execute(query, args)
            result = cur.fetchone()
            print("result = ",result)
        return result
    except mysql.connector.Error as err83:
        print(f"Error: {err83}")
        return None

def signup(userName: str, password: str) -> bool:
    if not userName or not password:
        st.error("Invalid user name or password")
        return False

    # ユーザー名がすでに存在するかチェック
    check_query = "SELECT COUNT(1) FROM users WHERE username = %s"
    existing_user = execute_sql_query(check_query, (userName,))
    
    if existing_user[0] == 1:
        # すでにユーザーが存在する場合
        st.error("そのユーザー名は既に存在します")
        return False

    # 新しいユーザーを登録
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        execute_sql_query(query, (userName, hashed_password))
        CNX.commit()  # データベースに変更を反映
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False