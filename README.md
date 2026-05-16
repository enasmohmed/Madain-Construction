# 🧩 Django CMS + Landing Page

A dynamic **Content Management System (CMS)** built with **Django**, designed to manage a full website and landing pages from the admin panel without touching the code.

The project allows admins to control:
- Website content
- Landing pages
- Sections
- Texts & images
- SEO settings
- Multi-language support

---

## 🚀 Features

- 🧠 **Dynamic CMS**
  - Manage pages, sections, and content from Django Admin
  - No hardcoded content in templates

- 🎯 **Landing Page Builder**
  - Create and edit landing pages dynamically
  - Control sections order and visibility

- 🌍 **Multi-language Support**
  - Arabic / English
  - Django i18n ready

- 🖼️ **Media Management**
  - Upload images, logos, and assets from admin

- 🔐 **Admin Dashboard**
  - Secure Django admin panel
  - Easy content editing

- 📱 **Responsive Design**
  - Bootstrap-based responsive templates

- ⚙️ **SEO Ready**
  - Meta titles & descriptions
  - Clean URLs

---

## 🛠️ Tech Stack

- **Backend:** Django
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (can be replaced with PostgreSQL / MySQL)
- **Languages:** Python, HTML, CSS
- **CMS:** Django Admin
- **Internationalization:** Django i18n

---

## 📂 Project Structure

```text
project_root/
│
├── core/                # Main CMS logic
├── pages/               # Dynamic pages & landing pages
├── templates/           # HTML templates
├── static/              # CSS, JS, Images
├── media/               # Uploaded files
├── locale/              # Translation files
├── manage.py
└── requirements.txt



⚙️ Installation & Setup
1️⃣   Clone the repository
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name

2️⃣   Create virtual environment
    python -m venv venv
    source venv/bin/activate  # Linux / Mac
    venv\Scripts\activate     # Windows

3️⃣   Install dependencies
    pip install -r requirements.txt

4️⃣   Apply migrations
    python manage.py migrate

5️⃣   Create superuser
    python manage.py createsuperuser

6️⃣   Run the project
    python manage.py runserver


Now open:

    http://127.0.0.1:8000/
    http://127.0.0.1:8000/admin/

🌍 Multi-language Setup

To compile translations:

    django-admin compilemessages
    
    To add a new language:
    
    Update settings.py
    
    Add translation files in /locale
    
    Restart the server

🧪 Demo Content

    After login to admin panel:
    
    Add Pages
    
    Add Sections
    
    Control landing page content
    
    Upload images & logos

📌 Use Cases

    Company website
    
    Business landing page
    
    Corporate CMS
    
    Factory / Industrial website
    
    Portfolio or service website

🔮 Future Improvements

    Page builder UI
    
    Role-based permissions
    
    REST API
    
    Headless CMS support
    
    Caching & performance optimization

👩‍💻 Author

    Enas Mohamed
    Backend & Full-Stack Developer
    Specialized in Django & Web Systems