from typing import List, Dict, Optional, Any
from src.tools.auth import Auth
import os
import requests
import json
from datetime import datetime

class Invoice:
    def __init__(self):
        self.base_url = os.getenv("OA_URL", "https://oa.myoa888.com")
    
    def get_invoice_list(self, filters: Optional[Dict[str, Any]] = None) -> List[dict]:
        """
        获取发票列表
        
        Args:
            filters (dict, optional): 过滤条件，例如日期范围、金额范围等
                - keyword (str): 搜索关键词
                - state (str): 状态，默认为'all'
                - page_size (int): 每页数量，默认为40
                - page_no (int): 页码，默认为1
                - fetch_all (bool): 是否获取所有数据，默认为False
            
        Returns:
            List[dict]: 包含发票列表的数据，如果fetch_all为True，则返回所有数据
        """
        filters = filters or {}
        
        try:
            # 获取认证信息
            auth = Auth()
            phpsessid = auth.login()
            
            if not phpsessid:
                print("登录失败，无法获取PHPSESSID")
                return []
            
            # 设置请求参数
            state = filters.get('state', 'all')
            page_size = filters.get('page_size', 40)
            keyword = filters.get('keyword', '')
            page_no = filters.get('page_no', 1)
            fetch_all = filters.get('fetch_all', False)
            
            # 构建URL
            url = f"{self.base_url}/general/appbuilder/web/invoice/invoice/invoicelist"
            
            # 设置请求头
            headers = self._get_headers()
            
            # 设置cookies
            cookies = {
                'PHPSESSID': phpsessid
            }
            
            all_data = []
            current_page = page_no
            
            while True:
                # 构建当前页的请求参数
                params = {
                    'state': state,
                    'pageSize': page_size,
                    'keyword': keyword,
                    'pageNo': current_page,
                    'flowId': '',
                    'prcsId': '',
                    'flowPrcs': '',
                    'runId': ''
                }
                
                # 发送请求
                response = requests.get(
                    url,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    timeout=30  # 添加超时设置
                )
                
                # 检查响应状态
                response.raise_for_status()  # 如果状态码不是200，将引发异常
                
                result = response.json()
                
                # 检查API返回的数据
                if not result.get('data'):
                    break
                    
                # 将新数据添加到现有数据中
                if isinstance(result['data'], list):
                    # 如果data是列表，直接遍历添加
                    for item in result['data']:
                        all_data.append({
                            'id': item.get('id', ''),
                            'InvoiceDate': item.get('InvoiceDate', ''),
                            'TotalAmount': item.get('TotalAmount', ''),
                            'TotalTax': item.get('TotalTax', ''),
                            'SellerName': item.get('SellerName', '')
                        })
                else:
                    # 如果data是字典，按原来方式处理
                    all_data.append({
                        'id': result['data'].get('id', ''),
                        'InvoiceDate': result['data'].get('InvoiceDate', ''),
                        'TotalAmount': result['data'].get('TotalAmount', ''),
                        'TotalTax': result['data'].get('TotalTax', ''),
                        'SellerName': result['data'].get('SellerName', '')
                    })
                
                # 如果不需要获取所有数据或者没有更多数据，则退出循环
                if not fetch_all or (isinstance(result['data'], list) and len(result['data']) == 0):
                    break
                    
                current_page += 1

            return all_data
                
        except requests.exceptions.RequestException as e:
            return []
        except json.JSONDecodeError as e:
            return []
        except Exception as e:
            return []
    
    def upload_invoice(self, file_path: str) -> str:
        """
        上传发票
        
        Args:
            file_path (str): 发票文件路径
            
        Returns:
            str: 发票ID
        """
        try:
            # 获取认证信息
            auth = Auth()
            phpsessid = auth.login()
            
            if not phpsessid:
                print("登录失败，无法获取PHPSESSID")
                return False
            
            # 设置请求头
            headers = {
                'accept': '*/*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'referer': f'{self.base_url}/general/appbuilder/web/invoice/invoice/upload',
                'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                # 注意：不要包含Content-Type，因为requests会自动添加正确的Content-Type和boundary
            }
            
            # 设置cookies
            cookies = {
                'PHPSESSID': phpsessid
            }
            
            # 构建URL
            url = f"{self.base_url}/general/appbuilder/web/invoice/invoice/upload"
            
            # 构建文件名
            file_name = os.path.basename(file_path)
            
            # 准备文件
            with open(file_path, 'rb') as f:
                files = {
                    'id': (None, 'WU_FILE_0'),
                    'name': (None, file_name),
                    'type': (None, self._get_file_type(file_name)),
                    'lastModifiedDate': (None, self._get_current_time()),
                    'size': (None, str(os.path.getsize(file_path))),
                    'file': (file_name, f, self._get_file_type(file_name))
                }
                
                # 发送请求
                response = requests.post(
                    url,
                    headers=headers,
                    cookies=cookies,
                    files=files,
                    timeout=30
                )
                
                # 检查响应状态
                response.raise_for_status()
                
                # 解析响应
                result = response.json()
                
                # 检查上传是否成功
                if result.get('status') == 1 or result.get('code') == 200:
                    url = result.get('url', '')
                    id = url.split('id=')[-1] if 'id=' in url else ''
                    return id
                else:
                    print(f"上传失败：{result.get('msg', '未知错误')}")
                    return False
                
        except requests.exceptions.RequestException as e:
            print(f"请求异常：{str(e)}")
            return False
        except json.JSONDecodeError as e:
            print(f"JSON解析错误：{str(e)}")
            return False
        except Exception as e:
            print(f"上传发票时发生错误：{str(e)}")
            return False
            
    def _get_file_type(self, file_name: str) -> str:
        """根据文件名获取MIME类型"""
        extension = os.path.splitext(file_name)[1].lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.pdf': 'application/pdf',
            '.txt': 'text/plain',
            '.csv': 'text/csv',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.xls': 'application/vnd.ms-excel',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }
        return mime_types.get(extension, 'application/octet-stream')
        
    def _get_current_time(self) -> str:
        """获取当前时间，格式化为通达OA需要的格式"""
        current_time = datetime.now()
        # 格式：Fri Mar 07 2025 14:17:22 GMT+0800 (中国标准时间)
        weekday_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
        month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 
                   7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        
        weekday = weekday_map[current_time.weekday()]
        month = month_map[current_time.month]
        
        return f"{weekday} {month} {current_time.day} {current_time.year} {current_time.hour}:{current_time.minute}:{current_time.second} GMT+0800 (中国标准时间)"

    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': f'{self.base_url}/general/invoice/my.php',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
    
    def upload_invoices_from_directory(self, directory_path: str) -> Dict[str, bool]:
        """
        上传指定目录下的所有PDF文件
        
        Args:
            directory_path (str): 包含发票PDF文件的目录路径
            
        Returns:
            Dict[str, bool]: 文件名和上传结果的字典
        """
        results = {}
        
        try:
            # 检查目录是否存在
            if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
                print(f"目录不存在或不是有效目录: {directory_path}")
                return results
                
            # 获取目录中的所有PDF文件
            pdf_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.pdf')]
            
            if not pdf_files:
                print(f"目录中没有PDF文件: {directory_path}")
                return results
                
            print(f"找到 {len(pdf_files)} 个PDF文件待上传")
            
            # 上传每个PDF文件
            for pdf_file in pdf_files:
                file_path = os.path.join(directory_path, pdf_file)
                print(f"正在上传: {pdf_file}")
                
                # 调用单文件上传方法
                invoice_id = self.upload_invoice(file_path)
                results[pdf_file] = invoice_id
                
                if invoice_id:
                    print(f"上传成功: {pdf_file}")
                else:
                    print(f"上传失败: {pdf_file}")
                    
            return results
            
        except Exception as e:
            print(f"上传目录中的发票时发生错误: {str(e)}")
            return results
