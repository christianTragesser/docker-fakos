import ssl
import socket
from datetime import datetime, date
import logs

log = logs.logger('certs')

def get_not_after_date(site):
    port = '443'
    context = ssl.create_default_context()
    with socket.create_connection((site, port)) as sock:
        with context.wrap_socket(sock, server_hostname=site) as ssock:
            data = ssock.getpeercert()
    
    dt = (datetime.strptime(data['notAfter'], '%b %d %H:%M:%S %Y %Z'))
    return dt.date()

def cert_days_remaining(site):
    today = date.today()
    try:
        certNotAfterDate = get_not_after_date(site)
        daysRemaining = certNotAfterDate - today
        return daysRemaining.days
    except Exception as e:
        log.error('A certificate check is failing, {0:s} is not valid:'.format(site))
        log.error(e)
        return -1