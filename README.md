# 🫀 Organ Donation & Transplantation Management System

An end-to-end web application built with **Django** and **Python** to streamline the organ donation and request workflow. It connects organ donors, recipient patients, registered hospitals, and medical administrators through a centralized, transparent platform.

---

## 🌟 Key Features

### 👤 User / Donor Portal
- **User Registration & Authentication**: Secure sign-up with blood group identification and contact details.
- **Donate Organ**: Register organ pledge forms (Kidney, Liver, Heart, Lungs, etc.) linked to partner healthcare facilities.
- **Donation History**: Track personal donation registrations and approval statuses.
- **Request Organ**: Submit emergency or scheduled organ requirements with medical specifications.
- **Matching Requests**: View verified requests matching the donor's blood type.
- **Profile Management**: Update user profile information anytime.

### 🏥 Hospital Portal
- **Hospital Registration**: Onboarding for verified healthcare institutions with admin approval workflow.
- **Organ Donations Review**: View and verify organ donations assigned to the hospital.
- **Patient Organ Requests**: Access active patient requests and communicate requirements.
- **Hospital Profile**: Maintain hospital contact, address, and credentials.

### 🛡️ Admin Dashboard
- **Centralized Command Center**: Real-time overview of total donors, approved vs. pending requests, and registered hospitals.
- **Hospital Verification**: Review, approve, or reject new hospital registrations.
- **Organ Request Approvals**: Validate and approve recipient patient organ requests.
- **System Records**: Full view of all organ donation submissions and medical records across the system.

---

## 💻 Tech Stack

- **Backend**: Python 3.13, Django 5.1
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 4, FontAwesome
- **Text-to-Speech**: pyttsx3 (integrated voice feedback)

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/sebatiji15-cloud/organ_donation.git
cd organ_donation
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
python manage.py migrate
```

### 5. Launch the Development Server
```bash
python manage.py runserver
```

The application will be live at: **`http://127.0.0.1:8000/`**

---

## 🔑 Demo & Test Accounts

| Role | Username | Password | Dashboard URL |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin` | `http://127.0.0.1:8000/adminp/` |
| **Hospital** | `district12` | `district12` | `http://127.0.0.1:8000/hospitalindex/` |
| **Hospital** | `muthoot23` | `muthoot23` | `http://127.0.0.1:8000/hospitalindex/` |
| **User / Donor** | `tiji` | `tiji12` | `http://127.0.0.1:8000/user/` |
| **User / Donor** | `malar` | `malar12` | `http://127.0.0.1:8000/user/` |

---

## 📂 Project Structure

```text
organ_donation/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── db.sqlite3
├── organ_donation/        # Django project configuration & static assets
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── static/            # Static CSS, JS, fonts, and images
└── myapp/                 # Core application
    ├── models.py          # User, Hospital, Donation, and OrganRequest models
    ├── views.py           # Application views & business logic
    ├── urls.py            # App route definitions
    └── templates/         # HTML templates
```

---

## 📄 License
This project is developed for educational and academic purposes. Feel free to use and modify for learning.
