import time
import string
import random
import threading
import os
import json
import ctypes
import httpx

from datetime import datetime

from tls_client import Session
from faker import Faker
from kopeechka import KopeechkaApiError, MailActivations
from colorama import Fore

from helper.humanize import humanize_account
from helper.totp import totp

config = json.load(open("config.json", encoding="utf-8"))

class Stats:
    created = 0
    failed = 0
    locked = 0
    humanized = 0
    total = 0
    start = time.time()
    working = True

def title():
    while True:
        try:
            success_rate = round((Stats.created / (Stats.failed + Stats.created)) * 100, 2)
        except ZeroDivisionError:
            success_rate = 0
        title = f"Instagram Account Creator ┃ G: {Stats.created} ┃ H: {Stats.humanized} ┃ F: {Stats.failed} ┃ L: {Stats.locked} ┃ T: {Stats.total} ┃ Succses Rate: {success_rate}% ┃ Time: {round(time.time() - Stats.start, 2)}s "
        ctypes.windll.kernel32.SetConsoleTitleW(title)
        time.sleep(0.01) 
        
class Logging:
    """Logging Class"""

    @staticmethod
    def linput(value: str) -> str:
        """
        Prompt the user for input with a formatted message.
        """
        return input(
            f"{Fore.YELLOW}[{Fore.LIGHTBLACK_EX}INPUT{Fore.YELLOW}] {Fore.LIGHTBLACK_EX}{value}:{Fore.YELLOW} "
        )

    @staticmethod
    def debug(message: str, value: str) -> None:
        """
        Print a debug message.
        """
        timestamp =  datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{Fore.YELLOW}[{Fore.LIGHTBLACK_EX}{timestamp}{Fore.YELLOW}] {Fore.LIGHTBLACK_EX}{message} -> {Fore.YELLOW}{value}")

    @staticmethod
    def success(message: str, value: str) -> None:
        """
        Print a success message.
        """
        timestamp =  datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{Fore.YELLOW}[{Fore.LIGHTBLACK_EX}{timestamp}{Fore.YELLOW}] {Fore.LIGHTBLACK_EX}{message} -> {Fore.LIGHTGREEN_EX}{value}")

    @staticmethod
    def error(message: str, value: str) -> None:
        """
        Print an error message.
        """
        timestamp =  datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{Fore.YELLOW}[{Fore.LIGHTBLACK_EX}{timestamp}{Fore.YELLOW}] {Fore.LIGHTBLACK_EX}{message} -> {Fore.RED}{value}")
        
class KopeechkaApi:
    def __init__(self):
        self.api_key = config["kopeechka_api"]
        self.api = MailActivations(api_token=self.api_key)
    
    def get_email(self):
        try:
            response = self.api.mailbox_get_email(site='instagram.com', mail_type=random.choice(config["mail_domains"]), soft_id=99)
            if response.status == 'OK':
                Logging.debug(message="Email", value=response.mail)
                return response
            else:
                raise Exception('Failed to get email.')
        except KopeechkaApiError as e:
            Logging.error(message="Kopeechka API Error", value=e)
            raise Exception(e)

    def get_verification_token(self, task_id):
        tries = 0
        while tries < 300:
            response = httpx.get(f"http://api.kopeechka.store/mailbox-get-message?id={task_id}&token={self.api_key}&api=2.0")
            if 'OK' in response.text:
                token = response.json()['value']
                self.api.mailbox_cancel(task_id)   
                return token
            else:
                tries += 1
                time.sleep(0.1)

        self.api.mailbox_cancel(task_id)     
        Logging.error("Failed to retrieve email verification token.")
        raise Exception('Mail not received.')

class InstagramGen:
    def __init__(self):
        with open("data/proxies.txt", "r", encoding="utf-8") as f:
            self.proxies = f.read().splitlines()
        
        self.fake = Faker()
        
        self.proxy = random.choice(self.proxies)
        self.version = random.randint(120, 131)
        self.useragent = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.version}.0.0.0 Safari/537.36'

        if "@" not in self.proxy:
            self.proxy = f"{self.proxy.split(':')[2]}:{self.proxy.split(':')[3]}@{self.proxy.split(':')[0]}:{self.proxy.split(':')[1]}"

        self.session = Session(
            client_identifier=f"chrome_{self.version}"
        )

        self.session.proxies = {
            "http": f"http://{self.proxy}",
            "https": f"http://{self.proxy}",
        }

        self._set_default_headers()
        status = self._getsignup()
        if not status:
            return

        self.full_name = self.fake.name()
        self.first_name, self.surname = self.full_name.split(' ', 1)
        self.username = self.full_name.replace(' ', '') + str(random.randint(1111111111, 9999999999999))

        self.day = str(random.randint(1, 25))
        self.month = str(random.randint(1, 12))
        self.year = str(random.randint(1980, 2000))

        self.mailapi = KopeechkaApi()
        self.responsek = self.mailapi.get_email()
        self.email = self.responsek.mail
        self.password = self._generate_password()

        self._register()
        
    def _set_default_headers(self):
        self.session.headers = {
            'authority': 'www.instagram.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://www.instagram.com/accounts/emailsignup/',
            'sec-ch-ua': f'"Chromium";v="{self.version}", "Not(A:Brand";v="24", "Brave";v="{self.version}"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.useragent
        }
    
    @staticmethod
    def _encpass(password: str) -> str:
        return f'#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:{password}'
        
    @staticmethod
    def _generate_password():
        """
        Generates a simple secure password of the specified length.

        :param length: Length of the password (default is 12).
        :return: A randomly generated password.
        """
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for _ in range(16))
        Logging.debug(message="Password", value=password)
        return password

    def _get_csrftoken(self):
        try:
            response = self.session.get('https://www.instagram.com/data/shared_data/')
            return response.text.split('csrf_token":"')[1].split('"')[0]
        except Exception as e:
            self.logger.error(f"Error retrieving csrftoken: {e}")
            return None

    def _getsignup(self) -> None:
        try:
            response = self.session.get('https://www.instagram.com/accounts/emailsignup/')
            self.device_id =response.text.split('"machine_id":"')[1].split('"')[0]
            self.session.headers.update({
                "x-asbd-id": '129477',
                "x-csrftoken": self._get_csrftoken(),
                "x-ig-app-id": '936619743392459',
                "x-ig-www-claim": '0',
            })
            self.session.get('https://www.instagram.com/api/v1/web/login_page/')
            return True
        except Exception as e:
            return False
        

    def _register(self) -> None:
        try:
            data = {
                'enc_password': self._encpass(password=self.password),
                'email': self.email,
                'first_name': self.first_name,
                'username': self.username,
                'opt_into_one_tap': 'false',
            }

            response = self.session.post(
                'https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/',
                data=data,
            )

            data = {
                'day': self.day,
                'month': self.month,
                'year': self.year,
            }

            response = self.session.post(
                'https://www.instagram.com/api/v1/web/consent/check_age_eligibility/',
                data=data,
            )

            data = {
                'device_id': self.device_id,
                'email': self.email,
            }

            response = self.session.post(
                'https://www.instagram.com/api/v1/accounts/send_verify_email/',
                data=data,
            )
            Logging.debug(message="Sent verification email to", value=self.email)

            code = self.mailapi.get_verification_token(self.responsek.id)
            Logging.debug(message="Got OTP code", value=code)

            data = {
                'code': code,
                'device_id': self.device_id,
                'email': self.email,
            }

            response = self.session.post(
                'https://www.instagram.com/api/v1/accounts/check_confirmation_code/',
                data=data,
            )

            signup_code = response.json()["signup_code"]

            data = {
                'enc_password': self._encpass(password=self.password),
                'day': self.day,
                'email': self.email,
                'first_name': self.first_name,
                'month': self.month,
                'username': self.username,
                'year': self.year,
                'client_id': self.device_id,
                'seamless_login_enabled': '1',
                'tos_version': 'row',
                'force_sign_up_code': signup_code,
            }

            response = self.session.post(
                'https://www.instagram.com/api/v1/web/accounts/web_create_ajax/',
                data=data,
            )

            if response.json().get("account_created"):
                Logging.success(message="Account successfully created", value=f"{self.email}:{self.password}")
                session_id = response.cookies.get('sessionid')
                username_password, proxy_ip_port = self.proxy.split("@")
                username, password = username_password.split(":")
                proxy_ip, port = proxy_ip_port.split(":")

                self.formatted_proxy = f"https:{proxy_ip}:{port}:{username}:{password}"
                with open("results/accounts.txt", "a+", encoding="utf-8") as f:
                    f.write(f"{self.username}:{self.password}|{self.useragent}|{self.formatted_proxy}|{session_id}\n")
                    
                Stats.created += 1
                Stats.total += 1
                try:
                    if config["humanization"]:
                        new_username = humanize_account(username=self.username, session_id=session_id, proxy=self.proxy)
                        if new_username:
                            self.username = new_username
                            Logging.success(message="Account successfully Humanized", value=f"{self.email}:{self.password}")
                            with open("results/humanized.txt", "a+", encoding="utf-8") as f:
                                f.write(f"{new_username}|{self.password}|{self.useragent}|{self.formatted_proxy}|{session_id}\n")
                                Stats.humanized += 1
                        else:
                            with open("results/locked.txt", "a+", encoding="utf-8") as f:
                                f.write(f"{self.username}|{self.password}|{self.useragent}|{self.formatted_proxy}|{session_id}\n")
                            Stats.locked += 1
                            Stats.failed += 1
                            return
                                
                except Exception as e:
                    Logging.error(message="Failed To Humanize", value=e)

                try:
                    if config["2fa"]:
                        session_id = response.cookies.get('sessionid')
                        codes = totp(sessionid=session_id ,username=self.username, proxy=self.proxy).enable()

                        if codes:
                            with open("results/full.txt", "a+", encoding="utf-8") as f:
                                f.write(f"{self.username}|{self.password}|{self.useragent}|{self.formatted_proxy}|{session_id}|{codes}\n")
                                Stats.humanized += 1

                except Exception as e:
                    Logging.error(message="Failed To Enable 2FA", value=e)
                    
            else:
                Logging.error(message=f"Account creation failed for {self.email}", value=response.json())
                Stats.failed += 1
                Stats.total += 1

        except Exception as e:
            Logging.error(message="Error during account creation", value=e)
            Stats.failed += 1


def instagram_gen():
    while True:
        try:
            InstagramGen()
        except Exception as e:
            Logging.error(message="An error occurred", value=e)
        finally:
            time.sleep(1)

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    thread_count = Logging.linput("Threads")
    
    threading.Thread(target=title, daemon=True).start()

    for _ in range(int(thread_count)):
        threading.Thread(target=instagram_gen, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
            Logging.info("Program terminated by user.")