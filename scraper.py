from playwright.sync_api import sync_playwright
import csv, sys, os

def main():

    city = input("Enter any city you want to scrape cars from: ").lower() # Get the city that we want to scrape cars from
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=False, proxy={
            "server": "brd.superproxy.io:22225",
            "username": os.environ["USERNAME"],
            "password": os.environ["PASSWORD"]
        })
        page = browser.new_page() # Launch the browser using Playwright

        try: # Go to the cars listing section on Craigslist of the city entered by the user
            page.goto(f'https://{city}.craigslist.org/search/cta#search=1~gallery~0~0')
        except:
            print("Page does not exist on Craigslist")
            sys.exit(1)
        
        page.wait_for_timeout(15000)

        cars = page.get_by_role("listitem").all() # Grab all the listings on the page

        with open("cars.csv", "w") as csvfile: # Write to a CSV file
            writer = csv.writer(csvfile)
            writer.writerow(
                ['Car', 'Price', 'Miles Driven', 'Location', 'Posted', 'Link']) # Columns of the CSV file
            for car in cars: # Looping over each of the listings
                try:
                    meta = []
                    price = car.locator("span.priceinfo").inner_text() # Price of the car
                    text = car.locator("a > span.label").inner_text() # Title of the listing
                    link = car.locator("a.posting-title").get_attribute('href') # Link to the listing
                    info = car.locator("div.meta").inner_text() # Meta info (Posted ago, miles driven, location)
                    meta = info.split("·")
                    time, miles, location = meta[0], meta[1], meta[2]
                    writer.writerow([text, price, miles, location, time, link]) # Writing to CSV file
                except:
                    print(f"Inadequate information about the car \n -------------")

        page.wait_for_timeout(10000)
        browser.close()


if __name__ == "__main__":
    main()
