# -*- coding: utf-8 -*-
"""
@File: xhttp
@Author: ltw
@Time: 2022/10/14
"""
import hashlib
import logging
import time
import urllib.parse

import requests
import ujson as json


def http_request(
    url, data, is_https=False, method="post", is_json_type=False, add_headers=None
):
    try:
        headers = {}
        if is_json_type is True:
            content_type = "application/json; charset=UTF-8"
        else:
            content_type = "application/x-www-form-urlencoded; charset=UTF-8"
        if is_https is True:
            url = f"https://{url}"
        else:
            url = f"http://{url}"
        headers["Content-Type"] = content_type
        if add_headers:
            headers.update(add_headers)

        post_data = set_params(data) if is_json_type is False else json.dumps(data)
        if method == "post":
            result = requests.post(url, data=post_data, headers=headers, verify=False)
        else:
            result = requests.get(url + "?" + post_data, headers=headers, verify=False)
        content = result.content
        if not content:
            return None
        return content
    except Exception as e:
        logging.error("http_request  Error Exception: %s", e)
        return None


def md5(md5_str):
    """
    md5加密[center接口定]
    :param md5_str:
    :return:
    """
    sign_str = hashlib.md5()
    sign_str.update(md5_str.encode("utf-8"))
    return sign_str.hexdigest()


def set_params(params=None):
    """
    生成参数
    """
    if not isinstance(params, dict):
        raise TypeError("You must pass in a dictionary!")
    params_list = []
    for k, _v in params.items():
        if isinstance(_v, list) and _v:
            if isinstance(_v[0], dict):
                params_list.append((k, json.dumps(_v)))
            else:
                params_list.extend([(k, x) for x in _v])
        elif isinstance(_v, dict):
            params_list.append((k, json.dumps(_v)))
        else:
            params_list.append((k, _v))
    return urllib.parse.urlencode(params_list)


def http_push_server(url, data, server_api_key):
    """
    单服推送
    :param url:
    :param data:
    :param server_api_key:
    :return:
    """
    if not url:
        logging.error(
            f"Error http_push_server url: {url}  data: {json.dumps(data)}"
        )
        return None

    _t = int(time.time())
    values = {"time": _t, "params": json.dumps(data)}
    keys = values.keys()
    keys = sorted(keys)
    params = []
    for key in keys:
        params.append(f"{key}={values[key]}")
    params = "&".join(params)
    timestamp = str(_t + (_t % 38975))
    _tmp = md5(f"{params}{server_api_key}")
    sign = md5(f"{timestamp}{_tmp}")

    post_data = {"time": _t, "params": data, "sign": sign}

    post_data_log = json.dumps(post_data, ensure_ascii=False)
    logging.info(f"http_push_server url:{url} post_data: {post_data_log}")

    result = http_request(url, post_data, False, "post")
    logging.info(f"http_push_server url:{url} res: {result}")
    return result


def make_post_data(ex_params, api_key):
    """
    生成post_data
    """
    _t = int(time.time())
    values = {"time": _t, "params": json.dumps(ex_params)}
    keys = values.keys()
    keys = sorted(keys)
    params = []
    for key in keys:
        params.append(f"{key}={values[key]}")
    params = "&".join(params)
    timestamp = str(_t + (_t % 38975))
    _tmp = md5(f"{params}{api_key}")
    sign = md5(f"{timestamp}{_tmp}")

    post_data = {"time": _t, "params": ex_params, "sign": sign}
    post_data = set_params(post_data)
    return post_data
