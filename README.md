# Book Recommendation System

A data science project that implements multiple recommendation algorithms to suggest books to users.

## Features

- **Content-Based Filtering**: Recommends books based on book descriptions and features
- **Collaborative Filtering**: Recommends books based on user behavior and ratings
- **Genre-Based Search**: Search and filter books by genre (Comedy, Fantasy, Horror, etc.)
- **Expanded Book Database**: 40+ books across 7 different genres
- **Interactive Search**: User-friendly genre search interface
- **Sample Data**: Includes comprehensive book data for testing

## Project Structure

```
book_recommendation_system/
├── data/                   # Dataset files
│   └── books.csv          # Book database with genres
├── notebooks/              # Jupyter notebooks for analysis
│   └── data_exploration.ipynb
├── src/                    # Source code
│   └── recommendation_system.py
├── models/                 # Saved models
├── main.py                # Main execution script
├── genre_search.py        # Interactive genre search
├── demo_comedy.py         # Comedy books demo
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the main script:
```bash
python main.py
```

3. Search books by genre interactively:
```bash
python genre_search.py
```

4. View comedy books demo:
```bash
python demo_comedy.py
```

5. Explore data in Jupyter notebook:
```bash
jupyter notebook notebooks/data_exploration.ipynb
```

## Algorithms Implemented

### Content-Based Filtering
- Uses TF-IDF vectorization on book descriptions
- Calculates cosine similarity between books
- Recommends similar books based on content

### Collaborative Filtering
- Uses Singular Value Decomposition (SVD)
- Finds similar users based on rating patterns
- Recommends books liked by similar users

### Genre-Based Filtering
- Search books by genre categories
- Filter by Comedy, Fantasy, Science Fiction, Mystery, Romance, Horror, Classic
- Sort results by rating and popularity

## Data Sources

You can use datasets from:
- Goodreads API
- Amazon Books dataset
- Book-Crossing dataset
- Kaggle book datasets

## Available Genres

- **Comedy** (10 books): Humorous novels, memoirs, and satirical works
- **Fantasy** (5 books): Epic fantasy, magical adventures, and mythical worlds
- **Science Fiction** (5 books): Space opera, cyberpunk, and futuristic stories
- **Mystery** (5 books): Thrillers, detective stories, and psychological suspense
- **Romance** (5 books): Love stories, romantic comedies, and relationship dramas
- **Horror** (5 books): Scary stories, supernatural thrillers, and psychological horror
- **Classic** (5 books): Timeless literature and canonical works

## Usage Examples

### Search Comedy Books
```python
from src.recommendation_system import BookRecommendationSystem
import pandas as pd

recommender = BookRecommendationSystem()
recommender.load_data('data/books.csv')
comedy_books = recommender.search_by_genre('Comedy')
print(comedy_books)
```

### Interactive Search
```bash
python genre_search.py
# Then type: comedy
# Or: fantasy
# Or: all (to see all books)
```

## Next Steps

- [ ] Add hybrid recommendation system
- [ ] Implement deep learning models
- [ ] Add web interface with Flask/Streamlit
- [ ] Include book cover images
- [ ] Add real-time recommendations
- [ ] Expand book database with more titles
- [ ] Add user rating system