import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

if __name__ == "__main__":
    import dotenv
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    dotenv.load_dotenv()
    
# NOTE: BY DEFAULT, smtp.gmail.com:587
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))

# NOTE: for smtp.gmail.com generate app password from `https://myaccount.google.com/apppasswords`
SENDER_EMAIL = os.environ["SMTP_SENDER_EMAIL"]
SENDER_PASSWORD = os.environ["SMTP_SENDER_PASSWORD"]
RECIPIENT_EMAIL = os.environ["SMTP_RECIPIENT_EMAIL"]

def send_email():
    try:
        logging.info("Connecting to SMTP server...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        logging.info("Logging in...")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = "Test Email (SMTP)"
        msg.attach(MIMEText("Hello! This is a test email sent using Python SMTP by 2302mc05.", "plain"))

        logging.info("Sending email...")
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        logging.info("Email sent successfully.")

        server.quit()
    except Exception as e:
        logging.error(f"SMTP failed: {e}")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            # logging.FileHandler(filename='smtp.log', mode='a')
        ]
    )
    send_email()
