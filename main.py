import streamlit as st
from user import login #user.pyからよみこみ
from user import signup
# Third change in april
 
headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
signupSection = st.container()
logOutSection = st.container()
 
def show_main_page():
    with mainSection:
        dataFile = st.text_input("Enter your Test file name: ")
        Topics = st.text_input("Enter your Model Name: ")
        ModelVersion = st.text_input("Enter your Model Version: ")
        processingClicked = st.button ("Start Processing", key="processing")
        if processingClicked:
            st.balloons() 
 
def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    
def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.button ("Log Out", key="logout", on_click=LoggedOut_Clicked)
    
def LoggedIn_Clicked(userName, password):
    if login(userName, password):
        st.session_state['loggedIn'] = True
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
    st.title("Streamlit Application")
    #first run will have nothing in session_state
    if 'loggedIn' not in st.session_state: #ログインステータスの初期化
        st.session_state['loggedIn'] = False
        st.rerun() #強制的に再描画する
        # show_login_page()
        # show_signup_page()
    else:
        if st.session_state['loggedIn']:
            show_logout_page()    
            show_main_page()  
        else:
            show_login_page()
            show_signup_page()