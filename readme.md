# 🛍️ DrivnBD — E-commerce Clothing Store (Backend)

**DrivnBD** is a modern **Django REST Framework**–powered backend for a clothing e-commerce platform.  
It handles product listings, user accounts, and order management with JWT-based authentication.  
Deployed on **Vercel**, connected to a **PostgreSQL (Supabase)** database, and integrated with **Cloudinary** for media storage.

---

## 🚀 Live Links

- **Backend (Root API):** [https://drivnbd-serverside.vercel.app/](https://drivnbd-serverside.vercel.app/)
- **Swagger Docs:** [https://drivnbd-serverside.vercel.app/api/docs](https://drivnbd-serverside.vercel.app/api/docs)
- **Frontend (React):** [https://drivnbd-client.vercel.app/](https://drivnbd-client.vercel.app/)

---

## ⚙️ Tech Stack

- **Backend:** Django 5 + Django REST Framework  
- **Database:** PostgreSQL (Supabase)  
- **Authentication:** JWT (via `djangorestframework-simplejwt`)  
- **Media Storage:** Cloudinary  
- **Docs:** Swagger UI (via `drf-yasg`)  
- **Deployment:** Vercel (Serverless WSGI app)

---

## 📂 Project Structure

drivnbd/
├── api/                # Core API endpoints
├── users/              # Custom user model and authentication
├── store/              # Product catalog, categories, featured items
├── order/              # Order management and checkout logic
├── drivnbd/settings.py # Main configuration
├── drivnbd/wsgi.py     # WSGI entrypoint for Vercel
└── requirements.txt

---

## 🧰 Features

- 🧾 **RESTful API** with Django REST Framework  
- 🧑‍💼 **JWT authentication** via Djoser  
- 🧺 **Product categories, stock, and featured items**  
- ☁️ **Cloudinary integration** for image/media uploads  
- 📊 **Swagger documentation** (via DRF YASG)  
- 🧱 **Vercel Serverless deployment** with WhiteNoise for static assets  
- 🔐 Secure production configuration using environment variables

---

## 🧑‍💻 Local Development

### 1️⃣ Clone the repository
```bash
git clone https://github.com/blu3be3tle/drivnbd-server.git
cd drivnbd-server

2️⃣ Create a virtual environment

python -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

3️⃣ Install dependencies

pip install -U pip
pip install -r requirements.txt

4️⃣ Add a .env file at the project root

SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgresql://user:password@host:port/dbname
CLOUD_NAME=your_cloudinary_cloud
API_KEY=your_cloudinary_api_key
API_SECRET=your_cloudinary_api_secret
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password

5️⃣ Apply migrations and run

python manage.py migrate
python manage.py runserver

Now visit → http://127.0.0.1:8000/api/docs

⸻

🌐 Deployment (Vercel)

The backend is configured for Vercel’s Python 3.12 serverless runtime.

vercel.json

{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "functions": {
    "drivnbd/wsgi.py": {
      "runtime": "python3.12",
      "memory": 1024,
      "maxDuration": 10
    }
  },
  "rewrites": [
    { "source": "/(.*)", "destination": "/drivnbd/wsgi.py" }
  ],
  "buildCommand": "python -m pip install -U pip && pip install -r requirements.txt && python manage.py collectstatic --noinput"
}

⚠️ Make sure to set all environment variables in your Vercel dashboard
(Settings → Environment Variables) before deploying.

⸻

📸 API Documentation

Interactive Swagger UI is available at:
👉 https://drivnbd-serverside.vercel.app/api/docs

⸻

🤝 Frontend Integration

The React client for this API is hosted separately:
	•	Frontend repo: https://drivnbd-client.vercel.app/

It consumes the REST endpoints served by this backend.

⸻

🧾 License

This project is licensed under the MIT License.

⸻


“DrivnBD — crafted for speed, style, and seamless e-commerce.”
