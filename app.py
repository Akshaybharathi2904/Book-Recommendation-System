from flask import Flask, render_template, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

# Load book data
books_df = None

def load_books():
    global books_df
    try:
        books_df = pd.read_csv('data/books.csv')
        return True
    except:
        return False

@app.route('/')
def index():
    if not load_books():
        return "Error: Books data not found. Run generate_books.py first."
    
    genres = books_df['genre'].unique().tolist()
    total_books = len(books_df)
    genre_counts = books_df['genre'].value_counts().to_dict()
    
    return render_template('index.html', 
                         genres=genres, 
                         total_books=total_books,
                         genre_counts=genre_counts)

@app.route('/search')
def search():
    genre = request.args.get('genre', '')
    page = int(request.args.get('page', 1))
    per_page = 20
    
    if genre and genre != 'all':
        filtered_books = books_df[books_df['genre'].str.contains(genre, case=False, na=False)]
    else:
        filtered_books = books_df
    
    # Sort by rating
    filtered_books = filtered_books.sort_values('rating', ascending=False)
    
    # Pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_books = filtered_books.iloc[start_idx:end_idx]
    
    total_pages = (len(filtered_books) + per_page - 1) // per_page
    
    return render_template('search.html',
                         books=page_books.to_dict('records'),
                         genre=genre,
                         page=page,
                         total_pages=total_pages,
                         total_books=len(filtered_books))

@app.route('/api/books')
def api_books():
    genre = request.args.get('genre', '')
    
    if genre and genre != 'all':
        filtered_books = books_df[books_df['genre'].str.contains(genre, case=False, na=False)]
    else:
        filtered_books = books_df
    
    return jsonify(filtered_books.to_dict('records'))

@app.route('/stats')
def stats():
    if not books_df is not None:
        return "No data available"
    
    stats_data = {
        'total_books': len(books_df),
        'genres': books_df['genre'].nunique(),
        'avg_rating': round(books_df['rating'].mean(), 2),
        'avg_price': round(books_df['price'].mean(), 2),
        'genre_stats': books_df.groupby('genre').agg({
            'rating': ['mean', 'count'],
            'price': 'mean'
        }).round(2).to_dict()
    }
    
    return render_template('stats.html', stats=stats_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)