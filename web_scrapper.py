import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from PIL import Image
import easyocr
import psycopg2
from bs4 import BeautifulSoup



def get_captcha_text(location, size):
    reader = easyocr.Reader(['en'])
    im = Image.open('screenshot.png') # uses PIL library to open image in memory
    size['width']+=5
    left = location['x']+220
    top = location['y'] + 190
    right = left + size['width']
    bottom = top + size['height']


    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save('screenshot2.png')
    result = reader.readtext('screenshot2.png')
    print(result[0][1])
    return result[0][1]



# Initialize the Chrome WebDriver and Extension for translating
op = Options()
op.add_extension('Superb-Copy.crx')
driver = webdriver.Chrome(options=op)
driver.set_window_size(1024, 600)
driver.maximize_window()
driver.get("https://pay2igr.igrmaharashtra.gov.in/eDisplay/propertydetails")


#Filling the form details
select_year = driver.find_element(By.ID, "dbselect")
select_year.send_keys("2023")
time.sleep(5)
district = driver.find_element(By.ID, "district_id")
district.send_keys("मुंबई उपनगर")
time.sleep(2)
taluka = driver.find_element(By.ID, "taluka_id")
taluka.send_keys("अंधेरी")
time.sleep(2)
village = driver.find_element(By.ID, "village_id")
village.send_keys("बांद्रा")
time.sleep(2)
doc_property_cts = driver.find_element(By.ID, "free_text")
doc_property_cts.send_keys("2023")
time.sleep(2)


#Code To Automate Captch
element = driver.find_elements(By.ID,"captcha")
location = element[1].location
size = element[1].size
driver.save_screenshot('screenshot.png')
captcha_text = get_captcha_text(location, size)
textbox = driver.find_element(By.ID,"cpatchaTextBox")
textbox.send_keys(captcha_text)

#Search Details
time.sleep(2)
search_button = driver.find_element(By.ID, "submit")
search_button.click()
time.sleep(30)

# Change the "Record Details" to display 50 records at once
record_details = driver.find_element(By.NAME, "tableparty_length")
record_details.send_keys("50")
time.sleep(50)

# Extract the HTML source code
page_source = driver.page_source

# Close the WebDriver
driver.quit()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')
data = []
table = soup.find("table", {"id": "tableparty"})
rows = table.find_all("tr")

for row in rows[1:]:  # Skip the header row

    columns = row.find_all("td")
    reg_no = columns[1].text
    reg_type = columns[2].text
    reg_office = columns[3].text
    year = columns[4].text
    buyer_name = columns[5].text
    seller_name =   columns[6].text
    other_info = columns[7].text
    link = columns[8].find("a")["href"]
    data.append([reg_no,reg_type,reg_office,year,buyer_name,seller_name,other_info,link])



column_names = ["Registration Number", "Regsitration Type", "Office", "Year","Buyer Name","Seller Name","Other Information","Link"]
df = pd.DataFrame(columns=column_names)
for row in data:
    df.loc[len(df)] = row



print(df)


# Connect to PostgreSQL
conn = psycopg2.connect(
    database="Web Scrapper",
    user="postgres",
    password="Abhi1234@5",
    host="localhost",
    port="5433",
)

cur = conn.cursor()
create_table_query = """
CREATE TABLE IF NOT EXISTS Scrapped_Data (
    Registration_Number int PRIMARY KEY,
    Registration_Type varchar(40),
    Office TEXT,
    Year DATE,
    Buyer_Name TEXT,
    Seller_Name TEXT,
    Other_Information TEXT,
    Link TEXT

)
"""
cur.execute(create_table_query)

# Insert data into the table
insert_query = """
INSERT INTO Scrapped_Data (Registration_Number,Registration_Type,Office,Year,Buyer_Name,Seller_Name,Other_Information,Link)
VALUES (%s, %s, %s,%s,%s,%s,%s,%s);
"""
for row in data:
    cur.execute(insert_query, row)

# Commit changes and close connections
conn.commit()
cur.close()
conn.close()
