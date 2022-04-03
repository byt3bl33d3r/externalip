import time
import os
import requests
import logging
from prometheus_client import start_http_server, Summary, Info

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        style="{",
        fmt="[{asctime}] {levelname} - {message}"
    )
)

log = logging.getLogger("externalip")
log.setLevel(logging.INFO)
log.addHandler(handler)


QUERY_INTERVAL = os.environ.get("INTERVAL") or 3
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
EXTERNAL_IP = Info('external_ip', 'External IP Address')

def get_external_ip():
    external_ip = ""
    error = ""

    with REQUEST_TIME.time():
        try:
            r = requests.get("https://ifconfig.me")
            external_ip = r.text
        except Exception as e:
            if 'requests.exceptions' in str(e.__class__):
                error = str(e)
                log.error(e)

    EXTERNAL_IP.info({'external_ip': external_ip, "error": error, "interval": str(QUERY_INTERVAL)})

def main():
    interval = int(QUERY_INTERVAL)
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        get_external_ip()
        time.sleep(interval)

if __name__ == '__main__':
    main()
