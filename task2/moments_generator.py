from task4.common.big_model_interface import *
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from task2.image_analysis import llm_result
import sys
from io import StringIO
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

class MomentsGenerator:
    def get_llm_result(self, image_analysis, country, gender):
        
        # 定义system提示词
        system_prompt = """你是一个专业的社交媒体文案生成专家。你的任务是根据图片分析结果、目标国家和性别信息，生成一条富有创意和个性的朋友圈文案。
        要求：
        1. 文案要符合目标国家的文化特点，生成的信息是对应国家的语言，如果输入用的繁体字或者中国台湾，用中文繁体字
        2. 语气要符合性别特征
        3. 要自然、有趣、富有感染力
        4. 长度适中（20-30字），适合朋友圈展示
        5. 可以适当使用emoji表情
        请直接输出文案内容，不需要其他解释。"""
        
        # 定义user提示词
        human_prompt = """图片分析结果：
        {image_analysis}
        
        目标国家：{country}
        性别：{gender}
        
        请生成一条符合要求的朋友圈文案。"""
        # 创建提示模板
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(human_prompt)
        ])
        messages = prompt.format_messages(
            image_analysis=image_analysis,
            country=country,
            gender=gender
        )
        # 生成文案
        res, comment_token = generate_result(messages)
        return res, comment_token
    
    def get_image_analysis(self, image_path: str) -> str:
        # 重定向标准输出以捕获llm_result的输出
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        # 调用zhipu_main.py中的llm_result函数
        token_num = llm_result(image_path)
        sys.stdout = old_stdout
        # 获取输出
        image_analysis = mystdout.getvalue()
        return image_analysis, token_num

def main():
    generator = MomentsGenerator()
    # 获取用户输入
    image_path = input("请输入图片URL：")
    country = input("请输入目标国家：")
    gender = input("请输入性别（男/女）：")
    # 生成文案
    image_analysis, img_token = generator.get_image_analysis(image_path)
    print("生成的朋友圈文案：")
    comment, comment_token = generator.get_llm_result(image_analysis, country, gender)
    # 计算总token数量
    total_token = img_token + comment_token
    print(f"图片分析结果使用了{img_token}个token")
    print(f"文案使用了{comment_token}个token")
    print(f"本次共使用了{total_token}个token")
    # 输出结果

if __name__ == "__main__":
    main()
