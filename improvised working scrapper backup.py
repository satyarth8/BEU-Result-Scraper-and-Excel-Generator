import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def extract_subject_mapping(html):
    
    soup = BeautifulSoup(html, 'html.parser')
    subject_mapping = {}
    
    # Extract subject mapping from the theory section
    theory_table = soup.find('table', {'id': 'ContentPlaceHolder1_GridView1'})
    if theory_table:
        for row in theory_table.find_all('tr')[1:]:  # Skip header row
            columns = row.find_all('td')
            subject_code = columns[0].text.strip()
            subject_name = columns[1].text.strip()
            subject_mapping[subject_code] = subject_name
    
    return subject_mapping

def extract_student_info(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Find the elements containing the data you want
    name_element = soup.find('span', {'id': 'ContentPlaceHolder1_DataList1_StudentNameLabel_0'})
    sgpa_element = soup.find('span', {'id': 'ContentPlaceHolder1_DataList1_TotalSGPALabel_0'})

    # Get the text from the found elements
    name = name_element.text.strip() if name_element else "N/A"

    # Extract SGPA as float, replace ',' with '.' to handle different number formats
    sgpa_text = sgpa_element.text.strip().replace(',', '.') if sgpa_element else "N/A"
    sgpa = float(sgpa_text) if sgpa_text != "N/A" else "N/A"
    return {'Name': name, 'SGPA': sgpa}

def extract_subject_marks(html, subjects, roll_no):
    soup = BeautifulSoup(html, 'html.parser')
    
        # Find the elements containing the data you want
    name_element = soup.find('span', {'id': 'ContentPlaceHolder1_DataList1_StudentNameLabel_0'})
    sgpa_element = soup.find('span', id='ContentPlaceHolder1_DataList5_GROSSTHEORYTOTALLabel_0')

    # Get the text from the found elements
    name = name_element.text.strip() if name_element else "N/A"

    # Extract SGPA as float, replace ',' with '.' to handle different number formats
    sgpa = sgpa_element.text.strip() if sgpa_element else "N/A"
    print(name)
    # Carry Papers
    remark_element=soup.find('span', {'id': 'ContentPlaceHolder1_DataList3_remarkLabel_0'})
    remark=remark_element.text.strip() if remark_element else "N/A"
    default=sum(c == ':' for c in remark)
    more_fails=sum(c == ',' for c in remark)
    carries=int(default+more_fails)

    # Extract total marks for each subject from the theory section
    theory_table = soup.find('table', {'id': 'ContentPlaceHolder1_GridView1'})
    if theory_table:
        data = {'Roll No.': roll_no, 'Name': name, 'SGPA': sgpa ,'Carry Paper': carries}
        for row in theory_table.find_all('tr')[1:]:  # Skip header row
            columns = row.find_all('td')
            subject_code = columns[0].text.strip()
            
            if subject_code in subjects:
                subject_name = subjects[subject_code]
                total_marks = int(columns[4].text.strip())
                data[subject_name] = total_marks
        
        return data

# ... (previous code remains unchanged)

def process_result_single(roll_no, base_url, subjects, result_df):
    # Construct the result URL for the given roll number
    result_url = f"{base_url}{roll_no}"
    print(roll_no)
    # Send a GET request to the result URL
    response = requests.get(result_url)
    count=1
    while(response.status_code!=200):
        print(count)
        response=requests.get(result_url)
        print("\nstatus code:",response.status_code)
        count=count+1
        if(count>60):
            break

    if response.status_code == 200:
        # Extract student info
        student_info = extract_student_info(response.text)
        if student_info:
            # Extract subject marks for the given roll number and subjects
            subject_marks = extract_subject_marks(response.text, subjects, roll_no)
            
            # Combine student info and subject marks 
            # if the values are nonetype handling
            student_info = student_info or {}
            subject_marks = subject_marks or {}

            combined_data = {**student_info, **subject_marks}
            
            # Convert the combined data to a DataFrame
            result_df_single = pd.DataFrame([combined_data])
            
            # Ensure result_df is a DataFrame
            if not isinstance(result_df, pd.DataFrame):
                result_df = result_df_single
            else:
                # Append the data to the existing DataFrame
                result_df = pd.concat([result_df, result_df_single], ignore_index=True)
            
            print(f"Result for Roll No. {roll_no} processed.")
        else:
            print(f"Failed to extract student info for Roll No. {roll_no}")
    else:
        print(f"Failed to fetch result for Roll No. {roll_no}")

    return result_df
# ... (remaining code remains unchanged)

# Example usage:
first_roll_no = '21101154008'
base_result_url = 'http://results.beup.ac.in/ResultsBTech4thSem2023_B2021Pub.aspx?Sem=IV&RegNo='  # Replace with the actual URL
#base_result_url = 'http://results.beup.ac.in/ResultsBTech2ndSem2023_B2022Pub.aspx?Sem=II&RegNo=' 
#base_result_url = 'http://results.beup.ac.in/ResultsBTech6thSem2023_B2020Pub.aspx?Sem=VI&RegNo='

#http://results.beup.ac.in/ResultsBTech6thSem2023_B2020Pub.aspx?Sem=VI&RegNo=20105111007
# Extract subject mapping from the first roll number

response_for_map = requests.get(f"{base_result_url}{first_roll_no}")
count=1
while(response_for_map.status_code!=200):
        print(count)
        response_for_map=requests.get(f"{base_result_url}{first_roll_no}")
        print("\nstatus code:",response_for_map.status_code)
        count=count+1
        if(count>100):
            break

subject_mapping = extract_subject_mapping(response_for_map.text)
subjects = {code: name for code, name in subject_mapping.items() if 'P' not in code}

# Initialize an empty DataFrame to store all results
all_results_df = pd.DataFrame(columns=['Roll No.', 'Name', 'SGPA', 'Carry Paper'] + list(subjects.values()))

# Process results for subsequent roll numbers
for roll_no in range(21101154001, 2110115411):  # Replace with the desired range of roll numbers
    time.sleep(0)
    all_results_df = process_result_single(str(roll_no), base_result_url, subjects, all_results_df)
for roll_no in range(21101154901, 21101154931):  # Replace with the desired range of roll numbers for lateral entry 
    time.sleep(0)
    all_results_df = process_result_single(str(roll_no), base_result_url, subjects, all_results_df)


# Get the desktop path
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop/")

# Save the DataFrame to a single Excel file on the desktop
excel_filename = 'geck_4th.xlsx'
excel_path = os.path.join(desktop_path, excel_filename)
all_results_df.to_excel(excel_path, index=False)

print(f"All results processed and saved to '{excel_filename}' on the desktop.")
