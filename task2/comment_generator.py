import io
import os
import sys
from task4.common.big_model_interface import *
# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from task2.image_analysis import llm_result

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

def read_input_text(input_text_file):
    try:
        with open(input_text_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取输入文案失败: {e}")
        return None



def capture_stdout(func, *args, **kwargs):
    """
    # 捕获函数输出
    # 捕获函数输出，并返回输出内容
    # 参数：
    # func：要捕获输出的函数
    # *args：函数参数
    # **kwargs：函数关键字参数
    # 返回：函数输出内容
    """
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    
    try:
        token_num = func(*args, **kwargs)
        output = new_stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    
    return output, token_num

def save_comment(comment, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(comment)
    except Exception as e:
        print(f"保存评论失败: {e}")

def main():
    # 获取用户输入
    image_path = input("请输入图片URL：")
    input_text = input("请输入文案：")
    output_file = "generated_comment.txt"      # 输出评论文件

    if not input_text or not image_path:
        print("无法继续执行：缺少必要的输入内容")
        return
    # 获取图片分析结果
    image_analysis, img_token = capture_stdout(llm_result, image_path)
    # 构建提示词
    system_prompt = """你是一个专业的社交媒体评论生成专家。你的任务是根据图片分析结果和输入文案，生成一条大众化的评论。
    要求：
    1. 评论必须使用与输入文案完全相同的语言（如中文、英文、日文等）
    2. 评论的语言风格必须与输入文案保持一致（包括用词、语气、表达方式等）
    3. 如果输入文案是正式语言，评论也要用正式语言
    4. 如果输入文案是网络用语，评论也要用网络用语
    5. 如果输入文案是方言，评论也要用相同的方言
    6. 评论长度控制在10-20字之间
    7. 结合图片分析中的关键信息
    8. 保持输入文案的情感基调
    9. 添加适当的表情
    请直接输出评论内容，不需要其他解释。"""

    human_prompt = """图片分析结果：
    {image_analysis}

    输入内容：
    {input_text}

    请生成一条与输入文案语言和风格完全一致大众化的评论。"""

    # 创建提示模板
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_prompt),
        HumanMessagePromptTemplate.from_template(human_prompt)
    ])
    messages = prompt.format_messages(
        image_analysis=image_analysis,
        input_text=input_text
    )
    # 生成评论
    comment, comment_token = generate_result(messages)
    # 计算总token数量
    total_token = img_token + comment_token
    print(f"本次共使用了{total_token}个token")
    # save_comment(comment, output_file)

if __name__ == "__main__":
    main() 