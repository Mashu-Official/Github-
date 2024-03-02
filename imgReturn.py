import requests
import os
import base64
import re

# 处理路径 生成文件名
def remove(text):
    pattern = r'^img/'
    result = re.sub(pattern, '', text)

    return result
def download_images(remote_image_folder):   # remote_image_folder为仓库中储存img的那个文件夹
    # 设置 GitHub 仓库信息
    owner = ""  # 仓库拥有者(你的账户)
    repo = ""  # 仓库名
    github_access_token = ""  # 你的token

    # 构建 GitHub API 获取仓库中文件列表的 URL
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{remote_image_folder}"

    # 发送 GET 请求到 GitHub API
    headers = {"Authorization": f"token {github_access_token}"}

    response = requests.get(api_url, headers=headers)

    # 存储图片的URL列表
    image_urls = []

    # 检查是否成功获取数据
    if response.status_code == 200:
        # 解析 API 响应的 JSON 数据
        data = response.json()

        # 循环处理每个文件
        for item in data:
            # 获取文件的路径和类型
            file_path = item['path']
            file_type = item['type']
            origin_text =item['path']
            result_text = remove(origin_text)
            print(result_text)

            # 检查是否是文件夹，如果是文件夹则跳过
            if file_type == 'dir':
                continue

            # 构建 GitHub API 获取文件内容的 URL
            file_api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
            file_response = requests.get(file_api_url, headers=headers)

            # 检查是否成功获取文件内容
            if file_response.status_code == 200:
                # 解析文件内容的 JSON 数据
                file_data = file_response.json()
                image_url = f"https://cdn.jsdelivr.net/gh/Mashu-Official/Blog_IMG-Cabin/img/{result_text}"
                image_urls.append(image_url)
            else:
                print(f"Failed to fetch image '{file_path}'. Status code: {file_response.status_code}")
    else:
        print(f"Failed to fetch file list. Status code: {response.status_code}")

    return image_urls

# 设置图片在仓库中的文件夹路径
remote_image_folder = "img"

# 打印获取的图片URL列表
# print("Image URLs:")
# for url in image_urls:
#     print(url)
