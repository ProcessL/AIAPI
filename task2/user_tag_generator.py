import json
from typing import Dict

from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from task4.common.big_model_interface import generate_result


class UserTagGenerator:
    def gen_tag(self, user_info):
        system_prompt = """
        你是一个专业的用户特征分析专家。请根据提供的用户信息，从以下维度进行深入分析，每个维度用一句话总结核心特征。请使用用户所在国家的语言进行回答。

        1. 人口统计学特征
        用一句话总结用户的基本人口统计学特征，包括年龄段、性别特征、地理位置和文化背景等。

        2. 兴趣爱好
        用一句话概括用户的主要兴趣领域、爱好、习惯、内容偏好和活动模式。

        3. 性格特征
        用一句话描述用户的性格特点、行为模式和价值观。

        4. 社交风格
        用一句话总结用户的社交参与度、互动模式和影响力水平。

        5. 心理特征与沟通策略
        用一句话总结最适合的沟通方式和话术策略，包括如何建立信任、激发兴趣和促进互动。

        6. 整体印象
        用3-5个词总结关键标签。

        请确保：
        1. 每个维度只用一句话总结
        2. 分析要客观、专业，避免主观臆测
        3. 每句话都要包含具体的分析依据
        4. 语言要简洁、准确、专业
        5. 考虑用户所在国家的文化背景和特点
        6. 使用用户所在国家的语言进行回答
        7. 如果用户所在国家使用多种语言，请使用最常用的官方语言
        """
        human_prompt = """  
        请根据以下用户信息进行全面的特征分析，并使用用户所在国家的语言回答。每个维度请用一句话总结：

        用户信息：
        {user_info}

        请从上述六个维度进行分析，每个维度用一句话总结，并确保使用用户所在国家的语言。
        """
        # 创建提示模板
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(human_prompt)
        ])
        messages = prompt.format_messages(
            user_info=user_info
        )
        res, total_tokens = generate_result(messages)
        return res, total_tokens

    def generate_tags(self, user_info: Dict) -> Dict:
        # 格式化用户信息
        posts_bio = []
        for i in range(min(5, len(user_info.get('posts_bio_n_img', [])))):
            post_bio = user_info['posts_bio_n_img'][i].get('post_bio', [''])[0] if user_info['posts_bio_n_img'][i].get('post_bio') else ''
            posts_bio.append(post_bio)
        
        # 补齐不足5条的朋友圈文案
        while len(posts_bio) < 5:
            posts_bio.append('')
        
        formatted_info = f"""
        用户名：{user_info.get('user_name', '')}
        全名：{user_info.get('full_name', '')}
        个人简介：{user_info.get('bio', '')}
        粉丝数：{user_info.get('followers_num', '0')}
        关注数：{user_info.get('following_num', '0')}
        帖子数：{user_info.get('posts_num', '0')}
        认证账户：{'是' if user_info.get('is_verified', False) else '否'}
        头像URL：{user_info.get('avatar_url', '')}
        账号创建时间：{user_info.get('date_joined', '')}
        国家：{user_info.get('account_based_in', '未知')}
        用户ID：{user_info.get('user_id', '')}
        朋友圈文案1：{posts_bio[0]}
        朋友圈文案2：{posts_bio[1]}
        朋友圈文案3：{posts_bio[2]}
        朋友圈文案4：{posts_bio[3]}
        朋友圈文案5：{posts_bio[4]}
        """
        
        # 生成标签
        res, total_tokens = self.gen_tag(formatted_info)
        return res, total_tokens


def get_user_input() -> Dict:
    """
    通过命令行输入获取用户信息
    
    Returns:
        Dict: 包含用户信息的字典
    """
    print("\n请输入用户信息：")
    user_info = {
        "username": input("用户名: "),
        "bio": input("个人简介: "),
        "followers_count": int(input("粉丝数: ")),
        "following_count": int(input("关注数: ")),
        "is_private": input("是否为私密账户 (是/否): ").lower() == "是",
        "is_verified": input("是否为认证账户 (是/否): ").lower() == "是",
        "avatar_url": input("头像URL: "),
        "created_at": input("账号创建时间 (YYYY-MM): "),
        # "gender": input("性别 (男/女): "),
        "country": input("国家: "),  # 国家可能没有
        "content1": input("朋友圈文案1: "),
        "content2": input("朋友圈文案2: "),
        "content3": input("朋友圈文案3: "),
        "content4": input("朋友圈文案4: "),
        "content5": input("朋友圈文案5: "),
    }
    return user_info




def get_user_info_from_file() -> Dict:
    """
    从文件中读取用户信息
    """
    with open("task5/user_info.json", "r", encoding="utf-8") as f:
        user_info_list = json.load(f)
        # 默认使用第一个用户的信息
        if user_info_list and len(user_info_list) > 0:
            return user_info_list[0]
        else:
            raise ValueError("用户信息文件为空或格式不正确")



def main():
    # 示例使用
    generator = UserTagGenerator()
    
    try:
        print("从user_info.json文件中读取用户信息...")
        # 直接从文件中读取用户信息
        user_info = get_user_info_from_file()
        print(f"成功读取用户 '{user_info.get('user_name', '')}' 的信息")
        
        # 生成标签
        print("\n开始生成用户标签...\n")
        res, total_tokens = generator.generate_tags(user_info)
        print("\n标签生成完成!")
        print(f"\n本次共使用了{total_tokens}个token")
        
    except ValueError as e:
        print(f"\n输入错误：{str(e)}")
    except Exception as e:
        print(f"\n发生错误：{str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 