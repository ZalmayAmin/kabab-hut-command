# 🏛️ Kabab Hut: Central Command

A bespoke, production-ready Lead Management System designed for catering operations. This tool captures inquiries, calculates revenue forecasts, and generates kitchen-ready work orders.

## 🚀 Quick Start (For Windows)

1. **Install Dependencies**:
   Open your terminal in this folder and run:
   ```powershell
   pip install -r requirements.txt
   Launch the System:
Double-click start_kabab_hut.bat or run:

PowerShell
python serve.py
Access the Vault:
Open your browser to: http://localhost:5001/admin/inquiries

✨ Key Features
Revenue Forecasting: Automatically estimates pipeline value based on guest counts ($50/head).

One-Click Reply: Integrated mailto logic that triggers your email client and updates lead status to "Replied" simultaneously.

Kitchen Print Mode: A dedicated print layout that strips away financial data and UI buttons, leaving only event logistics for the chefs.

Production-Grade: Powered by Waitress for stability and concurrent request handling.

📂 Project Structure
app.py: Core Flask logic and database models.

serve.py: Production WSGI server configuration.

kabab_hut.db: SQLite database (Stores all leads and statuses).

templates/: HTML vault (Admin Dashboard, Contact Forms).

static/: Design assets (Tailwind CSS, Images).

🛠️ Maintenance
To change the revenue estimate or business logic, edit the variables in app.py and restart the server. For UI changes, edit the files in the /templates folder and refresh your browser.
