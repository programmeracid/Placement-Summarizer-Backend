def read_branches_from_file():
    return [
  "B.Tech - Aerospace Engineering",
  "B.Tech - Biotechnology",
  "B.Tech - Bioengineering",
  "B.Tech - Chemical Engineering",
  "B.Tech - Civil Engineering",
  "B.Tech - Civil Engineering (In Collaboration with L & T)",
  "B.Tech - Computer Science and Engineering",
  "B.Tech - Computer Science and Engineering (Bioinformatics)",
  "B.Tech - Computer Science and Engineering and Business Systems(in collaboration with TCS)",
  "B.Tech - Computer Science and Engineering (Blockchain)",
  "B.Tech - Computer Science and Engineering (Software Engineering)",
  "B.Tech - Computer Science and Engineering (Data Science)",
  "B.Tech - Computer Science and Engineering (Artificial Intelligence and Machine Learning)",
  "B.Tech - Computer Science and Engineering (Artificial Intelligence and Data Engineering)",
  "B.Tech - Computer Science and Engineering (Artificial Intelligence and Robotics)",
  "B.Tech - Computer Science and Engineering (Cyber Security)",
  "B.Tech - Computer Science and Engineering (Cyber Physical Systems)",
  "B.Tech - Computer Science & Engineering (Cyber Security & Digital Forensics)",
  "B.Tech - Computer Science & Engineering (Cloud Computing & Automation)",
  "B.Tech - Computer Science & Engineering (E-Commerce Technology)",
  "B.Tech - Computer Science & Engineering (Education Technology)",
  "B.Tech - Computer Science & Engineering (Gaming Technology)",
  "B.Tech. Computer Science and Business Systems",
  "B.Tech - Computer Science & Engineering (Health Informatics)",
  "B.Tech - Computer Science and Engineering (Data Analytics)",
  "B.Tech - Electrical and Computer Science Engineering",
  "B.Tech - Electronics and Communication Engineering",
  "B.Tech - Electronics and Communication Engineering (VLSI)",
  "B.Tech - Electrical and Electronics Engineering",
  "B.Tech - Electronics and Instrumentation Engineering",
  "B.Tech - Electronics and Communication Engineering (Biomedical Engineering)",
  "B.Tech - Electronics Engineering (VLSI Design and Technology)",
  "B.Tech - Electronics and Computer Engineering",
  "B.Tech - Electronics and Communication Engineering (Embedded Systems)",
  "B.Tech - Electronics & Communication Engineering (Artificial Intelligence & Cybernetics)",
  "B.Tech - Fashion Technology",
  "B.Tech - Health Sciences and Technology",
  "B.Tech - Information Technology",
  "B.Tech - Mechanical Engineering",
  "B.Tech - Mechanical Engineering (Automotive Design)",
  "B.Tech - Mechanical Engineering (Artificial Intelligence & Robotics)",
  "B.Tech - Mechanical Engineering (Electric Vehicles)",
  "B.Tech - Mechatronics and Automation",
  "B.Tech - Mechanical Engineering (Robotics)",
  "B.Tech - Mechanical Engineering (Smart Manufacturing)"
]

from firebase_init import firestore_init

def upload_branches():
    db = firestore_init()
    branches = read_branches_from_file()

    for branch in branches:
        db.collection("branches").document(branch).set({"name": branch})

    print(f"✅ Uploaded {len(branches)} branches to Firestore.")

if __name__ == "__main__":
    #upload_branches()
    print(len("Vellore Institute of Technology (VIT), India - Engineering and Technology: 142 nd in the World and 9 th in India(QS World University Rankings by Subject 2025) Four subjects (CS&IT, data science & AI, EEE and material science) were ranked among the top 200 in the world (QS World University Rankings by Subject 2025) 10 th best University, 13 th best research institution and 11 th best engineering institution in India (NIRF Ranking, Govt. of India 2024) 2 nd in India and 501- 600 in the world (Shanghai ARWU ranking 2024) NAAC Accreditation with A++ grade (3.66 out of 4) 396 th in the world and 8 th in India (QS World University Rankings : Sustainability 2025) Disclaimer: This message was sent from Vellore Institute of Technology. The contents of this email may contain legally protected confidential or privileged information of “Vellore Institute of Technology”. If you are not the intended recipient, you should not disseminate, distribute or copy this e-mail. Please notify the sender immediately and destroy all copies of this message and any attachments. If you have received this email in error, please promptly notify the sender by reply email and delete the original email and any backup copies without reading them."))