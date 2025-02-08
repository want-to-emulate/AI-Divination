# -*- coding: gbk -*-

import requests
import serial

#初始化串口
ser = serial.Serial(port, baud, timeout=1)

#端口和波特率
port="com4"
baud=115200

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


name = input("请输入你的名字：")
birth_date_str = input("请输入你的生日（格式为M-D）：")
try:
    month, day = map(int, birth_date_str.split('-'))
    constellation_number = get_constellation_number(month, day)
    a=constellation_number
except ValueError:
    print("输入的日期格式不正确，请按照M/D的格式输入。")




import requests

# 您的密钥
api_secret = "UHbh7CMB4midIKcrCInzS7i0j"
# 请求择日择时接口
gateway_host_url = "https://api.yuanfenju.com/index.php/v1/Zhanbu/yunshi"


# 请求参数
request_data = {
    'api_key':api_secret,
    'type': '1',
    'title_yunshi': str(a),
}

    # 获取API数据
def process_host(request_data, gateway_host_url):
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # 检查请求是否成功
        try:
            return response.json()  # 尝试解析为JSON
        except ValueError:
            print("API返回数据不是有效的JSON格式。")
            return None
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {e}")
        return None

    # 发送数据到电阻屏
def send_to_screen(text):
    max_length = 255  # 假设文本框最大长度为255
    if len(text) > max_length:
        text = text[:max_length]
    command = f't0.txt="{text}"\xFF\xFF\xFF'  # t0是文本框控件ID，末尾加\xFF\xFF\xFF表示结束符
    try:
        ser.write(command.encode('gbk'))  # 使用GBK编码发送
    except UnicodeEncodeError:
        ser.write(command.encode('utf-8'))  # 尝试使用UTF-8编码
    print(f"发送到屏幕: {command}")

# 主程序
if __name__ == "__main__":
    # 获取API数据
    api_response = process_host(request_data, gateway_host_url)
    if api_response:
        # 假设API返回的JSON中有4个字段：content1, content2, content3，content4
        content1 = api_response.get("content1", "无内容1")
        content2 = api_response.get("content2", "无内容2")
        content3 = api_response.get("content3", "无内容3")
        content3 = api_response.get("content4", "无内容4")

        # 发送到电阻屏的4个文本框
        send_to_screen("t1", content1)  # 发送到t1文本框
        send_to_screen("t2", content2)  # 发送到t2文本框
        send_to_screen("t3", content3)  # 发送到t3文本框
        send_to_screen("t4", content4)  # 发送到t4文本框
    else:
        print("未获取到API数据，请检查API请求。")

    # 关闭串口
    ser.close()


