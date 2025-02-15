"""humanize.py Handles the account humanization."""
import random
import os 

from urllib.parse import urlencode

from curl_cffi import CurlMime
from curl_cffi.requests import Session

from colorama import Fore  

from datetime import datetime
import time

class Logging:
    """Logging Class"""

    @staticmethod
    def linput(value: str) -> str:
        """
        Prompt the user for input with a formatted message.
        """
        return input(
            f"{Fore.YELLOW}[{Fore.LIGHTBLACK_EX}INPUT{Fore.YELLOW}] {Fore.LIGHTBLACK_EX}{value}: "
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

class Utils:
    def __init__(self):
        pass

    def get_username(self, path: str) -> str:
        path = f".\\helper\\data\\{path}"
        username_file = os.path.join(path, "usernames.txt")

        if not os.path.exists(username_file):
            raise FileNotFoundError(f"Username file not found at {username_file}")

        with open(username_file, 'r', encoding="utf-8") as file:
            username = [line.strip() for line in file.readlines()]

        username = random.choice(username)
        username = username.replace("\n", " ").replace("\r", "").strip()
        return username

    def get_bio(self, path: str) -> str:
        path = f".\\helper\\data\\{path}"
        bio_file = os.path.join(path, "bios.txt")

        if not os.path.exists(bio_file):
            raise FileNotFoundError(f"Bio file not found at {bio_file}")

        with open(bio_file, 'r', encoding="utf-8") as file:
            bio = [line.strip() for line in file.readlines()]

        bio = random.choice(bio)
        bio = bio.replace("\n", " ").replace("\r", "").strip()
        return bio

    def get_pfp(self, path: str) -> str:
        path = f".\\helper\\data\\{path}\\pfp"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Directory not found at {path}")

        jpg_files = [f for f in os.listdir(path) if f.lower().endswith('.jpg')]

        if not jpg_files:
            raise FileNotFoundError(f"No .jpg files found in directory {path}")

        random_pfp = random.choice(jpg_files)

        return os.path.join(path, random_pfp)

class InstaHumanize:
    def __init__(self, session_id: str, username: str, proxy: str = None, debug: bool = False):
        self.logger = Logging()

        self.session = Session()
        self.session_id = session_id
        self.username = username
        self.proxy = proxy
        self.debug = debug  
        self.locked = False
        
        self._set_session_proxies()
        self._set_default_headers()

    def _set_session_proxies(self):
        if self.proxy:
            self.session.proxies = {
                'http': self.proxy,
                'https': self.proxy
            }

    def _set_default_headers(self):
        self.session.headers = {
            "authority": "www.instagram.com",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7,en-DE;q=0.6",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.instagram.com",
            "priority": "u=1, i",
            "referer": "https://www.instagram.com/accounts/edit/",
            "sec-ch-prefers-color-scheme": "dark",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-full-version-list": "\"Google Chrome\";v=\"131.0.6778.205\", \"Chromium\";v=\"131.0.6778.205\", \"Not_A Brand\";v=\"24.0.0.0\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "\"\"",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua-platform-version": "\"15.0.0\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }

    def _get_csrftoken(self):
        try:
            response = self.session.get('https://www.instagram.com/')
            return response.cookies.get("csrftoken")
        except Exception as e:
            self.logger.error(message="Error retrieving csrftoken", value=e)
            return None

    def _fill_headers(self):
        csrftoken = self._get_csrftoken()
        if not csrftoken:
            return None

        self.session.headers.update({
            "x-asbd-id": '129477',
            "x-csrftoken": csrftoken,
            "x-ig-app-id": '936619743392459',
            "x-ig-www-claim": '0',
        })

        self.session.cookies.set("sessionid", self.session_id)
        return self.session.headers

    def get_username(self, base_username: str) -> None:
        """Fetches a new username suggestion by modifying the base username."""
        suffixes = [".lol", ".xoxo", "xoxo", "XD"]
        new_username = base_username + random.choice(suffixes)

        email = f"{new_username}@gmail.com"
        
        data = {
            "enc_password": "",
            "email": email,
            "failed_birthday_year_count": {},
            "first_name": "",
            "username": new_username,
            "opt_into_one_tap": False,
            "use_new_suggested_user_name": True
        }
        
        try:
            csrftoken = self._get_csrftoken()
            self.session.headers.update({"x-csrftoken": csrftoken})
        except Exception as e:
            self.logger.error(message="Error retrieving CSRF token", value=e)
            return

        try:
            response = self.session.post(
                "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/", 
                data=data
            )
            response_data = response.json()
        except Exception as e:
            self.logger.error(message="Error during POST request", value=e)
            return

        if 'username_suggestions' in response_data:
            if response_data['username_suggestions']:  
                new_user = random.choice(response_data['username_suggestions'])
                self.logger.debug(message="Changed Username", value=new_user)
                self.username = new_user
            else:
                self.username = new_username
        else:
            self.username = new_username
            
        return self.username


    def change_bio(self, bio: str):
        payload = {
            "biography": bio,
            "chaining_enabled": "on",
            "email": "",
            "external_url": "",
            "first_name": "",
            "phone_number": "",
            "username": self.username
        }

        self._send_post_request(
            url="https://www.instagram.com/api/v1/web/accounts/edit/",
            payload=payload,
            action="bio",
            bio=bio
        )

    def change_gender(self, gender: str):
        gender_map = {
            "male": 1,
            "female": 2,
            "prefer not to say": 3
        }

        gender_value = gender_map.get(gender.lower())
        if gender_value is None:
            self.logger.error("Invalid gender value. Please choose from 'male', 'female', or 'prefer not to say'.")
            return

        payload = {
            "custom_gender": "",
            "gender": gender_value
        }

        self._send_post_request(
            url="https://www.instagram.com/api/v1/web/accounts/set_gender/",
            payload=payload,
            action="gender",
            gender=gender
        )

    def _send_post_request(self, url: str, payload: dict, action: str, bio: str = None, gender: str = None):
        encoded_payload = urlencode(payload)
        try:
            headers = self._fill_headers()
            if not headers:
                return

            response = self.session.post(url, headers=headers, data=encoded_payload)
            if action == "bio":
                if response.status_code == 200:
                    self.logger.debug(message=f"{self.username} Changed Bio", value=bio)
                    return
            elif action == "gender":
                if response.status_code == 200:
                    self.logger.debug(message=f"{self.username} Changed Gender", value=gender)
                    return
            
            if "lock" in response.json():
                self.logger.error(message=self.username, value="Locked")
                self.locked = True
                return
                
        except Exception as e:
            self.logger.error(message=f"Error during {action} change request to {url}", value=e)

    def change_pfp(self, pfp_path: str):
        try:
            headers = self._fill_headers()
            if not headers:
                return

            mp = CurlMime(self.session.curl)
            boundary = '----WebKitFormBoundary4u1KBSz0k3xMOyX0'

            mp.addpart(
                name="profile_pic",
                content_type="image/jpeg",
                filename="profilepic.jpg",
                local_path=pfp_path,
            )

            headers["content-type"] = f"multipart/form-data; boundary={boundary}"

            response = self.session.post(
                "https://www.instagram.com/api/v1/web/accounts/web_change_profile_picture/",
                headers=headers,
                multipart=mp
            )
            if "lock" in response.json():
                self.logger.error(message=self.username, value="Locked")
                self.locked = True
                return
            
            self.logger.debug(message=f"{self.username} Changed PFP", value=response.status_code)

        except Exception as e:
            self.logger.error(f"Error during PFP change request: {e}")
        finally:
            mp.close()
    
    def humanize(self):
        gender = random.choice(["Male", "Female"])
        self.logger.debug(message=f"{self.username} Humanize Gender", value=gender)
        if gender.lower() == "male":
            path = "boys"

        if gender.lower() == "female":
            path = "girls"

        username = Utils().get_username(path=path)
        bio = Utils().get_bio(path=path)
        pfp = Utils().get_pfp(path=path)
        username = self.get_username(base_username=username)
        self.change_bio(bio=bio)
        if self.locked:
            return False
        self.change_gender(gender=gender)
        if self.locked:
            return False
        self.change_pfp(pfp_path=pfp)
        if self.locked:
            return False
        return username



def humanize_account(username, session_id, proxy):
    username = InstaHumanize(
        session_id=session_id,
        username=username,
        debug=True,
        proxy=proxy
    ).humanize()
    return username
