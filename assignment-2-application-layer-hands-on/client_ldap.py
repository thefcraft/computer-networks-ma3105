import os
import logging
from ldap3 import Server, Connection, ALL


if __name__ == "__main__":
    import dotenv
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    dotenv.load_dotenv()

# NOTE: BY DEFAULT, public test LDAP server
LDAP_SERVER = os.environ.get("LDAP_SERVER", "ldap.forumsys.com")
USERNAME = os.environ.get("LDAP_USERNAME", "cn=read-only-admin,dc=example,dc=com")
PASSWORD = os.environ.get("LDAP_PASSWORD", "password")

def ldap_client():
    logging.info("Connecting to LDAP server...")
    
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=USERNAME, password=PASSWORD)
    
    if not conn.bind(): # type: ignore
        logging.error("Failed to bind to LDAP server.")
        return
    
    logging.info("LDAP bind successful.")
    
    # Search example
    conn.search("dc=example,dc=com", "(objectClass=person)", attributes=["cn", "mail"]) # type: ignore
    for entry in conn.entries: # type: ignore
        logging.info(str(entry).strip('\n')) # type: ignore
        
    conn.unbind() # type: ignore
    
def main():
    try:
        ldap_client()
    except Exception as e:
        logging.error(f"LDAP failed: {e}")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            # logging.FileHandler(filename='ldap.log', mode='a')
        ]
    )
    main()
