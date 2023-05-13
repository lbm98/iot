import requests

TARGET_URL = 'http://127.0.0.1:8080/sensor'


def main():
    requests.post(
        url=TARGET_URL,
        json={
            'humidity': 25
        }
    )


if __name__ == '__main__':
    main()
