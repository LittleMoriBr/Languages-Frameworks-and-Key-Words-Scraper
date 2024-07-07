# Languages, Frameworks and Key Words Scraper

Objective:
Develop a web scraping bot to analyze job postings on a job search platform, specifically focusing on identifying the most frequently requested programming languages, frameworks, and the 50 most common relevant words in job descriptions.

Challenges:

Web Navigation: Automating the login process and navigating the job search results.
Dynamic Content Loading: Handling dynamic content loading by scrolling and navigating through multiple pages of job listings.
Text Extraction and Analysis: Extracting job descriptions accurately and counting the occurrences of programming languages and frameworks while filtering out common stopwords.
Technologies:

Selenium: For automating web browsing, interacting with job search boxes, and navigating job listings.
BeautifulSoup: For parsing HTML and extracting job descriptions from the loaded web pages.
NLTK: For removing common stopwords in English and Portuguese from the job descriptions.
Python Libraries: Including re for regular expressions, Counter from the collections module for counting occurrences, and time for handling delays in dynamic content loading.
