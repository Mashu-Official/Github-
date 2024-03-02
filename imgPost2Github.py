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

