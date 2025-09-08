import os
import ftplib
import logging
import io # for file upload, as i want to upload from memory not disk...
from typing import Protocol

if __name__ == "__main__":
    import dotenv
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    dotenv.load_dotenv()

# NOTE: BY DEFAULT, public test FTP server
FTP_SERVER = os.environ.get("FTP_SERVER", "ftp.dlptest.com")
USERNAME = os.environ.get("FTP_USERNAME", "dlpuser")
PASSWORD = os.environ.get("FTP_PASSWORD", "rNrKYTX9g7z3RgJRmxWuGHbeu")

class Readable(Protocol): # ignore it...
    def read(self, size: int | None = -1, /) -> bytes: ...
class Writable(Protocol): # ignore it...
    def write(self, data: bytes, /) -> int: ...
    
def ftp_client(upload_file: Readable, download_file: Writable) -> None:
    logging.info("Connecting to FTP server...")
    
    ftp = ftplib.FTP()
    ftp.connect(FTP_SERVER, port=21, timeout=20)
    
    ftp.set_pasv(True) # usually fixes firewall issue... 
    # ftp.set_pasv => Use passive or active mode for data transfers. With a false argument, use the normal PORT mode, With a true argument, use the PASV command.
    
    ftp.login(USERNAME, PASSWORD)
    logging.info("Login successful.")
    
    # Upload a file from memory
    ftp.storbinary("STOR upload_test_2302mc05_iitp.txt", upload_file)
    logging.info("File uploaded successfully (from memory).")
    
    # Download the same file into memory
    ftp.retrbinary("RETR upload_test_2302mc05_iitp.txt", download_file.write)
    logging.info("File downloaded successfully (into memory).")
    
    # List directory contents
    logging.info("Listing directory contents:")
    ftp.retrlines("LIST")
    
    ftp.quit()

def main():
    with (
        io.BytesIO(b"Hello FTP World from memory!") as upload_file, 
        io.BytesIO() as download_file
    ):
        try:
            ftp_client(upload_file, download_file)
        except Exception as e:
            logging.error(f"FTP failed: {e}")
            return
        # Verify content
        upload_file.seek(0, io.SEEK_SET)
        download_file.seek(0, io.SEEK_SET)
        if download_file.getvalue() == upload_file.getvalue():
            logging.info("Downloaded content matches uploaded content ✅")
        else:
            logging.warning("Content mismatch ❌")
    
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            # logging.FileHandler(filename='ftp.log', mode='a')
        ]
    )
    main()
