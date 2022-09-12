import time
from csv import writer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as ec

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.topcv.vn/")

def search_role(role):
    search = driver.find_element(By.ID, "keyword")
    search.send_keys(role)
    search.send_keys(Keys.ENTER)


def select_city(city):
    select = Select(driver.find_element(By.ID, 'city'))
    time.sleep(2)
    select.select_by_visible_text(city)
    button = driver.find_element(By.CSS_SELECTOR, "div.input-data.search-submit")
    button.click()

def main():
    # role = input("Nhập vị trí ứng tuyển của bạn:")
    # address = input("Nhập thành phố bạn muốn làm việc:")
    role = "IT"
    address = "Đà Nẵng"
    search_role(role)
    select_city(address)
    try:
        main = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, "main"))
        )
        jobs = main.find_elements(By.CLASS_NAME, "job-item.job-ta.result-job-hover")

        header = ['Role', 'Company Name', 'Salary', 'Address', 'Time Left']
        with open('job.csv', 'w', newline='', encoding='utf-8') as f:
            writer_csv = writer(f)
            # Tạo header
            writer_csv.writerow(header)
            for job in jobs:
                # Name, addres ,...
                role = job.find_element(By.CLASS_NAME, "bold.transform-job-title")
                company_name = job.find_element(By.CLASS_NAME, "company.underline-box-job")
                salary = job.find_element(By.CLASS_NAME, "salary")
                address = job.find_element(By.CLASS_NAME, "address")
                time_left = job.find_element(By.CLASS_NAME, "deadline")
                data = [role.text, company_name.text, salary.text, address.text, time_left.text]
                print(data, end='\n===========\n')
                # Viết data
                writer_csv.writerow(data)
    finally:
        driver.quit()
if __name__== "__main__":
    main()


