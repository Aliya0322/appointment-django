import base64


def encrypting(data):
    encoded_data = base64.b64encode(str(data).encode()).decode()
    return encoded_data

print(encrypting(6043199293))