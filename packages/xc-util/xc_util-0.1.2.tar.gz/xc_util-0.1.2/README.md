# XJY RSA Util

一个简单的RSA加密工具库，提供签名和构建请求体功能。

## 安装

```bash
pip install xc-util
```

## 使用方法

### 签名消息

```python
from rsa_util import sign_message

# 私钥（PEM格式）
private_key_pem = """-----BEGIN PRIVATE KEY-----
您的私钥内容
-----END PRIVATE KEY-----"""

# 要签名的消息
message = "Hello, World!".encode()

# 生成签名
signature = sign_message(private_key_pem, message)
print(signature)
```

### 构建请求体

```python
from rsa_util import build_request_body

# 私钥（PEM格式）
private_key_pem = """-----BEGIN PRIVATE KEY-----
您的私钥内容
-----END PRIVATE KEY-----"""

# 商户ID
merchant_id = "your_merchant_id"

# 请求数据
data = {"key": "value"}

# 构建请求体
request_body = build_request_body(data, private_key_pem, merchant_id)
print(request_body)
```

## 功能

- `sign_message(private_key_pem: str, message: bytes) -> str`: 使用RSA私钥对消息进行签名
- `build_request_body(data, private_key_pem: str, merchant_id: str, timestamp: int) -> dict`: 构建包含签名的请求体

## 依赖

- cryptography