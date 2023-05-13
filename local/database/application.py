from flask import Flask, request
from database import create_connection, create_database_if_not_exists, insert_data

app = Flask(__name__)

conn = create_connection()
create_database_if_not_exists(conn)


@app.route('/sensor', methods=['POST'])
def post_sensor_data():
    sensor_data = request.json
    humidity = sensor_data['humidity']

    insert_data(
        connection=conn,
        humidity=humidity
    )

    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
