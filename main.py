import smtplib
from bs4 import BeautifulSoup
import requests

# Define the URL of the product
URL = "https://www.amazon.com/dp/B08N5WRWNW"

# Your email details
YOUR_EMAIL = "your_email@example.com"
YOUR_PASSWORD = "your_password"
YOUR_SMTP_ADDRESS = "smtp.example.com"

# Define the price threshold
BUY_PRICE = 200

# Send a request to the Amazon product page
headers = {
    "User-Agent": "Your User-Agent",
    "Accept-Language": "en-US,en;q=0.5"
}
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Extract the product title
title = soup.find(id="productTitle").get_text().strip()
print(title)

# Extract the product price
price_str = soup.find("span", class_="a-offscreen").get_text().strip()
price_as_float = float(price_str.replace("$", "").replace(",", ""))
print(price_as_float)

# Check if the price is below the desired threshold
if price_as_float < BUY_PRICE:
    message = f"{title} is now ${price_as_float}"

    # Send an email notification
    with smtplib.SMTP(YOUR_SMTP_ADDRESS, port=587) as connection:
        connection.starttls()
        result = connection.login(YOUR_EMAIL, YOUR_PASSWORD)
        connection.sendmail(
            from_addr=YOUR_EMAIL,
            to_addrs=YOUR_EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{URL}".encode("utf-8")
        )
        print("Email sent successfully!")

# Improvements:
# 1. Use environment variables to store sensitive information like email and password.
# 2. Add error handling for network requests and email sending.
# 3. Use a more robust method to parse the price.
# 4. Extract headers into a constant for reuse and clarity.
# 5. Add logging instead of print statements for production use.

# Example of using environment variables
import os
YOUR_EMAIL = os.getenv("YOUR_EMAIL")
YOUR_PASSWORD = os.getenv("YOUR_PASSWORD")
YOUR_SMTP_ADDRESS = os.getenv("YOUR_SMTP_ADDRESS")
