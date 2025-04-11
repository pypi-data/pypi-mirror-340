from dataclasses import dataclass


@dataclass
class AppContext:
    account_id: str
    api_token: str
