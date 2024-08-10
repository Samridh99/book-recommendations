import requests

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

def search_books(query, max_results=10):
    params = {
        "q": query,
        "maxResults": max_results,
    }
    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
    response.raise_for_status()
    return response.json()

def get_book_details(book_id):
    url = f"{GOOGLE_BOOKS_API_URL}/{book_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()