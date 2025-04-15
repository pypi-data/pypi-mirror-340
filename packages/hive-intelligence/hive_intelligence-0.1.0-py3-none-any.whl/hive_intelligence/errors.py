
class HiveSearchAPIError(Exception):
    def __init__(self, status_code: int, reason: str, message: str):
        self.status_code = status_code
        self.reason = reason
        self.message = message
        super().__init__(f"HiveSearch API Error: {status_code} {reason} - {message}")