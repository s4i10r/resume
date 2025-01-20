import streamlit as st

# Routing
about_page = st.Page(
    page="views/about.py",
    title="About me",
    icon="⚡",
    default=True,
)

blog_page = st.Page(
    page="views/blog.py",
    title="Blog",
    icon="📚",
)

weather = st.Page(
    page="views/weather.py",
    title="Weather History",
    icon="🌂",
)


# Navigation
pg = st.navigation(
    {
        "About": {about_page, blog_page},
        "Projects": {weather}
    }
)

pg.run()