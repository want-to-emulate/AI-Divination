# -*- coding: gbk -*-

import requests
import serial
import time

# 初始化串口
port = "COM4"  # 实际串口号
baud = 115200  # 波特率
ser = serial.Serial(port, baud, timeout=1)
print(f"串口已初始化: {port}, 波特率: {baud}")

# 获取星座编号
def get_constellation_number(month, day):
    if (month == 3 and 21 <= day <= 31) or (month == 4 and 1 <= day <= 19):
        return 0
    elif (month == 4 and 20 <= day <= 30) or (month == 5 and 1 <= day <= 20):
        return 1
    elif (month == 5 and 21 <= day <= 31) or (month == 6 and 1 <= day <= 21):
        return 2
    elif (month == 6 and 22 <= day <= 30) or (month == 7 and 1 <= day <= 22):
        return 3
    elif (month == 7 and 23 <= day <= 31) or (month == 8 and 1 <= day <= 22):
        return 4
    elif (month == 8 and 23 <= day <= 31) or (month == 9 and 1 <= day <= 22):
        return 5
    elif (month == 9 and 23 <= day <= 30) or (month == 10 and 1 <= day <= 23):
        return 6
    elif (month == 10 and 24 <= day <= 31) or (month == 11 and 1 <= day <= 22):
        return 7
    elif (month == 11 and 23 <= day <= 30) or (month == 12 and 1 <= day <= 21):
        return 8
    elif (month == 12 and 22 <= day <= 31) or (month == 1 and 1 <= day <= 19):
        return 9
    elif (month == 1 and 20 <= day <= 31) or (month == 2 and 1 <= day <= 18):
        return 10
    else:
        return 11

# 接收生日信息
def receive_birthday():
    print("等待接收数据...")
    buffer = b''  # 用于存储接收到的字节数据
    while True:
        if ser.in_waiting > 0:
            # 增加一点延迟，确保数据完全发送
            time.sleep(0.2)
            raw_data = ser.read(ser.in_waiting)
            buffer += raw_data
            print(f"接收到的原始字节数据: {buffer}")
            try:
                data = buffer.decode('utf-8')
                print(f"接收到数据: {data}")
                # 检查数据是否包含生日信息
                if ' ' in data:
                    birth_date_str = data.split(" ")[-1]
                    if len(birth_date_str.split('-')) == 2:
                        return birth_date_str
            except UnicodeDecodeError:
                try:
                    data = buffer.decode('gbk')
                    print(f"接收到数据: {data}")
                    # 检查数据是否包含生日信息
                    if ' ' in data:
                        birth_date_str = data.split(" ")[-1]
                        if len(birth_date_str.split('-')) == 2:
                            return birth_date_str
                except UnicodeDecodeError:
                    print("无法使用utf-8或gbk解码接收到的数据。")
        time.sleep(0.1)  # 避免 CPU 占用过高

# 发送数据到电阻屏
def send_to_screen(control_id, text):
    max_length = 255  # 假设文本框最大长度为255
    if len(text) > max_length:
        text = text[:max_length]
    command = f'{control_id}.txt="{text}"\xFF\xFF\xFF'  # 发送指令
    ser.write(command.encode('gbk'))  # 使用GBK编码发送
    print(f"发送到屏幕的指令: {command}")

# 请求API
def process_host(request_data, gateway_host_url):
    try:
        response = requests.post(gateway_host_url, data=request_data)
        response.raise_for_status()  # 检查请求是否成功
        print(f"API 响应状态码: {response.status_code}")
        print(f"API 返回内容: {response.text}")
        try:
            return response.json()  # 尝试解析为JSON
        except ValueError:
            print("API返回数据不是有效的JSON格式。")
            return None
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {e}")
        return None

# 主程序
if __name__ == "__main__":
    try:
        # 接收生日信息
        birth_date_str = receive_birthday()
        try:
            month, day = map(int, birth_date_str.split('-'))
            constellation_number = get_constellation_number(month, day)
            print(f"星座编号: {constellation_number}")
        except ValueError:
            print("输入的日期格式不正确，请按照M-D的格式输入。")
            exit()

        # 请求API
        api_secret = "UHbh7CMB4midIKcrCInzS7i0j"
        gateway_host_url = "https://api.yuanfenju.com/index.php/v1/Zhanbu/yunshi"
        request_data = {
            'api_key': api_secret,
            'type': '0',
            'title_yunshi': str(constellation_number),
        }
        api_response = process_host(request_data, gateway_host_url)

        if api_response:
            # 假设API返回的JSON中有4个字段：content1, content2, content3, content4
            content1 = api_response.get("content1", "无内容1")
            content2 = api_response.get("content2", "无内容2")
            content3 = api_response.get("content3", "无内容3")
            content4 = api_response.get("content4", "无内容4")

            # 发送到电阻屏的4个文本框
            send_to_screen("t10", content1)  # 发送到t10文本框
            send_to_screen("t11", content2)  # 发送到t11文本框
            send_to_screen("t12", content3)  # 发送到t12文本框
            send_to_screen("t13", content4)  # 发送到t13文本框
        else:
            print("未获取到API数据，请检查API请求。")
    except KeyboardInterrupt:
        print("程序已终止。")
    finally:
        # 关闭串口
        ser.close()
        print("串口已关闭。")
