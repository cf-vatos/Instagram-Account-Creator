"""totp.py used for getting 2fa codes."""

import uuid
import time
from datetime import datetime

import tls_client
import requests

from colorama import Fore

class Logging:
    """Logging Class"""

    @staticmethod
    def linput(value: str) -> str:
        """
        Prompt the user for input with a formatted message.
        """
        return input(
            f"{Fore.YELLOW}[{Fore.LIGHTBLACK_EX}INPUT{Fore.YELLOW}] {value}: "
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
        
def between(text, a, b, i=1) -> str:
    return text.split(a)[i].split(b)[0]


class totp:
    def __init__(self, sessionid: str, username: str, proxy: str):
        self.session = tls_client.Session(client_identifier="chrome_120")
        self.session.headers = self._get_headers()
        self.sessionid = sessionid
        self.username = username
        self.session.cookies.update(
            {"wd": "1440x2440", "sessionid": self.sessionid}
        )
        self.session.proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }

    @staticmethod
    def _get_headers():
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "dpr": "1",
            "pragma": "no-cache",
            "prefer": "safe",
            "priority": "u=0, i",
            "referer": "https://www.instagram.com/",
            "sec-ch-prefers-color-scheme": "dark",
            "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-full-version-list": '"Microsoft Edge";v="131.0.2903.112", "Chromium";v="131.0.6778.205", "Not_A Brand";v="24.0.0.0"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": '""',
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua-platform-version": '"15.0.0"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "viewport-width": "1440",
        }

    def get2fa(self, secret: str):
        r = requests.get(f"https://2fa.live/tok/{secret.replace(' ', '')}")
        code = r.json()["token"]
        Logging.debug(message=f"{self.username} Got 2FA Code", value=code)
        return code

    def doweirdreq(self):

        self.session.headers.clear()
        self.session.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "origin": "https://accountscenter.instagram.com",
            "pragma": "no-cache",
            "prefer": "safe",
            "priority": "u=1, i",
            "referer": "https://accountscenter.instagram.com/",
            "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        }

        js_sites = [
            "https://static.xx.fbcdn.net/rsrc-translations.php/v8igFL4/yV/l/en_US/3bCoQUuyGjh.js",
            "https://static.xx.fbcdn.net/rsrc-translations.php/v8iEOf4/yG/l/en_US/dacXJ8PwooB.js",
            "https://static.xx.fbcdn.net/rsrc-translations.php/v8iVNv4/y0/l/en_US/SNoZHFzcNAS.js",
            "https://static.xx.fbcdn.net/rsrc-translations.php/v8iQmq4/y_/l/en_US/jl-ku260hin.js",
        ]
        for url in js_sites:
            self.session.get(url)

        self.session.headers.clear()
        self.session.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://accountscenter.instagram.com",
            "pragma": "no-cache",
            "prefer": "safe",
            "priority": "u=1, i",
            "referer": "https://accountscenter.instagram.com/password_and_security/two_factor/",
            "sec-ch-prefers-color-scheme": "dark",
            "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-full-version-list": '"Microsoft Edge";v="131.0.2903.112", "Chromium";v="131.0.6778.205", "Not_A Brand";v="24.0.0.0"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": '""',
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua-platform-version": '"15.0.0"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "x-asbd-id": "129477",
            "x-fb-lsd": self.lsd,
            "x-ig-app-id": "936619743392459",
        }

    def enable(self):
        r = self.session.get(
            "https://accountscenter.instagram.com/password_and_security/two_factor/",
            allow_redirects=True,
        )
        hs = between(r.text, '"haste_session":"', '"')
        av = between(r.text, '"actorID":"', '"')
        version = between(r.text, '"app_version":"1.0.0.0 (', ")")
        hsi = between(r.text, '"brsid":"', '"')
        fb = between(r.text, '"f":"', '"')
        jazo = between(r.text, "__comet_req=24&jazoest=", '"')
        self.lsd = between(r.text, '"LSD",[],{"token":"', '"')
        mut = str(uuid.uuid4())

        data2 = {
            "av": av,
            "__user": "0",
            "__a": "1",
            "__req": "l",
            "__hs": hs,
            "dpr": "1",
            "__ccg": "EXCELLENT",
            "__rev": version,
            "__s": "::g7hmpx",
            "__hsi": hsi,
            "__dyn": "7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo19oe8hw2nVE4W099w8G1Dz81s8hwnU2lwv89k2C1Fwc60D82IzXwae4UaEW0Loco5G0zK1swa-0nK3qazo7u0zEiwaG1LwTwNw4mwr86C1nw4xxW1owLwHwea",
            "__csr": "gJaNG2kYZirmO9lkWsJFlGXtlXHfcCGRTGSWhugOfqnllSoWkF5nQLF94F5HUJpqHWGaUHUB5HVLlpWAlHF6ELsDvKKmCFCEiitAKWTG9joGFKAUiLAhLGt13WBmngmFdBFaOeVHAmEG8zqAypHQnzFozK59UGJ4AVEqCw04-MxmU428w5sw6cGVaXGElWBHg9-FXyQXw4jw5NyxcPwBglDQtcIU0-eQ3abwEJeui0cyze4qjBGWGKA0FFEVbGE0RyuHG2R0wypaGqWwpVZwk8Twam5U4Sq8yUJ6DgGqfhohxu0qmax6641UgcU1zhHgGq5VHc1WCx-9GjKjOa3OGxmElCzU-kje8h9okxidwjo2ay9dLKimi053Q6O0",
            "__comet_req": "24",
            "fb_dtsg": fb,
            "jazoest": jazo,
            "lsd": self.lsd,
            "__spin_r": version,
            "__spin_b": "trunk",
            "__spin_t": str(time.time())[:10],
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "useFXSettingsTwoFactorGenerateTOTPKeyMutation",
            "variables": str(
                {
                    "input": {
                        "client_mutation_id": str(mut),
                        "actor_id": str(av),
                        "account_id": str(av),
                        "account_type": "INSTAGRAM",
                        "device_id": "device_id_fetch_ig_did",
                        "fdid": "device_id_fetch_ig_did",
                    }
                }
            ),
            "server_timestamps": "true",
            "doc_id": "6282672078501565",
        }

        data = {
            "av": av,
            "__user": "0",
            "__a": "1",
            "__req": "l",
            "__hs": hs,
            "dpr": "1",
            "__ccg": "EXCELLENT",
            "__rev": version,
            "__s": "::g7hmpx",
            "__hsi": hsi,
            "__dyn": "7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo19oe8hw2nVE4W099w8G1Dz81s8hwnU2lwv89k2C1Fwc60D82IzXwae4UaEW0Loco5G0zK1swa-0nK3qazo7u0zEiwaG1LwTwNw4mwr86C1nw4xxW1owLwHwea",
            "__csr": "gJaNG2kYZirmO9lkWsJFlGXtlXHfcCGRTGSWhugOfqnllSoWkF5nQLF94F5HUJpqHWGaUHUB5HVLlpWAlHF6ELsDvKKmCFCEiitAKWTG9joGFKAUiLAhLGt13WBmngmFdBFaOeVHAmEG8zqAypHQnzFozK59UGJ4AVEqCw04-MxmU428w5sw6cGVaXGElWBHg9-FXyQXw4jw5NyxcPwBglDQtcIU0-eQ3abwEJeui0cyze4qjBGWGKA0FFEVbGE0RyuHG2R0wypaGqWwpVZwk8Twam5U4Sq8yUJ6DgGqfhohxu0qmax6641UgcU1zhHgGq5VHc1WCx-9GjKjOa3OGxmElCzU-kje8h9okxidwjo2ay9dLKimi053Q6O0",
            "__comet_req": "24",
            "fb_dtsg": fb,
            "jazoest": jazo,
            "lsd": self.lsd,
            "__spin_r": version,
            "__spin_b": "trunk",
            "__spin_t": str(time.time())[:10],
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "useFXSettingsTwoFactorGenerateTOTPKeyMutation",
            "variables": str(
                {
                    "input": {
                        "client_mutation_id": str(mut),
                        "actor_id": str(av),
                        "account_id": str(av),
                        "account_type": "INSTAGRAM",
                        "device_id": "device_id_fetch_ig_did",
                        "fdid": "device_id_fetch_ig_did",
                    }
                }
            ),
            "server_timestamps": "true",
            "doc_id": "6282672078501565",
        }

        self.session.headers.clear()
        self.session.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://accountscenter.instagram.com",
            "pragma": "no-cache",
            "prefer": "safe",
            "priority": "u=1, i",
            "referer": "https://accountscenter.instagram.com/password_and_security/two_factor/",
            "sec-ch-prefers-color-scheme": "dark",
            "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-full-version-list": '"Microsoft Edge";v="131.0.2903.112", "Chromium";v="131.0.6778.205", "Not_A Brand";v="24.0.0.0"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": '""',
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua-platform-version": '"15.0.0"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "x-asbd-id": "129477",
            "x-fb-lsd": self.lsd,
            "x-ig-app-id": "936619743392459",
            "x-fb-friendly-name": "useFXSettingsTwoFactorGenerateTOTPKeyMutation",
        }
        self.session.headers.update(
            {
                "x-fb-friendly-name": "FXAccountsCenterTwoFactorSelectMethodDialogQuery",
            }
        )
        self.session.post(
            "https://accountscenter.instagram.com/api/graphql/", data=data
        )
        self.doweirdreq()
        data["fb_api_req_friendly_name"] = (
            "FXAccountsCenterTwoFactorTOTPQRCodeDialogQuery"
        )
        data["variables"] = str(
            {"account_type": "INSTAGRAM", "interface": "IG_WEB", "user_id": av}
        )
        data["spin_t"] = str(time.time())[:10]
        data["req"] = "h"
        data["doc_id"] = "8005164792840288"
        self.session.headers.update(
            {
                "x-fb-friendly-name": "FXAccountsCenterTwoFactorTOTPQRCodeDialogQuery",
            }
        )
        load = self.session.post(
            "https://accountscenter.instagram.com/api/graphql/", data=data2
        )
        key: str = load.json()["data"]["xfb_two_factor_generate_totp_key"][
            "totp_key"
        ][
            "key_text"
        ]  
        Logging.debug(message=f"{self.username} Sent 2FA Code", value=key)
        code = self.get2fa(key)
        self.session.headers.update(
            {"x-fb-friendly-name": "useFXSettingsTwoFactorEnableTOTPMutation"}
        )
        data["fb_api_req_friendly_name"] = (
            "useFXSettingsTwoFactorEnableTOTPMutation"
        )
        data["variables"] = str(
            {
                "input": {
                    "client_mutation_id": str(mut),
                    "actor_id": str(av),
                    "account_id": str(av),
                    "account_type": "INSTAGRAM",
                    "verification_code": str(code),
                    "device_id": "device_id_fetch_ig_did",
                    "fdid": "device_id_fetch_ig_did",
                }
            }
        )
        data["spin_t"] = str(time.time())[:10]
        data["__req"] = "10"
        data["doc_id"] = "7032881846733167"
        verify = self.session.post(
            "https://accountscenter.instagram.com/api/graphql/", data=data
        )
        data["fb_api_req_friendly_name"] = (
            "useFXSettingsTwoFactorFetchRecoveryCodesMutation"
        )
        data["variables"] = str(
            {
                "input": {
                    "client_mutation_id": str(mut),
                    "actor_id": str(av),
                    "account_id": str(av),
                    "account_type": "INSTAGRAM",
                    "fdid": "device_id_fetch_ig_did",
                }
            }
        )
        data["spin_t"] = str(time.time())[:10]
        data["__req"] = "1t"
        data["doc_id"] = "24140213678960162"
        data["__ccg"] = "POOR"
        verify = self.session.post(
            "https://accountscenter.instagram.com/api/graphql/", data=data
        )
        codes = verify.json()["data"]["xfb_two_factor_fetch_recovery_codes"]["recovery_codes"]
        Logging.success(message=f"{self.username} Enabled 2FA", value=codes)
        return codes
