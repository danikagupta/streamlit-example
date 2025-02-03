import streamlit as st

st.set_page_config(page_title="Auth demo", page_icon=":material/person_add:")

st.title("Auth demo!")


google_button = st.button("Google Login")

if google_button:
    st.login(provider="google")


st.write(":sparkles: :rainbow[User data]")
st.write(st.experimental_user)

query_params = st.query_params
for key, value in query_params.items():
    st.write(f"{key}: {value}")


logout_button = st.button("Logout")
if logout_button:
    st.logout()


