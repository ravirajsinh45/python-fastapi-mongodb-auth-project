import streamlit as st
import os
import requests
import json
import pandas as pd
from decouple import config

register_url = f"{config('BACKEND_URL')}/api/auth/register"
login_url = f"{config('BACKEND_URL')}/api/auth/login"
refresh_url = f"{config('BACKEND_URL')}/api/auth/refresh"




def login_api(login_url,user_name,password):
   
    payload = json.dumps({
    "email": user_name,
    "password": password
    })
    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", login_url, headers=headers, data=payload)
    # print(response.cookies)

    return response
    # print(response.text)


def refresh(url,cookies):
    payload = {}
    cookies=cookies
    response = requests.request("GET", url, cookies=cookies, data=payload)
    return response



# Initialize session state if it doesn't exist
if 'username' not in st.session_state:
    st.session_state.username = ""
    st.session_state.signed_in = False
    st.session_state.cookies = []

def sign_in():
    """
    Sign in form 
    """
    st.subheader("Please Enter Credentials")
    username = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        auth_response = login_api(login_url, username, password)
        response = json.loads(auth_response.text)
        if auth_response.status_code == 200:
            if response['status'] == "success":
                st.session_state.username = username
                st.session_state.signed_in = True
                st.session_state.cookies = auth_response.cookies
            else:
                st.error("Invalid username or password")

def sign_up():
    """
    Sign up form
    """
    st.subheader("Sign Up")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match")
        else:
            payload = {
                    "name": name,
                    "email":email,
                    "role": "user",
                    "password": password,
                    "passwordConfirm": confirm_password,
                    }
            response = requests.post(register_url, json=payload)
            if response.status_code == 201:
                st.success("Registration successful. You can now log in.")
            else:
                st.error("Registration failed. Please try again")

def main():
    st.title("Welcome to demo auth application!")

    if st.session_state.signed_in:
        st.sidebar.write(f"User: {st.session_state.username}")
        if st.sidebar.button("Log Out"):
            st.session_state.signed_in = False
            st.session_state.username = None
            st.session_state.current_page = "login"
        else:
            st.write(f"Welcome, {st.session_state.username}!")
    else:
        st.session_state.current_page = st.radio("Select a Page", ["Login", "Sign Up"])
        if st.session_state.current_page == "Login":
            sign_in()
        else:
            sign_up()

if __name__ == "__main__":
    main()