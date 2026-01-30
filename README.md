# 🌱 Better Everyday - Habit Tracker

A minimal, aesthetic, and distraction-free habit tracker built with **Django** and **Tailwind CSS**. Designed to help you improve 1% every day.

![App Screenshot](https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?auto=format&fit=crop&q=80&w=2072&ixlib=rb-4.0.3)

## ✨ Features

- **📊 Consistency Grid:** GitHub-style heatmap to visualize your streak (Last 30 days).
- **📱 PWA Support:** Installable on Mobile & Desktop (Add to Home Screen).
- **🌗 Hybrid UI:** Bottom navigation for mobile, Top navigation for desktop.
- **💡 Daily Inspiration:** Auto-fetching motivational quotes.
- **⚡ Fast & Light:** Built with pure Django templates and Tailwind via CDN.

## 🚀 How to Run Locally

If you want to run this project on your own machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Aalok786/Better-Everyday.git
   cd Better-Everyday
   ```

2. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   ```

   - **Activate on Windows:**
     ```bash
     venv\Scripts\activate
     ```

   - **Activate on macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations (Create Database):**
   ```bash
   python manage.py migrate
   ```

5. **Start Server:**
   ```bash
   python manage.py runserver
   ```

   Now open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## ☁️ Deployment (Render Guide)

Create a new Web Service on Render.

Connect this repository.

Use these settings:

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn core.wsgi:application`

Add Environment Variable in settings:

- **Key:** `PYTHON_VERSION`
- **Value:** `3.11.0`

## 🤝 Contributing

Feel free to fork this repo and customize it for your own goals!

Built with ❤️ by Aalok