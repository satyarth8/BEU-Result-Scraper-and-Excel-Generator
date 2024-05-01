### Updates
- Added provision for if the server gives 404 response to retry

## BEU Result Scrapping & Excel Generation
- https://github.com/satyarth8/BEU-Result-Scraper-and-Excel-Generator/blob/main/BEU%20result%20scraper.ipynb
- Follow the Instructions below...
- Comply with Fair use and read the Legal Disclaimer

## Output Excel file looks like this
<img src="https://github.com/satyarth8/BEU-Result-Scraper-and-Excel-Generator/assets/126249188/b8f1254c-e31f-43ac-bf6c-38fc415c3f6d" alt="" style="width:80%;height:auto;" />

# Instructions
### Step 1: Download the Required Libraries
Open a terminal or command prompt and install the required libraries by running the following commands:  
``` pip install requests ```
``` pip install beautifulsoup4 ```
``` pip install pandas ```
### Step 2: Set the Result Links and Roll Number Range
- Replace the ```base_result_url``` variable with the actual URL of the result page.
- Set the range of roll numbers for regular and lateral entry students in the for loops.
### Step 3: Set the Excel File Location and Name
- Replace the ```desktop_path variable``` with the actual path to your desktop.
- Set the ```excel_filename``` variable to the desired name for the Excel file.
### Step 4: Run the Script
- Save the script to a file (e.g., result_scraper.py) and run it using Python (e.g., python result_scraper.py).
- The script will fetch the results for the specified roll numbers, extract the required information, and save it to an Excel file on your desktop.
### Note: Make sure to adjust the script according to your specific needs and the structure of the result page. Additionally, be respectful of the website's terms of use and avoid overwhelming the server with too many requests.

# Overview
> The BEU Result Automation & Excel Generation project is a Python-based tool designed to automate the retrieval, organization, and reporting of student results from the Bihar Engineering University (BEU) result portal. The script employs web scraping techniques to extract data accurately and efficiently, generating detailed Excel reports for further analysis.


# Technologies Used
- Python
- BeautifulSoup
- pandas
- requests

## Legal Disclaimer
>The BEU Result Automation & Excel Generation project is intended for educational and non-commercial purposes only. By using this tool, you agree that:

#### Educational Purposes:
>This project is developed solely for educational and learning purposes. It is not intended for commercial use or any other malicious activities.

#### Non-Endorsement:
>The BEU Result Automation & Excel Generation project is not endorsed or affiliated with Bihar Engineering University (BEU) or any other educational institution. It is an independent project developed by [Your Name] for educational purposes.

#### Use Responsibly: 
>Users of this tool are responsible for their actions and must use it in compliance with applicable laws and regulations. Any misuse of the tool for unauthorized access or illegal activities is strictly prohibited.

#### Legal Compliance: 
>Users must ensure that their use of this tool complies with all relevant laws, including but not limited to copyright laws, data protection laws, and terms of service agreements.

