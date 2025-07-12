import streamlit as st
import hashlib
from datetime import datetime
import requests
import json
# from app import inject_custom_css

# Page Config
st.set_page_config(
    page_title="BrightCore Application",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def inject_custom_css():
    st.markdown("""
    <style>
        /* Remove all sidebar elements */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        
        /* Remove the main sidebar toggle button (hamburger) */
        button[title="View fullscreen"] {
            display: none !important;
        }
        
        /* Remove the arrow icon (expand/collapse button) */
        div[data-testid="stToolbar"] {
            display: none !important;
        }
        
        /* Remove the resize handle */
        div[data-testid="stDecoration"] {
            display: none !important;
        }
        
        /* Adjust main content padding */
        .stApp {
            padding: 0 !important;
            margin: 0 !important;
        }
        
        /* Remove Streamlit's default header/footer */
        header[data-testid="stHeader"], footer[data-testid="stFooter"] {
            display: none !important;
        }
        /* Base Styles */
        body, .stApp {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: #e0e0e0;
            font-family: 'Segoe UI', sans-serif;
        }
        
        /* Modern Navbar */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 5%;
            margin: -1rem -1rem 30px -1rem;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e) !important;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
            position: sticky;
            top: 0;
            z-index: 1000;
            backdrop-filter: blur(5px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .navbar-title {
            font-size: 2.2rem;
            margin: 0;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 10px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
            background: linear-gradient(to right, #ffffff, #f9f9f9);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .navbar-tabs {
            display: flex;
            gap: 15px;
        }
        
        .navbar-tab {
            justify-content: center;
            padding: 8px 20px;
            color: rgba(255, 255, 255, 0.9);
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            font-size: 1rem;
            position: relative;
            white-space: nowrap;
            border-radius: 50px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .navbar-tab:hover {
            color: white;
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .navbar-tab.active {
            color: white;
            background: rgba(255, 255, 255, 0.3);
            font-weight: 700;
        }
        
        .navbar-tab.active::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 50%;
            transform: translateX(-50%);
            width: 60%;
            height: 3px;
            background: white;
            border-radius: 3px;
        }
        
        /* Hero Section */
        .hero-section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 10px 40px;
            border-radius: 16px;
            text-align: center;
            margin-top: 0;
            margin-bottom: 50px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }
        
        .hero-content {
            position: relative;
            z-index: 2;
        }
        
        .hero-header {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 20px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
            background: linear-gradient(to right, #ffffff, #f9f9f9);
            -webkit-background-clip: text;
            background-clip: text;
        }
        
        .hero-subtitle {
            font-size: 22px;
            color: rgba(255,255,255,0.9);
            margin-bottom: 30px;
        }
        
        /* Cards */
        .custom-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            margin-bottom: 25px;
            height: 100%;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .custom-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 28px rgba(0,0,0,0.2);
            border-color: rgba(255, 255, 255, 0.4);
        }
        
        .custom-card h2 {
            color: white;
            margin-top: 0;
        }
        
        .custom-card p {
            color: rgba(255,255,255,0.8);
        }
        
        .custom-card ul {
            padding-left: 20px;
            color: rgba(255,255,255,0.8);
        }
        
        /* Buttons */
        .stButton>button {
    border-radius: 50px;
    padding: 12px 28px;
    font-weight: 700;
    background: rgba(255, 255, 255, 0.08) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    letter-spacing: 0.5px;
}

.stButton>button:hover {
    background: rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(255, 255, 255, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.stButton>button:active {
    transform: translateY(0);
    background: rgba(255, 255, 255, 0.05) !important;
}

.stButton>button::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255, 255, 255, 0.1),
        transparent
    );
    transition: 0.5s;
}

.stButton>button:hover::after {
    left: 100%;
}

/* For gold accent version (optional) */
.stButton>button.accent {
    color: #fdbb2d !important;
    border-color: rgba(253, 187, 45, 0.4);
}

.stButton>button.accent:hover {
    background: rgba(253, 187, 45, 0.1) !important;
}
        
        /* Images */
        .feature-img {
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            margin-bottom: 25px;
            width: 100%;
            height: 250px;
            object-fit: cover;
        }
        
        .feature-img:hover {
            transform: scale(1.02);
        }
        
        /* Testimonials */
        .testimonial-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            margin: 25px 0;
            border-left: 4px solid #fdbb2d;
        }
        
        .testimonial-text {
            font-style: italic;
            color: rgba(255,255,255,0.9);
            margin-bottom: 20px;
        }
        
        .testimonial-author {
            font-weight: 700;
            color: white;
        }
        
        /* Feature Cards */
        .feature-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            margin: 25px 0;
            border-left: 4px solid #5f2c82;
            transition: all 0.3s ease;
            text-align: center;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 28px rgba(0,0,0,0.2);
            border-color: rgba(255, 255, 255, 0.4);
        }
        
        /* Stats */
        .stats-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 30px;
            border-radius: 16px;
            text-align: center;
            margin: 15px 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .navbar {
                flex-direction: column;
                gap: 15px;
                padding: 15px;
            }
            
            .navbar-tabs {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 10px;
            }
            
            .hero-header {
                font-size: 2.5rem;
            }
            
            .hero-subtitle {
                font-size: 18px;
            }
            
            .custom-card {
                padding: 20px;
            }
            
            .feature-img {
                height: 200px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
inject_custom_css()


# Firebase Configuration
FIREBASE_PROJECT_ID = "brightcore-86c38"  # Replace with your Firebase project ID
FIREBASE_DB_URL = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents"

# Initialize session state
if 'application_submitted' not in st.session_state:
    st.session_state.application_submitted = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    return '@' in email and '.' in email.split('@')[-1]

def validate_password(password):
    return len(password) >= 8

def firebase_store_application(user_data):
    """Store application in Firestore"""
    doc_path = f"applications/{user_data['email']}"
    url = f"{FIREBASE_DB_URL}/{doc_path}"
    
    firestore_data = {
        "fields": {
            "first_name": {"stringValue": user_data["first_name"]},
            "last_name": {"stringValue": user_data["last_name"]},
            "email": {"stringValue": user_data["email"]},
            "phone": {"stringValue": user_data["phone"]},
            "university": {"stringValue": user_data["university"]},
            "degree": {"stringValue": user_data["degree"]},
            "major": {"stringValue": user_data["major"]},
            "program": {"stringValue": user_data["program"]},
            "graduation_year": {"integerValue": str(user_data["graduation_year"])},
            "programming_languages": {
                "arrayValue": {
                    "values": [{"stringValue": lang} for lang in user_data["programming_languages"]]
                }
            },
            "project_description": {"stringValue": user_data["project_description"]},
            "password_hash": {"stringValue": user_data["password_hash"]},
            "application_date": {"stringValue": user_data["application_date"]},
            "status": {"stringValue": "pending"}
        }
    }
    
    try:
        response = requests.patch(url, json=firestore_data)
        if response.status_code == 200:
            return {"success": True}
        return {"error": response.text}
    except Exception as e:
        return {"error": str(e)}

def check_existing_user(email):
    """Check if user exists in Firestore"""
    url = f"{FIREBASE_DB_URL}/applications/{email}"
    try:
        response = requests.get(url)
        return response.status_code == 200
    except:
        return False

# Application form
def show_application_form():
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 30px;'>
            <h1 style='color: #fdbb2d; margin-bottom: 10px;margin-top: -80px;'>BrightCore Academy</h1>
            <h2 style='color: #ffffff; font-weight: 300;'>Future Leaders Program Application</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    with st.form("application_form", clear_on_submit=True):
        st.markdown("""
        <style>
        div[data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        }
        .form-section {
            margin-bottom: 25px;
        }
        .section-title {
            color: #fdbb2d;
            font-size: 18px;
            font-weight: 600;
            margin: 20px 0 10px 0;
            padding-bottom: 5px;
            border-bottom: 1px solid rgba(75, 139, 255, 0.3);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Personal Information
        st.markdown('<div class="section-title">Personal Information</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        first_name = col1.text_input("First Name*", placeholder="John")
        last_name = col2.text_input("Last Name*", placeholder="Doe")
        
        col1, col2 = st.columns([2, 1])
        email = col1.text_input("Email Address*", placeholder="john.doe@example.com")
        phone = col2.text_input("Phone Number", placeholder="+1 (123) 456-7890")
        
        # Education Background
        st.markdown('<div class="section-title">Education Background</div>', unsafe_allow_html=True)
        university = st.text_input("University/Institution*", placeholder="Stanford University")
        
        col1, col2, col3 = st.columns(3)
        degree = col1.selectbox("Degree Level*", ["", "High School", "Bachelor's", "Master's", "PhD"], index=2)
        major = col2.text_input("Major/Field of Study*", placeholder="Computer Science")
        graduation_year = col3.number_input("Expected Graduation Year*", min_value=2000, max_value=2030, step=1, value=2025)
        
        # Program Details
        st.markdown('<div class="section-title">Program Details</div>', unsafe_allow_html=True)
        program = st.selectbox("Program of Interest*", 
                             ["", 
                              "Artificial Intelligence", 
                              "Data Science", 
                              "Full Stack Development", 
                              "Cybersecurity", 
                              "Cloud Engineering",
                              "Blockchain Technology"],
                             index=2)
        
        # Technical Skills
        st.markdown('<div class="section-title">Technical Skills</div>', unsafe_allow_html=True)
        programming_languages = st.multiselect(
            "Programming Languages (Select all that apply)",
            ["Python", "JavaScript", "Java", "C++", "Go", "Rust", "Swift", "Kotlin"],
            default=["Python", "JavaScript"]
        )
        other_language = st.text_input("Other Languages (comma separated)", placeholder="TypeScript, Dart")
        
        # Experience
        st.markdown('<div class="section-title">Project Experience</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size: 14px; color: #aaa; margin-bottom: 10px;'>
            Describe a technical project you've worked on (include technologies used, your role, and outcomes)
        </div>
        """, unsafe_allow_html=True)
        project_description = st.text_area("", height=150, 
                                         placeholder="Developed a web application using React and Flask...")
        
        # Account Setup
        st.markdown('<div class="section-title">Account Setup</div>', unsafe_allow_html=True)
        password = st.text_input("Create Password*", type="password", 
                                help="Minimum 8 characters")
        confirm_password = st.text_input("Confirm Password*", type="password")
        
        # Form Submission
        st.markdown('<div style="margin: 25px 0 15px 0;"></div>', unsafe_allow_html=True)
        submitted = st.form_submit_button("Submit Application", use_container_width=True)
        
        if submitted:
            errors = []
            if not first_name: errors.append("First name is required")
            if not last_name: errors.append("Last name is required")
            if not validate_email(email): errors.append("Valid email is required")
            if not university: errors.append("University is required")
            if not degree: errors.append("Degree level is required")
            if not major: errors.append("Major is required")
            if not program: errors.append("Program of interest is required")
            if not project_description: errors.append("Project description is required")
            if not password: errors.append("Password is required")
            if password != confirm_password: errors.append("Passwords do not match")
            if not validate_password(password): errors.append("Password must be at least 8 characters")
            if check_existing_user(email): errors.append("Email already registered")

            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Combine selected and typed languages
                all_languages = programming_languages
                if other_language:
                    all_languages.extend([lang.strip() for lang in other_language.split(",")])
                
                user_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone": phone,
                    "university": university,
                    "degree": degree,
                    "major": major,
                    "program": program,
                    "graduation_year": graduation_year,
                    "programming_languages": all_languages,
                    "project_description": project_description,
                    "password_hash": hash_password(password),
                    "application_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Store in Firebase
                result = firebase_store_application(user_data)
                if "error" in result:
                    st.error(f"Failed to submit application: {result['error']}")
                else:
                    st.session_state.application_submitted = True
                    st.session_state.current_user = email
                    st.success("Application submitted successfully!")
                    st.balloons()
                    
                    # Show next steps
                    st.markdown("""
                    <div style='background: rgba(75, 139, 255, 0.1); padding: 20px; border-radius: 10px; margin-top: 20px;'>
                        <h3 style='color: #fdbb2d; margin-top: 0;'>Next Steps</h3>
                        <ol style='padding-left: 20px;'>
                            <li>You'll receive a confirmation email within 24 hours</li>
                            <li>Our admissions team will review your application</li>
                            <li>Check your dashboard for updates and next steps</li>
                        </ol>
                        <p style='font-style: italic;'>We appreciate your interest in BrightCore Academy!</p>
                    </div>
                    """, unsafe_allow_html=True)
        
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("Back To Home", key="back_button"):
            st.switch_page("app.py")

# Main app logic
def main():
    if not st.session_state.application_submitted:
        show_application_form()
    else:
        st.success(f"Welcome! Your application has been submitted.")
        if st.button("Logout"):
            st.session_state.application_submitted = False
            st.session_state.current_user = None
            st.rerun()

if __name__ == "__main__":
    main()