from typing import Union, Dict, Any

import requests
from django.core.files.uploadedfile import UploadedFile

class ImageUploadUtil:
    # 上传API地址和API Key常量
    UPLOAD_URL = "https://www.picgo.net/api/1/upload"
    API_KEY =PICGO_SECRET_KEY

    @classmethod
    def upload_image(cls, file: UploadedFile, filename: str, post_type:str) -> Union[
        dict[str, Union[str, Any]], dict[str, Union[str, Any]], dict[str, str], dict[str, str]]:
        """
        文件上传方法
        :param file: Django上传的文件对象
        :param filename: 文件名
        :return: 上传结果（图片URL或错误信息）
        """
        try:
            # 构建请求的文件和其他数据
            files = {
                'source': file
            }

            # 构建请求数据
            data = {
                'key': cls.API_KEY,
                'album_id': 'SRFNu' if post_type == 'post' else 'SRPu4',
                'title': filename,
                'format': 'json'
            }

            # 发送文件上传请求
            response = requests.post(
                cls.UPLOAD_URL,
                files=files,
                data=data,
                timeout=(10, 10)  # 连接超时和读取超时，单位为秒
            )

            # 检查响应
            response_data = response.json()

            if response.status_code == 200 and 'image' in response_data:
                return {
                    'status': 'success',
                    'url': response_data['image']['url'],
                    'delete_url': response_data['image']['delete_url'],
                    'width': response_data['image']['width'],
                    'height': response_data['image']['height']
                }

            # 服务器返回的错误信息
            if 'error' in response_data:
                return {
                    'status': 'error',
                    'message': response_data['error'].get('message', '未知错误')
                }

            # 未知的响应格式
            return {
                'status': 'error',
                'message': '无法解析服务器响应'
            }

        except requests.RequestException as e:
            return {
                'status': 'error',
                'message': f'网络请求失败: {str(e)}'
            }

    @classmethod
    def delete_image(cls,delete_url:str)->bool:
        """
        删除图片
        :param deletUrl: 图片删除URL
        :return: 删除结果
        """
        try:
            response = requests.delete(
                delete_url,
                timeout=(10, 10)  # 连接超时和读取超时，单位为秒
            )
            return response.status_code == 200
        except requests.RequestException:
            return False