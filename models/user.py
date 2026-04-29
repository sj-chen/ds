from dataclasses import dataclass
from typing import Optional


@dataclass
class TestLoginUser:
    name: str
    username: str
    password: str
    expect_code: int
    expect_msg: str

@dataclass
class TestInfo:
    name: str
    username: str
    password: str
    expect_code: int
    expect_msg: str

@dataclass
class TestRegister:
    name: str
    username: str
    password: str
    telephone: str
    expect_code: int
    expect_msg: str

@dataclass
class TestUpdatePassword:
    name: str
    telephone: str
    password: str
    expect_code: str
    expect_msg: str
    authCode: Optional[str] = None
