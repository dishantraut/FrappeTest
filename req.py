import json
from pprint import pprint
from requests import request, RequestException


def make_http_request(url, method='GET', params=None, data=None, headers=None, auth=None):
    """
    Make an HTTP request and display the response.

    :param url: The URL to send the request to.
    :param method: The HTTP method (e.g., GET, POST, PUT, DELETE).
    :param params: Query parameters as a dictionary.
    :param data: Request payload as a dictionary.
    :param headers: Request headers as a dictionary.
    :param auth: Authentication tuple (username, password) if required.
    """
    try:
        response = request(
            method, url, params=params, data=data, headers=headers, auth=auth, timeout=10
        )

        # print(f"Request: {method} {url}")
        # print(f"Status Code: {response.status_code}")
        # print("Headers:")
        # for key, value in response.headers.items():
        #     print(f"    {key}: {value}")

        if response.text:
            return response.text

        return None

    except RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":

    # URL = "http://172.22.193.4:6060/"
    URL = "https://frappe.io/api/method/frappe-library?page=1&title=and"
    result_json = make_http_request(url=URL, method='GET')
    if result_json:
        result_dict = json.loads(result_json)
        # print("\n\nResponse Data:")
        # pprint(result_dict)
        for k in result_dict.get('message'):
            print(k)
