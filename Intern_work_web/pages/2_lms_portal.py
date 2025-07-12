import streamlit as st
import hashlib
from datetime import datetime, date, timedelta
import requests
import json
import io
import zipfile
import base64
# from app import inject_custom_css

# -----------------------
# Streamlit Config (MUST BE FIRST)
# -----------------------
st.set_page_config(
    page_title="BrightCore LMS Portal",
    page_icon="🎓",
    layout="wide",
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


# -----------------------
# Firebase Configuration
# -----------------------
FIREBASE_PROJECT_ID = "brightcore-86c38"
FIREBASE_DB_URL = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents"

# -----------------------
# Session State Initialization
# -----------------------
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

if 'initialized' not in st.session_state:
    # First run - fetch users and check for persisted login
    try:
        response = requests.get(f"{FIREBASE_DB_URL}/applications")
        if response.status_code == 200:
            documents = response.json().get('documents', [])
            users_db = {}
            for doc in documents:
                fields = doc.get('fields', {})
                email = fields.get('email', {}).get('stringValue', '').lower().strip()
                if email:
                    users_db[email] = {
                        "first_name": fields.get('first_name', {}).get('stringValue', ''),
                        "last_name": fields.get('last_name', {}).get('stringValue', ''),
                        "email": email,
                        "phone": fields.get('phone', {}).get('stringValue', ''),
                        "university": fields.get('university', {}).get('stringValue', ''),
                        "degree": fields.get('degree', {}).get('stringValue', ''),
                        "major": fields.get('major', {}).get('stringValue', ''),
                        "program": fields.get('program', {}).get('stringValue', 'N/A'),
                        "graduation_year": int(fields.get('graduation_year', {}).get('integerValue', 0)),
                        "password": fields.get('password_hash', {}).get('stringValue', ''),
                        "status": fields.get('status', {}).get('stringValue', 'pending'),
                        "role": fields.get('role', {}).get('stringValue', 'student'),
                        "total_marks": int(fields.get('total_marks', {}).get('integerValue', 0)),
                        "tasks": []
                    }
                    if 'tasks' in fields:
                        tasks = fields['tasks'].get('arrayValue', {}).get('values', [])
                        for t in tasks:
                            task_data = {
                                "name": t.get('mapValue', {}).get('fields', {}).get('name', {}).get('stringValue', ''),
                                "description": t.get('mapValue', {}).get('fields', {}).get('description', {}).get('stringValue', ''),
                                "due_date": t.get('mapValue', {}).get('fields', {}).get('due_date', {}).get('stringValue', ''),
                                "max_marks": int(t.get('mapValue', {}).get('fields', {}).get('max_marks', {}).get('integerValue', 0)),
                                "assigned_date": t.get('mapValue', {}).get('fields', {}).get('assigned_date', {}).get('stringValue', ''),
                                "completed": t.get('mapValue', {}).get('fields', {}).get('completed', {}).get('booleanValue', False),
                                "submitted": t.get('mapValue', {}).get('fields', {}).get('submitted', {}).get('booleanValue', False),
                                "submission_date": t.get('mapValue', {}).get('fields', {}).get('submission_date', {}).get('stringValue', ''),
                                "marks": int(t.get('mapValue', {}).get('fields', {}).get('marks', {}).get('integerValue', 0)),
                                "remarks": t.get('mapValue', {}).get('fields', {}).get('remarks', {}).get('stringValue', ''),
                                "late": t.get('mapValue', {}).get('fields', {}).get('late', {}).get('booleanValue', False)
                            }
                            if 'submission_file' in t.get('mapValue', {}).get('fields', {}):
                                task_data["submission_file"] = t['mapValue']['fields']['submission_file']['stringValue']
                            users_db[email]['tasks'].append(task_data)
            st.session_state.users_db = users_db
    except Exception as e:
        st.error(f"Initialization error: {str(e)}")
    
    st.session_state.initialized = True

    # Check for persisted login from query params
    query_params = st.query_params.to_dict()
    if 'auth_token' in query_params:
        try:
            auth_token = query_params['auth_token']
            if isinstance(auth_token, list):
                auth_token = auth_token[0]
            email, token = auth_token.split('|')
            if email in st.session_state.users_db:
                user = st.session_state.users_db[email]
                if user['password'] == token:  # Compare hashed passwords directly
                    st.session_state.logged_in_user = email
        except Exception as e:
            st.error(f"Login error: {str(e)}")
            
st.markdown("""
    <style>
        .task-container {
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border: 1px solid #ddd;
            background-color: rgba(253, 187, 45, 0.1);
        }
        .completed-task-container {
            background-color: rgba(46, 204, 113, 0.1); /* light green */
        }
        .late-task-container {
            background-color: rgba(231, 76, 60, 0.1); /* light red */
        }
        .submitted-task-container {
            background-color: rgba(241, 196, 15, 0.1); /* light yellow */
        }
        .pending-task-container {
            background-color: rgba(149, 165, 166, 0.1); /* light gray */
        }
        .task-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .task-header h4 {
            margin: 0;
            color: #2c3e50;
        }
        .task-due {
            font-weight: bold;
            color: #e67e22;
        }
        .task-status {
            font-weight: bold;
            margin-top: 10px;
        }
        .task-status.late {
            color: #e74c3c;
        }
        .task-status.completed {
            color: #2ecc71;
        }
        .task-status.submitted {
            color: #f39c12;
        }
        .edit-btn {
            color: white;
            background-color: #3498db;
            border-radius: 4px;
            padding: 2px 8px;
            margin-right: 5px;
        }
        .delete-btn {
            color: white;
            background-color: #e74c3c;
            border-radius: 4px;
            padding: 2px 8px;
        }
        .block-btn {
            color: white;
            background-color: #e74c3c;
            border-radius: 4px;
            padding: 5px 10px;
            margin-top: 10px;
        }
        .unblock-btn {
            color: white;
            background-color: #2ecc71;
            border-radius: 4px;
            padding: 5px 10px;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)


# Inject custom CSS (from your app.py)
# inject_custom_css()

# -----------------------
# Firestore Utilities
# -----------------------
def update_user_in_firestore(user_data):
    email = user_data["email"]
    doc_path = f"applications/{email}"
    url = f"{FIREBASE_DB_URL}/{doc_path}"

    # Prepare tasks for Firestore
    tasks_data = []
    for task in user_data.get("tasks", []):
        task_map = {
            "name": {"stringValue": task["name"]},
            "description": {"stringValue": task["description"]},
            "due_date": {"stringValue": task["due_date"]},
            "max_marks": {"integerValue": str(task["max_marks"])},
            "assigned_date": {"stringValue": task["assigned_date"]},
            "completed": {"booleanValue": task["completed"]},
            "submitted": {"booleanValue": task["submitted"]},
            "late": {"booleanValue": task.get("late", False)},
        }
        if "submission_file" in task:
            task_map["submission_file"] = {"stringValue": task["submission_file"]}
        if "submission_date" in task:
            task_map["submission_date"] = {"stringValue": task["submission_date"]}
        if "marks" in task:
            task_map["marks"] = {"integerValue": str(task["marks"])}
        if "remarks" in task:
            task_map["remarks"] = {"stringValue": task["remarks"]}
        
        tasks_data.append({"mapValue": {"fields": task_map}})

    # Prepare the base firestore data
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
            "password_hash": {"stringValue": user_data["password"]},
            "status": {"stringValue": user_data["status"]},
            "role": {"stringValue": user_data.get("role", "student")},
            "total_marks": {"integerValue": str(user_data.get("total_marks", 0))},
            "tasks": {
                "arrayValue": {
                    "values": tasks_data
                }
            }
        }
    }

    # Add optional fields if they exist
    if "application_date" in user_data:
        firestore_data["fields"]["application_date"] = {"stringValue": user_data["application_date"]}

    response = requests.patch(url, json=firestore_data)
    if response.status_code == 200:
        # Refresh the users data after update
        response = requests.get(f"{FIREBASE_DB_URL}/applications")
        if response.status_code == 200:
            documents = response.json().get('documents', [])
            for doc in documents:
                fields = doc.get('fields', {})
                email = fields.get('email', {}).get('stringValue', '').lower().strip()
                if email in st.session_state.users_db:
                    st.session_state.users_db[email].update({
                        "status": fields.get('status', {}).get('stringValue', 'pending'),
                        "total_marks": int(fields.get('total_marks', {}).get('integerValue', 0)),
                        "tasks": []
                    })
                    if 'tasks' in fields:
                        tasks = fields['tasks'].get('arrayValue', {}).get('values', [])
                        st.session_state.users_db[email]['tasks'] = []
                        for t in tasks:
                            task_data = {
                                "name": t.get('mapValue', {}).get('fields', {}).get('name', {}).get('stringValue', ''),
                                "description": t.get('mapValue', {}).get('fields', {}).get('description', {}).get('stringValue', ''),
                                "due_date": t.get('mapValue', {}).get('fields', {}).get('due_date', {}).get('stringValue', ''),
                                "max_marks": int(t.get('mapValue', {}).get('fields', {}).get('max_marks', {}).get('integerValue', 0)),
                                "assigned_date": t.get('mapValue', {}).get('fields', {}).get('assigned_date', {}).get('stringValue', ''),
                                "completed": t.get('mapValue', {}).get('fields', {}).get('completed', {}).get('booleanValue', False),
                                "submitted": t.get('mapValue', {}).get('fields', {}).get('submitted', {}).get('booleanValue', False),
                                "submission_date": t.get('mapValue', {}).get('fields', {}).get('submission_date', {}).get('stringValue', ''),
                                "marks": int(t.get('mapValue', {}).get('fields', {}).get('marks', {}).get('integerValue', 0)),
                                "remarks": t.get('mapValue', {}).get('fields', {}).get('remarks', {}).get('stringValue', ''),
                                "late": t.get('mapValue', {}).get('fields', {}).get('late', {}).get('booleanValue', False)
                            }
                            if 'submission_file' in t.get('mapValue', {}).get('fields', {}):
                                task_data["submission_file"] = t['mapValue']['fields']['submission_file']['stringValue']
                            st.session_state.users_db[email]['tasks'].append(task_data)
        return True
    else:
        st.error(f"Error updating user: {response.text}")
        return False

def delete_task_from_firestore(email, task_name):
    """Delete a task from a student's record in Firestore"""
    student = st.session_state.users_db[email]
    student['tasks'] = [t for t in student['tasks'] if t['name'] != task_name]
    return update_user_in_firestore(student)

def block_student_in_firestore(email):
    """Block a student by changing their status"""
    student = st.session_state.users_db[email]
    student['status'] = 'blocked'
    return update_user_in_firestore(student)

def unblock_student_in_firestore(email):
    """Unblock a student by changing their status"""
    student = st.session_state.users_db[email]
    student['status'] = 'approved'
    return update_user_in_firestore(student)

# -----------------------
# Admin Dashboard
# -----------------------
def display_tasks(task_list, student_email, tab_name=""):
    student = st.session_state.users_db[student_email]
    for task_idx, task in enumerate(task_list):
        with st.container(border=True):
            cols = st.columns([4, 1])
            cols[0].markdown(f"**{task['name']}**")
            
            # Generate unique keys
            edit_key = f"edit_{student['email']}_{task['name']}_{tab_name}_{task_idx}"
            delete_key = f"delete_{student['email']}_{task['name']}_{tab_name}_{task_idx}"
            editing_key = f"editing_task_{student['email']}_{task['name']}_{task_idx}"
            
            
            
            # Editing form (only shown when editing)
            if st.session_state.get(editing_key, False):
                with st.form(key=f"edit_form_{student['email']}_{task['name']}_{task_idx}"):
                    new_name = st.text_input("Task Name", value=task['name'])
                    new_desc = st.text_area("Description", value=task['description'])
                    new_due_date = st.date_input("Due Date", 
                                               value=datetime.strptime(task['due_date'], "%Y-%m-%d").date())
                    new_max_marks = st.number_input("Max Marks", 
                                                  min_value=1, 
                                                  value=task['max_marks'])
                    
                    col1, col2 = st.columns(2)
                    if col1.form_submit_button("Save Changes"):
                        task['name'] = new_name
                        task['description'] = new_desc
                        task['due_date'] = new_due_date.strftime("%Y-%m-%d")
                        task['max_marks'] = new_max_marks
                        if update_user_in_firestore(student):
                            st.success("Task updated successfully!")
                            st.session_state[editing_key] = False
                            st.rerun()
                    
                    if col2.form_submit_button("Cancel"):
                        st.session_state[editing_key] = False
                        st.rerun()

            # Rest of the task display code remains the same...
            status = "✅ Completed" if task.get('completed') else "📝 Pending"
            if task.get('submitted') and not task.get('completed'):
                status = "📤 Submitted"
            
            cols[1].markdown(f"**Status:** {status}")
            
            st.write(f"**Description:** {task['description']}")
            st.write(f"**Due Date:** {task['due_date']}")
            st.write(f"**Assigned on:** {task['assigned_date']}")
            st.write(f"**Max Marks:** {task['max_marks']}")
            
            if task.get('submitted'):
                st.success("📤 Task submitted for review")
                st.write(f"**Submitted on:** {task['submission_date']}")
                # Move buttons outside the form
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if task.get('submission_file'):
                        try:
                            download_key = f"download_{student['email']}_{task['name']}_{tab_name}_{task_idx}"
                            file_bytes = base64.b64decode(task['submission_file'])
                            st.download_button(
                                label="⬇️ Download Submission",
                                data=file_bytes,
                                file_name=f"{student['first_name']}_{student['last_name']}_{task['name']}.zip",
                                mime="application/zip",
                                key=download_key
                            )
                        except Exception as e:
                            st.error(f"Error preparing file for download: {str(e)}")
                    
                    
                # Edit button
                if col3.button("✏️ Edit", key=edit_key):
                    st.session_state[editing_key] = True
                
                # Delete button - now outside any form
                if col4.button("🗑️ Delete", key=delete_key):
                    if delete_task_from_firestore(student['email'], task['name']):
                        st.success("Task deleted successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to delete task")
                if not task['completed']:
                    grade_form_key = f"grade_form_{student['email']}_{task['name']}_{tab_name}_{task_idx}"
                    with st.form(key=grade_form_key):
                        marks_key = f"marks_{student['email']}_{task['name']}_{tab_name}_{task_idx}"
                        marks = st.number_input(
                            "Assign Marks",
                            min_value=0,
                            max_value=task['max_marks'],
                            value=task.get('marks', 0),
                            key=marks_key
                        )
                        remarks_key = f"remarks_{student['email']}_{task['name']}_{tab_name}_{task_idx}"
                        remarks = st.text_area(
                            "Remarks",
                            value=task.get('remarks', ''),
                            key=remarks_key
                        )
                        
                        if st.form_submit_button("Grade Task"):
                            task['marks'] = marks
                            task['remarks'] = remarks
                            task['completed'] = True
                            student['total_marks'] = sum(
                                t.get('marks', 0) 
                                for t in student['tasks'] 
                                if t.get('completed')
                            )
                            update_user_in_firestore(student)
                            st.success("Task graded successfully!")
                            st.rerun()
            else:
                st.info("Task not submitted yet")

def show_admin_dashboard():
    admin = st.session_state.users_db[st.session_state.logged_in_user]

    st.markdown(f"""
    <div class="admin-header">
        <h1 style="color: #fdbb2d; display: flex; margin-top: -80px;">👑 Admin Dashboard</h1>
        <p>Welcome back, {admin['first_name']} {admin['last_name']}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="stats-card">
                <h3 style="color:#fdbb2d;">Total Students</h3>
                <p style="font-size:2rem;">{len([u for u in st.session_state.users_db.values() if u.get('role') != 'admin'])}</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="stats-card">
                <h3 style="color:#fdbb2d;">Pending Applications</h3>
                <p style="font-size:2rem;">{len([u for u in st.session_state.users_db.values() if u.get('status') == 'pending'])}</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="stats-card">
                <h3 style="color:#fdbb2d;">Active Students</h3>
                <p style="font-size:2rem;">{len([u for u in st.session_state.users_db.values() if u.get('status') == 'approved' and u.get('role') != 'admin'])}</p>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="stats-card">
                <h3 style="color:#fdbb2d;">Blocked Students</h3>
                <p style="font-size:2rem;">{len([u for u in st.session_state.users_db.values() if u.get('status') == 'blocked'])}</p>
            </div>
        """, unsafe_allow_html=True)

    with st.expander("📝 User Management", expanded=True):
        tab1, tab2 = st.tabs(["Pending Approvals", "All Students"])

        with tab1:
            pending_users = [u for u in st.session_state.users_db.values() if u.get('status') == 'pending']
            if not pending_users:
                st.info("No pending applications.")
            else:
                for user in pending_users:
                    with st.container(border=True):
                        cols = st.columns([3, 2, 2, 2])
                        cols[0].write(f"**{user['first_name']} {user['last_name']}** ({user['email']})")
                        cols[1].write(user.get('program', 'N/A'))
                        if cols[2].button("✅ Approve", key=f"approve_{user['email']}"):
                            user['status'] = "approved"
                            update_user_in_firestore(user)
                            st.rerun()
                        if cols[3].button("❌ Reject", key=f"reject_{user['email']}"):
                            requests.delete(f"{FIREBASE_DB_URL}/applications/{user['email']}")
                            del st.session_state.users_db[user['email']]
                            st.rerun()

        with tab2:
            all_students = [u for u in st.session_state.users_db.values() if u.get('role') != 'admin']
            if not all_students:
                st.info("No students registered.")
            else:
                for student in all_students:
                    with st.container(border=True):
                        cols = st.columns([4, 1, 1, 1])
                        cols[0].markdown(
                            f"""
                            <span style='color: #fdbb2d; font-size: 24px; font-weight: bold;'>
                                {student['first_name']} {student['last_name']} - {student.get('program', 'N/A')}
                            </span>
                            """,
                            unsafe_allow_html=True
                        )

                        
                        if cols[1].button("📊 View Details", key=f"details_{student['email']}", 
                                         help="Click to view student details",
                                         type="primary"):
                            st.session_state[f"show_details_{student['email']}"] = not st.session_state.get(f"show_details_{student['email']}", False)
                        
                        if cols[2].button("📋 View Tasks", key=f"tasks_{student['email']}", 
                                         help="Click to view student tasks",
                                         type="primary"):
                            st.session_state[f"show_tasks_{student['email']}"] = not st.session_state.get(f"show_tasks_{student['email']}", False)
                        
                        if cols[3].button(f"{'🔓 Unblock' if student.get('status') == 'blocked' else '🚫 Block'}", 
                                         key=f"block_{student['email']}",
                                         help="Block/Unblock this student"):
                            if student.get('status') == 'blocked':
                                if unblock_student_in_firestore(student['email']):
                                    st.success("Student unblocked successfully!")
                                    st.rerun()
                            else:
                                if block_student_in_firestore(student['email']):
                                    st.success("Student blocked successfully!")
                                    st.rerun()
                        
                        if st.session_state.get(f"show_details_{student['email']}", False):
                            with st.container(border=True):
                                st.markdown("#### Student Details")
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write(f"**Email:** {student['email']}")
                                    st.write(f"**Contact:** {student.get('phone', 'N/A')}")
                                    st.write(f"**University:** {student.get('university', 'N/A')}")
                                    st.write(f"**Major:** {student.get('major', 'N/A')}")
                                with col2:
                                    st.write(f"**Status:** {student.get('status', 'N/A')}")
                                    st.write(f"**Total Marks:** {student.get('total_marks', 0)}")
                                    st.write(f"**Graduation Year:** {student.get('graduation_year', 'N/A')}")
                        
                        if st.session_state.get(f"show_tasks_{student['email']}", False):
                            with st.container(border=True):
                                # st.markdown("#### Task Management")
                                st.markdown(
    "<h4 style='color: #fdbb2d;'>Task Management</h4>",
    unsafe_allow_html=True
)

                                if 'tasks' in student and student['tasks']:
                                    completed_tasks = [t for t in student['tasks'] if t.get('completed')]
                                    pending_tasks = [t for t in student['tasks'] if not t.get('completed') and not t.get('submitted')]
                                    submitted_tasks = [t for t in student['tasks'] if t.get('submitted') and not t.get('completed')]
                                    overdue_tasks = [t for t in student['tasks'] if datetime.strptime(t['due_date'], "%Y-%m-%d").date() < date.today() and not t.get('completed')]
                                    total_marks_possible = sum(t['max_marks'] for t in student['tasks'])
                                    marks_earned = sum(t.get('marks', 0) for t in student['tasks'] if t.get('completed'))
                                    
                                    tab_summary, tab_all, tab_completed, tab_pending, tab_submitted, tab_overdue, tab_assign = st.tabs([
                                        "📊 Summary",
                                        "All Tasks", 
                                        f"✅ Completed ({len(completed_tasks)})", 
                                        f"📝 Pending ({len(pending_tasks)})",
                                        f"📤 Submitted ({len(submitted_tasks)})",
                                        f"⚠️ Overdue ({len(overdue_tasks)})",
                                        "➕ Assign Task"
                                    ])
                                    
                                    with tab_summary:
                                        st.markdown("### Task Summary")
                                        cols = st.columns(3)
                                        cols[0].metric("Total Tasks", len(student['tasks']))
                                        cols[1].metric("Completed Tasks", len(completed_tasks))
                                        cols[2].metric("Pending Tasks", len(pending_tasks))
                                        cols[0].metric("Submitted Tasks", len(submitted_tasks))
                                        cols[1].metric("Overdue Tasks", len(overdue_tasks))
                                        cols[2].metric("Completion Rate", f"{len(completed_tasks)/len(student['tasks'])*100:.1f}%" if len(student['tasks']) > 0 else "0%")
                                        
                                        st.markdown("---")
                                        st.markdown("### Marks Summary")
                                        cols = st.columns(2)
                                        cols[0].metric("Total Possible Marks", total_marks_possible)
                                        cols[1].metric("Marks Earned", marks_earned)
                                        st.progress(marks_earned/total_marks_possible if total_marks_possible > 0 else 0)
                                        percentage = (marks_earned/total_marks_possible)*100
                                        st.caption(f"Percentage: {percentage:.1f}%")
                                        
                                        if percentage >= 80:
                                            st.caption("Grade: A1")
                                        elif percentage >= 70:
                                            st.caption("Grade: A")
                                        elif percentage >= 60:
                                            st.caption("Grade: B")
                                        elif percentage >= 50:
                                            st.caption("Grade: C")
                                        else:
                                            st.caption("Grade: FAIL")
                                    
                                    with tab_all:
                                        if student['tasks']:
                                                display_tasks(student['tasks'], student['email'], "all")
                                        else:
                                            st.info("No tasks found in this category")
                                    
                                    with tab_completed:
                                        if completed_tasks:
                                            display_tasks(completed_tasks, student['email'], "completed")
                                        else:
                                            st.info("No completed tasks found")
                                    
                                    with tab_pending:
                                        if pending_tasks:
                                            display_tasks(pending_tasks, student['email'], "pending")
                                        else:
                                            st.info("No pending tasks found")
                                    
                                    with tab_submitted:
                                        if submitted_tasks:
                                            display_tasks(submitted_tasks, student['email'], "submitted")
                                        else:
                                            st.info("No submitted tasks found")
                                    
                                    with tab_overdue:
                                        if overdue_tasks:
                                            display_tasks(overdue_tasks, student['email'], "overdue")
                                        else:
                                            st.info("No overdue tasks found")
                                    
                                    with tab_assign:
                                        with st.form(key=f"assign_task_form_{student['email']}"):
                                            st.write("**Assign New Task**")
                                            task_name = st.text_input("Task Name", key=f"task_name_{student['email']}")
                                            task_desc = st.text_area("Description", key=f"task_desc_{student['email']}")
                                            due_date = st.date_input("Due Date", value=date.today(), key=f"due_date_{student['email']}")
                                            max_marks = st.selectbox("Max Marks", [10, 20, 30, 50, 100], key=f"max_marks_{student['email']}")
                                            
                                            if st.form_submit_button("Assign Task"):
                                                if task_name:
                                                    new_task = {
                                                        "name": task_name,
                                                        "description": task_desc,
                                                        "due_date": due_date.strftime("%Y-%m-%d"),
                                                        "max_marks": max_marks,
                                                        "assigned_date": datetime.now().strftime("%Y-%m-%d"),
                                                        "completed": False,
                                                        "submitted": False,
                                                        "submission_file": "",
                                                        "submission_date": "",
                                                        "marks": 0,
                                                        "remarks": "",
                                                        "late": False
                                                    }
                                                    if 'tasks' not in student:
                                                        student['tasks'] = []
                                                    student['tasks'].append(new_task)
                                                    if update_user_in_firestore(student):
                                                        st.success(f"Task '{task_name}' assigned to {student['first_name']} {student['last_name']}.")
                                                        st.rerun()
                                                    else:
                                                        st.error("Failed to assign task")
                                                else:
                                                    st.warning("Please enter a task name")
                                else:
                                    with st.form(key=f"assign_task_form_{student['email']}"):
                                        st.write("**Assign New Task**")
                                        task_name = st.text_input("Task Name", key=f"task_name_{student['email']}")
                                        task_desc = st.text_area("Description", key=f"task_desc_{student['email']}")
                                        due_date = st.date_input("Due Date", value=date.today(), key=f"due_date_{student['email']}")
                                        max_marks = st.selectbox("Max Marks", [10, 20, 30, 50, 100], key=f"max_marks_{student['email']}")
                                        
                                        if st.form_submit_button("Assign Task"):
                                            if task_name:
                                                new_task = {
                                                    "name": task_name,
                                                    "description": task_desc,
                                                    "due_date": due_date.strftime("%Y-%m-%d"),
                                                    "max_marks": max_marks,
                                                    "assigned_date": datetime.now().strftime("%Y-%m-%d"),
                                                    "completed": False,
                                                    "submitted": False,
                                                    "submission_file": "",
                                                    "submission_date": "",
                                                    "marks": 0,
                                                    "remarks": "",
                                                    "late": False
                                                }
                                                if 'tasks' not in student:
                                                    student['tasks'] = []
                                                student['tasks'].append(new_task)
                                                if update_user_in_firestore(student):
                                                    st.success(f"Task '{task_name}' assigned to {student['first_name']} {student['last_name']}.")
                                                    st.rerun()
                                                else:
                                                    st.error("Failed to assign task")
                                            else:
                                                st.warning("Please enter a task name")
                                    st.info("No tasks assigned to this student")

# -----------------------
# User Dashboard
# -----------------------
def is_task_late(due_date_str):
    """Check if task is overdue and return boolean"""
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    return date.today() > due_date

def show_user_dashboard():
    user = st.session_state.users_db[st.session_state.logged_in_user]
    
    st.markdown(f"""
        <div class="user-header">
            <h1 style="color: #fdbb2d; display: flex; margin-top: -80px;" >👤 Student Dashboard</h1>
            <p>Welcome back, {user['first_name']} {user['last_name']}</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        completed_tasks = len([t for t in user.get('tasks', []) if t.get('completed')])
        st.markdown(f"""
            <div class="stats-card">
                <h3 style="color: #fdbb2d;" >Completed Tasks</h3>
                <p style="font-size:2rem;">{completed_tasks}</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        pending_tasks = len([t for t in user.get('tasks', []) if not t.get('completed')])
        st.markdown(f"""
            <div class="stats-card">
                <h3 style="color: #fdbb2d;" >Pending Tasks</h3>
                <p style="font-size:2rem;">{pending_tasks}</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="stats-card">
                <h3 style="color: #fdbb2d;" >Total Marks</h3>
                <p style="font-size:2rem;">{user.get('total_marks', 0)}</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <h2 style='color: #fdbb2d;'>📋 Your Tasks</h2>
""", unsafe_allow_html=True)
    
    if 'tasks' not in user or not user['tasks']:
        st.info("You have no tasks assigned.")
    else:
        for task_idx, task in enumerate(user['tasks']):
            with st.expander(f"Task {task_idx + 1}: {task['name']}"):
                container_class = "task-container "
                if task.get('completed'):
                    container_class += "completed-task-container"
                elif is_task_late(task['due_date']):
                    container_class += "late-task-container"
                    task['late'] = True
                elif task.get('submitted'):
                    container_class += "submitted-task-container"
                else:
                    container_class += "pending-task-container"

                st.markdown(f"""
                <div class="{container_class}">
                    <div class="task-header">
                        <h4 style='color: #fdbb2d;'>{task['name']}</h4>
                        <span class="task-due">Due: {task['due_date']}</span>
                    </div>
                    <div class="task-content">
                        <p><strong>Description:</strong> {task['description']}</p>
                        <p><strong>Max Marks:</strong> {task['max_marks']}</p>
                        <p><strong>Assigned on:</strong> {task['assigned_date']}</p>
                """, unsafe_allow_html=True)

                if task.get('late'):
                    st.markdown('<p class="task-status late">⚠️ This task is overdue!</p>', unsafe_allow_html=True)

                if not task['completed']:
                    if task.get('submitted'):
                        st.markdown('<p class="task-status submitted">📤 Task submitted - awaiting review</p>', unsafe_allow_html=True)
                        st.write(f"**Submitted on:** {task['submission_date']}")
                        if task.get('submission_file'):
                            try:
                                file_bytes = base64.b64decode(task['submission_file'])
                                st.download_button(
                                    label="⬇️ Download My Submission",
                                    data=file_bytes,
                                    file_name=f"my_submission_{task['name']}.zip",
                                    mime="application/zip",
                                    key=f"download_my_{task_idx}"
                                )
                            except Exception as e:
                                st.error(f"Error preparing file for download: {str(e)}")
                    else:
                        st.markdown("### Submit Task")
                        uploaded_file = st.file_uploader(
                            "Upload your solution (.zip)", 
                            type=["zip"],
                            key=f"upload_{task_idx}"
                        )
                        if uploaded_file is not None:
                            try:
                                with zipfile.ZipFile(io.BytesIO(uploaded_file.read())) as test_zip:
                                    if test_zip.testzip() is None:
                                        uploaded_file.seek(0)
                                        file_content = uploaded_file.read()
                                        task['submission_file'] = base64.b64encode(file_content).decode('utf-8')
                                        task['submission_date'] = datetime.now().strftime("%Y-%m-%d")
                                        task['submitted'] = True
                                        if update_user_in_firestore(user):
                                            st.success("Task submitted successfully!")
                                            st.rerun()
                                        else:
                                            st.error("Failed to submit task")
                                    else:
                                        st.error("Invalid ZIP file - corrupted or empty")
                            except zipfile.BadZipFile:
                                st.error("Invalid file format - please upload a valid ZIP file")
                            except Exception as e:
                                st.error(f"Error processing file: {str(e)}")
                else:
                    st.markdown('<p class="task-status completed">✅ Task Completed</p>', unsafe_allow_html=True)
                    if task.get('marks') is not None:
                        st.write(f"**Marks Obtained:** {task['marks']}/{task['max_marks']}")
                        st.write(f"**Remarks:** {task.get('remarks', 'No remarks')}")
                    if task.get('submission_file'):
                        try:
                            file_bytes = base64.b64decode(task['submission_file'])
                            st.download_button(
                                label="⬇️ Download My Submission",
                                data=file_bytes,
                                file_name=f"my_submission_{task['name']}.zip",
                                mime="application/zip",
                                key=f"download_completed_{task_idx}"
                            )
                        except Exception as e:
                            st.error(f"Error preparing file for download: {str(e)}")

                st.markdown("</div></div>", unsafe_allow_html=True)
                st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
                
# -----------------------
# Login Page
# -----------------------
def show_login():
    
    st.markdown("""
        <h1 style="text-align: center; color: #fdbb2d; font-family: 'Helvetica Neue'; font-weight: bold;">
            🎓 BrightCore LMS Portal
        </h1>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
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
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.form_submit_button("Login"):
            if email in st.session_state.users_db:
                user = st.session_state.users_db[email]
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if user["password"] == hashed_password:
                    if user.get("status") == "approved":
                        st.session_state.logged_in_user = email
                        st.query_params["auth_token"] = f"{email}|{hashed_password}"
                        if user.get("role") == "admin":
                            st.success("Admin login successful!")
                        else:
                            st.success("Student login successful!")
                        st.rerun()
                    elif user.get("status") == "blocked":
                        st.error("Your account has been blocked. Please contact the administrator.")
                    else:
                        st.error("Your application is pending approval.")
                else:
                    st.error("Invalid password.")
            else:
                st.error("Account not found.")
                
    if st.button("Back To Home"):
        st.switch_page("app.py")

# -----------------------
# Main App Logic
# -----------------------
if st.session_state.logged_in_user:
    user = st.session_state.users_db[st.session_state.logged_in_user]
    if user.get("role") == "admin":
        show_admin_dashboard()
    else:
        show_user_dashboard()

    if st.button("Logout", key="logout_btn"):
        st.session_state.logged_in_user = None
        st.query_params.clear()
        st.rerun()
else:
    show_login()