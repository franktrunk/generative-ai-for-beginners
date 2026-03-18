import os
import requests
import dashscope
from dashscope import MultiModalConversation
from PIL import Image
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置 API Key（推荐方式）
dashscope.api_key = os.getenv("QWEN_API_KEY")

# 接口地址
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# prompt
messages = [
    {
        "role": "user",
        "content": [
            {"text": "一只兔子骑在马上，梦幻风格"}
        ]
    }
]

# 调用模型
resp = MultiModalConversation.call(
    model="qwen-image-2.0-pro",
    messages=messages,
    result_format='message',
    stream=False,
    watermark=False,
    size='1024*1024'
)

if resp.status_code == 200:
    content = resp.output.choices[0].message.content

    for item in content:
        if "image" in item:
            image_url = item["image"]
            print("🖼️ 图片URL:", image_url)

            try:
                # 下载图片
                img_resp = requests.get(image_url, timeout=30)
                img_resp.raise_for_status()

                image_path = "output.png"

                with open(image_path, "wb") as f:
                    f.write(img_resp.content)

                print("✅ 图片已保存:", image_path)

                # 打开图片
                img = Image.open(image_path)
                img.show()

            except requests.exceptions.RequestException as e:
                print("❌ 下载失败:", e)

else:
    print(f"HTTP返回码：{resp.status_code}")
    print(f"错误码：{resp.code}")
    print(f"错误信息：{resp.message}")