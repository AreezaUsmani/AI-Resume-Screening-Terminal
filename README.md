# AI-Resume-Screening-Terminal
**🧠 AI Resume matcher pro**

The AI Skill Matcher Pro is a modern, data-driven application designed to give job seekers an edge in the competitive hiring landscape. By leveraging machine learning principles (mocked via keyword analysis) and providing an intuitive, interactive user interface, it helps candidates analyze their resume fit, identify skill gaps, and practice tailored interview questions.

**✨ Core Features**

**1. Resume Analysis & Dashboard**

ATS Match Score: Get an immediate ATS (Applicant Tracking System) Score based on the keywords and skills extracted from your uploaded resume.

Skill Gap Analysis: Visualize your proficiency in key domains against the required level for your recommended job role using an interactive bar gauge.

Career Recommendations: Receive a Predicted Job Category and a highly Recommended Role based on your experience.

Future Skills: Targeted suggestions for advanced skills to learn next, ensuring you stay ahead in your career path.

**2. Interview Prep Environment**

Dynamic Sessions: Start a structured interview session with 5 questions tailored (simulated) specifically to your predicted job role and extracted skills.

Interactive Practice: Utilize buttons for simulated Voice/Typing an answer, requesting a Hint (STAR method reminder), or Skipping a question.

Simulated AI Scoring: Upon submission, receive instant feedback and a mock score to help you refine your response structure and content.

**3. Candidate Profile**

View mock metrics like Job Matches and Profile Completion.

Simulate Platform Integrations (LinkedIn, GitHub, Stack Overflow) to demonstrate how external data could be synced for a richer analysis.

🛠️ Technology Stack

Component         Technology                     Role

Backend           Python / Flask                 Handles all file I/O (PyPDF2),                                                  routing, and the core data                                                      processing/keyword analysis                                                     logic.

Frontend & UI    HTML5, JavaScript (Vanilla JS)   Manages all client-side view                                                    routing, state for the                                                          Interview Prep session, and                                                     interactive elements.

Styling          Tailwind CSS                      Provides the utility-first                                                      foundation for the modern,                                                      dark-mode-first aesthetic                                                       and full responsiveness                                                         across all devices.

Analysis         Pickle Models (Mocked)            Uses keyword rules within                                                       Python to simulate the                                                          predictive power of a                                                           genuine ML model for role                                                       matching and categorization.


**⚙️ Setup and Installation (For Local Development)**

This application requires Python and Flask to run the server-side processing.

Prerequisites

Python 3.8+

pip (Python package installer)

Steps

Clone the Repository:

git clone [your-repo-link]
cd ai-skill-matcher-pro


Install Dependencies:

pip install Flask PyPDF2


Run the Flask Application:

python app.py


**🧠 How It Works**

->Upload a resume file (.pdf or .docx).

->The backend extracts key details (skills, contact info, etc.).

->The ML model classifies the candidate’s domain.

->A role recommendation and ATS feedback are generated.

->Results are displayed on the /pred page with detailed visuals.

**🧾 Example Output**

<img width="1913" height="930" alt="Screenshot 2025-10-28 185054" src="https://github.com/user-attachments/assets/25a79478-af4d-4b52-9bc0-2550f227a868" />
<img width="1912" height="969" alt="Screenshot 2025-10-28 185115" src="https://github.com/user-attachments/assets/8b502572-3b1a-43cf-8373-1c737ed32e4f" />
<img width="1887" height="967" alt="Screenshot 2025-10-30 191840" src="https://github.com/user-attachments/assets/8ba95a76-cbf3-4794-bfb0-bc50599f59e5" />
<img width="1879" height="926" alt="Screenshot 2025-10-28 185142" src="https://github.com/user-attachments/assets/836582fc-eb6c-479d-9a3c-e6b578fbc501" />
<img width="1891" height="973" alt="Screenshot 2025-10-30 192046" src="https://github.com/user-attachments/assets/64edcd5b-c01c-42a0-866a-5c580732dfe7" />
<img width="1911" height="967" alt="Screenshot 2025-10-30 192012" src="https://github.com/user-attachments/assets/b4aeea71-b7d9-4b9d-af7b-97bca06f2333" />


**💬 Future Enhancements**

->Add NLP-based keyword optimization suggestions.

->Integrate real-time job API (e.g., LinkedIn/Indeed).

->Implement multilingual resume support.

->Enable cloud deployment (AWS, Render, or HuggingFace Spaces).

**👩‍💻 Author**

**Areeza Usmani**

gmail:areezausmani@gmail.com

github repo:https://github.com/AreezaUsmani/AI-Resume-Screening-Terminal.git
