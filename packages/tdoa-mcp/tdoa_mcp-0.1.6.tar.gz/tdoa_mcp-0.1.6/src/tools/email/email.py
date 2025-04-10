import os
import re
import random
import string
import markdown
import requests
from src.tools.auth import Auth
from src.utils.logger import (
    info,
)

class Email(Auth):
    def __init__(self):
        super().__init__()

    def write(self, subject: str, content: str) -> str:
        info(f"写入邮件: {subject}", console_output=False)

        phpsessid = self.login()
        if not phpsessid:
            return ""
        
        csrf_token = self.get_csrftoken(phpsessid)
        if not csrf_token:
            return ""

        content = markdown.markdown(content)

        boundary_value = self._generate_boundary()

        url = self.base_url + "/general/email/new/submit.php"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "content-type": f"multipart/form-data; boundary={boundary_value}",
            "proxy-connection": "keep-alive",
            "upgrade-insecure-requests": "1",
            "cookie": f"PHPSESSID={phpsessid}",
            "Referer": f"{self.base_url}/general/email/new/",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
        body = f"""
--{boundary_value}\r\nContent-Disposition: form-data; name=\"SECRET_LEVEL\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"TO_ID\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"TO_NAME\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"COPY_TO_ID\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"COPY_TO_NAME\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"SECRET_TO_ID\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"SECRET_TO_NAME\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"TO_WEBMAIL\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"COPY_TO_WEBMAIL\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"SECRET_TO_WEBMAIL\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"SUBJECT\"\r\n\r\n{subject}\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"TD_HTML_EDITOR_CONTENT\"\r\n\r\n{content}\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"ATTACHMENT_0\"; filename=\"\"\r\nContent-Type: application/octet-stream\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"ATTACH_NAME\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"ATTACH_DIR\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"DIR_ID\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"DISK_ID\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"ATTACHMENT_1000\"; filename=\"\"\r\nContent-Type: application/octet-stream\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"ATTACH_NAME_Multiple\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"ATTACH_DIR_Multiple\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"DISK_ID_Multiple\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"SMS_REMIND\"\r\n\r\non\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"CONTENT_NAME\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"EMAIL_ID\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"BODY_ID\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"ISUPDATE\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"IMPORTANT\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"ATTACHMENT_ID_OLD\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"ATTACHMENT_NAME_OLD\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"SEND_FLAG\"\r\n\r\n0\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"OP\"\r\n\r\n1\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"BTN_CLOSE\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"REPLAY\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"FW\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"BOX_ID\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"FIELD\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"ASC_DESC\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"IS_R\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"IS_F\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"RECENT_LINKMAN\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"FROM_FLAG\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"COPY_TIME\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"FROM\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"ACTION_TYPE\"\r\n\r\n\r\n--{boundary_value}\r\nContent-Disposition: form-data; name=\"csrf_token\"\r\n\r\n{csrf_token}\r\n--{boundary_value}--\r\n
"""

        response = requests.post(url, headers=headers, data=body)
        if response.status_code == 200:
            # 匹配 body_id 的值
            match = re.search(r'body_id=(\d+)', response.text, re.IGNORECASE)
            if match:
                body_id = match.group(1)
                return body_id
            else:
                return ""
        else:
            return ""
        
    def _generate_boundary(self) -> str:
        # 使用随机生成的字符串作为boundary的一部分
        rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        # 拼接成完整的boundary值
        boundary = "----WebKitFormBoundary" + rand_str
        return boundary
