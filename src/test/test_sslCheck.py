from unittest import mock
import os
import sys
from datetime import datetime, timedelta, timezone
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ssl_check

now = datetime.now(tz=timezone.utc)
notBefore = (now - timedelta(weeks=8))
notAfter = (now + timedelta(weeks=8))

socketResponse = [(2, 1, 6, 'test.io', ('1.1.1.1', 443))]
certResponse = {
    "subject": [[["commonName", "test.io"]]],
    "issuer": [
        [["countryName", "US"]],
        [["organizationName", "Let's Encrypt"]],
        [["commonName", "Let's Encrypt Authority X3"]]
    ],
    "serialNumber": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "notBefore": notBefore.strftime('%b %d %H:%M:%S %Y %Z'),
    "notAfter": notAfter.strftime('%b %d %H:%M:%S %Y %Z'),
    "subjectAltName": [["DNS", "test.io"]]
}


@mock.patch('socket.getaddrinfo', return_value=socketResponse)
@mock.patch('socket.create_connection')
@mock.patch('ssl.create_default_context')
def test_get_not_after_date(mock_create_default_context, mock_create_connection, mock_get_addr_info):
    # takes in fqdn
    # retreives certificate information
    # returns certificate notAfter datetime.date
    mock_create_connection.return_value = mock_get_addr_info
    mock_create_default_context.return_value.wrap_socket.return_value.__enter__.return_value.getpeercert.return_value = certResponse

    expireDate = ssl_check.get_not_after_date('test.io')
    assert expireDate == notAfter.date()


notAfterResponse = notAfter.date()


@mock.patch('ssl_check.get_not_after_date', return_value=notAfterResponse)
def test_cert_days_remain(mock_get_not_after_date):
    # takes in cert notAfter date
    # get today's date
    # return difference in days between today and notAfter date
    daysRemaining = ssl_check.cert_days_remaining('test.io')
    assert daysRemaining == 56
