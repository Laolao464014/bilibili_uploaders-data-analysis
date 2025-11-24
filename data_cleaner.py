import pandas as pd
import numpy as np
import re
import os


def clean_numeric_value(value):
    """
    清理数值数据，处理万单位和其他格式
    """
    if pd.isna(value) or value == '':
        return 0

    # 转换为字符串处理
    value_str = str(value).strip()

    # 处理万单位 (如 4.53w -> 45300)
    if 'w' in value_str.lower() or '万' in value_str:
        # 提取数字部分
        num_part = re.findall(r'[\d.]+', value_str)
        if num_part:
            number = float(num_part[0])
            return int(number * 10000)

    # 处理普通数字
    try:
        # 移除逗号等分隔符
        value_str = value_str.replace(',', '').replace('，', '')
        return float(value_str)
    except:
        return 0


def clean_bilibili_data(file_path):
    """
    清洗B站数据
    """
    try:
        # 读取数据
        df = pd.read_excel(file_path)
        print(f"原始数据形状: {df.shape}")
        print(f"原始列名: {df.columns.tolist()}")

        # 根据原始中文列名进行精确映射
        column_mapping = {
            '榜单类型': 'rank_type',
            '创作领域': 'domain',
            '时间': 'date',
            '投币数': 'coins',
            '头像': 'avatar',
            '涨粉数': 'fans_growth',
            '等级': 'level',
            '获赞数': 'likes',
            'mid': 'mid',
            'up主': 'up_name',
            'up主标签': 'up_tag',
            '投稿视频数': 'video_count',
            '播放数': 'plays',
            '排名': 'rank',
            '性别': 'gender',
            '类型': 'type',
            '弹幕数': 'danmu'
        }

        # 应用列名映射
        df = df.rename(columns=column_mapping)
        print(f"重命名后列名: {df.columns.tolist()}")

        # 添加缺失的必要列
        if 'video_title' not in df.columns:
            # 创建虚拟的视频标题列
            df['video_title'] = df.apply(lambda row: f"{row['up_name']}_视频", axis=1)
            print("已创建虚拟 video_title 列")

        # 清理数值列
        numeric_columns = ['plays', 'coins', 'likes', 'danmu', 'fans_growth', 'video_count', 'level', 'rank']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].apply(clean_numeric_value)
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                # 对于整数列，转换为int
                if col in ['plays', 'coins', 'likes', 'danmu', 'fans_growth', 'video_count', 'rank']:
                    df[col] = df[col].astype(int)
                print(f"已清理数值列: {col}")

        # 清理文本列
        text_columns = ['up_name', 'domain', 'gender', 'rank_type', 'type', 'up_tag', 'video_title']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].fillna(f'未知{col}').astype(str)
                print(f"已清理文本列: {col}")

        # 处理日期列
        if 'date' in df.columns:
            try:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
                print("已处理日期列")
            except:
                print("日期列处理失败")

        # 确保必要的列存在
        required_columns = ['up_name', 'domain', 'plays', 'coins', 'likes', 'danmu', 'video_title']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"警告: 缺少以下必要列: {missing_columns}")

        print(f"清洗后数据形状: {df.shape}")
        print("数据清洗完成!")
        print("最终列名:", df.columns.tolist())

        # 显示前几行数据确认
        print("\n前5行数据预览:")
        print(df[['up_name', 'domain', 'plays', 'coins', 'likes', 'danmu', 'video_title']].head())

        return df

    except Exception as e:
        print(f"数据清洗错误: {e}")
        import traceback
        traceback.print_exc()
        return None


def create_sample_data():
    """
    创建示例数据用于测试
    """
    np.random.seed(42)

    # 创建示例数据
    domains = ['游戏', '生活', '知识', '音乐', '舞蹈', '美食', '科技', '时尚']
    genders = ['男', '女', '未知']
    up_names = [f'UP主_{i}' for i in range(1, 51)]

    data = []
    for i in range(1000):
        up_name = np.random.choice(up_names)
        domain = np.random.choice(domains)
        gender = np.random.choice(genders)

        # 生成视频数据
        video_title = f'视频_{i + 1}'

        # 根据领域和UP主设置不同的表现水平
        base_plays = np.random.randint(1000, 50000)
        if domain in ['游戏', '生活']:
            base_plays *= 2

        plays = int(base_plays * np.random.uniform(0.5, 2.0))
        coins = int(plays * np.random.uniform(0.01, 0.05))
        likes = int(plays * np.random.uniform(0.02, 0.08))
        danmu = int(plays * np.random.uniform(0.005, 0.02))

        data.append({
            'up_name': up_name,
            'domain': domain,
            'video_title': video_title,
            'plays': plays,
            'coins': coins,
            'likes': likes,
            'danmu': danmu,
            'gender': gender
        })

    df = pd.DataFrame(data)
    print("示例数据创建完成!")
    print(f"示例数据形状: {df.shape}")

    return df


def save_cleaned_data(df, file_path='cleaned_bilibili_data.xlsx'):
    """
    保存清洗后的数据
    """
    try:
        df.to_excel(file_path, index=False)
        print(f"数据已保存到: {file_path}")
        return True
    except Exception as e:
        print(f"保存数据失败: {e}")
        return False


def test_data_loading():
    """测试数据加载和清洗"""
    print("开始测试数据加载...")

    # 尝试加载原始数据
    try:
        df = clean_bilibili_data('bilibili_data.xlsx')

        if df is not None and not df.empty:
            print("✅ 原始数据加载成功!")
            print(f"数据形状: {df.shape}")
            print(f"列名: {df.columns.tolist()}")

            # 保存清洗后的数据
            save_cleaned_data(df, 'cleaned_bilibili_data.xlsx')

            return df
        else:
            print("❌ 原始数据加载失败，创建示例数据...")
            df = create_sample_data()
            save_cleaned_data(df, 'cleaned_bilibili_data.xlsx')
            return df

    except Exception as e:
        print(f"❌ 数据加载测试失败: {e}")
        print("创建示例数据...")
        df = create_sample_data()
        save_cleaned_data(df, 'cleaned_bilibili_data.xlsx')
        return df


if __name__ == "__main__":
    # 直接运行这个文件时进行数据清洗测试
    test_data_loading()