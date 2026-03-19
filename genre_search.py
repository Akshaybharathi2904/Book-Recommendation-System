from src.recommendation_system import BookRecommendationSystem
import pandas as pd

def interactive_genre_search():
    """Interactive genre search functionality"""
    # Load the book data
    recommender = BookRecommendationSystem()
    books_df = pd.read_csv('data/books.csv')
    recommender.load_data('data/books.csv')
    
    print("BOOK GENRE SEARCH SYSTEM")
    print("=" * 50)
    
    # Show available genres
    genres = books_df['genre'].unique()
    print("\nAvailable Genres:")
    for i, genre in enumerate(genres, 1):
        count = len(books_df[books_df['genre'] == genre])
        print(f"  {i}. {genre} ({count} books)")
    
    print("\n" + "=" * 50)
    print("Tips:")
    print("  - Type genre name (e.g., 'comedy', 'fantasy', 'horror')")
    print("  - Search is case-insensitive")
    print("  - Type 'all' to see all books")
    print("  - Type 'quit' to exit")
    print("=" * 50)
    
    while True:
        genre_input = input("\nEnter genre to search: ").strip()
        
        if genre_input.lower() == 'quit':
            print("Thanks for using the Book Search System!")
            break
        
        if genre_input.lower() == 'all':
            print(f"\nALL BOOKS ({len(books_df)} total):")
            print("-" * 60)
            all_books = books_df[['title', 'author', 'genre', 'rating']].sort_values('rating', ascending=False)
            print(all_books.to_string(index=False))
            continue
        
        # Search for books by genre
        genre_books = books_df[books_df['genre'].str.contains(genre_input, case=False, na=False)]
        
        if len(genre_books) > 0:
            print(f"\nFound {len(genre_books)} books in '{genre_input.title()}' genre:")
            print("-" * 60)
            results = genre_books[['title', 'author', 'genre', 'rating']].sort_values('rating', ascending=False)
            print(results.to_string(index=False))
            
            # Show average rating for the genre
            avg_rating = genre_books['rating'].mean()
            print(f"\nAverage rating for {genre_input.title()} books: {avg_rating:.1f}")
            
        else:
            print(f"No books found for genre '{genre_input}'")
            print(f"Available genres: {', '.join(genres)}")

if __name__ == "__main__":
    interactive_genre_search()