from Kaggle_data import df
import re
from datetime import datetime
from nltk.stem import PorterStemmer

# --- Stemming helper ---
stemmer = PorterStemmer()

def tokenize_and_stem(text):
    """Lower, remove non-letters, split and stem -> return set of stems."""
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    stems = [stemmer.stem(w) for w in words]
    return set(stems)

# --- Safe date parser ---
def parse_date_safe(date_str):
    try:
        return datetime.strptime(str(date_str), "%Y-%m-%d").toordinal()
    except Exception:
        return 0

# --- Recommendation function (fixed duplicate issue) ---
def get_recommendations(selected_title, top_n=None, dedupe_by_title=True):
    """
    Find movies whose titles contain selected_title, pick the first match as the
    "selected" movie, then search all movies for description-word overlap.

    top_n: if given, return only the top N matches; otherwise return all matches.
    dedupe_by_title: if True, return only one recommendation per movie title
                     (prevents repeated identical titles). Set False to allow
                     different rows with same title (e.g., remakes) to appear.
    """
    # find candidate selected rows (title contains the search text)
    movies = df[df["title"].str.lower().str.contains(selected_title.lower(), na=False)]
    if movies.empty:
        return []

    # choose the first matched movie as the 'selected' one
    selected_movie = movies.iloc[0]
    selected_index = selected_movie.name
    selected_desc = str(selected_movie.get("overview", ""))
    selected_words = tokenize_and_stem(selected_desc)

    similarities = []
    seen = set()  # used to avoid adding the same title/overview multiple times

    for idx, row in df.iterrows():
        # skip the exact same row (same index)
        if idx == selected_index:
            continue

        # skip rows that are exact duplicates of the selected row
        # (same title and same overview). This avoids the "same movie repeated" issue.
        if (str(row.get("title", "")).lower() == str(selected_movie.get("title", "")).lower()
                and str(row.get("overview", "")) == selected_desc):
            continue

        desc_words = tokenize_and_stem(row.get("overview", ""))
        overlap = len(selected_words & desc_words)

        if overlap > 0:
            title = row.get("title", "")
            release = row.get("release_date", "")
            overview = row.get("overview", "")

            # build dedupe key
            if dedupe_by_title:
                key = title.strip().lower()
            else:
                # allow same title if overview differs (keeps remakes separate)
                key = (title.strip().lower(), str(overview))

            if key in seen:
                # already added this title/overview -> skip to avoid duplicates
                continue
            seen.add(key)

            similarities.append((title, release, overview, overlap))

    # sort by overlap desc, then by release date (newest first)
    similarities.sort(key=lambda x: (-x[3], -parse_date_safe(x[1])))

    # return top_n if requested, else all matches
    if top_n:
        return similarities[:top_n]
    return similarities
