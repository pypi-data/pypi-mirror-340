import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
import base64
import time

'''
根据私钥和字符串生成签名

author: XieChen
data: 2025-04-12
'''
def sign_message(private_key_pem: str, message: bytes) -> str:
    private_key = load_pem_private_key(
        private_key_pem.encode(),
        password=None,
        backend=default_backend()
    )
    # 确保是RSA密钥类型
    assert isinstance(private_key, rsa.RSAPrivateKey)
    signature = private_key.sign(
        message,
        padding.PKCS1v15(),
        hashes.SHA1()
    )
    return base64.b64encode(signature).decode()

'''
根据请求数据、私钥、商户号生成请求体

author: XieChen
data: 2025-04-12
'''
def build_request_body(data, private_key_pem: str, merchant_id: str, timestamp: int = (int(time.time() * 1000))):
    # 拼接初始化请求参数
    params = {
        "merchantId": merchant_id,
        "timeStamp": timestamp,
        "params": data
    }

    # 生成签名
    params_json_str = json.dumps(params, ensure_ascii=False).replace(" ", "") # ensure_ascii=False表示不转换为ascii码，replace(" ", "")表示去掉空格
    signature = sign_message(private_key_pem, params_json_str.encode()) # 生成签名

    # 将签名加入请求参数
    params["sign"] = signature

    # 将请求参数转字符串去除空格后转json对象返回
    return json.loads(json.dumps(params, ensure_ascii=False).replace(" ", ""))

'''
下划线转驼峰命名

author: XieChen
data: 2025-04-12
'''
def underscore_to_camel(name: str) -> str:
    """下划线转驼峰命名"""
    parts = name.split('_')
    return parts[0] + ''.join(x.capitalize() for x in parts[1:])