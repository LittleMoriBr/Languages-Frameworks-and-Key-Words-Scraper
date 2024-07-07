from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords

# Ensure NLTK stopwords are downloaded
nltk.download('stopwords')

# Predefined list of programming languages
programming_languages = [
    'Python', 'Java', 'C++', 'JavaScript', 'C#', 'PHP', 'Swift', 'Ruby', 
    'TypeScript', 'Kotlin', 'Objective\-C', 'Perl', 'Rust', 'Dart',
    'SQL', 'MATLAB', 'VBA'
]

# Predefined list of frameworks
frameworks = [
    'React', 'Angular', 'Vue', 'Django', 'Flask', 'Spring', 'Rails', 'Laravel', 
    '.NET', 'Express', 'Ember', 'Svelte', 'Bootstrap', 'jQuery', 'Backbone'
]

# Add Stopwords. English and Portuguese Example
stop_words = set(stopwords.words('english') + stopwords.words('portuguese'))

# Initialize WebDriver
options = Options()
options.headless = False  # Run in headless mode (change to True if you don't need to see the browser)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.maximize_window()
# Navigate to the website
url = 'https:/BaseUrl' #Set the base Url
driver.get(url)

# Log into LinkedIn
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
username.send_keys("username") # Enter your email
password.send_keys("password") # Enter your password
driver.find_element(By.XPATH, '//*[@type="submit"]').click()

time.sleep(10)  # Wait for login to complete

# Navigate to job search
driver.get(f"{url}/jobs/")
time.sleep(5)  # Wait for the page to load

# Locate the job search box and enter your role
Role = 'Your Role'

# Locate the location search box and enter your location
location = 'Yor Location'

driver.get(f"{url}/jobs/search/?keywords={Role}&location={location}")

time.sleep(5)  # Wait for search results to load

# Dictionaries to hold the count of each programming language and framework
language_counts = Counter()
framework_counts = Counter()
word_counts = Counter()

def extract_languages_and_frameworks(description):
    found_languages = set()  # Use a set to avoid counting a language more than once per job
    found_frameworks = set()  # Use a set to avoid counting a framework more than once per job

    for language in ['R', 'Go']: #Handling false positives for common words that are also programming languages 
        if re.search(r'\b' + re.escape(language) + r'\b', description, re.IGNORECASE):
            found_languages.add(language)
            print(f"Found language: {language}")

    for language in programming_languages:
        if language not in found_languages:
            if re.search(re.escape(language), description, re.IGNORECASE):
                found_languages.add(language)
                print(f"Found language: {language}")

    for framework in frameworks:
        if re.search(re.escape(framework), description, re.IGNORECASE):
            found_frameworks.add(framework)
            print(f"Found framework: {framework}")

    for language in found_languages:
        language_counts[language] += 1

    for framework in found_frameworks:
        framework_counts[framework] += 1

    # Count words in the description for common word analysis
    words = re.findall(r'\b\w+\b', description.lower())
    word_counts.update(words)

# Get job descriptions from job titles
def get_job_descriptions(job_titles):
    for index, job_title in enumerate(job_titles):  # Process each job title
        try:
            print(f"Clicking on job title {index + 1}")
            job_title.click()
            time.sleep(2)  # Wait for the job details to load
            job_page = BeautifulSoup(driver.page_source, 'html.parser')
            description = job_page.find('div', class_='jobs-description-content__text')
            if description:
                description_text = description.get_text()
                print(f"Full Job Description:\n{description_text}\n")
                extract_languages_and_frameworks(description_text)
            else:
                print("Job description not found.")
        except Exception as e:
            print(f"Error extracting job details for job {index + 1}: {e}")

# Scroll within the job listings container
def scroll_job_listings():
    job_listings_container = driver.find_element(By.CLASS_NAME, 'jobs-search-results-list')
    last_height = driver.execute_script("return arguments[0].scrollHeight", job_listings_container)
    scroll_increment = last_height // 4  # Calculate one-fourth of the container height

    while True:
        driver.execute_script("arguments[0].scrollTop += arguments[1];", job_listings_container, scroll_increment)
        time.sleep(2)  # Wait for more jobs to load
        new_height = driver.execute_script("return arguments[0].scrollHeight", job_listings_container)
        if new_height == last_height:
            break
        last_height = new_height

# Main loop to scroll and process job titles
all_processed_jobs = set()
start = 0
total_jobs_processed = 0
max_jobs_to_process = 200  # Set the maximum number of jobs to process

while total_jobs_processed < max_jobs_to_process:
    # Scroll the job listings container to load all jobs
    scroll_job_listings()

    # Get current job titles
    job_titles = driver.find_elements(By.CLASS_NAME, 'job-card-list__title')

    # Filter out already processed job titles
    new_job_titles = [job_title for job_title in job_titles if job_title not in all_processed_jobs]
    all_processed_jobs.update(new_job_titles)

    # Get job descriptions from the new job titles
    jobs_to_process = new_job_titles[:min(25, max_jobs_to_process - total_jobs_processed)]
    get_job_descriptions(jobs_to_process)

    total_jobs_processed += len(jobs_to_process)
    if total_jobs_processed >= max_jobs_to_process:
        break

    # Update the URL with the next start value and navigate to the next page
    start += 25
    next_page_url = f"{url}/jobs/search/?keywords={Role}&location={location}&start={start}"
    driver.get(next_page_url)
    time.sleep(5)  # Wait for the next page to load

# Filter out stopwords from word_counts
filtered_word_counts = Counter({word: count for word, count in word_counts.items() if word not in stop_words})

# Print the counts of each programming language and framework
print("\nProgramming Languages Count:")
for language, count in language_counts.items():
    print(f"{language}: {count}")

print("\nFrameworks Count:")
for framework, count in framework_counts.items():
    print(f"{framework}: {count}")

# Print the 50 most common words (excluding stopwords)
print("\n50 Most Common Words:")
for word, count in filtered_word_counts.most_common(50):
    print(f"{word}: {count}")

# Close the driver
driver.quit()




