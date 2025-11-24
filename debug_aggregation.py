import pandas as pd
import sys
import os

# 添加当前目录到Python路径
sys.path.append('.')


def debug_aggregation():
    print("=== 调试数据聚合过程 ===")

    # 直接读取清洗后的数据
    if os.path.exists('cleaned_bilibili_data.xlsx'):
        print("找到清洗后的数据文件")
        df = pd.read_excel('cleaned_bilibili_data.xlsx')
        print(f"数据形状: {df.shape}")
        print(f"列名: {df.columns.tolist()}")

        if not df.empty:
            print(f"\n数据基本信息:")
            print(f"总行数: {len(df)}")
            print(f"UP主数量: {df['up_name'].nunique() if 'up_name' in df.columns else 'N/A'}")
            print(f"领域数量: {df['domain'].nunique() if 'domain' in df.columns else 'N/A'}")

            # 检查前几行数据
            print(f"\n前5行数据:")
            print(df.head())

            # 检查数值列
            print(f"\n数值列统计:")
            numeric_cols = ['plays', 'coins', 'likes', 'danmu']
            for col in numeric_cols:
                if col in df.columns:
                    print(f"{col}: min={df[col].min()}, max={df[col].max()}, mean={df[col].mean():.2f}")
                else:
                    print(f"{col}: 列不存在")

            # 测试手动聚合
            print(f"\n=== 手动测试聚合 ===")
            if 'up_name' in df.columns:
                # 简单的分组测试
                test_agg = df.groupby('up_name').agg({
                    'up_name': 'count'
                }).rename(columns={'up_name': 'video_count'})
                print(f"简单聚合结果形状: {test_agg.shape}")
                print(f"简单聚合结果:")
                print(test_agg.head())

                # 尝试完整聚合
                print(f"\n=== 完整聚合测试 ===")
                from utils.data_loader import get_up_aggregated_data
                up_aggregated = get_up_aggregated_data(df)

                if up_aggregated.empty:
                    print("聚合失败: 返回空数据框")
                else:
                    print(f"聚合成功! 形状: {up_aggregated.shape}")
                    print(f"聚合列名: {up_aggregated.columns.tolist()}")
                    print(f"聚合数据预览:")
                    print(up_aggregated.head())
            else:
                print("错误: 缺少 up_name 列")
        else:
            print("数据文件为空")
    else:
        print("未找到清洗后的数据文件")


if __name__ == "__main__":
    debug_aggregation()