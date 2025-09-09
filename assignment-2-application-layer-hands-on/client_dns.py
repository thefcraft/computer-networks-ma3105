from dns import resolver
from typing import Literal
import logging

def log_dns_query(domain: str, record_type: Literal["A", "MX", "CNAME"]) -> set[str] | None: 
    # resolver.get_default_resolver().nameservers = ['8.8.8.8', '8.8.4.4']
    logging.info(f"NameServers: {resolver.get_default_resolver().nameservers}")
    try:
        answers = resolver.resolve(domain, record_type)
        logging.info(f"DNS {record_type} records for {domain}:")
        for rdata in answers:
            logging.info(rdata)
    except resolver.NoAnswer:
        logging.error(f"No {record_type} records found for {domain}.")
    except resolver.NXDOMAIN:
        logging.error(f"Domain {domain} does not exist.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    
def main() -> None:
    log_dns_query('google.com', record_type='A')
    logging.info('-'*50)
    log_dns_query('google.com', record_type='MX')
    logging.info('-'*50)
    log_dns_query('www.google.com', record_type='CNAME')
    
if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("dns.log", mode='a'),
            logging.StreamHandler()
        ]
    )
    main()