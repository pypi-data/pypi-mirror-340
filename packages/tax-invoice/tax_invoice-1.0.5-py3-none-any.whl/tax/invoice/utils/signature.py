import hashlib
import random
import string
import time


def calculate_signature(app_id, app_secret, timestamp, nonce_str, data=None):
    """
    计算签名
    
    Args:
        app_id: 应用ID
        app_secret: 应用密钥
        timestamp: 时间戳
        nonce_str: 随机字符串
        data: 请求数据（可选）
        
    Returns:
        计算得到的签名
    """
    # 构建签名字符串
    sign_str = f"app_id={app_id}&app_secret={app_secret}&timestamp={timestamp}&nonce_str={nonce_str}"
    
    # 如果有数据，将数据添加到签名字符串
    if data and isinstance(data, dict):
        # 按照键排序
        sorted_data = sorted(data.items(), key=lambda x: x[0])
        for key, value in sorted_data:
            if value is not None and value != "":
                sign_str += f"&{key}={value}"
    
    # 计算MD5
    md5 = hashlib.md5()
    md5.update(sign_str.encode('utf-8'))
    return md5.hexdigest().upper()


def generate_random_string(length=16):
    """
    生成指定长度的随机字符串
    
    Args:
        length: 字符串长度，默认16
        
    Returns:
        随机字符串
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def get_timestamp():
    """
    获取当前时间戳（秒）
    
    Returns:
        当前时间戳字符串
    """
    return str(int(time.time()))