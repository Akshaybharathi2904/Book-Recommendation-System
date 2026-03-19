from flask import Flask, render_template, request, jsonify
import pandas as pd
import webbrowser
import threading
import time

app = Flask(__name__)
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
    book_name = request.args.get('book_name', '')
    author = request.args.get('author', '')
    min_rating = request.args.get('min_rating', '')
    max_price = request.args.get('max_price', '')
    page = int(request.args.get('page', 1))
    per_page = 20
    
    filtered_books = books_df.copy()
    
    # Filter by genre
    if genre and genre != 'all':
        filtered_books = filtered_books[filtered_books['genre'].str.contains(genre, case=False, na=False)]
    
    # Filter by book name
    if book_name:
        filtered_books = filtered_books[filtered_books['title'].str.contains(book_name, case=False, na=False)]
    
    # Filter by author
    if author:
        filtered_books = filtered_books[filtered_books['author'].str.contains(author, case=False, na=False)]
    
    # Filter by minimum rating
    if min_rating:
        try:
            min_rating_float = float(min_rating)
            filtered_books = filtered_books[filtered_books['rating'] >= min_rating_float]
        except ValueError:
            pass
    
    # Filter by maximum price
    if max_price:
        try:
            max_price_float = float(max_price)
            filtered_books = filtered_books[filtered_books['price'] <= max_price_float]
        except ValueError:
            pass
    
    filtered_books = filtered_books.sort_values('rating', ascending=False)
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_books = filtered_books.iloc[start_idx:end_idx]
    
    total_pages = (len(filtered_books) + per_page - 1) // per_page
    
    return render_template('search.html',
                         books=page_books.to_dict('records'),
                         genre=genre,
                         book_name=book_name,
                         author=author,
                         min_rating=min_rating,
                         max_price=max_price,
                         page=page,
                         total_pages=total_pages,
                         total_books=len(filtered_books))

@app.route('/quick_search')
def quick_search():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    # Search in title and author
    results = books_df[
        (books_df['title'].str.contains(query, case=False, na=False)) |
        (books_df['author'].str.contains(query, case=False, na=False))
    ].head(10)
    
    return jsonify([
        {
            'title': book['title'],
            'author': book['author'],
            'genre': book['genre'],
            'rating': book['rating'],
            'price': book['price']
        }
        for _, book in results.iterrows()
    ])

@app.route('/stats')
def stats():
    if books_df is None:
        return "No data available"
    
    genre_stats = books_df.groupby('genre').agg({
        'rating': ['mean', 'count'],
        'price': 'mean'
    }).round(2)
    
    stats_data = {
        'total_books': len(books_df),
        'genres': books_df['genre'].nunique(),
        'avg_rating': round(books_df['rating'].mean(), 2),
        'avg_price': round(books_df['price'].mean(), 2),
        'genre_stats': genre_stats.to_dict()
    }
    
    return render_template('stats.html', stats=stats_data)

def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("Starting Book Recommendation System...")
    print("Database loaded: 1400 books across 7 genres")
    print("Opening browser at http://localhost:5000")
    
    # Open browser automatically
    threading.Thread(target=open_browser).start()
    
    app.run(debug=False, host='localhost', port=5000)