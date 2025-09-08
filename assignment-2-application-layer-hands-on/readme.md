# CN Lab (MA3105) Assignment 2 — Application Layer Protocols

## 📌 Objective
To understand and implement the functionality of various Application Layer protocols — HTTP, SMTP, FTP, DNS, and LDAP — using Python programming to build client-side applications.

### ⚠️ Caution
This `README` file was **AI-generated**. (cause i hate writing readme.md by my own...)

---

## 🖥️ Features
This assignment includes client implementations for several key Application Layer protocols:

*   **HTTP (`client_http.py`)**:
    *   Sends asynchronous GET and POST requests using `aiohttp`.
    *   Logs response status codes, headers, and body previews.
    *   Includes error handling and logging for failed requests.
*   **SMTP (`client_smtp.py`)**:
    *   Connects and logs into an SMTP server (`smtplib`).
    *   Constructs and sends a test email with a subject and plain text body.
    *   Logs the entire communication process.
    *   Requires environment variables for sender/recipient emails and app password.
*   **FTP (`client_ftp.py`)**:
    *   Connects and logs into an FTP server (`ftplib`).
    *   Demonstrates file upload from memory and download to memory.
    *   Verifies the integrity of uploaded and downloaded content.
    *   Lists directory contents on the server.
    *   Supports passive mode for better firewall compatibility.
*   **DNS (`client_dns.py`)**:
    *   Performs DNS queries for A (IP address), MX (Mail Exchange), and CNAME (Canonical Name) records using `dnspython`.
    *   Logs the retrieved records to both console and a `dns.log` file.
    *   Includes robust error handling for `NoAnswer` and `NXDOMAIN` cases.
*   **LDAP (`client_ldap.py`)**:
    *   Connects and binds to an LDAP server (`ldap3`).
    *   Executes a search query for common attributes (`cn`, `mail`) for entries with `objectClass=person`.
    *   Logs bind status and search results.
    *   Uses environment variables for server, username, and password.
*   **General**:
    *   Comprehensive logging (`logging` module) for all operations and errors.
    *   Configuration via `.env` files for sensitive credentials where applicable.

---

## 📂 Files
- `client_http.py` — HTTP client code
- `client_smtp.py` — SMTP client code
- `client_ftp.py` — FTP client code
- `client_dns.py` — DNS client code
- `client_ldap.py` — LDAP client code
- `cnlab2.pdf` — The Assignment File (assuming it's similar to `cnlab1.pdf`)

---

## ▶️ How to Run

### 1. Setup Environment Variables
Some scripts (SMTP, FTP, LDAP) require credentials that are best handled via environment variables. Create a file named `.env` in the same directory as your Python scripts.

An example `.env` structure:
```ini
# .env
# --- For client_smtp.py ---
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_SENDER_EMAIL=your_email@gmail.com
SMTP_SENDER_PASSWORD=your_app_password_for_gmail # IMPORTANT: For Gmail, use an App Password!
SMTP_RECIPIENT_EMAIL=recipient_email@example.com

# --- For client_ftp.py (Optional: uses public test server by default if not set) ---
# FTP_SERVER=ftp.dlptest.com
# FTP_USERNAME=dlpuser
# FTP_PASSWORD=rNrKYTX9g7z3RgJRmxWuGHbeu

# --- For client_ldap.py (Optional: uses public test server by default if not set) ---
# LDAP_SERVER=ldap.forumsys.com
# LDAP_USERNAME=cn=read-only-admin,dc=example,dc=com
# LDAP_PASSWORD=password
```
**Note for SMTP**: If using Gmail, you *must* generate an [App Password](https://myaccount.google.com/apppasswords) as direct password login is often blocked for security reasons.

### 2. Install Dependencies
Ensure you have all necessary Python packages installed:
```bash
pip install aiohttp dnspython ldap3 python-dotenv
```

### 3. Run Each Client Script
Navigate to the directory containing the scripts and run each one individually:

*   **HTTP Client**:
    ```bash
    python client_http.py
    ```
    (This will perform both GET and POST requests sequentially by default).

*   **SMTP Client**:
    ```bash
    python client_smtp.py
    ```
    (Ensure your `.env` file is correctly configured with SMTP credentials).

*   **FTP Client**:
    ```bash
    python client_ftp.py
    ```
    (Will connect to the public test server by default or your configured server).

*   **DNS Client**:
    ```bash
    python client_dns.py
    ```
    (Logs will be printed to console and saved in `dns.log`).

*   **LDAP Client**:
    ```bash
    python client_ldap.py
    ```
    (Will connect to the public test server by default or your configured server).

---

## 🛠️ Notes
*   **Python Version**: Requires **Python 3.7+** (preferably 3.9+ for specific type hinting syntax like `set[str]`).
*   **Dependencies**: All necessary libraries (`aiohttp`, `dnspython`, `ldap3`, `python-dotenv`) should be installed as per the "Install Dependencies" section.
*   **SMTP App Passwords**: For email providers like Gmail, standard password login for `smtplib` is often deprecated. Use an "App Password" generated from your account security settings.
*   **Public Test Servers**: `client_ftp.py` and `client_ldap.py` are configured with public test server details by default, allowing for immediate testing without needing to set up private servers. You can override these with your own server details in the `.env` file if needed.
*   **Logging**: All scripts use Python's built-in `logging` module. Output is directed to `StreamHandler` (console) by default. Uncomment `FileHandler` lines in each script's `if __name__ == "__main__":` block to enable logging to files (e.g., `http.log`, `smtp.log`).