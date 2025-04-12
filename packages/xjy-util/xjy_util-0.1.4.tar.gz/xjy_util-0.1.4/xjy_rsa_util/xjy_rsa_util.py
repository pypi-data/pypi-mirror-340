import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
import base64
import time

'''
生成RSA公私钥对

author: XieChen
data: 2025-04-12
'''
def generate_rsa_keys_pcks8(key_size=1024):
    # 生成私钥
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    
    # 序列化私钥
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # 从私钥生成公钥
    public_key = private_key.public_key()
    
    # 序列化公钥
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_pem.decode(), public_pem.decode()


'''
根据私钥和字符串生成签名

author: XieChen
data: 2025-04-12
'''
def sign_message_by_private_key(private_key_pem: str, message: bytes) -> str:
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
    signature = sign_message_by_private_key(private_key_pem, params_json_str.encode()) # 生成签名

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
    parts = name.split('_')
    return parts[0] + ''.join(x.capitalize() for x in parts[1:])

'''
校验签名

author: XieChen
data: 2025-04-12
'''
def verify_signature_by_public_key(public_key_pem: str, message: bytes, signature: str) -> bool:
    # 加载公钥
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode(),
        backend=default_backend()
    )
    
    # 确保是RSA公钥
    assert isinstance(public_key, rsa.RSAPublicKey)
    
    # 解码签名
    sig_bytes = base64.b64decode(signature)
    
    try:
        # 验证签名(PKCS1v15填充 + SHA1哈希)
        public_key.verify(
            sig_bytes,
            message,
            padding.PKCS1v15(),
            hashes.SHA1()
        )
        return True
    except Exception as e:
        print(f"签名验证失败: {str(e)}")
        return False