# https://rapidapi.com/reversecoders/api/tiktok4free
# Support: https://t.me/reversecoders

import random
import time
import requests

from random             import choices
from urllib.parse       import urlencode
from faker              import Faker
from device_register    import DeviceRegister
from request_tiktok     import tt_common_post_request
from utils              import printf


def xor(string: str) -> str:
    return "".join([hex(ord(_) ^ 5)[2:] for _ in string])

def generate_nickname():
    fake        = Faker()
    adjective   = fake.word()
    noun        = fake.word()

    return f"{adjective}_{noun}"


def letters():
    return random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])

def numbers():
    return random.randint(0,9)

def characters():
    return random.choice(['@', '.', ','])

def generate_random_password():
    return f'{letters()}{letters().lower()}{numbers()}{letters()}{characters()}{letters().lower()}{characters()}{letters().lower()}{numbers()}{letters().lower()}'



if __name__ == "__main__":
    # -------- START ONLY CHANGE HERE -------- #
    proxy   = None
    username    = ""
    password    = ""
    # NOTE: If you change country, please also change the domains inside domains.py!
    country = 'pl'
    token       = ''.join(choices('0123456789abcdefghiklmnopqrstuvwxyz', k=8))
    proxy       = f'{username}:{password}_country-{random.choice(["de", "cz", "es", "it"])}_session-{token}_lifetime-5m@geo.iproyal.com:12321'
    # -------- END ONLY CHANGE HERE -------- #

    session = requests.Session()
    if proxy:
        session.proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}

    device = DeviceRegister(proxy=proxy, country=country, session=session)

    printf(f'\n==== START GET DEVICE TEMPLATE ====\n')
    device.process_dev_info()
    printf(f'\n==== END GET DEVICE TEMPLATE ====')

    printf(f'\n==== START REGISTER DEVICE ====\n')
    r = device.post_device_register()
    dev_info = device.dev_info
    dev_info["device"]["installId"] = device.install_id
    dev_info["device"]["deviceId"] = device.device_id
    if dev_info["device"]["installId"] and dev_info["device"]["deviceId"] == 0 or dev_info["device"]["installId"] and dev_info["device"]["deviceId"] == '' or dev_info["device"]["installId"] and dev_info["device"]["deviceId"] == '0':
        printf('Device not registered')
        raise ('Device not registered')
    printf(f'\n==== END REGISTER DEVICE ====')
    time.sleep(3)

    printf(f'\n==== START APP ALERT CHECK ====\n')
    device.send_app_alert_check()
    printf(f'\n==== END APP ALERT CHECK ====')
    time.sleep(4)

    printf("\n==== START GET SEED ====\n")
    obj = device.get_seed()
    try:
        dev_info["extra"]["seed"] = obj['data']['token']
        dev_info["extra"]["seedAlgorithm"] = obj['data']['algo']
    except:
        printf('No seed')
        raise ('No seed')
    printf("\n==== END GET SEED ====")
    time.sleep(7)

    printf(f'\n==== START GET SEC DEV ID ====\n')
    token = device.get_token()
    printf(f'\n==== END GET SEC DEV ID ====')

    printf(f"\n==== START RI REPORT ====\n")
    dev_info["extra"]["secDeviceIdToken"] = token
    device.post_ri_report(0)
    time.sleep(2)
    device.post_ri_report(1)
    time.sleep(2)
    device.post_ri_report(2)
    time.sleep(2)
    device.post_ri_report(3)
    time.sleep(2)
    device.post_ri_report(4)
    printf("\n==== END ri/report ====")
    time.sleep(8)

    printf(f'\n==== START MSCC SETTING ====\n')
    token = device.post_mscc_setting()
    printf(f'\n==== END MSCC SETTING ====')
    time.sleep(2)

    printf(f'\n==== START DEVICE TRUST USERS ====\n')
    device.send_device_trust_users()
    printf(f'\n==== END DEVICE TRUST USERS ====')

    printf("\n==== START DEVICE INFO ====\n")
    printf(dev_info)
    printf("\n==== END DEVICE INFO ====")
    time.sleep(2)

    printf("\n==== START REGISTER ACCOUNT ====\n")
    randomnickname = generate_nickname()
    randomemail = f'{randomnickname}{random.randint(1111, 9999)}{random.choice(["@gmail.com", "@outlook.com", "@icloud.com"])}'
    email = xor(randomemail)
    randompassword = generate_random_password()
    password = xor(randompassword)
    birthday = f'{random.randint(1960, 2004)}-0{random.randint(1, 9)}-{random.randint(10, 26)}'
    payload = urlencode({
        'birthday': birthday,
        'password': f'{password}',
        'fixed_mix_mode': '1',
        'account_sdk_source': 'app',
        'rule_strategies': '1%2C2',
        'mix_mode': '1',
        'multi_signup': '0',
        'multi_login': '1',
        'email': f'{email}',
    })
    device.send_passport_region(randomemail)
    time.sleep(2)
    extra = {
        "passport-sdk-version": "5050490",
        "last_install_time": str(round(time.time())),
        "reg_store_region": dev_info['geo']['region'].lower(),
    }
    tt_common_post_request(session=session, dev_info=dev_info, host=f"{dev_info['geo']['domain_normal']}/", url='passport/email/register/v2/', body=payload, account_info=None, extra=extra)
    printf("\n==== END REGISTER ACCOUNT ====")
