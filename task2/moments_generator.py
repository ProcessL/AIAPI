from big_model_interface import *
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from image_analysis import llm_result
import sys
from io import StringIO
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from loguru import logger

class MomentsGenerator:
    def get_llm_result(self, image_analysis, country, gender):
        
        # 定义system提示词
        system_prompt = """
        你是一个专业的社交媒体文案生成专家。你的任务是根据图片分析结果、目标国家和性别信息，生成一条富有创意和个性的朋友圈文案。
        要求：
        1. 文案要符合目标国家的文化特点，生成的信息是对应国家的语言，如果输入用的繁体字或者中国台湾，用中文繁体字
        2. 语气要符合性别特征
        3. 要自然、有趣、富有感染力
        4. 长度适中（20-30字），适合朋友圈展示
        5. 可以适当使用emoji表情
        请直接输出文案内容，不需要其他解释。
        """
        
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

def main(params):
    generator = MomentsGenerator()
    image_path = params.get('image_path', '')
    country = params.get('country', '')
    gender = params.get('gender', '')
    if not image_path or not country or not gender:
        logger.error("缺少必要的输入内容")
    # 生成文案
    image_analysis, img_token = generator.get_image_analysis(image_path)
    logger.info("正在生成朋友圈文案，请稍候...")
    comment, comment_token = generator.get_llm_result(image_analysis, country, gender)
    # 计算总token数量
    total_token = img_token + comment_token
    logger.info(f"朋友圈文案生成完成，本次共使用了{total_token}个token")
    # 输出结果
    return comment, total_token

if __name__ == "__main__":
    params = {
        "image_path": "https://scontent-lhr6-1.cdninstagram.com/v/t51.2885-19/471646931_633244312369538_8955977711726470575_n.jpg?_nc_ht=scontent-lhr6-1.cdninstagram.com&_nc_cat=102&_nc_oc=Q6cZ2QFvk6mSTkLVcxoij9_3BeJ4Dc8DwyIzXrGa6AD2UghazXlhAG0sWlajvEW3yJ6jZ8s&_nc_ohc=oOj_J5yt4UEQ7kNvwFV_cwT&_nc_gid=1Pwfc_iQHDwBtGNqD3NhTQ&edm=AP4sbd4BAAAA&ccb=7-5&oh=00_AfMXuOHcRiYAf_GI7HkPLbLTVSvulB2HYpZEKmFs6151NQ&oe=686812BD&_nc_sid=7a9f4b",
        "country": "China",
        "gender": "男"
    }
    main(params)
