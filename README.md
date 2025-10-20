# AI-Resume-Screening-Terminal
**🧠 AI Resume Screening Terminal**

AI Resume Screening Terminal is a machine-learning–powered web application designed to analyze resumes, extract key information, predict job categories, and recommend suitable roles.
Built with Flask and a Neon Blue UI, it offers a futuristic interface that simulates an ATS (Applicant Tracking System) environment.

**🚀 Features**

📂 Resume Upload: Supports PDF and DOCX resume uploads.

🤖 Machine Learning Model: Predicts job category (e.g., Data Science, Software Developer).

💼 Role Recommendation: Suggests relevant job titles.

📊 ATS Score: Simulated score based on keyword and skill match.

🧾 Feedback Section: Personalized suggestions to improve resume structure and targeting.

🔍 Information Extraction: Extracts candidate name, email, phone, and skills automatically.

💡 Modern UI: Styled with neon blue and dark theme aesthetics.

**🧩 Tech Stack**
     **Component**	          **Technology**
      Backend	                Python (Flask)
      
      Frontend	                HTML, CSS (Neon Blue Theme), Bootstrap
      
      ML Model	                Scikit-learn / NLP
      
      Resume Parsing    	    PyPDF2, docx2txt, regex
      
      Visualization	            Chart.js / Custom progress bar
      
      Deployment	            Localhost (Flask)

**⚙️ Installation & Setup**

->Follow the steps below to run the project locally:

->Clone the repository

git clone https://github.com/<your-username>/AI-Resume-Screener.git
cd AI-Resume-Screener


->Create and activate a virtual environment

python -m venv venv
venv\Scripts\activate    # For Windows
source venv/bin/activate # For Linux/Mac


->Install dependencies

pip install -r requirements.txt


->Run the Flask application

python app.py


->Open your browser and visit

http://127.0.0.1:5000

**🧠 How It Works**

->Upload a resume file (.pdf or .docx).

->The backend extracts key details (skills, contact info, etc.).

->The ML model classifies the candidate’s domain.

->A role recommendation and ATS feedback are generated.

->Results are displayed on the /pred page with detailed visuals.

**🧾 Example Output**

<img width="1899" height="1012" alt="Screenshot 2025-10-20 193815" src="https://github.com/user-attachments/assets/47e9ad71-377f-4da6-a187-7f10748673cb" />
<img width="1890" height="1007" alt="Screenshot 2025-10-20 193838" src="https://github.com/user-attachments/assets/bd82ab74-d6d3-48ad-9b16-62dbdc58ead8" />
<img width="1891" height="1004" alt="Screenshot 2025-10-20 193852" src="https://github.com/user-attachments/assets/2d60af9c-fcd7-4e6a-bbce-6b20690370df" />
<img width="1896" height="1002" alt="Screenshot 2025-10-20 193904" src="https://github.com/user-attachments/assets/e7de8ea3-1e2f-45fb-81b3-8ea0edbf051f" />


**💬 Future Enhancements**

->Add NLP-based keyword optimization suggestions.

->Integrate real-time job API (e.g., LinkedIn/Indeed).

->Implement multilingual resume support.

->Enable cloud deployment (AWS, Render, or HuggingFace Spaces).

**👩‍💻 Author**

**Areeza Usmani**

gmail:areezausmani@gmail.com

github repo:https://github.com/AreezaUsmani/AI-Resume-Screening-Terminal.git
