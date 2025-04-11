# xjy_rsa_util

RSA签名工具包，用于生成RSA签名和构建请求体。

## 安装

```bash
pip install xjy_rsa_util
```

## 使用示例

```python
from xjy_rsa_util import rsa_util

# 你的RSA私钥
private_key = """-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----"""

# 构建请求体
request_body = rsa_util.build_request_body(
    data={"key": "value"},
    private_key_pem=private_key,
    merchant_id="your_merchant_id"
)

print(request_body)
```

## 功能

- `sign_message`: 使用RSA私钥对消息进行签名
- `build_request_body`: 构建包含签名的请求体

## 依赖

- cryptography>=3.4