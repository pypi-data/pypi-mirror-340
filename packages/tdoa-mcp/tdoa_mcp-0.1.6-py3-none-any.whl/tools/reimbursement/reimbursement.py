import os
import requests
import json
from src.tools.auth import Auth
class Reimbursement:
    def __init__(self):
        self.base_url = os.getenv("OA_URL", "https://oa.myoa888.com")
    
    def reimburse(self, flow_id: str, invoice_ids: str) -> dict:
        """报销
        
        Args:
            flow_id: 报销流程ID
            invoice_id: 发票ID
            
        Returns:
            dict: 包含成功状态和消息的字典，例如：{"success": True, "message": "报销成功", "url": "..."}
        """
        auth = Auth()
        phpsessid = auth.login()
        
        url = f"{self.base_url}/inc/ocr/api/toRun.php"
        
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': self.base_url,
            'referer': f'{self.base_url}/general/invoice/my.php',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        
        # 构建请求数据，根据curl命令中的data-raw部分
        data = {
            'billId': invoice_ids,
            'flowId': flow_id,
            'flowPrcs': '1'
        }

        cookies = { 
            'PHPSESSID': phpsessid
        }
        
        try:
            response = requests.post(url, headers=headers, data=data, cookies=cookies)
            response.raise_for_status()
            
            # 解析返回的JSON结果
            result = json.loads(response.text)
            
            if result.get("status") == "ok":
                return {
                    "success": True,
                    "message": "报销提交成功",
                    "url": result.get("url", ""),
                    "raw_response": result
                }
            else:
                return {
                    "success": False,
                    "message": "报销提交失败",
                    "raw_response": result
                }
                
        except json.JSONDecodeError:
            return {
                "success": False,
                "message": "解析响应数据失败，非有效JSON格式",
                "raw_response": response.text
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"报销请求失败: {str(e)}",
                "raw_response": None
            }
