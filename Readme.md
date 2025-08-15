# 🍽️ FeastExpress – Multi-Vendor E-commerce Platform

![Django](https://img.shields.io/badge/Django-4.x-green?logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)
![PostGIS](https://img.shields.io/badge/PostGIS-Extension-lightblue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.x-purple?logo=bootstrap)
![Linode](https://img.shields.io/badge/Deployed%20on-Linode-green?logo=linode)


**Live Website:** [🌐 FeastExpress Online](https://www.feastexpress.online)

---

## 📖 About the Project
FeastExpress is a **fully-featured Multi-Vendor Food E-Commerce Marketplace** built with Django, Bootstrap, PostgreSQL, and PostGIS.  
It includes **location-based search, nearby restaurants, dynamic business hours, payment gateway, and more** – all production-ready.

---
## ✨ Features
- 📍 **Get user's location** & show nearby restaurants  
- 📧 **Email-based authentication & verification** for secure sign-ups and logins  
- 🛒 **Cart functionalities** for customers
- 🔗 **Many-to-Many Relationships** between vendors & items  
- 💳 **PayPal Payment Gateways** for secure online payments  
- ⏰ **Dynamic Business Hours Module** for vendors  
- 🛠 **Full Vendor Dashboard** with revenue page, menu management, and order history  
- 🗺 **Google Autocomplete for Addresses** with integration to Google Places API  
- 👥 **Separate role-based features** for customers and vendors (e.g., browsing vs. managing orders)  


---

## 🛠 Tech Stack
| Technology     | Purpose |
|----------------|---------|
| **Python / Django** | Backend framework |
| **PostgreSQL** | Database |
| **PostGIS** | Geolocation & spatial queries |
| **CSS / Bootstrap classes** | Frontend styling |
| **PayPal APIs** | Payment processing |
| **Google Maps API** | Location & autocomplete |

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Sumit-320/feastexpress.git
cd feastexpress
```

### 2️⃣ Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

### 3️⃣ Setup PostgreSQL & PostGIS
Make sure PostgreSQL is installed and PostGIS extension is enabled:
```sql
CREATE DATABASE feastexpress;
CREATE EXTENSION postgis;
```

### 4️⃣ Configure Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_NAME=feastexpress
DATABASE_USER=postgres
DATABASE_PASSWORD=yourpassword
DATABASE_HOST=localhost
DATABASE_PORT=5432
EMAIL_HOST_USER=youremail@example.com
EMAIL_HOST_PASSWORD=your_email_password
RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_SECRET=your_paypal_secret
```

### 5️⃣ Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py runserver
```

---

## 🚀 Key Features Implemented & Skills Gained
- ✅ Online **multi-vendor food e-commerce platform** implementation in Django, enabling multiple restaurant vendors to manage their menus and orders.
- ✅ Secure email-based authentication with token verification.
- ✅ **Shopping cart** functionality with item quantities.
- ✅ **PostGIS spatial queries** to find and sort nearby restaurants based on user location.
- ✅ **Google Places & Autocomplete API** integration for smooth and accurate address entry during checkout.
- ✅ Secure **PayPal payment integration** for handling online transactions.
- ✅ Deployed on **Linode** cloud server with **Nginx as a reverse proxy** and **Gunicorn** as the WSGI application server, ensuring high performance and scalability.
---

## 📋 Prerequisites
- Basic understanding of **HTML, CSS, JavaScript** for frontend integration.
- Intermediate **Python & Django** knowledge for backend development.
- **PostgreSQL** installed with **PostGIS** extension enabled.
- Familiarity with basic **Linux commands** for server management and troubleshooting.
- Understanding of **Nginx** configuration for reverse proxy setup.
- Basic knowledge of **Gunicorn** (WSGI HTTP Server) for deploying Django applications.

---

🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue first to discuss what you’d like to change.

--- 

💡 **Tip:** Run in **DEBUG=False** in production and secure the `.env` file.

--- 

**Sumit Vishwakarma**  
💼 [LinkedIn](https://www.linkedin.com/in/sumit-vishwakarma-16a601273/) 
💻 [GitHub](https://github.com/Sumit-320)  
🌐 [Live Site](https://www.feastexpress.online)  

