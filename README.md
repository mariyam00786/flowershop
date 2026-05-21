# Rose & Ivy | Premium Luxury Floral Boutique UAE

Welcome to **Rose & Ivy**, a bespoke e-commerce boutique storefront tailored for high-end luxury floral curations, signature bouquets, and premium gifts in Dubai and Abu Dhabi.

This platform has been redesigned to deliver a premium, minimalist visual experience matching the luxurious aesthetic of "White Rose Flowers UAE".

---

## 🎨 Visual Identity & Features
* **Premium Design System**: Complete Tailwind CSS integration utilizing an opulent white (`#FFFFFF`) background, charcoal (`#222222`) typography/borders, and muted gold active accents.
* **Modern Typography**: Classic, elegant serif headings (`Cormorant Garamond`) and clean body sans-serif text (`Inter`).
* **AJAX Cart Drawer**: Seamless slide-out cart drawer with live subtotal calculations, product quantity counters, and interactive checkout upsells (e.g. Helium Balloons, Luxury Chocolates).
* **Universal AED Pricing**: All currency representations transitioned to United Arab Emirates Dirham (`AED`).
* **Sandbox Wallet Credits**: Simulates store wallet deposits and instant balance deductions at checkout.
* **Responsive Layout**: Fluid UI optimized for 2-column mobile displays and 4-column desktop storefronts.

---

## 🛠️ Tech Stack & Structure
* **Backend**: Django 4.2.3
* **Frontend**: HTML5, Vanilla JS, and Tailwind CSS (Play CDN)
* **Icons**: Lucide Icons CDN
* **Database**: SQLite3 (`db.sqlite3` included with pre-seeded luxury products, mock orders, and sandbox credits)

---

## 🚀 Running the Project Locally

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Install Dependencies
Install all package dependencies via pip:
```bash
pip install -r requirements.txt
```

### 3. Run Development Server
Start the local server:
```bash
python manage.py runserver
```
Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web browser to explore the store!

---

## 🛠️ Development Setup (Coordinated Dev Server & Auto-Push)

To streamline local coding, the project includes an automated Git push system so that every saved file modification is automatically staged, committed, and pushed to your remote repository.

### 1. Run the Development Environment
You can launch both the Django development server and the background file-watcher with a single command:
```bash
bash run_dev.sh
```
> [!NOTE]
> On Windows, execute this shell script in a Bash-compliant terminal such as **Git Bash** or **WSL**.

### 2. How the Auto-Push Works
* **Automatic Recursive Watcher**: Powered by `watchdog`, the script recursively monitors all project folders.
* **Ignored Paths**: Files/folders like `.git`, `__pycache__`, `.pyc`, `.DS_Store`, `node_modules`, `migrations/`, and `db.sqlite3` are strictly filtered out.
* **10-Second Debounce Cooldown**: Once a saved file is detected, a 10-second timer begins. If further saves occur during this time, the timer resets. This bundles multiple edits into a single push.
* **Smart Commit Messages**: Automatically classifies modifications to select highly relevant, readable commit logs:
  * Modified templates (`.html`) ➔ `"update: template [filename]"`
  * Modified views (`views.py`) ➔ `"update: views [app_name]"`
  * Modified models (`models.py`) ➔ `"update: models [app_name]"`
  * Modified stylesheets (`.css`) ➔ `"update: styles"`
  * Modified routing rules (`urls.py`) ➔ `"update: urls"`
  * Other files ➔ `"auto: update [timestamp]"`
* **Zero-Change Clean Check**: If you save without actual changes, the script detects a clean `git status` and skips commit/push operations silently.
* **Fault-Resilience**: If a network interruption or authentication error happens, the script logs the failure gracefully and continues watching.

### 3. How to Stop
To safely close both background servers:
* Press `Ctrl + C` in the running terminal. The launcher traps the signal and terminates both active subprocesses cleanly.

---

## 📸 Mockup Preview
The design leverages generous luxury whitespace and responsive visual zoom states to create an opulent digital boutique experience.
