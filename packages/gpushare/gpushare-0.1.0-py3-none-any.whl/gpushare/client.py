import re, requests
from datetime import datetime
from .exceptions import AuthenticationError, AuthorizationError, APIError

class GPUShareClient:
    def __init__(self, base_url: str):
        self.base = base_url.rstrip("/")
        self.session = requests.Session()
        self.token = None
        self.authenticated = False
        self.gpu_id = None
        self.mode = "user"
        self.allowed_roles = []

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
        print("OTP sent to your email.")
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
            raise APIError("API token not found")
        self.token = m.group(1)
        print("API token acquired.")

    def set_api_token(self, token: str):
        self.token = token
        self.authenticated = True
        print("API token set; you are now authenticated.")

    def _auth_headers(self):
        if not self.token:
            raise AuthenticationError("No API token; call get_api_token() first.")
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def select_gpu(self, gpu_id: int):
        if not self.authenticated:
            raise AuthenticationError("Authenticate before selecting a GPU.")
        self.gpu_id = gpu_id
        url = f"{self.base}/api/gpu_roles/{gpu_id}"
        r = self.session.get(url, headers=self._auth_headers())
        if r.status_code != 200:
            raise APIError(r.text)
        self.allowed_roles = r.json().get("roles", [])
        print("Allowed roles:", self.allowed_roles)

    def switch_mode(self, mode: str):
        if mode not in self.allowed_roles:
            raise AuthorizationError(f"You do not have role '{mode}' for GPU {self.gpu_id}")
        self.mode = mode
        print("Switched mode to:", mode)

    def list_available_gpus(self):
        url = f"{self.base}/api/available_gpus?mode={self.mode}"
        r = self.session.get(url, headers=self._auth_headers())
        if r.status_code != 200:
            raise APIError(r.text)
        return r.json()

    def request_access(self, code: str = None):
        if self.gpu_id is None:
            raise APIError("Select a GPU first.")
        url = f"{self.base}/request_gpu/{self.gpu_id}"
        payload = {}
        if code:
            payload["code"] = code
        r = self.session.post(url, headers=self._auth_headers(), json=payload)
        if r.status_code != 200:
            raise APIError(r.text)
        return r.json()

    def approve_request(self, req_id: int):
        if self.mode not in ("owner","admin","moderator"):
            raise AuthorizationError("Cannot approve in current mode.")
        url = f"{self.base}/approve_request/{req_id}"
        r = self.session.post(url, headers=self._auth_headers())
        if r.status_code != 200:
            raise APIError(r.text)

    def deny_request(self, req_id: int):
        if self.mode not in ("owner","admin","moderator"):
            raise AuthorizationError("Cannot deny in current mode.")
        url = f"{self.base}/deny_request/{req_id}"
        r = self.session.post(url, headers=self._auth_headers())
        if r.status_code != 200:
            raise APIError(r.text)

    def revoke_access(self, request_id: int):
        if self.mode not in ("owner","admin","user"):
            raise AuthorizationError("Cannot revoke in current mode.")
        url = f"{self.base}/revoke_access/{request_id}"
        r = self.session.post(url, headers=self._auth_headers())
        if r.status_code != 200:
            raise APIError(r.text)

    def execute_code(self, code: str):
        if self.gpu_id is None:
            raise APIError("Select a GPU first.")
        url = f"{self.base}/api/execute_code/{self.gpu_id}"
        r = self.session.post(url, headers=self._auth_headers(), json={"code": code})
        if r.status_code != 200:
            raise APIError(r.text)
        return r.json().get("output")
