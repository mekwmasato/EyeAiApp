import streamlit as st

import socket

###
HOST = '172.31.35.121'
PORT = 12345
###
 
headerSection = st.container()
mainSection = st.container()

 
def show_main_page():
    with mainSection:
        uploaded_image = st.file_uploader("眼底画像をアップロード",type=["png", "jpg"])

        if st.button ("Start Processing", key="processing"):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((HOST, PORT))
                print("サーバーに接続しました。")

                # 画像のデータを読み込み、送信
                image_data = uploaded_image.read()
                client_socket.sendall(image_data)  # 画像データ全体を一括で送信
                st.write("画像を送信しました。")
 
with headerSection:
    st.title("眼底検査AI Webアプリケーション")
    show_main_page()  
