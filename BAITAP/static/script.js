async function fetchData() {
    // Lấy dữ liệu từ API sensor_data
    const sensorResponse = await fetch('/api/sensor_data');
    const sensorData = await sensorResponse.json();

    // Hiển thị nhiệt độ và độ ẩm
    document.getElementById('temperature').innerText = `Temperature: ${sensorData.temperature.toFixed(2)}°C`;
    document.getElementById('humidity').innerText = `Humidity: ${sensorData.humidity.toFixed(2)}%`;

    // Lấy dữ liệu joystick
    const joystickResponse = await fetch('/api/joystick');
    const joystickData = await joystickResponse.json();
    document.getElementById('joystick').innerText = JSON.stringify(joystickData.joystick);
}

// Hiển thị tên lên LED matrix
async function displayName() {
    const name = document.getElementById('name').value;
    await fetch(`/api/display/${name}`);
}

// Lấy dữ liệu định kỳ mỗi giây
setInterval(fetchData, 1000);
