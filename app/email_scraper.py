from google import genai
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access environment variables
gemini_api_key = os.getenv("gemini-api-key")
model = os.getenv("model")

# Configure your API key
# You can also set it as an environment variable (e.g., GOOGLE_API_KEY)
client=genai.Client(api_key=gemini_api_key)

# "gemma-3-27b-it"
# "gemini-2.0-flash-lite"

"""
from the above email body, extract the following information and present it in a json format:
Company Name 

Scope (Internship/Placement/Internship leading to Placement)

Type of event (Online Assessment/Interview/Registration/others)

Date

Start Time

End Time

Short Description

Forms/Registrations required 

If such info can not be scraped from the email body simply return:
{False}

Remember to be as concise and to the point as possible, return ONLY the json and NOTHING ELSE
 """

def extract_email_info(email_body: str) -> str:
    instructions = """from the above email body, extract the following information and present it in a json format:
Company Name 

Scope (Internship/Placement/Internship leading to Placement)

Type of event (Physical Process/Selection Process/Online Assessment/Online Test/Interview/Registration/others)

Date

Start Time

End Time

Short Description

Forms/Registrations required 

If such info can not be scraped from the email body simply return False

If u find a table containing eligible students, return a list of their rgister numbers ONLY in a new field in the JSON called "eligible students"
,otherwise return False in the same field

Remember to be as concise and to the point as possible, return ONLY the json and NOTHING ELSE
 """
    response = client.models.generate_content(
        model=model,
        contents=email_body+instructions
    )
    return response.text #, len(response.text)

text=r"""Marquee Internship /  Placement – 2026 Batch
 

 

 

Name of the Company

 

BalkanID

 

 

Category

 

Marquee offer



 

 

Date of Visit:                    

 

Virtual process



 

 

 

Eligible Branches          

 

 

Ø  B. Tech ( CSE & IT Related branches)

 

 

 

Eligibility Criteria          

 

% in X and XII – 80% or 8.0 CGPA

in  Pursuing Degree – 80% or 8.0 CGPA

No Standing Arrears

 

 

CTC

 

80 Lacs ( If converted)

 

Stipend

 

40,000 - 85,000 ( Based on Job role)



 

 

Last date for Registration

 

3rd September 2025 (10.00 am)



 

 

 

Website

 

www.balkan.id

 

 

NOTE: BalkanID does not offer pre-placement offers (PPOs) directly. Students are required to complete a full-time internship successfully with us for a minimum duration . PPOs may be extended based on individual performance and company requirements.


 

Full Stack Engineer



Job Profile https://balkanid.notion.site/Full-Stack-Engineering-Intern-b878a64778904a9499a7bf423065ff0d

 

Service Agreement: 3 months



Job location: Bengaluru (or Remote)

 

No Manual Registration & extension will be entertained.



Interested students are said to register in the Neopat Portal on or before 10 am tomorrow



 

 

Mandatory Note:

 

1. Branches, eligibilities and date for the selection process are tentative and subject to change.

2. Please update your resume with all relevant details and projects done, in Campus interaction Portal as there would be shortlisting by the company for the selection process.

3.  Appear for the selection process in formal dress.

4.  Carry your updated Resumes, photos, College photo ID and all other relevant certificates.

     before the selection process.

5.  Late comers will not be allowed to attend the selection process. 

 

 


--

Warm regards

Dr. V. Samuel Rajkumar, B.E.,MBA, MHRM, PhD

Director(Career Development Centre)

VIT Vellore

Vellore Institute of Technology (VIT), India -

Engineering and Technology: 142nd in the World and 9th in India(QS World University Rankings by Subject 2025)
Four subjects (CS&IT, data science & AI, EEE and material science) were ranked among the top 200 in the world  (QS World University Rankings by Subject 2025)
10th best University, 13th best research institution and 11th best engineering institution in India (NIRF Ranking, Govt. of India 2024)
2nd   in India and 501- 600 in the world (Shanghai ARWU ranking 2024)
NAAC Accreditation with A++ grade (3.66 out of 4)
396th in the world and  8th in India  (QS World University Rankings : Sustainability 2025)   

Disclaimer:
This message was sent from Vellore Institute of Technology.  The contents of this email may contain legally protected confidential or privileged information of “Vellore Institute of Technology”.  If you are not the intended recipient, you should not disseminate, distribute or copy this e-mail. Please notify the sender immediately and destroy all copies of this message and any attachments. If you have received this email in error, please promptly notify the sender by reply email and delete the original email and any backup copies without reading them.
 
from the above email body, extract the following information and present it in a json format:
Company Name 

Scope (Internship/Placement/Internship leading to Placement)

Type of event (Online Assessment/Interview/Registration/Pre Placement Talk)

Date

Start Time

End Time

Short Description

Forms/Registrations required 

If such info can not be scraped from the email body simply return:
{False}

Remember to be as concise and to the point as possible, return ONLY the json and NOTHING ELSE
 """


if __name__ == "__main__":

    print(extract_email_info(text))