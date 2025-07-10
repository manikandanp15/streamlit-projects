import streamlit as st

st.title("My first streamlit app")

name = st.text_input ("Enter your name")

if st.button("say Hello"):

    if name:
        st.success(f"hello {name} ,welcome to my page")
    else:
       st.warning("please enter your name")

