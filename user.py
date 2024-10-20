# pip  install mysql-connector-python
import mysql.connector
import streamlit as st
from configparser import ConfigParser
CNX: mysql.connector.connect = None
 

def login(userName: str, password: str) -> bool:
    if not userName or not password:
        return False
    query = "SELECT COUNT(1) FROM users WHERE username = %s AND password = %s"
    result = execute_sql_query(query, (userName, password))
    
    # result[0] will be 1 if a match is found, otherwise 0
    return result[0] == 1

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
        CNX = mysql.connector.connect(
            host=_host, 
            database=_database,
            user=_user,
            passwd=_password,
            port=_port
        )

    try:
        with CNX.cursor() as cur:
            cur.execute(query, args)
            result = cur.fetchone()
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
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
        st.error("user is aldeady exist.")
        return False

    # 新しいユーザーを登録
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    try:
        execute_sql_query(query, (userName, password))
        CNX.commit()  # データベースに変更を反映
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False