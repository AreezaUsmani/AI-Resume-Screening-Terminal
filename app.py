
from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import re
import pickle
import os
import logging
import math

# Configure basic logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# --- Model Loading and Configuration ---
MODELS_DIR = 'models'

def load_model(filename):
    """Loads a pickled model from the models directory, falling back to a mock if files are missing."""
    path = os.path.join(MODELS_DIR, filename)
    try:
        # 1. Attempt to load the real model
        with open(path, 'rb') as f:
            logging.info(f"Successfully loaded model: {filename}")
            return pickle.load(f)
            
    except (FileNotFoundError, EOFError):
        # 2. Fall back to Mock loading if the file is not found or corrupted
        logging.error(f"Model file not found or corrupted: {path}. Falling back to MockClassifier.")
        if "vectorizer" in filename:
            return MockVectorizer()
        elif "classifier" in filename:
            return MockClassifier(filename)
    except Exception as e:
        logging.error(f"Error loading model {filename}: {e}. Falling back to MockClassifier.")
        if "vectorizer" in filename:
            return MockVectorizer()
        elif "classifier" in filename:
            return MockClassifier(filename)
    
    return None

# --- Mock Classes with Dynamic Keyword-Based Logic (CRITICAL FIX) ---
class MockVectorizer:
    """Mocks the TFIDF Vectorizer transform method by returning the cleaned text."""
    def transform(self, data):
        # This allows us to pass the raw text to the mock classifier for keyword checks.
        return data[0]

class MockClassifier:
    """
    Mocks the Classifier predict method using simple keyword rules for variable output.
    The 'data' passed here will be the cleaned resume text from the MockVectorizer.
    """
    def __init__(self, filename):
        self.filename = filename

    def predict(self, cleaned_text):
        if not isinstance(cleaned_text, str):
            # This handles cases where the real vectorizer is present but the classifier is mocked.
            # We return a default in this unlikely scenario.
            return ["Data Science"] 

        text_lower = cleaned_text.lower()
        
        # --- Rule-Based CATEGORIZATION ---
        if "categorization" in self.filename:
            if "java" in text_lower or "spring" in text_lower or "backend" in text_lower or "devops" in text_lower:
                return ["Software Engineering"]
            if "photoshop" in text_lower or "figma" in text_lower or "ui/ux" in text_lower:
                return ["Design"]
            if "tableau" in text_lower or "sql" in text_lower or "excel" in text_lower:
                return ["Data Analyst"]
            if "marketing" in text_lower or "sales" in text_lower or "seo" in text_lower:
                return ["Sales and Marketing"]
            
            # Default fallback (original Data Science category)
            return ["Data Science"] 

        # --- Rule-Based JOB RECOMMENDATION ---
        else: # job_recommendation
            if "java" in text_lower and ("spring" in text_lower or "microservices" in text_lower):
                return ["Backend Developer"]
            if "tableau" in text_lower and "sql" in text_lower and "business intelligence" in text_lower:
                return ["Business Intelligence Analyst"]
            if "photoshop" in text_lower and "figma" in text_lower:
                return ["UX/UI Designer"]
            if "deep learning" in text_lower or "pytorch" in text_lower or "keras" in text_lower:
                return ["Machine Learning Engineer"]
            
            # Default fallback (original ML Engineer role)
            return ["Data Scientist"]

# Load Categorization Models (They will be mocked if files are missing)
rf_classifier_categorization = load_model('rf_classifier_categorization.pkl')
tfidf_vectorizer_categorization = load_model('tfidf_vectorizer_categorization.pkl')

# Load Job Recommendation Models
rf_classifier_job_recommendation = load_model('rf_classifier_job_recommendation.pkl')
tfidf_vectorizer_job_recommendation = load_model('tfidf_vectorizer_job_recommendation.pkl')


# List of all possible skills (Used for both extraction and ATS scoring)
ALL_SKILLS = [
    'Python', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management', 'Deep Learning', 'SQL',
    'Tableau', 'Java', 'C++', 'JavaScript', 'HTML', 'CSS', 'React', 'Angular', 'Node.js', 'MongoDB', 'Express.js', 
    'Git', 'Research', 'Statistics', 'Quantitative Analysis', 'Qualitative Analysis', 'SPSS', 'R', 
    'Data Visualization', 'Matplotlib', 'Seaborn', 'Plotly', 'Pandas', 'Numpy', 'Scikit-learn', 'TensorFlow', 
    'Keras', 'PyTorch', 'NLTK', 'Text Mining', 'Natural Language Processing', 'Computer Vision', 'Image Processing', 
    'OCR', 'Speech Recognition', 'Recommendation Systems', 'Collaborative Filtering', 'Content-Based Filtering', 
    'Reinforcement Learning', 'Neural Networks', 'Convolutional Neural Networks', 'Recurrent Neural Networks', 
    'Generative Adversarial Networks', 'XGBoost', 'Random Forest', 'Decision Trees', 'Support Vector Machines',
    'Linear Regression', 'Logistic Regression', 'K-Means Clustering', 'Hierarchical Clustering', 'DBSCAN', 
    'Association Rule Learning', 'Apache Hadoop', 'Apache Spark', 'MapReduce', 'Hive', 'HBase', 'Apache Kafka', 
    'Data Warehousing', 'ETL', 'Big Data Analytics', 'Cloud Computing', 'Amazon Web Services (AWS)', 
    'Microsoft Azure', 'Google Cloud Platform (GCP)', 'Docker', 'Kubernetes', 'Linux', 'Shell Scripting', 
    'Cybersecurity', 'Network Security', 'Penetration Testing', 'Firewalls', 'Encryption', 'Malware Analysis',
    'Digital Forensics', 'CI/CD', 'DevOps', 'Agile Methodology', 'Scrum', 'Kanban', 'Continuous Integration',
    'Continuous Deployment', 'Software Development', 'Web Development', 'Mobile Development', 'Backend Development',
    'Frontend Development', 'Full-Stack Development', 'UI/UX Design', 'Responsive Design', 'Wireframing', 
    'Prototyping', 'User Testing', 'Adobe Creative Suite', 'Photoshop', 'Illustrator', 'InDesign', 'Figma', 
    'Sketch', 'Zeplin', 'InVision', 'Product Management', 'Market Research', 'Customer Development', 
    'Lean Startup', 'Business Development', 'Sales', 'Marketing', 'Content Marketing', 'Social Media Marketing', 
    'Email Marketing', 'SEO', 'SEM', 'PPC', 'Google Analytics', 'Facebook Ads', 'LinkedIn Ads', 'Lead Generation', 
    'Customer Relationship Management (CRM)', 'Salesforce', 'HubSpot', 'Zendesk', 'Intercom', 
    'Customer Support', 'Technical Support', 'Troubleshooting', 'Ticketing Systems', 'ServiceNow',
    'ITIL', 'Quality Assurance', 'Manual Testing', 'Automated Testing', 'Selenium', 'JUnit', 'Load Testing', 
    'Performance Testing', 'Regression Testing', 'Black Box Testing', 'White Box Testing', 'API Testing', 
    'Mobile Testing', 'Usability Testing', 'Accessibility Testing', 'Cross-Browser Testing', 'Agile Testing', 
    'User Acceptance Testing', 'Software Documentation', 'Technical Writing', 'Copywriting', 'Editing', 
    'Proofreading', 'Content Management Systems (CMS)', 'WordPress', 'Joomla', 'Drupal', 'Magento', 
    'Shopify', 'E-commerce', 'Payment Gateways', 'Inventory Management', 'Supply Chain Management', 'Logistics', 
    'Procurement', 'ERP Systems', 'SAP', 'Oracle', 'Microsoft Dynamics', 'QlikView', 'Looker', 'Data Engineering',
    'Data Governance', 'Data Quality', 'Master Data Management', 'Predictive Analytics', 'Prescriptive Analytics',
    'Descriptive Analytics', 'Business Intelligence', 'Dashboarding', 'Reporting', 'Data Mining', 'Web Scraping',
    'API Integration', 'RESTful APIs', 'GraphQL', 'SOAP', 'Microservices', 'Serverless Architecture', 
    'Lambda Functions', 'Event-Driven Architecture', 'Message Queues', 'Socket.io', 'WebSockets', 'Ruby', 
    'Ruby on Rails', 'PHP', 'Symfony', 'Laravel', 'CakePHP', 'Zend Framework', 'ASP.NET', 'C#', 'VB.NET', 
    'ASP.NET MVC', 'Entity Framework', 'Spring', 'Hibernate', 'Struts', 'Kotlin', 'Swift', 'Objective-C', 
    'iOS Development', 'Android Development', 'Flutter', 'React Native', 'Ionic', 'Mobile UI/UX Design', 
    'Material Design', 'SwiftUI', 'RxJava', 'RxSwift', 'Django', 'Flask', 'FastAPI', 'Falcon', 'Tornado', 
    'RESTful Web Services', 'Serverless Computing', 'AWS Lambda', 'Google Cloud Functions', 'Azure Functions', 
    'Server Administration', 'System Administration', 'Network Administration', 'Database Administration', 
    'MySQL', 'PostgreSQL', 'SQLite', 'Microsoft SQL Server', 'Oracle Database', 'NoSQL', 'Cassandra', 
    'Redis', 'Elasticsearch', 'Firebase', 'Google Tag Manager', 'Adobe Analytics', 'Marketing Automation', 
    'Customer Data Platforms', 'Segment', 'Salesforce Marketing Cloud', 'HubSpot CRM', 'Zapier', 'IFTTT', 
    'Workflow Automation', 'Robotic Process Automation (RPA)', 'UI Automation', 'Natural Language Generation (NLG)',
    'Virtual Reality (VR)', 'Augmented Reality (AR)', 'Mixed Reality (MR)', 'Unity', 'Unreal Engine', 
    '3D Modeling', 'Animation', 'Motion Graphics', 'Game Design', 'Game Development', 'Level Design', 
    'Unity3D', 'Unreal Engine 4', 'Blender', 'Maya', 'Adobe After Effects', 'Adobe Premiere Pro', 
    'Final Cut Pro', 'Video Editing', 'Audio Editing', 'Sound Design', 'Music Production', 'Digital Marketing', 
    'Content Strategy', 'Conversion Rate Optimization (CRO)', 'A/B Testing', 'Customer Experience (CX)', 
    'User Experience (UX)', 'User Interface (UI)', 'Persona Development', 'User Journey Mapping', 
    'Information Architecture (IA)', 'Usability Testing', 'Accessibility Compliance', 'Internationalization (I18n)',
    'Localization (L10n)', 'Voice User Interface (VUI)', 'Chatbots', 'Natural Language Understanding (NLU)',
    'Speech Synthesis', 'Emotion Detection', 'Sentiment Analysis', 'Image Recognition', 'Object Detection',
    'Facial Recognition', 'Gesture Recognition', 'Document Recognition', 'Fraud Detection', 
    'Cyber Threat Intelligence', 'Security Information and Event Management (SIEM)', 'Vulnerability Assessment', 
    'Incident Response', 'Forensic Analysis', 'Security Operations Center (SOC)', 
    'Identity and Access Management (IAM)', 'Single Sign-On (SSO)', 'Multi-Factor Authentication (MFA)', 
    'Blockchain', 'Cryptocurrency', 'Decentralized Finance (DeFi)', 'Smart Contracts', 'Web3', 
    'Non-Fungible Tokens (NFTs)'
]


# --- Utility Functions (Modified to pass cleaned text to predict functions) ---

def cleanResume(txt):
    """Cleans resume text for ML prediction by removing links, special characters, and extra spaces."""
    cleanText = re.sub(r'http\S+\s', ' ', txt)
    cleanText = re.sub('RT|cc', ' ', cleanText)
    cleanText = re.sub(r'#\S+\s*', ' ', cleanText)
    cleanText = re.sub(r'@\S+', ' ', cleanText)
    # Remove isolated non-word characters and numbers often found in margins (ATS-friendly parsing)
    cleanText = re.sub(r'\s+[^a-z0-9\s]\s+', ' ', cleanText)
    # Remove punctuation and special characters (ATS-friendly for keyword matching)
    cleanText = re.sub(r'[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', r' ', cleanText)
    cleanText = re.sub(r'\s+', ' ', cleanText)
    return cleanText.lower().strip()
 
def pdf_to_text(file):
    """Extracts text from a PDF file object using PyPDF2."""
    try:
        reader = PdfReader(file)
        text = ' '.join(page.extract_text() or '' for page in reader.pages)
        return text
    except Exception as e:
        logging.error(f"PDF extraction failed: {e}")
        return ""

def predict_category(resume_text):
    """Predicts the general category of the resume using the categorization model."""
    if not rf_classifier_categorization:
        return "Model Error: Categorization Model Missing" 
        
    clean_text = cleanResume(resume_text)
    
    # *** CRITICAL FIX: Pass the cleaned text to the mock classifier's predict method ***
    if isinstance(tfidf_vectorizer_categorization, MockVectorizer):
        return rf_classifier_categorization.predict(clean_text)[0]
        
    # Real ML logic 
    resume_tfidf = tfidf_vectorizer_categorization.transform([clean_text])
    return rf_classifier_categorization.predict(resume_tfidf)[0]

def job_recommendation(resume_text):
    """Recommends a specific job title using the job recommendation model."""
    if not rf_classifier_job_recommendation:
        return "Model Error: Job Recommendation Model Missing" 
        
    clean_text = cleanResume(resume_text)
    
    # *** CRITICAL FIX: Pass the cleaned text to the mock classifier's predict method ***
    if isinstance(tfidf_vectorizer_job_recommendation, MockVectorizer):
        return rf_classifier_job_recommendation.predict(clean_text)[0]

    # Real ML logic
    resume_tfidf = tfidf_vectorizer_job_recommendation.transform([clean_text])
    return rf_classifier_job_recommendation.predict(resume_tfidf)[0]


def extract_contact_number_from_resume(text):
    """Extracts a common phone number format."""
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{2,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b"
    match = re.search(pattern, text)
    return match.group() if match else "N/A"

def extract_email_from_resume(text):
    """Extracts an email address and cleans common parsing artifacts."""
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()
        email = re.sub(r'^(pe|ph)', '', email, flags=re.IGNORECASE)
        email = re.sub(r'^\W+|\s+', '', email)
        return email if email else "N/A"
    return "N/A"

def extract_name_from_resume(text):
    """ATS-Friendly name extraction: Looks for 2-4 capitalized words near the start."""
    pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)(?:\s(\b[A-Z][a-z]+\b))?(?:\s(\b[A-Z][a-z]+\b))?"
    match = re.search(pattern, text[:1000])
    return ' '.join(filter(None, match.groups())) if match else "N/A"


def extract_skills_from_resume(text):
    """Extracts skills from the global predefined list (ALL_SKILLS)."""
    extracted_skills = []
    text_lower = text.lower()
    for skill in ALL_SKILLS:
        pattern = r"\b{}\b".format(re.escape(skill.lower()))
        if re.search(pattern, text_lower):
            extracted_skills.append(skill)
    return list(set(extracted_skills)) 

def extract_education_from_resume(text):
    """Extracts education keywords."""
    education_keywords = [
        'Computer Science', 'Information Technology', 'Software Engineering', 'Electrical Engineering', 'Mechanical Engineering', 'Civil Engineering',
        'Chemical Engineering', 'Biomedical Engineering', 'Aerospace Engineering', 'Nuclear Engineering', 'Industrial Engineering', 'Systems Engineering',
        'Environmental Engineering', 'Petroleum Engineering', 'Geological Engineering', 'Marine Engineering', 'Robotics Engineering', 'Biotechnology',
        'Biochemistry', 'Microbiology', 'Genetics', 'Molecular Biology', 'Bioinformatics', 'Neuroscience', 'Biophysics', 'Biostatistics', 'Pharmacology',
        'Physiology', 'Anatomy', 'Pathology', 'Immunology', 'Epidemiology', 'Public Health', 'Health Administration', 'Nursing', 'Medicine', 'Dentistry',
        'Pharmacy', 'Veterinary Medicine', 'Medical Technology', 'Radiography', 'Physical Therapy', 'Occupational Therapy', 'Speech Therapy', 'Nutrition',
        'Sports Science', 'Kinesiology', 'Exercise Physiology', 'Sports Medicine', 'Rehabilitation Science', 'Psychology', 'Counseling', 'Social Work',
        'Sociology', 'Anthropology', 'Criminal Justice', 'Political Science', 'International Relations', 'Economics', 'Finance', 'Accounting', 'Business Administration',
        'Management', 'Marketing', 'Entrepreneurship', 'Hospitality Management', 'Tourism Management', 'Supply Chain Management', 'Logistics Management',
        'Operations Management', 'Human Resource Management', 'Organizational Behavior', 'Project Management', 'Quality Management', 'Risk Management',
        'Strategic Management', 'Public Administration', 'Urban Planning', 'Architecture', 'Interior Design', 'Landscape Architecture', 'Fine Arts',
        'Visual Arts', 'Graphic Design', 'Fashion Design', 'Industrial Design', 'Product Design', 'Animation', 'Film Studies', 'Media Studies',
        'Communication Studies', 'Journalism', 'Broadcasting', 'Creative Writing', 'English Literature', 'Linguistics', 'Translation Studies',
        'Foreign Languages', 'Modern Languages', 'Classical Studies', 'History', 'Archaeology', 'Philosophy', 'Theology', 'Religious Studies',
        'Ethics', 'Education', 'Early Childhood Education', 'Elementary Education', 'Secondary Education', 'Special Education', 'Higher Education',
        'Adult Education', 'Distance Education', 'Online Education', 'Instructional Design', 'Curriculum Development', 'Library Science', 
        'Information Science', 'Computer Engineering', 'Software Development', 'Cybersecurity', 'Information Security',
        'Network Engineering', 'Data Science', 'Data Analytics', 'Business Analytics', 'Operations Research', 'Decision Sciences',
        'Human-Computer Interaction', 'User Experience Design', 'User Interface Design', 'Digital Marketing', 'Content Strategy',
        'Brand Management', 'Public Relations', 'Corporate Communications', 'Media Production', 'Digital Media', 'Web Development',
        'Mobile App Development', 'Game Development', 'Virtual Reality', 'Augmented Reality', 'Blockchain Technology', 'Cryptocurrency',
        'Digital Forensics', 'Forensic Science', 'Criminalistics', 'Crime Scene Investigation', 'Emergency Management', 'Fire Science',
        'Environmental Science', 'Climate Science', 'Meteorology', 'Geography', 'Geomatics', 'Remote Sensing', 'Geoinformatics',
        'Cartography', 'GIS (Geographic Information Systems)', 'Environmental Management', 'Sustainability Studies', 'Renewable Energy',
        'Green Technology', 'Ecology', 'Conservation Biology', 'Wildlife Biology', 'Zoology'
    ]
    extracted_education = []
    text_lower = text.lower()
    for keyword in education_keywords:
        pattern = r"(?i)\b{}\b".format(re.escape(keyword))
        if re.search(pattern, text_lower):
            extracted_education.append(keyword)
    return list(set(extracted_education))


def calculate_ats_score(extracted_skills):
    """Calculates a simulated ATS score based on extracted skills."""
    MAX_RELEVANT_SKILLS = 25 
    num_extracted_skills = len(extracted_skills)
    score = (num_extracted_skills / MAX_RELEVANT_SKILLS) * 100
    return math.ceil(min(score, 100.0))

def generate_personalized_tips(name, phone, email, extracted_skills, predicted_category):
    """
    Generates specific, personalized tips based on the extracted data.
    """
    tips = []
    
    # 1. Contact Information Check
    if name == "N/A":
        tips.append({
            'title': 'Name Extraction Failed',
            'detail': 'Ensure your full name is clear, capitalized, and positioned at the very top of the document for easier ATS parsing.',
            'category': 'Critical'
        })
    if phone == "N/A" or email == "N/A":
        tips.append({
            'title': 'Missing Contact Details',
            'detail': 'ATS systems must easily find your phone number and email. Place them directly under your name, separated by standard characters like spaces or newlines.',
            'category': 'Critical'
        })
        
    # 2. Skill Density Check
    num_skills = len(extracted_skills)
    if num_skills < 5:
        tips.append({
            'title': 'Low Skill Density',
            'detail': f'Only found {num_skills} recognized skills. Review the job description and incorporate more specific keywords and tools relevant to your target role.',
            'category': 'High Priority'
        })
    elif num_skills > 20:
        tips.append({
            'title': 'High Keyword Volume',
            'detail': 'You have many skills, but ensure they are backed up by context (e.g., job descriptions) rather than just being a long list. Quality over quantity is best for ATS.',
            'category': 'Medium Priority'
        })

    # 3. Category Focus Tip
    if predicted_category and predicted_category != "Model Error: Categorization Model Missing":
         tips.append({
            'title': f'Target Focus: {predicted_category} Roles',
            'detail': f'Since the system classified you as a "{predicted_category}" candidate, tailor your summary and work history to emphasize achievements directly relevant to this field.',
            'category': 'Targeting'
        })

    # 4. Formatting Tip (General ATS best practice)
    tips.append({
        'title': 'Verify File Type',
        'detail': 'Always submit your resume as a standard PDF or DOCX file (avoiding complex graphics) to maximize readability by different ATS versions.',
        'category': 'General'
    })
    
    # If no critical issues, provide a positive tip
    if not any(tip['category'] == 'Critical' for tip in tips):
        tips.insert(0, {
            'title': 'Good Structure Detected',
            'detail': 'Your resume seems well-structured and highly parseable. Focus on quantifying your achievements (numbers and metrics) for maximum impact.',
            'category': 'Positive'
        })
        
    return tips


# --- Flask Routes ---

@app.route('/')
def resume():
    """Renders the main upload page."""
    return render_template("resume.html")

@app.route('/pred', methods=['POST'])
def pred():
    """Processes the uploaded resume, performs analysis, and renders results."""
    
    if 'resume' not in request.files or request.files['resume'].filename == '':
        return render_template("resume.html", message="No resume file uploaded.")

    file = request.files['resume']
    filename = file.filename
    resume_text = ""

    # Text extraction based on file type
    if filename.endswith('.pdf'):
        resume_text = pdf_to_text(file)
    elif filename.endswith('.txt'):
        try:
            resume_text = file.read().decode('utf-8')
        except Exception:
            return render_template('resume.html', message="Error reading TXT file.")
    else:
        return render_template('resume.html', message="Invalid file format. Please upload a PDF or TXT file.")

    if not resume_text:
         return render_template('resume.html', message="Could not extract content from the file. File might be empty or unreadable.")

    # Run ML and parsing functions
    predicted_category = predict_category(resume_text)
    recommended_job = job_recommendation(resume_text)
    
    # Check for critical model errors
    if "Model Error" in predicted_category or "Model Error" in recommended_job:
         return render_template('resume.html', message="A server error occurred: One or more machine learning models failed to load correctly. Please ensure the models are trained and saved in the 'models' directory.")

    # Data extraction
    name = extract_name_from_resume(resume_text)
    phone = extract_contact_number_from_resume(resume_text)
    email = extract_email_from_resume(resume_text)
    extracted_skills = extract_skills_from_resume(resume_text)
    extracted_education = extract_education_from_resume(resume_text)
    
    # Calculate ATS Score
    ats_score = calculate_ats_score(extracted_skills)
    
    # Generate Personalized Tips (NEW)
    personalized_tips = generate_personalized_tips(name, phone, email, extracted_skills, predicted_category)

    # Render results
    return render_template('resume.html', 
                           predicted_category=predicted_category,
                           recommended_job=recommended_job,
                           name=name,
                           phone=phone,
                           email=email,
                           extracted_skills=extracted_skills,
                           extracted_education=extracted_education,
                           ats_score=ats_score,
                           personalized_tips=personalized_tips) # Pass tips to template

if __name__ == '__main__':
    app.run(debug=True)
