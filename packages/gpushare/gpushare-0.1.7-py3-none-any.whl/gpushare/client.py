# gpushare/client.py

import re
import requests
from datetime import datetime
from .exceptions import (
    GPUShareError, AuthenticationError, AuthorizationError, APIError
)

class GPUShareClient:
    def __init__(self, base_url: str):
        self.base = base_url.rstrip("/")
        self.session = requests.Session()
        self.token = None
        self.authenticated = False
        self.gpu_id = None
        self.mode = "user"
        self.allowed_roles = []

    # --------------------
    # Authentication
    # --------------------

    def login(self, email: str, password: str, token: str, mode: str = "user"):
        if mode not in ("user","owner","admin","moderator"):
            raise ValueError("Mode must be one of user, owner, admin, moderator.")
        self.mode = mode
        url = f"{self.base}/login"
        r = self.session.post(url, json={
            "email": email,
            "password": password,
            "token": token,
            "mode": mode,
            "gpu_id": self.gpu_id or 0
        })
        if r.status_code != 200:
            raise AuthenticationError(r.text)
        print("OTP sent. Call verify_otp(otp) to complete login.")
        self.authenticated = False

    def verify_otp(self, otp: str):
        url = f"{self.base}/verify_otp"
        r = self.session.post(url, json={"otp": otp})
        if r.status_code != 200:
            raise AuthenticationError(r.text)
        print("Login successful.")
        self.authenticated = True

    def get_api_token(self):
        url = f"{self.base}/get_api_token"
        r = self.session.get(url)
        if r.status_code != 200:
            raise APIError("Failed to get API token")
        m = re.search(r"<pre.*?>([\w\-\._~\+/=]+)</pre>", r.text)
        if not m:
            raise APIError("API token not found in response")
        self.token = m.group(1)
        self.authenticated = True
        print("API token acquired.")

    def set_api_token(self, token: str):
        """
        Directly set a pre‑obtained API token. 
        Bypass login/OTP flow.
        """
        if not token or not isinstance(token, str):
            raise AuthenticationError("API token must be a non‑empty string.")
        self.token = token
        self.authenticated = True
        print("API token set; you are now authenticated.")

    # --------------------
    # Internal Helpers
    # --------------------

    def _auth_headers(self):
        if not self.token:
            raise AuthenticationError("No API token; call get_api_token() first.")
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _parse_response(self, r: requests.Response):
        if not r.ok:
            # Try to extract JSON error
            try:
                err = r.json().get("error", r.text)
            except Exception:
                err = r.text or f"HTTP {r.status_code}"
            raise APIError(err)
        ct = r.headers.get("Content-Type", "")
        if "application/json" in ct:
            return r.json()
        return r.text

    # --------------------
    # Role & GPU Selection
    # --------------------

    def select_gpu(self, gpu_id: int):
        if not self.authenticated:
            raise AuthenticationError("Authenticate before selecting a GPU.")
        self.gpu_id = gpu_id
        url = f"{self.base}/api/gpu_roles/{gpu_id}"
        r = self.session.get(url, headers=self._auth_headers())
        data = self._parse_response(r)
        self.allowed_roles = data.get("roles", [])
        print("Allowed roles:", self.allowed_roles)

    def switch_mode(self, mode: str):
        if mode not in self.allowed_roles:
            raise AuthorizationError(f"You do not have role '{mode}' for GPU {self.gpu_id}")
        self.mode = mode
        print("Switched mode to:", mode)

    # --------------------
    # GPU & Access APIs
    # --------------------

    def list_available_gpus(self):
        url = f"{self.base}/api/available_gpus?mode={self.mode}"
        r = self.session.get(url, headers=self._auth_headers())
        return self._parse_response(r)

    def get_gpu_detail(self):
        if self.gpu_id is None:
            raise APIError("Select a GPU first.")
        url = f"{self.base}/api/gpu_detail/{self.gpu_id}"
        r = self.session.get(url, headers=self._auth_headers())
        return self._parse_response(r)

    def request_access(self, code: str = None):
        if self.gpu_id is None:
            raise APIError("Select a GPU first.")
        url = f"{self.base}/request_gpu/{self.gpu_id}"
        payload = {}
        if code:
            payload["code"] = code
        r = self.session.post(url, headers=self._auth_headers(), json=payload)
        return self._parse_response(r)

    def get_my_requests(self):
        url = f"{self.base}/my_requests"
        r = self.session.get(url, headers=self._auth_headers())
        return self._parse_response(r)

    def approve_request(self, req_id: int):
        if self.mode not in ("owner","admin","moderator"):
            raise AuthorizationError("Cannot approve in current mode.")
        url = f"{self.base}/approve_request/{req_id}"
        r = self.session.post(url, headers=self._auth_headers())
        return self._parse_response(r)

    def deny_request(self, req_id: int):
        if self.mode not in ("owner","admin","moderator"):
            raise AuthorizationError("Cannot deny in current mode.")
        url = f"{self.base}/deny_request/{req_id}"
        r = self.session.post(url, headers=self._auth_headers())
        return self._parse_response(r)

    def revoke_access(self, request_id: int):
        if self.mode not in ("owner","admin","user"):
            raise AuthorizationError("Cannot revoke in current mode.")
        url = f"{self.base}/revoke_access/{request_id}"
        r = self.session.post(url, headers=self._auth_headers())
        return self._parse_response(r)

    # --------------------
    # Code Review & Execution
    # --------------------

    def download_reviewed_code(self, review_id: int, dest_path: str):
        url = f"{self.base}/download_review/{review_id}"
        r = self.session.get(url, headers=self._auth_headers(), stream=True)
        if r.status_code != 200:
            raise APIError("Failed to download reviewed code.")
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        print(f"Review {review_id} downloaded to {dest_path}")

    def run_reviewed_code(self, review_id: int):
        url = f"{self.base}/run_reviewed_code/{review_id}"
        r = self.session.get(url, headers=self._auth_headers())
        return self._parse_response(r)

    def execute_code(self, code: str):
        if self.gpu_id is None:
            raise APIError("Select a GPU first.")
        url = f"{self.base}/api/execute_code/{self.gpu_id}"
        r = self.session.post(url, headers=self._auth_headers(), json={"code": code})
        data = self._parse_response(r)
        if isinstance(data, dict) and "output" in data:
            return data["output"]
        return data
    # --------------------
    # Token Management
    # --------------------

    def get_token_info(self):
        """
        Returns a dict with:
          - issued_at: ISO8601 string
          - expires_at: ISO8601 string
        """
        if not self.token:
            raise AuthenticationError("No API token set.")
        url = f"{self.base}/api/token_info"
        r = self.session.get(url, headers=self._auth_headers())
        data = self._parse_response(r)
        return data

    def refresh_token(self):
        """
        Requests the server to extend your token's expiry.
        Returns the new token and expiry.
        """
        if not self.token:
            raise AuthenticationError("No API token to refresh.")
        url = f"{self.base}/api/refresh_token"
        r = self.session.post(url, headers=self._auth_headers())
        data = self._parse_response(r)
        new_token = data.get("token")
        if not new_token:
            raise APIError("Server did not return a new token.")
        self.token = new_token
        print("API token refreshed; new expiry:", data.get("expires_at"))
        return data

    def kill_token(self):
        """
        Revokes the current API token so it can no longer be used.
        """
        if not self.token:
            raise AuthenticationError("No API token to revoke.")
        url = f"{self.base}/api/revoke_token"
        r = self.session.post(url, headers=self._auth_headers())
        self._parse_response(r)
        print("API token revoked.")
        self.token = None
        self.authenticated = False


    # --------------------
    # Admin Dashboard
    # --------------------

    def get_admin_dashboard(self):
        if self.mode != "admin":
            raise AuthorizationError("Only admin mode can access dashboard.")
        url = f"{self.base}/api/admin_dashboard"
        r = self.session.get(url, headers=self._auth_headers())
        return self._parse_response(r)


    def execute_code(self, code: str):
        if self.gpu_id is None:
            raise APIError("Select a GPU first.")
        url = f"{self.base}/api/execute_code/{self.gpu_id}"
        r = self.session.post(url, headers=self._auth_headers(), json={"code": code})
        data = self._parse_response(r)
        # If JSON, expect an "output" key; otherwise, return raw text
        if isinstance(data, dict) and "output" in data:
            return data["output"]
        return data
    def get_token_info(self):
        """
        Returns a dict with:
          - issued_at: ISO8601 string
          - expires_at: ISO8601 string
        """
        if not self.token:
            raise AuthenticationError("No API token set.")
        url = f"{self.base}/api/token_info"
        data = self._parse_response(self.session.get(url, headers=self._auth_headers()))
        return {
            "created_at": data["created_at"],
            "expires_at": data["expires_at"],
            "revoked": data["revoked"]
        }

    def refresh_token(self):
        """
        Requests the server to extend your token's expiry.
        Returns the new token and expiry.
        """
        if not self.token:
            raise AuthenticationError("No API token to refresh.")
        url = f"{self.base}/api/refresh_token"
        r = self.session.post(url, headers=self._auth_headers())
        data = self._parse_response(r)
        new_token = data.get("token")
        if not new_token:
            raise APIError("Server did not return a new token.")
        self.token = new_token
        print("API token refreshed; new expiry:", data.get("expires_at"))
        return data

    def kill_token(self):
        """
        Revokes the current API token so it can no longer be used.
        """
        if not self.token:
            raise AuthenticationError("No API token to revoke.")
        url = f"{self.base}/api/revoke_token"
        r = self.session.post(url, headers=self._auth_headers())
        self._parse_response(r)
        print("API token revoked.")
        self.token = None
        self.authenticated = False
