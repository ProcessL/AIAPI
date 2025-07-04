import json
import os

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from big_model_interface import generate_result

from loguru import logger


# 角色属性配置

PROFILE_CONFIG = {
    "基本信息": {
        "姓名": "",
        "年龄": "",
        "性别": "",
        "职业": ""
    },
    "性格特点": {
        "性格": "",
        "兴趣爱好": "",
        "生活习惯": ""
    },
    "社交特征": {
        "社交风格": "",
        "沟通方式": "",
        "人际关系": ""
    },
    "职业特征": {
        "专业领域": "",
        "工作态度": "",
        "职业规划": ""
    },
    "关键词": {
        "关键词": ["", "", "", "", ""]
    }
} 



class RoleGenerator:
    def role_gen(self, country: str, gender: str, age: int):
        system_prompt = """
        你是一个专业的角色生成专家。你的任务是根据用户提供的基本信息（国家、性别、年龄），生成一个完整的角色属性。
        要求：
        1. 生成的所有信息必须符合目标国家的文化特点
        2. 所有输出的内容必须使用目标国家的语言
        3. 生成的信息必须符合指定性别和年龄段的特征
        4. 所有生成的信息必须保持逻辑一致性
        5. 生成的内容要自然、合理、符合现实
        请按照JSON格式输出，不要添加任何额外的解释。"""
        
        # 定义人类提示词
        human_prompt = """请根据以下基本信息生成一个完整的角色属性：
        国家/地区：{country}
        性别：{gender}
        年龄：{age}
        
        请按照以下JSON格式生成所有属性：
        {profile_template}
        
        再根据生成的角色属性，生成角色可能会去搜索的五个关键词，关键词要符合角色属性，并且要符合目标国家的文化特点，关键词要符合目标国家的语言习惯
        注意：
        1. 所有生成的内容必须符合目标国家的文化特点，{profile_template}中所有的汉字直接原样输出
        2. 所有生成的内容必须使用目标国家的语言
        3. 生成的信息必须符合指定性别和年龄段的特征
        4. 所有生成的信息必须保持逻辑一致性
        5. 生成的内容要自然、合理、符合现实
        """
        
        # 创建提示模板
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(human_prompt)
        ])
        messages = prompt.format_messages(
            country=country,
            gender=gender,
            age=str(age),
            profile_template=json.dumps(PROFILE_CONFIG, ensure_ascii=False, indent=2)
        )
        res_text, total_tokens = generate_result(messages)
        return res_text, total_tokens

def main(params):
    generator = RoleGenerator()
    # 获取用户输入
    # country = input("请输入目标国家/地区：")
    # gender = input("请输入性别（男/女）：")
    # age = input("请输入年龄：")

    # 从参数中获取
    country = params.get('country', '')
    gender = params.get('gender', '')
    age = params.get('age', '')


    try:
        age = int(age)
    except ValueError:
        logger.error("年龄必须是数字！")
        return
    
    # 生成角色属性
    logger.info("正在生成角色属性，请稍候...")
    role_data, total_tokens = generator.role_gen(country, gender, age)
    
    if role_data:
        # 创建输出目录
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # 保存到文件
        output_file = os.path.join(output_dir, f"role_profile_{country}_{gender}_{age}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(role_data, f, ensure_ascii=False, indent=2)
        logger.info(f"角色属性已生成并保存到：{output_file}")
        logger.info(f"本次共使用了{total_tokens}个token")
        return role_data,total_tokens

if __name__ == "__main__":
    params = {
        "country": "中国",
        "gender": "男",
        "age": 20
    }
    main(params)