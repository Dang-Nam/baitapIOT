from flask import Flask, jsonify, render_template
from sense_emu import SenseHat  # Dùng Sense HAT emulator

# Khởi tạo SenseHat và Flask
sense = SenseHat()
app = Flask(__name__)


# Route API - Trả về nhiệt độ, độ ẩm và áp suất
@app.route('/api/sensor_data')
def get_sensor_data():
    try:
        # Lấy thông tin từ Sense HAT
        temp = sense.get_temperature()
        humidity = sense.get_humidity()
        pressure = sense.get_pressure()  # Lấy áp suất từ Sense HAT
        return jsonify({
            'temperature': temp,
            'humidity': humidity,
            'pressure': pressure
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route API - Trả về trạng thái joystick
@app.route('/api/joystick')
def get_joystick_status():
    try:
        # Lấy thông tin từ joystick
        joystick_events = sense.stick.get_events()
        return jsonify({
            'joystick': [{'direction': e.direction, 'action': e.action} for e in joystick_events]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route chính - Render giao diện index.html
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error rendering index.html: {e}", 500


# Chạy server Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
