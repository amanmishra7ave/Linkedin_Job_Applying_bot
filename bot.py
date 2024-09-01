import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# LinkedIn credentials
LINKEDIN_EMAIL = "your_Emai"
LINKEDIN_PASSWORD = "your_password"

# Job search parameters
JOB_TITLE = "Software Engineer"
JOB_LOCATION = "Remote"

# Path to your ChromeDriver
CHROME_DRIVER_PATH = './chromedriver'

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize the Chrome Driver
driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=chrome_options)

def linkedin_login():
    driver.get("https://www.linkedin.com/login")

    try:
        # Wait for the email and password fields to be present
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "session_key"))
        )
        password_field = driver.find_element(By.NAME, "session_password")

        email_field.clear()
        email_field.send_keys(LINKEDIN_EMAIL)
        password_field.clear()
        password_field.send_keys(LINKEDIN_PASSWORD)
        password_field.send_keys(Keys.RETURN)

        # Verify successful login by checking for a known element on the feed page
        WebDriverWait(driver, 10).until(
            EC.url_contains("https://www.linkedin.com/feed/")
        )
        print("Logged in successfully")
    except Exception as e:
        print(f"Error during login: {e}")

def search_jobs():
    driver.get("https://www.linkedin.com/jobs/")

    try:
        # Wait for the job title and location fields to be present
        search_job_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search job titles or companies']"))
        )
        search_location_field = driver.find_element(By.CSS_SELECTOR, "input[aria-label='Search location']")

        search_job_field.clear()
        search_job_field.send_keys(JOB_TITLE)
        
        search_location_field.clear()
        search_location_field.send_keys(JOB_LOCATION)
        search_location_field.send_keys(Keys.RETURN)

        time.sleep(5)  # Wait for search results to load
        print("Job search completed")
    except Exception as e:
        print(f"Error during job search: {e}")

def apply_to_jobs():
    driver.get("https://www.linkedin.com/jobs/")

    try:
        # Wait for job listings to be visible
        job_listings = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container"))
        )

        for job in job_listings:
            try:
                job.click()
                time.sleep(2)  # Wait for the job details to load

                # Check if 'Easy Apply' button is present
                try:
                    easy_apply_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button.jobs-apply-button[aria-label*='Easy Apply']"))
                    )

                    # Click 'Easy Apply' button
                    easy_apply_button.click()
                    print("Clicked 'Easy Apply' button")

                    # Handle the multi-step application process
                    while True:
                        try:
                            # Click 'Continue to next step' button if present
                            next_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Continue to next step']"))
                            )
                            next_button.click()
                            print("Clicked 'Continue to next step'")
                            time.sleep(2)
                        except Exception as e:
                            print(f"Next button error: {e}")
                            break  # No more 'Next' buttons, proceed to the next step

                    # Click 'Preview' button if present
                    try:
                        preview_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Preview']"))
                        )
                        preview_button.click()
                        print("Clicked 'Preview'")
                        time.sleep(2)
                    except Exception as e:
                        print(f"Preview button error: {e}")
                        print("No 'Preview' button found, skipping preview step")

                    # Click 'Submit' button
                    try:
                        submit_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Submit application']"))
                        )
                        submit_button.click()
                        print("Applied successfully")
                        time.sleep(5)  # Wait for the application to be processed
                    except Exception as e:
                        print(f"Submit button error: {e}")
                        print("No 'Submit' button found, skipping job")

                except Exception as e:
                    print(f"Easy Apply button not found, skipping job: {e}")
                    continue  # Skip to the next job if 'Easy Apply' button is not found

                # Skip jobs with 'Apply' button
                try:
                    apply_button = driver.find_element(By.CSS_SELECTOR, "button.jobs-apply-button[aria-label*='Apply']")
                    print("Apply button found, skipping job")
                    continue  # Skip this job if 'Apply' button is found
                except:
                    pass  # No 'Apply' button, continue with 'Easy Apply'

            except Exception as e:
                print(f"Error selecting job: {e}")
                continue  # Skip to the next job if there is an error

    except Exception as e:
        print(f"Error during job application: {e}")



def main():
    linkedin_login()
    search_jobs()
    apply_to_jobs()
    driver.quit()

if __name__ == "__main__":
    main()
