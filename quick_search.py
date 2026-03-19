import pandas as pd

def search_books():
    """Quick search for books by genre"""
    try:
        books_df = pd.read_csv('data/books.csv')
    except:
        print("Error: Run generate_books.py first to create the database")
        return
    
    print("BOOK SEARCH SYSTEM")
    print("=" * 50)
    print(f"Database: {len(books_df)} books across {books_df['genre'].nunique()} genres")
    
    # Show available genres
    genres = books_df['genre'].unique()
    print("\nAvailable Genres:")
    for i, genre in enumerate(genres, 1):
        count = len(books_df[books_df['genre'] == genre])
        print(f"  {i}. {genre} ({count} books)")
    
    print("\nType a genre name to search (e.g., 'comedy', 'fantasy', 'horror')")
    print("Type 'quit' to exit")
    print("=" * 50)
    
    while True:
        genre_input = input("\nEnter genre: ").strip()
        
        if genre_input.lower() == 'quit':
            break
        
        # Search for books
        results = books_df[books_df['genre'].str.contains(genre_input, case=False, na=False)]
        
        if len(results) > 0:
            print(f"\nFound {len(results)} books in '{genre_input.title()}' genre:")
            print("-" * 80)
            
            # Show first 20 books with details
            display_books = results.head(20)
            for idx, book in display_books.iterrows():
                print(f"{book['title']}")
                print(f"   Author: {book['author']}")
                print(f"   Rating: {book['rating']}/5.0 | Price: ${book['price']} | Pages: {book['pages']}")
                print(f"   Publisher: {book['publisher']} ({book['year']})")
                print()
            
            if len(results) > 20:
                print(f"... and {len(results) - 20} more books")
            
            # Show statistics
            avg_rating = results['rating'].mean()
            avg_price = results['price'].mean()
            print(f"\nGenre Statistics:")
            print(f"   Average Rating: {avg_rating:.1f}/5.0")
            print(f"   Average Price: ${avg_price:.2f}")
            print(f"   Total Books: {len(results)}")
            
        else:
            print(f"No books found for '{genre_input}'")
            print(f"Available genres: {', '.join(genres)}")

if __name__ == "__main__":
    search_books()