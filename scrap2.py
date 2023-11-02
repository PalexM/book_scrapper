import requests
from bs4 import BeautifulSoup
import csv
import re

# URL-ul paginii web pe care dorești să o scrapperi


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

data = []

with open("oras.txt", "r", encoding="utf-8") as oras_file:
    for line in oras_file:
        data.append(line.strip().split(","))

data_list = []
count = 0
for line in data:
    if count >= 1:
        break
    response = requests.get(line[2], headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    listing_elements = soup.find_all("div", class_="listing-item")
    _list = []
    for listing in listing_elements:
        company_address = (
            listing.find("div", class_="company-address").h4.a.get_text().strip()
        )
        company_number = (
            listing.find("div", class_="company-contact-number").h4.a.get_text().strip()
        )
        contact_link = listing.find(
            "a", class_="btn btn-blue city contact-management-btn"
        )["href"]
        hidden_info = (
            listing.find("a", class_="btn btn-blue city contact-management-btn")
            .span.get_text()
            .strip()
        )
        _list.append([hidden_info, company_address, company_number, contact_link])
    data_list.append([line[0], line[1], _list])
    count += 1

headers = [
    "City",
    "State",
    "Company Name",
    "Company Adress",
    "Company Phone Number",
    "Contact Company Link",
    "Company Name",
    "Company Adress",
    "Company Phone Number",
    "Contact Company Link",
    "Company Name",
    "Company Adress",
    "Company Phone Number",
    "Contact Company Link",
    "Company Name",
    "Company Adress",
    "Company Phone Number",
    "Contact Company Link",
    "Company Name",
    "Company Adress",
    "Company Phone Number",
    "Contact Company Link",
    "Company Name",
    "Company Adress",
    "Company Phone Number",
    "Contact Company Link",
    "Company Name",
    "Company Adress",
    "Company Phone Number",
    "Contact Company Link",
    "Company Name",
    "Company Adress",
    "Company Phone Number",
    "Contact Company Link",
    "Company Name",
    "Company Adress",
    "Company Phone Number",
    "Contact Company Link",
    "Company Name",
    "Company Adress",
    "Company Phone Number",
    "Contact Company Link",
    "Company Name",
    "Company Adress",
    "Company Phone Number",
    "Contact Company Link",
    "Company Name",
    "Company Adress",
    "Company Phone Number",
    "Contact Company Link",
]

data_as_strings = [
    ",".join(map(str, sublist)).replace("'", "") for sublist in data_list
]
data_as_strings = [re.sub(r"['\[\]]", "", s) for s in data_as_strings]

with open("output.csv", "w", newline="") as csv_file:
    csv_file.write(",".join(headers) + "\n")
    csv_file.write("\n".join(data_as_strings))
