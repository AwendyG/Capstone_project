import streamlit as st
from Kaggle_data import df
from Movie_filter import get_recommendations
from datetime import datetime

def run_ui():
    st.title("🎬 Movie Recommender")

    # Dropdown (searchable, handles ~7k movies)
    movie_title = st.selectbox("Pick a movie you like:", df["title"].tolist())

    if st.button("Get Recommendations"):
        results = get_recommendations(movie_title, top_n=5)

        if not results:
            st.warning("No similar movies found.")
        else:
            st.write(f"Because you liked **{movie_title}**, you might also enjoy:")
            for name, date, desc, score in results:
                st.subheader(name)

                # ✅ Safe date formatting
                if isinstance(date, str):
                    try:
                        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
                        st.caption(f"Release Date: {parsed_date} | Similarity Score: {score}")
                    except Exception:
                        st.caption(f"Release Date: Unknown | Similarity Score: {score}")
                else:
                    st.caption(f"Release Date: {date} | Similarity Score: {score}")

                st.write(desc)
                st.markdown("---")
