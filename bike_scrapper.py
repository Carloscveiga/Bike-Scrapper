from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv

# Initialize the Chrome Service
service = Service('./chromedriver.exe')

# Initialize the Chrome driver with the Chrome Service
driver = webdriver.Chrome(service=service)

# Open CSV file and write headers
with open('data.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    headers = ["Marca", "Quilómetros", "Ano", "Potência", "Cilindrada", "Preco", "Link"]
    writer.writerow(headers)

# Loop through pages
for page in range(1, 3):
    driver.get('https://www.standvirtual.com/motos?search%5Border%5D=created_at_first%3Adesc&page={}'.format(page))
    time.sleep(2)

    # Accept cookies
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler'))
        )
        element.click()
    except TimeoutException:
        print("Cookie accept button not found or took too long to load. Skipping...")
        pass

    # Find all article elements
    try:
        articles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//article[contains(@class, "ooa-yca59n") and contains(@class, "e1i3khom0")]'))
        )
    except TimeoutException:
        print("Articles not found or took too long to load on page {}. Skipping...".format(page))
        continue

    # Iterate over each article element
    for article in articles:
        # Find the grid element inside the article
        try:
            grid = article.find_element(By.XPATH, './/section[contains(@class, "ooa-10gfd0w") and contains(@class, "e1i3khom1")]')
        except NoSuchElementException:
            print("Grid element not found in article. Skipping...")
            continue

        # Find the second div inside the grid
        try:
            second_div = grid.find_elements(By.XPATH, './/div')[1]  # Indexing starts from 0, so 1 is the second div
        except NoSuchElementException:
            print("Second div not found in grid. Skipping...")
            continue

        # Find the h1 element inside the second div and extract brand information
        try:
            h1_element = second_div.find_element(By.XPATH, './/h1[@class="e1i3khom9 ooa-1ed90th er34gjf0"]')
            brand = h1_element.text
            print("Brand:", brand)
        except NoSuchElementException:
            print("Brand information not found in the second div. Skipping...")
            continue

        # Find the third div inside the grid
        try:
            third_div = grid.find_elements(By.XPATH, './/div')[2]  # Indexing starts from 0, so 2 is the third div
        except NoSuchElementException:
            print("Third div not found in grid. Skipping...")
            continue

        # Find the dl class inside the third div
        try:
            dl_class = third_div.find_element(By.XPATH, './/dl[contains(@class, "ooa-1uwk9ii") and contains(@class, "e1i3khom11")]')
        except NoSuchElementException:
            print("DL class not found in third div. Skipping...")
            continue

        # Find the dd elements with data-parameter attributes inside the dl class
        try:
            dd_mileage = dl_class.find_element(By.XPATH, './/dd[@data-parameter="mileage"]')
            mileage_text = dd_mileage.text
            print("Mileage:", mileage_text)
        except NoSuchElementException:
            mileage_text = "N/A"
            print("Mileage class not found in third div. Skipping...")
            
        try:
            dd_first_registration_year = dl_class.find_element(By.XPATH, './/dd[@data-parameter="first_registration_year"]')
            first_registration_year_text = dd_first_registration_year.text
            print("first_registration_year:", first_registration_year_text)
        except NoSuchElementException:
            first_registration_year_text = "N/A"
            print("first_registration_year class not found in third div. Skipping...")
        
        try:
            dd_engine_power = dl_class.find_element(By.XPATH, './/dd[@data-parameter="engine_power"]')
            engine_power_text = dd_engine_power.text
            print("engine_power:", engine_power_text)
        except NoSuchElementException:
            engine_power_text = "N/A"
            print("engine_power class not found in third div. Skipping...")
        
        try:
            dd_engine_capacity = dl_class.find_element(By.XPATH, './/dd[@data-parameter="engine_capacity"]')
            engine_capacity_text = dd_engine_capacity.text
            print("engine_capacity:", engine_capacity_text)
        except NoSuchElementException:
            engine_capacity_text = "N/A"
            print("engine_capacity class not found in third div. Skipping...")

        # Find the last div inside the article
        try:
            last_div = article.find_element(By.XPATH, './/div[@class="ooa-vtik1a ejfzopf0"]')
        except NoSuchElementException:
            print("Last div not found in article. Skipping...")
            continue

        # Find the grid inside the last div
        try:
            grid_inside_last_div = last_div.find_element(By.XPATH, './/div[@class="ooa-2p9dfw e1i3khom4"]')
        except NoSuchElementException:
            print("Grid inside last div not found. Skipping...")
            continue

        # Find the price element inside the grid inside the last div
        try:
            price_element = grid_inside_last_div.find_element(By.XPATH, './/h3[@class="e1i3khom16 ooa-1n2paoq er34gjf0"]')
            price_text = price_element.text
            print("Price:", price_text)
        except NoSuchElementException:
            price_text = "N/A"
            print("Price element not found inside last div. Skipping...")
            continue

        # Find the currency element inside the grid inside the last div
        try:
            currency_element = grid_inside_last_div.find_element(By.XPATH, './/p[@class="e1i3khom17 ooa-8vn6i7 er34gjf0"]')
            currency_text = currency_element.text
            print("Currency:", currency_text)
        except NoSuchElementException:
            currency_text = "N/A"
            print("Currency element not found inside last div. Skipping...")
            continue
        
        # Find the model link
        try:
            model_link_element = h1_element.find_element(By.TAG_NAME, 'a')
            model_link = model_link_element.get_attribute('href')
            print("Model Link:", model_link)
        except NoSuchElementException:
            print("Model link not found. Skipping...")
            continue
        


        # Write to CSV file
        row_data = [brand, mileage_text, first_registration_year_text, engine_power_text, engine_capacity_text, f"{price_text} {currency_text}", model_link]
        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row_data)

# Quit the driver
driver.quit()



