from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
url = "http://books.toscrape.com"
import pandas as pd 

# a function to extract the link of the needed pages, as specified by the page_amt argument in the function.
def page_to_scrape(url, page_amt):
    driver.get(url)
    pages_links = []
    for page in range(1,page_amt):
        page = "http://books.toscrape.com/catalogue/page-{}.html".format(page)
        pages_links.append(page)
    return pages_links

# this function extracts and returns all the books in a page.
def page_books(link):
    page_books =[]
    driver.get(link)
    books_in_page = driver.find_elements(By.XPATH, "//article[@class = 'product_pod']")
    for book in books_in_page:
        each_book = book.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, "a").get_attribute('href')
        page_books.append(each_book)
    return page_books

# this function does the proper scraping.
def bookscraper():
    BookName, Price, StockStatus, Rating, Description, ProductInfo, Category = [],[],[],[],[],[],[]
    pages_links = page_to_scrape(url, 3)
    for link in pages_links:
        books_in_page = page_books(link)
        for book_link  in books_in_page:
            # this retrives the value of the href key for all the book in a book page.
            
            driver.get(book_link)
            name = driver.find_element(By.TAG_NAME, 'h1').text
            BookName.append(name)
            price = driver.find_element(By.XPATH, " //p[@class = 'price_color']").text
            Price.append(price)
            stock_status = driver.find_element(By.XPATH, "//p[@ class = 'instock availability']").text
            StockStatus.append(stock_status)
            rating = driver.find_element(By.CSS_SELECTOR, " #content_inner > article > div.row > div.col-sm-6.product_main > p.star-rating.Three").get_attribute('class')
            Rating.append(rating)
            description = driver.find_element(By.CSS_SELECTOR, " #content_inner > article > p").text
            Description.append(description)
            product_information = driver.find_element(By.TAG_NAME, "tr").text
            ProductInfo.append(product_information)
            category = driver.find_element(By.CSS_SELECTOR, "#default > div > div > ul > li:nth-child(3) > a").text
            Category.append(category)
    
    book_catelouge = {"BookName": BookName, "Price": Price, "StockStaus": StockStatus, "Description": Description, "ProductInfo": ProductInfo, "Category": Category }
    df = pd.DataFrame(book_catelouge)
    df.to_csv("the first three pages.csv")
    df = pd.read_csv("first three pages.csv")
    df
    driver.quit()
    return book_catelouge


bookscraper()  
