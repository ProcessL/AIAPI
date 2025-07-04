import requests
import json



def check_deepseek_api(api_key):
    """
    检查deepseek api是否可用,余额
    """
    url = "https://api.deepseek.com/user/balance"

    payload={}
    headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {api_key}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # 输出详细信息
    # API是否可用
    is_available = response.json()['is_available']
    # 币种
    currency = response.json()['balance_infos'][0]['currency']
    # 余额
    balance = response.json()['balance_infos'][0]['total_balance']
    # 未过期的赠金余额
    # granted_balance = response.json()['balance_infos'][0]['granted_balance']
    # 充值的余额
    # topped_up_balance = response.json()['balance_infos'][0]['topped_up_balance']

    return is_available, currency, balance


if __name__ == "__main__":
    api_key = "sk-22df05dbda344a35830fb0e9f76a052b"
    is_available, currency, balance = check_deepseek_api(api_key)
    print(f"API是否可用: {is_available}")
    print(f"币种: {currency}")
    print(f"余额: {balance}")


# print(f"未过期的赠金余额: {granted_balance}")
# print(f"充值的余额: {topped_up_balance}")

