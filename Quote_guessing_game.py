import requests
from bs4 import BeautifulSoup
from csv import writer
from time import sleep
from random import choice

#list to store scrapped data
all_quotes = []

#this part of the url is Constant 
base_url = "http://quotes.toscrape.com/"

#thi part of the url will keep changing
url = "/page/1"

while url:
    #concatenating both urls
    # Making request 

    res = requests.get(f"{base_url}{url}")
    print(f"Now scraping {base_url}{url}")

# res.text provides the raw HTML content.
# BeautifulSoup(res.text) transforms this raw HTML
# into a structured object that you can easily manipulate.

    soup = BeautifulSoup(res.text, "html.phrase")

    quotes = soup.find_all(class_ = "quote") # because the content we need is present in the class called quote

    for quote in quotes:
        all_quotes.append({
            "text": quote.find(class_ = "text").get_text(),
            "author": quote.find(class_="author").get_text(),
            "bro-link": quote.find("a")["href"]
        })

    next_btn = soup.find(class_ = "next") # this _class might be a typo mistake so check this part if any error and change it to class_
    url = next_btn.find("a")["href"] if next_btn else None
    sleep(2)

quote = choice(all_quotes)
remaining_guesses = 4
print("Here is the quote")
print(quote,["text"])

guess = " "

while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
    guess = input( f"Who said this quote? Guesses remaining {remaining_guesses}")

    if guess == quote["author"]:
        print("congo you GOT IT RIGHT somehow, and I successfully wasted precious time of you life, it's a win win")
        break
    remaining_guesses = -1

    if remaining_guesses == 3:
        res = requests.get(f"{base_url}{quote['bio-link']}")
        soup = BeautifulSoup(res.text, "html.parser")
        birth_date = soup.find(class_="author-born-date").get_text()
        birth_place = soup.find(class_="author-born-location").get_text()
        print(
            f"Here's a hint: The author was born on {birth_date}{birth_place}")
    elif remaining_guesses == 2:
         print(
            f"Here's a hint: The author's first name starts with: {quote['author'][0]}")
         
    elif remaining_guesses == 1:
        last_initials = quote["author"].split(" ")[1][0]
        print(
            f"Here's a hint: The author's last name starts with: {last_initials}")
     
    else:
        print(
            f"Sorry, you ran out of guesses. The answer was {quote['author']}")
        
    
   
    
        
     


