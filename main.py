import streamlit as st
from user import login #user.pyからよみこみ
from user import signup

import socket

###
HOST = 'ip-172-31-42-245.ap-northeast-1.compute.internal'
PORT = 12345
###

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
signupSection = st.container()
logOutSection = st.container()

def show_main_page():
    with mainSection:
        st.write(f"ようこそ {st.session_state['username']} さん！")
        uploaded_image = st.file_uploader("眼底画像をアップロード",type=["png", "jpg"])

        if st.button ("Start Processing", key="processing"):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((HOST, PORT))
                print("サーバーに接続しました。")

                # 画像のデータを読み込み、送信
                image_data = uploaded_image.read()
                client_socket.sendall(image_data)  #画像データ全体を一括で送信
                st.write("画像を送信しました。")

def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    st.session_state['username'] = ""  # ログアウト時にユーザー名もクリア
    
def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.button ("Log Out", key="logout", on_click=LoggedOut_Clicked)
    
def LoggedIn_Clicked(userName, password):
    if login(userName, password):
        st.session_state['loggedIn'] = True
        st.session_state['username'] = userName  # ユーザー名をsession_stateに保存
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")
    
def show_login_page():
    with loginSection:
        if st.session_state['loggedIn'] == False:
            userName = st.text_input (label="username", value="", placeholder="Enter your user name")
            password = st.text_input (label="password", value="",placeholder="Enter password", type="password")
            st.button ("Login", on_click=LoggedIn_Clicked, args= (userName, password))#argsの変数がon_clickに指定された関数に渡される

def Signup_Clicked(newuserName, newpassword):
    if signup(newuserName, newpassword):
        st.write("new user created.")
    else:
        st.error("error occoured in signup process")
    
def show_signup_page():
    with signupSection:
        st.write("Create New User")
        newuserName = st.text_input (label="newuserName", value="", placeholder="Enter your user name")
        newpassword = st.text_input (label="newpassword", value="",placeholder="Enter password", type="password")
        st.button ("Signup", on_click=Signup_Clicked, args= (newuserName, newpassword))#argsの変数がon_clickに指定された関数に渡される

with headerSection:
    st.title("眼底検査AI Webアプリケーション")
    #first run will have nothing in session_state
    if 'loggedIn' not in st.session_state: #ログインステータスの初期化
        st.session_state['loggedIn'] = False
        st.session_state['username'] = "" # ユーザー名の初期化
        st.rerun() #強制的に再描画する
    else:
        if st.session_state['loggedIn']:
            show_logout_page()    
            show_main_page()  
        else:
            show_login_page()
            show_signup_page()
