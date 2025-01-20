import streamlit as st 
import pyperclip


st.title("About me")
mail_adress = st.secrets["general"]["mail"]


col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

with col1:
    st.image("assets/picture.png", width=300)
with col2:
    st.title(st.secrets["general"]["name"], anchor=False)
    st.write(
        """CS Student in Frankfurt (Germany)"""
    )

    st.link_button("💻 Github", url="https://github.com/s4i10r")

    if st.button("📧 Mail"):
        pyperclip.copy(mail_adress)
        st.success("Mail adress copied!")


st.write("\n")
st.subheader("About")
st.write("""
        - Currently studying Computer Science in Frankfurt (Germany)\n
        - Aspiring IT enthusiast looking for opportunities to contribute and grow\n
        - Currently studying: C++
        """)


st.write("\n")
st.subheader("Technology", anchor=False)
st.write(
    """
    - Programming: Python, SQL\n
    - Source control: Git
    """
)       