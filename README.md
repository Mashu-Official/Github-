<h2>Github做博客图床</h2>
通过GIthub api实现上传图片 同时可获取图片的URL（URl默认使用CDN）

代码如下
```python
import requests
import base64
import hashlib

def upload_image_to_github(image_path_temp):
    owner = ""  #仓库拥有者(你的账户)
    repo = ""  #仓库名
    github_access_token = "" #你的token
    branch = "main" #分支
    # image_path = "你要上传的图片的路径"

    # 构建API URL
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{image_path_temp}"

    # 读取图片文件内容
    with open(image_path_temp, "rb") as file:
        image_content = file.read()

    # 计算图片内容的SHA散列值
    sha256_hash = hashlib.sha256()
    sha256_hash.update(image_content)
    file_sha = sha256_hash.hexdigest()

    # 获取目标文件的当前SHA散列值（如果文件存在）
    response_existing_file = requests.get(url, headers={"Authorization": f"token {github_access_token}"})
    existing_file = response_existing_file.json()
    current_sha = existing_file.get("sha", "")

    # 构建请求头
    headers = {
        "Authorization": f"token {github_access_token}"
    }

    # 构建请求体
    data = {
        "message": "Update image",
        "content": base64.b64encode(image_content).decode("utf-8"),
        "branch": branch,
        "sha": current_sha  # 提供当前文件的SHA散列值
    }

    # 发送请求
    response = requests.put(url, json=data, headers=headers)
    print(response.json())
    # 返回结果
    return response.json()

# 使用示例
result = upload_image_to_github()
```



```python
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
    owner = "Mashu-Official"
    repo = "Blog_IMG-Cabin"
    github_access_token = "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"

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

                # url的拼接
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

```

