import requests


# HOST = '127.0.0.1'
HOST = '192.168.1.28'  # Change as needed

PORT = 8080
PATH = '/sensor'

TARGET_URL = f'http://{HOST}:{PORT}{PATH}'


def main():
    requests.post(
        url=TARGET_URL,
        json={
            'humidity': 25
        }
    )


if __name__ == '__main__':
    main()
