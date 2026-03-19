#!/usr/bin/env python3
"""
Enhanced Book Recommendation System Launcher
Run this script to start the beautiful book discovery application
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    required_packages = ['flask', 'pandas']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:", ', '.join(missing_packages))
        print("📦 Installing missing packages...")
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ Successfully installed {package}")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                return False
    
    return True

def check_data_file():
    """Check if books.csv exists, if not create sample data"""
    data_file = Path('data/books.csv')
    
    if not data_file.exists():
        print("📚 Books data not found. Creating sample data...")
        
        # Create data directory if it doesn't exist
        data_file.parent.mkdir(exist_ok=True)
        
        # Try to run the data generation script
        try:
            if Path('generate_books.py').exists():
                subprocess.run([sys.executable, 'generate_books.py'], check=True)
                print("✅ Sample book data created successfully!")
            else:
                print("❌ Data generation script not found. Please ensure generate_books.py exists.")
                return False
        except subprocess.CalledProcessError:
            print("❌ Failed to generate sample data")
            return False
    else:
        print("✅ Books data found!")
    
    return True

def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting Enhanced Book Discovery Hub...")
    print("📚 Features included:")
    print("   • Beautiful colorful interface with gradients")
    print("   • Book cover images for all books")
    print("   • Advanced search with filters")
    print("   • Autocomplete search suggestions")
    print("   • Grid and list view options")
    print("   • Detailed book pages with recommendations")
    print("   • Interactive statistics dashboard")
    print("   • Mobile-responsive design")
    
    try:
        # Import and run the enhanced app
        from enhanced_search_app import app
        
        print("\n🌐 Application will open in your browser automatically...")
        print("📍 URL: http://localhost:5001")
        print("⏹️  Press Ctrl+C to stop the server")
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:5001')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start the Flask app
        app.run(debug=False, host='0.0.0.0', port=5001)
        
    except ImportError as e:
        print(f"❌ Failed to import enhanced_search_app: {e}")
        return False
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        return False
    
    return True

def main():
    """Main function to run the enhanced book recommendation system"""
    print("=" * 60)
    print("📚 ENHANCED BOOK DISCOVERY HUB")
    print("🎨 Beautiful • 🔍 Searchable • 📱 Responsive")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path('enhanced_search_app.py').exists():
        print("❌ Please run this script from the book_recommendation_system directory")
        print("📁 Current directory:", os.getcwd())
        return
    
    # Step 1: Check requirements
    print("\n1️⃣ Checking requirements...")
    if not check_requirements():
        print("❌ Failed to install required packages")
        return
    
    # Step 2: Check data file
    print("\n2️⃣ Checking book data...")
    if not check_data_file():
        print("❌ Failed to prepare book data")
        return
    
    # Step 3: Start application
    print("\n3️⃣ Starting application...")
    start_application()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for using Book Discovery Hub!")
        print("📚 Happy reading!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("🔧 Please check the error message above and try again.")