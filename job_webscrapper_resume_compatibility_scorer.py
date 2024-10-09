import PyPDF2
import streamlit as st
import os
import io
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import randint
import pandas as pd
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
def generate_url(index,role,location):
    p1_str  = role.split(' ')[0]
    p2_str =  role.split(' ')[1]
  
    if index == 1:
        return format("https://www.naukri.com/{}-{}-jobs-in-{}".format(p1_str,p2_str,location))
        # return "https://www.naukri.com/data-scientist-jobs-in-mumbai"
    else:
        # print("index",index)
        # return format("https://www.naukri.com/data-scientist-jobs-in-mumbai-{}".format(index))
        return format("https://www.naukri.com/{}-{}-jobs-in-{}-{}".format(p1_str,p2_str,location,index))
        # print(url)
    return url

# def extract_rating(rating_a):
#     if rating_a is None or rating_a.find('span', class_="main-2") is None:
#         return "None"
#     else:
#         return rating_a.find('span', class_="main-2").text
  
def parse_job_data_from_soup(page_jobs):
    print("********PAGE_JOBS***********")
    for job in page_jobs:
        job = BeautifulSoup(str(job), 'html.parser')
        row1 = job.find('div', class_="row1")
        row2 = job.find('div', class_="row2")
        row3 = job.find('div', class_="row3")
        row4 = job.find('div', class_="row4")
        row5 = job.find('div', class_="row5")
        row6 = job.find('div', class_="row6")
        print("*************START***************")
        job_title = row1.a.text
        
        company_name = row2.span.a.text
        
        job_details = row3.find('div', class_="job-details")
        ex_wrap = job_details.find('span', class_="exp-wrap").span.span.text
        location = job_details.find('span', class_="loc-wrap ver-line").span.span.text
        min_requirements = None
        try:
            min_requirements = row4.span.text
        except:
            min_requirements = None

        all_tech_stack = []
        try:
            ts =  row5.ul.find_all('li', class_="dot-gt tag-li ")
            for tech_stack in ts:
                tech_stack = tech_stack.text
                all_tech_stack.append(tech_stack)
        except:
            print('empty')


        job_info = {
            "job_title" : job_title,
            "company_name" : company_name,
            "company_location" : location,
            "Job_description" : min_requirements         
        }
        job_list.append(job_info)

def start(role,location):
    options = webdriver.ChromeOptions() 
    # options.add_argument('--headless')
    options.headless = True 
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    start_page = 1
    # edit the page_end here
    page_end = 6
    # role = role
    # location = location
    for i in range(start_page, page_end):
        print(i)
        url = generate_url(i,role,location)
        driver.get(url)
        # sleep for 5-10 seconds randomly just to let it load
        sleep(randint(5, 10))
        get_url = driver.current_url
        if get_url == url:
            page_source = driver.page_source
    
        # Generate the soup
        soup = BeautifulSoup(page_source, 'html.parser')
        page_soup = soup.find_all("div", class_="srp-jobtuple-wrapper")
        parse_job_data_from_soup(page_soup)

# def match_resume_with_job(resume_text, job_description_text):
#     # Convert text to lowercase to perform case-insensitive matching
#     resume_text = resume_text.lower()
#     job_description_text = job_description_text.lower()

#     # Tokenize the text into words
#     resume_words = resume_text.split()
#     job_description_words = job_description_text.split()

#     # Define a set of keywords relevant to the job
#     job_keywords = set(job_description_words)

#     # Calculate the number of keywords in the resume that match the job description
#     matching_keywords_count = sum(1 for word in resume_words if word in job_keywords)

#     # Calculate the similarity score
#     resume_length = len(resume_words)
#     similarity_score = matching_keywords_count / resume_length if resume_length > 0 else 0
#     similarity_score = similarity_score * 100
#     match_compatability =''
#     if similarity_score > 50 :
#         match_compatability = 'You are not compatibile with this job description'
#     else :
#         match_compatability = 'You are compatibile with this job description '
#     return similarity_score,match_compatability

def match_resume_with_job(resume_text, job_description_text):
    # Convert text to lowercase to perform case-insensitive matching
    resume_text = resume_text.lower()
    job_description_text = job_description_text.lower()
    
    profile_keywords = ['data science','machine learning','Statistics','python','R','SQL','Data Analysis','Data Visualization',
                        'Big Data','Artificial Intelligence','Deep Learning','Natural Language Processing','Predictive Modeling','Hadoop',
                        'spark','django','flask','TensorFlow','Scikit-learn','Pandas','NumPy','Matplotlib','Tableau','Statistical Modeling','Experimental Design',
                        'Feature Engineering','Algorithm Development','Data Mining','Business Intelligence','Time Series Analysis',
                        'Regression Analysis','Clustering','Classification','Optimization']
    
    profile_keywords = [keyword.lower() for keyword in profile_keywords]
  
    resume_words = [word for part in resume_text.split(",") for word in part.split()]

    job_description_words = [word for part in job_description_text.split(",") for word in part.split()]

    resume_elements = [element for element in resume_words if element in profile_keywords]

    jd_elements = [element for element in job_description_words if element in profile_keywords]
    
    matching_elements = [item for item in resume_elements if item in jd_elements]
    similarity_score = len(matching_elements) / len(jd_elements) * 100

    match_compatability =''
    if similarity_score < 50 :
        match_compatability = 'You are not compatibile with this job description'
    else :
        match_compatability = 'You are compatibile with this job description '
    return similarity_score,match_compatability


def redirect_to_table_page():
    """
    Function to generate JavaScript to redirect to a new Streamlit page.
    """
    return """
        <script>
            window.location.href = window.location.origin + '/table_page';
        </script>
    """

def table_page(df):
    """
    Function to render the table page.
    """
    print(df)
    st.title('Table Page')
    # Example table data
    data = df

    # data = {
    #     'Name': ['John', 'Emma', 'Michael'],
    #     'Age': [30, 25, 35],
    #     'City': ['New York', 'San Francisco', 'Los Angeles']
    # }
    st.table(data)

# def main():
#     """
#     Main function to render the main page.
#     """
#     st.title('Redirect to Table Page Example')

#     if st.button('Submit'):
#         st.markdown(redirect_to_table_page())



def extract_text_from_pdf(pdf_path):
    text = ""
    # with open(pdf_path, 'rb') as file:
    # file = pdf_path.read()
    file_bytes = pdf_path.read()

    # Convert bytes to a file-like object
    file = io.BytesIO(file_bytes)
    reader = PyPDF2.PdfReader(file)
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num] 
        text += page.extract_text()
    return text

st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

option_1 = st.selectbox('Choose job profile', ('data scientist', 'data engineer', 'data analyst'))
option_2 = st.selectbox('Choose job location', ('mumbai', 'delhi', 'kolkata'))

role= option_1
location = option_2

job_search = st.button('job_search')

# start()

# job_list =[]
# df = pd.DataFrame(job_list)
if submit:
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        # text=input_pdf_text(uploaded_file)
        # response=get_gemini_repsonse(input_prompt)
        response,j = match_resume_with_job(text, jd)
        st.subheader(response,j)
       
job_list =[]
# df = pd.DataFrame(job_list)
if job_search:
    role= option_1
    location = option_2
    st.markdown(redirect_to_table_page())
    start(role,location)
    df = pd.DataFrame(job_list)
    print(df)

    table_page(df)


# Now you can use the `match_resume_with_job` function to compare `resume_text` with `job_description`
# Example usage:
# resume = "Experienced software engineer proficient in Python, Java, and SQL. Familiar with web development frameworks like Django and Flask."
# job_description = "We are looking for a software engineer with expertise in Python, Java, SQL, and experience with web development frameworks like Django or Flask."

