# Busamed WhatsApp Chatbot

A WhatsApp chatbot for the **Busamed Service Desk System** that allows staff and patients to log tickets, check their status, and access help directly via WhatsApp.

## 🚀 Features

- Log service desk tickets via WhatsApp  
- Check the status of existing tickets  
- Handle frequently asked questions (FAQs)  
- Integrates with SQL Server  
- Multi-user support (staff and patients)

## 🛠️ Setup Instructions

### ✅ Prerequisites

- Python 3.10+  
- SQL Server database  
- Access to the WhatsApp Business API  
- Meta Developer account

### 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <your-azure-repo-url>
   cd busamed-whatsapp-chatbot

2. **Create and activate a virtual environment**

python -m venv chatbot_env
chatbot_env\Scripts\activate   # On Windows
# OR
source chatbot_env/bin/activate  # On macOS/Linux

3. **nstall dependencies**
pip install -r requirements.txt

4. **Configure environment variables**
-Copy .env.example to .env
-Add your WhatsApp API credentials
-Add SQL Server database connection details

5. **Run the application**
python app/main.py



