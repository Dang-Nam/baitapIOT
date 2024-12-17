import pyrebase
from sense_emu import SenseHat  # Thay thế sense_emu bằng sense_hat nếu dùng trên Raspberry Pi thật
import time
import numpy as np

# Cấu hình Firebase
firebaseConfig = {
    "apiKey": "AIzaSyBBFo_SgUdtScFNYjNEfXN52quiY3FuJXo",
    "authDomain": "xdungiot.firebaseapp.com",
    "databaseURL": "https://xdungiot-default-rtdb.firebaseio.com",
    "projectId": "xdungiot",
    "storageBucket": "xdungiot.firebasestorage.app",
    "messagingSenderId": "238434722953",
    "appId": "1:238434722953:web:25b167ce8975760e439258",
    "measurementId": "G-5CTWZV253P"
}

# Khởi tạo Firebase và SenseHAT
firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()
sense = SenseHat()

# Biến toàn cục
n = 5  # Kích thước lịch sử mảng
history = [0] * n  # Khởi tạo mảng lịch sử
previous_T = 0  # Giá trị T trước đó
temperature_change_threshold = 1  # Ngưỡng thay đổi nhiệt độ (1 độ)

# Hàm đọc dữ liệu và tối ưu gửi
def push_optimized_data():
    global history, previous_T  # Sử dụng biến toàn cục
    while True:
        try:
            # Đọc nhiệt độ hiện tại từ SenseHAT
            current_temp = round(sense.get_temperature(), 2)

            # Tính trung bình của lịch sử
            mean_temp = np.mean(history)

            # Tính T_cập_nhật
            T_cap_nhat = round((current_temp + mean_temp) / 2, 2)

            # So sánh sự thay đổi nhiệt độ với ngưỡng
            if abs(current_temp - previous_T) > temperature_change_threshold:
                # Gửi dữ liệu lên Firebase
                sensor_data = {
                    "temperature": T_cap_nhat,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                database.child("OptimizedSensorData").set(sensor_data)
                print("Đã gửi dữ liệu lên Firebase:", sensor_data)

                # Cập nhật T
                previous_T = T_cap_nhat

            # Cập nhật mảng lịch sử
            history.pop(0)  # Xóa phần tử đầu tiên
            history.append(current_temp)  # Thêm giá trị mới vào cuối

            # In mảng lịch sử ra màn hình
            print("Lịch sử nhiệt độ:", history)

            # Tạm dừng 5 giây
            time.sleep(5)

        except Exception as e:
            print("Lỗi xảy ra:", e)

# Chạy chương trình
if __name__ == "__main__":
    print("Bắt đầu gửi dữ liệu tối ưu lên Firebase...")
    try:
        push_optimized_data()
    except KeyboardInterrupt:
        print("Đã dừng chương trình!")
