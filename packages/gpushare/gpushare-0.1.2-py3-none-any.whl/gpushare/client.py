# gpushare/client.py

import re, requests
from datetime import datetime
from .exceptions import AuthenticationError, AuthorizationError, APIError

class GPUShareClient:
    # ... [init, login, verify_otp, get_api_token, set_api_token unchanged] ...

    def _auth_headers(self):
        if not self.token:
            raise AuthenticationError("No API token; call get_api_token() first.")
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _parse_response(self, r: requests.Response):
        """Raise on HTTP error, then return JSON or text."""
        if not r.ok:
            # Try JSON error message
            try:
                err = r.json().get("error", r.text)
            except Exception:
                err = r.text or f"HTTP {r.status_code}"
            raise APIError(err)

        # OK response: try to parse JSON
        ct = r.headers.get("Content-Type", "")
        if "application/json" in ct:
            return r.json()
        return r.text

    def select_gpu(self, gpu_id: int):
        if not self.authenticated:
            raise AuthenticationError("Authenticate before selecting a GPU.")
        self.gpu_id = gpu_id
        url = f"{self.base}/api/gpu_roles/{gpu_id}"
        r = self.session.get(url, headers=self._auth_headers())
        data = self._parse_response(r)
        self.allowed_roles = data.get("roles", [])
        print("Allowed roles:", self.allowed_roles)

    def list_available_gpus(self):
        url = f"{self.base}/api/available_gpus?mode={self.mode}"
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
