from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_six_registered_projects(driver):
    section_id = 'ctl00_ContentPlaceHolder1_TabContainer1_TabPanel2'
    table_id = 'ctl00_ContentPlaceHolder1_TabContainer1_TabPanel2_gvProjectList'
    
    section = driver.find_element(By.ID, section_id)
    driver.execute_script("arguments[0].scrollIntoView();", section)
    time.sleep(3)
    
    project_data = []
    rows = driver.find_elements(By.XPATH, f'//table[@id="{table_id}"]/tbody/tr')

    for row in rows[:6]:
        try:
            rera_number = row.find_element(By.XPATH, './td[1]').text.strip()
            project_data.append({
                'RERA Number': rera_number
            })
        except Exception as e:
            print(f"Error extracting data: {e}")
            continue
    
    return pd.DataFrame(project_data)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = 'https://hprera.nic.in/PublicDashboard'
driver.get(url)

time.sleep(5)

print("Scraping and displaying 6 registered projects...")
six_registered_projects_df = scrape_six_registered_projects(driver)
print(six_registered_projects_df)

driver.quit()
