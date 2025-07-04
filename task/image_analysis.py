"""
1. 使用zhipuai的glm-4v模型，分析图片内容
2. 输出图片内容、场景分析、情感氛围、用途意图、总结
3. 拥有并发限制，最多同时处理5个图片
4. 平均每次使用2000-2500个token
""" 


import argparse
from zhipuai import ZhipuAI
import requests
from PIL import Image
import matplotlib.pyplot as plt
import io
import base64
import random
def img_show(image_path):
    """
    显示图片
    """
    response = requests.get(image_path)
    img = Image.open(io.BytesIO(response.content))
    plt.figure(figsize=(10, 8))
    plt.imshow(img)
    plt.axis('off')
    plt.title("image")
    plt.show()

def llm_result(image_path):
    """
    使用zhipuai的glm-4v模型，分析图片内容
    """
    # 使用两个api_key，随机选择一个
    api_key = ["02842b16d00a4dfb892144a625eabdee.7xG0Lg0KSROO887e","499da3cc30d54d44b567d74a9654716c.DNkxfiEXQTOhkycd"]
    client = ZhipuAI(api_key=random.choice(api_key))  # 替换为你的智普API密钥
    # 下载图片
    response = requests.get(image_path)
    image_data = response.content

    stream = client.chat.completions.create(
        model="glm-4v",  # 使用智普的GLM-4V模型，用于图像识别
        messages=[
            {
                "role": "system",
                "content": "你是一个专业的图像分析专家。请严格按照以下格式输出分析结果，每个类别单独一行：\n"
                          "【图片内容】\n"
                          "特别详细描述图片中包含的所有内容，包括主体、背景、细节等。\n"
                          "【场景分析】\n"
                          "详细分析图片中的场景类型、环境特征、空间布局等。\n"
                          "【情感氛围】\n"
                          "详细描述图片传达的情感、氛围、意境等。\n"
                          "【用途意图】\n"
                          "详细分析图片可能的用途、目的、创作意图等。\n"
                          "【总结】\n"
                          "用一句话详细总结以上内容。\n"
                          "请确保以上每个类别都有详细的分析，并严格按照上述格式输出。"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "请按照指定格式详细分析这张图片"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64.b64encode(image_data).decode()}"
                        }
                    }
                ]
            }
        ],
        temperature=0.6,
        stream=True  # 启用流式输出
    )
    # 流式输出分析结果
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="", flush=True)
        if chunk.usage is not None:
            print(f"\n本次共使用了{chunk.usage.total_tokens}个token")
            return chunk.usage.total_tokens


if  __name__ == "__main__":
    params = {
        "image_path": "https://p3.ssl.qhimgs1.com/sdr/400__/t01a44596706ed343dd.jpg"
    }
    image_path = params.get('image_path', '')
    llm_result(image_path)


