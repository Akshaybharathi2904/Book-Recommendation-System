from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import random

app = Flask(__name__)

# Load book data
books_df = None

def load_books():
    global books_df
    try:
        books_df = pd.read_csv('data/books.csv')
        # Add book cover images (placeholder URLs)
        books_df['cover_image'] = books_df.apply(lambda x: generate_book_cover_url(x['title'], x['genre']), axis=1)
        return True
    except:
        return False

def generate_book_cover_url(title, genre):
    """Generate placeholder book cover URLs"""
    # Using picsum.photos for random book-like images
    seed = abs(hash(title)) % 1000
    colors = {
        'Comedy': ['ffd93d', 'ff6b6b', 'ff9ff3'],
        'Fantasy': ['6c5ce7', 'a29bfe', '74b9ff'],
        'Science Fiction': ['00cec9', '55a3ff', '81ecec'],
        'Mystery': ['2d3436', '636e72', 'b2bec3'],
        'Romance': ['fd79a8', 'fdcb6e', 'e84393'],
        'Horror': ['2d3436', '636e72', 'a29bfe'],
        'Classic': ['6c5ce7', 'fdcb6e', 'fd79a8']
    }
    
    color = random.choice(colors.get(genre, ['74b9ff']))
    return f"https://picsum.photos/seed/{seed}/300/400"

@app.route('/')
def index():
    if not load_books():
        return "Error: Books data not found. Run generate_books.py first."
    
    genres = books_df['genre'].unique().tolist()
    total_books = len(books_df)
    genre_counts = books_df['genre'].value_counts().to_dict()
    
    # Get featured books (highest rated from each genre)
    featured_books = []
    for genre in genres[:6]:  # Show 6 featured books
        genre_books = books_df[books_df['genre'] == genre].nlargest(1, 'rating')
        if not genre_books.empty:
            featured_books.append(genre_books.iloc[0].to_dict())
    
    return render_template('enhanced_index.html', 
                         genres=genres, 
                         total_books=total_books,
                         genre_counts=genre_counts,
                         featured_books=featured_books)

@app.route('/search')
def search():
    # Get search parameters
    book_name = request.args.get('book_name', '').strip()
    author = request.args.get('author', '').strip()
    genre = request.args.get('genre', '').strip()
    min_rating = request.args.get('min_rating', '')
    max_price = request.args.get('max_price', '')
    page = int(request.args.get('page', 1))
    per_page = 12
    
    # Start with all books
    filtered_books = books_df.copy()
    
    # Apply filters
    if book_name:
        filtered_books = filtered_books[
            filtered_books['title'].str.contains(book_name, case=False, na=False)
        ]
    
    if author:
        filtered_books = filtered_books[
            filtered_books['author'].str.contains(author, case=False, na=False)
        ]
    
    if genre and genre != 'all' and genre != '':
        filtered_books = filtered_books[
            filtered_books['genre'].str.contains(genre, case=False, na=False)
        ]
    
    if min_rating:
        filtered_books = filtered_books[filtered_books['rating'] >= float(min_rating)]
    
    if max_price:
        filtered_books = filtered_books[filtered_books['price'] <= float(max_price)]
    
    # Sort by rating (highest first)
    filtered_books = filtered_books.sort_values('rating', ascending=False)
    
    # Pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_books = filtered_books.iloc[start_idx:end_idx]
    
    total_pages = (len(filtered_books) + per_page - 1) // per_page
    
    # Search summary
    search_params = {
        'book_name': book_name,
        'author': author,
        'genre': genre,
        'min_rating': min_rating,
        'max_price': max_price
    }
    
    return render_template('enhanced_search.html',
                         books=page_books.to_dict('records'),
                         search_params=search_params,
                         page=page,
                         total_pages=total_pages,
                         total_books=len(filtered_books),
                         genres=books_df['genre'].unique().tolist())

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """Show detailed view of a single book"""
    book = books_df[books_df['book_id'] == book_id]
    if book.empty:
        return "Book not found", 404
    
    book_data = book.iloc[0].to_dict()
    
    # Get similar books (same genre, similar rating)
    similar_books = books_df[
        (books_df['genre'] == book_data['genre']) & 
        (books_df['book_id'] != book_id) &
        (abs(books_df['rating'] - book_data['rating']) <= 0.5)
    ].nlargest(6, 'rating')
    
    return render_template('book_detail.html',
                         book=book_data,
                         similar_books=similar_books.to_dict('records'))

@app.route('/api/search')
def api_search():
    """API endpoint for AJAX search"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify([])
    
    # Search in title and author
    results = books_df[
        books_df['title'].str.contains(query, case=False, na=False) |
        books_df['author'].str.contains(query, case=False, na=False)
    ].head(10)
    
    return jsonify(results[['book_id', 'title', 'author', 'genre', 'rating', 'cover_image']].to_dict('records'))

@app.route('/stats')
def stats():
    if books_df is None:
        return "No data available"
    
    stats_data = {
        'total_books': len(books_df),
        'genres': books_df['genre'].nunique(),
        'avg_rating': round(books_df['rating'].mean(), 2),
        'avg_price': round(books_df['price'].mean(), 2),
        'genre_stats': books_df.groupby('genre').agg({
            'rating': ['mean', 'count'],
            'price': 'mean'
        }).round(2).to_dict(),
        'top_rated': books_df.nlargest(10, 'rating').to_dict('records'),
        'price_ranges': {
            'Under $15': len(books_df[books_df['price'] < 15]),
            '$15-$25': len(books_df[(books_df['price'] >= 15) & (books_df['price'] < 25)]),
            '$25+': len(books_df[books_df['price'] >= 25])
        }
    }
    
    return render_template('enhanced_stats.html', stats=stats_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)