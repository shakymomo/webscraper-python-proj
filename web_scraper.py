import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_books(base_url, num_pages):
    book_data = []

    for page in range(1, num_pages + 1):
        url = base_url.format(page)
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')

        if not books:
            break  # No more books found, exit the loop

        for book in books:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').get_text()
            book_data.append([title, price])

    df = pd.DataFrame(book_data, columns=['Title', 'Price'])
    df.to_csv('books.csv', index=False)
    print("Books data has been saved to books.csv")


if __name__ == '__main__':
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    num_pages = 5  # Adjust this number to scrape more pages
    scrape_books(base_url, num_pages)

