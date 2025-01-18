# -*- coding: gbk -*-

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



name = input("������������֣�")
birth_date_str = input("������������գ���ʽΪM/D����")
try:
    month, day = map(int, birth_date_str.split('/'))
    constellation_number = get_constellation_number(month, day)
    a=constellation_number
except ValueError:
    print("��������ڸ�ʽ����ȷ���밴��M/D�ĸ�ʽ���롣")




import requests

# ������Կ
api_secret = "UHbh7CMB4midIKcrCInzS7i0j"
# ����������ʱ�ӿ�
gateway_host_url = "https://api.yuanfenju.com/index.php/v1/Zhanbu/yunshi"


# �������
request_data = {
    'api_key':api_secret,
    'type': '0',
    'title_yunshi': str(a),
}

def process_host(data, url):
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        print(response.text)
    except requests.exceptions.RequestException as e:
        # Handle or output the error message as needed
        print(f"Request error: {e}")

process_host(request_data, gateway_host_url)
