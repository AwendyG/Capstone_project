# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import kagglehub
from kagglehub import KaggleDatasetAdapter

file_path = "movies.csv"

df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "fahmidasultanamahi/tmdb-movie-data-till-2024",
    file_path,
)

# ✅ Ensure required column exists
if "title" not in df.columns:
    raise KeyError(f"Expected 'title' column not found. Available: {df.columns.tolist()}")

print("First 5 records:", df.head())
