from Kaggle_data import df
from datetime import datetime

def parse_date_safe(date_str):
    """Convert release_date safely to ordinal."""
    try:
        return datetime.strptime(str(date_str), "%Y-%m-%d").toordinal()
    except Exception:
        return 0

def get_recommendations(selected_title, top_n=5):
    """
    Recommend movies based on description word overlap.
    """
    movie = df[df["title"].str.lower() == selected_title.lower()]
    if movie.empty:
        return []

    selected_desc = str(movie.iloc[0]["overview"])
    selected_words = set(selected_desc.lower().split())

    similarities = []
    for _, row in df.iterrows():
        if row["title"].lower() == selected_title.lower():
            continue  # skip the same movie

        desc_words = set(str(row["overview"]).lower().split())
        overlap = len(selected_words & desc_words)

        if overlap > 0:
            similarities.append((
                row["title"],
                row.get("release_date", ""),
                row.get("overview", ""),
                overlap
            ))

    # ✅ Sort safely: highest overlap first, then latest release date
    similarities.sort(key=lambda x: (-x[3], -parse_date_safe(x[1])))

    return similarities[:top_n]
