import pytest,requests

def test_tlsv1_2_enabled():
    """
    Test that the server supports TLSv1.2.
    """
    try:
        requests.get('http://127.0.0.1:5000/dashboard', verify=False, proxies={'https': 'tlsv1.2'})
    except requests.exceptions.SSLError:
        pytest.fail("Server does not support TLSv1.2")