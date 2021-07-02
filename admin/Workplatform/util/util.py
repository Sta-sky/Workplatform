# -*- coding: utf-8 -*-
import base64
import json
import os
import jwt
import time
import hashlib

from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5

from django.core.paginator import Paginator
from Workplatform import settings
from util.redis_connect import Redis


def encode_md5(passwd):
    """ 加密 """
    try:
        m = hashlib.md5()
        m.update(passwd.encode())
        password = m.hexdigest()
        return password
    except Exception:
        return False


def decode_passwd(passwd):
    try:
        path = os.path.abspath('') + '/config/rsa.key'
        with open(path) as fp:
            passwd_ = decrypt_rsa(fp, passwd)
            return passwd_
    except Exception as e:
        return False


def judge_dic_is_value(param_dic):
    for key in param_dic.values():
        if key is None:
            return False
    return True


# 定义生成token令牌的函数
def make_token(username, exp=3600 * 24):
    key = settings.JWT_TOKEN_KEY
    now = time.time()
    payload = {'username': username, 'exp': exp + now}
    return jwt.encode(payload=payload, key=key, algorithm='HS256')


def judge_data_complate(body_data):
    if not body_data:
        return False
    data = json.loads(body_data)
    json_data = judge_dic_is_value(data)
    if not json_data:
        return False
    return data


def upload_img_save(img_data, file_path):
    try:
        with open(file_path, 'wb') as fp:
            fp.write(img_data)
        return True
    except Exception as e:
        return False


def generate_base64(keywords):
    """
    base64 编码 base64穿入的参数只能是字节串  要用encode()参数进行转换
    """
    try:
        res = base64.b64encode(keywords.encode()).decode()
        return res
    except Exception:
        raise


def handle_search_content(keyword, content):
    res = content.find(keyword)
    content_info = content[res: res + 50]
    return content_info


def get_total_page(objs, max_page):
    try:
        pagetor = Paginator(objs, max_page)
        total_page = pagetor.count
        return total_page
    except Exception as e:
        raise


def get_page_info_list(query_set_objs, max_page, page):
    try:
        pagetor = Paginator(query_set_objs, max_page)
        page_info_list = pagetor.page(page)
        return page_info_list
    except Exception as e:
        raise


def user_pub_add_salt(txet, user_secrete):
    """
        公钥加密
    :param txet: 公钥文件的read()后的io对象
    :param user_secrete: 自定义的salt
    :return: 公钥跟salt加密后的秘钥对
    """
    try:
        public_key = txet.read()
        rsa_key_obj = RSA.importKey(public_key)
        passwd_obj = PKCS1_v1_5.new(rsa_key_obj)
        passwd_text = base64.b64encode(
            passwd_obj.encrypt(user_secrete.encode()))
        return passwd_text
    except Exception as e:
        print(f'公钥生成秘钥对失败，失败原因为{e}')
        raise


def decrypt_rsa(txet, Key_Pair):
    """
    私钥解密
    :param txet: 私钥文件read()后的io对象
    :param Key_Pair:  生成的秘钥对
    :return: 使用私钥解密后的salt
    """
    try:
        rsa_key_data = txet.read()
        # 创建私钥对象
        rsa_key_obj = RSA.importKey(rsa_key_data)
        passwd_rsa_data = PKCS1_v1_5.new(rsa_key_obj)
        random_generate = Random.new().read
        passwd_rsa_text = passwd_rsa_data.decrypt(base64.b64decode(Key_Pair), random_generate)
        return passwd_rsa_text.decode()
    except Exception as e:
        raise


def del_user_info_cache():
    redis_obj = Redis('user')
    redis_obj.redis_delete('user_info')
    redis_obj.redis_delete('all_user_info')


def save_imgage(save_path, img_obj):
    try:
        file_data = img_obj.file.read()
        with open(save_path, 'wb') as fp:
            fp.write(file_data)
        print('图片保存完成')
        return True
    except Exception as e:
        return False


import os
import zipfile


def win_zip_tool(dirname, zipfilename):
	filelist = []
	if os.path.isfile(dirname):
		filelist.append(dirname)
	else:
		for root, dirs, files in os.walk(dirname):
			for name in files:
				filelist.append(os.path.join(root, name))
	zf = zipfile.ZipFile(zipfilename, "w", zipfile.ZIP_STORED,allowZip64=True)
	for tar in filelist:
		arcname = tar[len(dirname):]
		zf.write(tar, arcname)
	zf.close()
