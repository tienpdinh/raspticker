try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json
import secret

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url)
    data = response.read().decode("utf-8")
    price = json.loads(data)[0]["price"]
    return price

url = (f"https://financialmodelingprep.com/api/v3/quote-short/AAPL?apikey={secret.API_KEY}")
print(get_jsonparsed_data(url))