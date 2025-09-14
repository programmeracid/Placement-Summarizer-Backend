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
    upload_branches()