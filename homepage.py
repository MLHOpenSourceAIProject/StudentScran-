import streamlit as st

st.set_page_config(page_title="StudentScran", page_icon="🍳", layout="wide")

st.title("Your week...")
st.subheader("Your Week")


col1, col2, col3 = st.columns(3)
col4, col5, col6, col7 = st.columns(4)

with col1:
    st.markdown("### Monday")
    st.info("Quick Pesto Pasta 🍝")

with col2:
    st.markdown("### Tuesday")
    st.info("Tuna Jacket Potato 🥔")

with col3:
    st.markdown("### Wednesday")
    st.info("Chicken Stir-Fry 🍜")

with col4:
    st.markdown("### Thursday")
    st.info("Chicken Stir-Fry 🍜")

with col5:
    st.markdown("### Friday")
    st.info("Chicken Stir-Fry 🍜")

with col6:
    st.markdown("### Saturday")
    st.info("Chicken Stir-Fry 🍜")

with col7:
    st.markdown("### Sunday")
    st.info("Chicken Stir-Fry 🍜")

st.sidebar.title("StudentScran")
st.sidebar.radio("Go to", ["Home", "Upload Food", "Meal Ideas"])