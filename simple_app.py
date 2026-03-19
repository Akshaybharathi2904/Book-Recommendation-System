from flask import Flask, render_template_string, request
import pandas as pd

app = Flask(__name__)

# HTML Template for homepage
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Book Search System</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; min-height: 100vh;
        }
        .container { 
            max-width: 1000px; margin: 0 auto; 
            background: white; padding: 30px; border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #333; font-size: 2.5em; margin-bottom: 10px; }
        
        .search-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px; border-radius: 15px; margin-bottom: 30px;
            text-align: center; color: white;
        }
        .search-form { display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; }
        .search-input { 
            padding: 15px 20px; border: none; border-radius: 25px; 
            font-size: 16px; min-width: 300px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .search-btn { 
            background: #ff6b6b; color: white; padding: 15px 30px; 
            border: none; border-radius: 25px; font-size: 16px; font-weight: bold;
            cursor: pointer; transition: all 0.3s; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .search-btn:hover { transform: translateY(-2px); background: #ff5252; }
        
        .genres { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; margin-top: 30px;
        }
        .genre-card { 
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 20px; border-radius: 15px; text-align: center; cursor: pointer;
            transition: all 0.3s; box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .genre-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        .genre-title { font-size: 1.3em; font-weight: bold; color: #333; margin-bottom: 10px; }
        .genre-count { color: #666; font-size: 1em; }
        
        .stats { 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; margin: 30px 0;
        }
        .stat-card { 
            background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
            color: white; padding: 20px; border-radius: 15px; text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .stat-card h3 { font-size: 2em; margin-bottom: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Book Search System</h1>
            <p>Search from {{ total_books }} books across {{ genres|length }} genres</p>
        </div>
        
        <div class="search-box">
            <h2 style="margin-bottom: 20px;">🔍 Search for Books</h2>
            <form class="search-form" action="/search" method="GET">
                <input type="text" name="query" placeholder="Enter book name, author, or genre..." class="search-input" required>
                <button type="submit" class="search-btn">Search Books</button>
            </form>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>{{ total_books }}</h3>
                <p>Total Books</p>
            </div>
            <div class="stat-card">
                <h3>{{ genres|length }}</h3>
                <p>Genres</p>
            </div>
            <div class="stat-card">
                <h3>200+</h3>
                <p>Books per Genre</p>
            </div>
        </div>
        
        <h2 style="text-align: center; margin: 30px 0; color: #333;">Browse by Genre</h2>
        <div class="genres">
            {% for genre in genres %}
            <div class="genre-card" onclick="window.location.href='/search?genre={{ genre }}'">
                <div class="genre-title">
                    {% if genre == 'Comedy' %}😂 Comedy
                    {% elif genre == 'Fantasy' %}🧙♂️ Fantasy
                    {% elif genre == 'Science Fiction' %}🚀 Science Fiction
                    {% elif genre == 'Mystery' %}🔍 Mystery
                    {% elif genre == 'Romance' %}💕 Romance
                    {% elif genre == 'Horror' %}👻 Horror
                    {% elif genre == 'Classic' %}📜 Classic
                    {% else %}📚 {{ genre }}
                    {% endif %}
                </div>
                <div class="genre-count">{{ genre_counts[genre] }} books</div>
            </div>
            {% endfor %}
        </div>
        
        <div style="text-align: center; margin-top: 40px;">
            <button onclick="window.location.href='/search?genre=all'" 
                    style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; 
                           padding: 15px 30px; border: none; border-radius: 25px; font-size: 16px; 
                           font-weight: bold; cursor: pointer;">
                View All Books
            </button>
        </div>
    </div>
</body>
</html>
"""

# HTML Template for search results
SEARCH_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Search Results</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; min-height: 100vh;
        }
        .container { 
            max-width: 1200px; margin: 0 auto; 
            background: white; padding: 30px; border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .back-btn { 
            background: #667eea; color: white; padding: 10px 20px; 
            border: none; border-radius: 20px; text-decoration: none; font-weight: bold;
        }
        
        .search-box {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 20px; border-radius: 15px; margin-bottom: 20px; color: white;
        }
        .search-form { display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; }
        .search-input { 
            padding: 12px 15px; border: none; border-radius: 20px; 
            font-size: 14px; min-width: 200px;
        }
        .search-btn { 
            background: rgba(255,255,255,0.9); color: #333; padding: 12px 20px; 
            border: none; border-radius: 20px; font-weight: bold; cursor: pointer;
        }
        
        .results-info { 
            background: #e3f2fd; padding: 15px; border-radius: 10px; 
            margin-bottom: 20px; text-align: center; color: #333;
        }
        
        .book-grid { 
            display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); 
            gap: 20px; margin-bottom: 30px;
        }
        .book-card { 
            background: #f8f9fa; border: 1px solid #ddd; padding: 20px; 
            border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .book-card:hover { transform: translateY(-5px); }
        .book-title { font-weight: bold; color: #333; margin-bottom: 8px; font-size: 1.2em; }
        .book-author { color: #666; margin-bottom: 10px; font-style: italic; }
        .book-details { font-size: 14px; color: #555; line-height: 1.5; }
        .book-details div { margin-bottom: 5px; }
        
        .rating { background: #ffd700; color: #333; padding: 3px 8px; border-radius: 10px; font-weight: bold; }
        .price { background: #4caf50; color: white; padding: 3px 8px; border-radius: 10px; font-weight: bold; }
        .genre { background: #2196f3; color: white; padding: 3px 8px; border-radius: 10px; font-size: 12px; }
        
        .pagination { text-align: center; margin: 30px 0; }
        .pagination a { 
            display: inline-block; padding: 10px 15px; margin: 0 5px; 
            background: #667eea; color: white; text-decoration: none; 
            border-radius: 20px; font-weight: bold;
        }
        .pagination .current { background: #ff6b6b; }
        
        .no-results { text-align: center; padding: 50px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📖 Search Results</h1>
            <a href="/" class="back-btn">← Back to Home</a>
        </div>
        
        <div class="search-box">
            <form class="search-form" action="/search" method="GET">
                <input type="text" name="query" placeholder="Book name, author, genre..." class="search-input" value="{{ query }}">
                <select name="genre" class="search-input">
                    <option value="">All Genres</option>
                    <option value="Comedy" {% if selected_genre == 'Comedy' %}selected{% endif %}>Comedy</option>
                    <option value="Fantasy" {% if selected_genre == 'Fantasy' %}selected{% endif %}>Fantasy</option>
                    <option value="Science Fiction" {% if selected_genre == 'Science Fiction' %}selected{% endif %}>Science Fiction</option>
                    <option value="Mystery" {% if selected_genre == 'Mystery' %}selected{% endif %}>Mystery</option>
                    <option value="Romance" {% if selected_genre == 'Romance' %}selected{% endif %}>Romance</option>
                    <option value="Horror" {% if selected_genre == 'Horror' %}selected{% endif %}>Horror</option>
                    <option value="Classic" {% if selected_genre == 'Classic' %}selected{% endif %}>Classic</option>
                </select>
                <button type="submit" class="search-btn">🔍 Search</button>
            </form>
        </div>
        
        <div class="results-info">
            <strong>{{ total_results }}</strong> books found
            {% if query %} for "{{ query }}"{% endif %}
            {% if selected_genre %} in {{ selected_genre }} genre{% endif %}
            {% if total_results > 0 %} (Page {{ page }} of {{ total_pages }}){% endif %}
        </div>
        
        {% if books %}
        <div class="book-grid">
            {% for book in books %}
            <div class="book-card">
                <div class="book-title">{{ book.title }}</div>
                <div class="book-author">by {{ book.author }}</div>
                <div class="book-details">
                    <div><span class="rating">⭐ {{ book.rating }}/5</span></div>
                    <div><span class="price">${{ book.price }}</span></div>
                    <div>📄 {{ book.pages }} pages</div>
                    <div>📅 {{ book.year }}</div>
                    <div>🏢 {{ book.publisher }}</div>
                    <div><span class="genre">{{ book.genre }}</span></div>
                </div>
            </div>
            {% endfor %}
        </div>
        
        {% if total_pages > 1 %}
        <div class="pagination">
            {% if page > 1 %}
                <a href="/search?query={{ query }}&genre={{ selected_genre }}&page={{ page - 1 }}">← Previous</a>
            {% endif %}
            
            {% for p in range(1, total_pages + 1) %}
                {% if p == page %}
                    <a href="#" class="current">{{ p }}</a>
                {% elif p <= 3 or p > total_pages - 3 or (p >= page - 2 and p <= page + 2) %}
                    <a href="/search?query={{ query }}&genre={{ selected_genre }}&page={{ p }}">{{ p }}</a>
                {% endif %}
            {% endfor %}
            
            {% if page < total_pages %}
                <a href="/search?query={{ query }}&genre={{ selected_genre }}&page={{ page + 1 }}">Next →</a>
            {% endif %}
        </div>
        {% endif %}
        
        {% else %}
        <div class="no-results">
            <h2>📚 No books found</h2>
            <p>Try different search terms or browse all books.</p>
            <a href="/search?genre=all" class="back-btn">View All Books</a>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    try:
        books_df = pd.read_csv('data/books.csv')
        genres = books_df['genre'].unique().tolist()
        genre_counts = books_df['genre'].value_counts().to_dict()
        total_books = len(books_df)
        
        return render_template_string(HOME_TEMPLATE, 
                                    genres=genres, 
                                    genre_counts=genre_counts,
                                    total_books=total_books)
    except:
        return "Error: Please run 'python generate_books.py' first to create the database."

@app.route('/search')
def search():
    try:
        books_df = pd.read_csv('data/books.csv')
        
        query = request.args.get('query', '').strip()
        genre = request.args.get('genre', '').strip()
        page = int(request.args.get('page', 1))
        per_page = 20
        
        # Filter books
        filtered_books = books_df.copy()
        
        if genre and genre != 'all':
            filtered_books = filtered_books[filtered_books['genre'] == genre]
        
        if query:
            # Search in title, author, and genre
            mask = (
                filtered_books['title'].str.contains(query, case=False, na=False) |
                filtered_books['author'].str.contains(query, case=False, na=False) |
                filtered_books['genre'].str.contains(query, case=False, na=False)
            )
            filtered_books = filtered_books[mask]
        
        # Sort by rating
        filtered_books = filtered_books.sort_values('rating', ascending=False)
        
        # Pagination
        total_results = len(filtered_books)
        total_pages = (total_results + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_books = filtered_books.iloc[start_idx:end_idx]
        
        return render_template_string(SEARCH_TEMPLATE,
                                    books=page_books.to_dict('records'),
                                    query=query,
                                    selected_genre=genre,
                                    page=page,
                                    total_pages=total_pages,
                                    total_results=total_results)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    print("Starting Book Search System...")
    print("Open your browser and go to: http://localhost:5000")
    print("Database: 1400 books across 7 genres")
    print("Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='localhost', port=5000)