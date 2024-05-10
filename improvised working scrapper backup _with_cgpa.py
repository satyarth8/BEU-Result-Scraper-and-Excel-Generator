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

def extract_cgpa(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Locate the CGPA table using its ID
    cgpa_table = soup.find('table', {'id': 'ContentPlaceHolder1_GridView3'})
    
    if cgpa_table:
        # Find the last row of the table
        last_row = cgpa_table.find_all('tr')[-1]
        
        # Find all cells (td) in the last row
        columns = last_row.find_all('td')
        
        # The last column should contain the CGPA
        cgpa_text = columns[-1].text.strip()
        
        # Convert the CGPA to a float
        try:
            cgpa = float(cgpa_text.replace(',', '.'))
        except ValueError:
            cgpa = "N/A"  # If conversion fails
        
        return cgpa
    else:
        return "N/A"  # If the table is not found or another issue arises

def extract_subject_marks(html, subjects, roll_no):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the elements containing the data you want
    name_element = soup.find('span', {'id': 'ContentPlaceHolder1_DataList1_StudentNameLabel_0'})
    sgpa_element = soup.find('span', id='ContentPlaceHolder1_DataList5_GROSSTHEORYTOTALLabel_0')

    # Get the text from the found elements
    name = name_element.text.strip() if name_element else "N/A"
    sgpa = sgpa_element.text.strip() if sgpa_element else "N/A"

    # Carry Papers
    remark_element = soup.find('span', {'id': 'ContentPlaceHolder1_DataList3_remarkLabel_0'})
    remark = remark_element.text.strip() if remark_element else "N/A"
    default = sum(c == ':' for c in remark)
    more_fails = sum(c == ',' for c in remark)
    carries = int(default + more_fails)

    # Extract total marks for each subject from the theory section
    theory_table = soup.find('table', {'id': 'ContentPlaceHolder1_GridView1'})
    if theory_table:
        data = {'Roll No.': roll_no, 'Name': name, 'SGPA': sgpa, 'Carry Paper': carries}
        
        for row in theory_table.find_all('tr')[1:]:  # Skip the header row
            columns = row.find_all('td')
            subject_code = columns[0].text.strip()
            
            if subject_code in subjects:
                subject_name = subjects[subject_code]
                total_marks = int(columns[4].text.strip())
                data[subject_name] = total_marks
        
        return data
    else:
        return None  # Return None if the theory table is not found

def process_result_single_with_cgpa(roll_no, base_url, subjects, result_df):
    # Construct the result URL for the given roll number
    result_url = f"{base_url}{roll_no}"
    
    response = requests.get(result_url)
    if response.status_code == 200:
        # Extract student info and CGPA
        student_info = extract_student_info(response.text)
        subject_marks = extract_subject_marks(response.text, subjects, roll_no)
        cgpa = extract_cgpa(response.text)
        
        if student_info and subject_marks:
            combined_data = {**student_info, **subject_marks, 'CGPA': cgpa}  # Add CGPA to the data
            
            result_df_single = pd.DataFrame([combined_data])
            
            if not isinstance(result_df, pd.DataFrame):
                result_df = result_df_single
            else:
                result_df = pd.concat([result_df, result_df_single], ignore_index=True)
            
            print(f"Result for Roll No. {roll_no} processed with CGPA.")
        else:
            print(f"Failed to extract student info for Roll No. {roll_no}")
    else:
        print(f"Failed to fetch result for Roll No. {roll_no}")

    return result_df

# Example usage:
first_roll_no = '22155154001'
base_result_url = 'http://results.beup.ac.in/ResultsBTech2ndSem2023_B2022Pub.aspx?Sem=II&RegNo='  # Change the URL as needed

# Extract subject mapping from the first roll number
response_for_map = requests.get(f"{base_result_url}{first_roll_no}")
subject_mapping = extract_subject_mapping(response_for_map.text)
subjects = {code: name for code, name in subject_mapping.items() if 'P' not in code}

# Initialize an empty DataFrame to store all results
all_results_df = pd.DataFrame(columns=['Roll No.', 'Name', 'SGPA', 'Carry Paper', 'CGPA'] + list(subjects.values()))

# Process results for a given range of roll numbers
for roll_no in range(22155154001, 22155154055):
    time.sleep(0.5)  # Optional sleep to avoid excessive requests
    all_results_df = process_result_single_with_cgpa(str(roll_no), base_result_url, subjects, all_results_df)

# Save the DataFrame to an Excel file
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop/")
excel_filename = 'geck_cse_1styear_with_cgpa.xlsx'
excel_path = os.path.join(desktop_path, excel_filename)
all_results_df.to_excel(excel_path, index=False)

print(f"All results processed and saved to '{excel_filename}' on the desktop.")
