import pandas as pd
import streamlit as st
import os


@st.cache_data
def load_data():
    """
    加载清洗后的数据，如果不存在则先进行清洗
    """
    return load_cleaned_data()


@st.cache_data
def load_cleaned_data():
    """
    加载清洗后的数据，如果不存在则先进行清洗
    """
    cleaned_file = 'cleaned_bilibili_data.xlsx'
    original_file = 'bilibili_data.xlsx'

    # 如果清洗后的数据不存在，先进行清洗
    if not os.path.exists(cleaned_file):
        st.info("Cleaning data, please wait...")
        try:
            # 尝试从根目录导入清洗函数
            import sys
            sys.path.append('.')  # 添加当前目录到Python路径
            from data_cleaner import clean_bilibili_data, save_cleaned_data

            if os.path.exists(original_file):
                df = clean_bilibili_data(original_file)
                if df is not None:
                    save_cleaned_data(df, cleaned_file)
                    st.success("Data cleaning completed!")
                else:
                    st.error("Data cleaning failed, using sample data")
                    from data_cleaner import create_sample_data
                    df = create_sample_data()
                    save_cleaned_data(df, cleaned_file)
            else:
                st.warning("Original data file not found, using sample data")
                from data_cleaner import create_sample_data
                df = create_sample_data()
                save_cleaned_data(df, cleaned_file)
        except Exception as e:
            st.error(f"Data cleaning process error: {e}")
            from data_cleaner import create_sample_data
            df = create_sample_data()
            save_cleaned_data(df, cleaned_file)
    else:
        # 直接加载清洗后的数据
        try:
            df = pd.read_excel(cleaned_file)
            st.success("Data loaded successfully!")
        except Exception as e:
            st.error(f"Failed to load cleaned data: {e}")
            from data_cleaner import create_sample_data
            df = create_sample_data()

    # 确保必要的列存在
    required_columns = ['up_name', 'domain', 'plays', 'coins', 'likes', 'danmu']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.warning(f"Missing the following items: {missing_columns}")

    return df


@st.cache_data
def get_filtered_data(df, filters):
    """根据筛选条件过滤数据"""
    filtered_df = df.copy()

    # 修复过滤逻辑 - 安全地处理filters参数
    if filters is not None:
        if 'domains' in filters and filters['domains']:
            domains = filters['domains']
            if isinstance(domains, list) and len(domains) > 0:
                filtered_df = filtered_df[filtered_df['domain'].isin(domains)]

        if 'genders' in filters and filters['genders']:
            genders = filters['genders']
            if isinstance(genders, list) and len(genders) > 0:
                filtered_df = filtered_df[filtered_df['gender'].isin(genders)]

        if 'min_plays' in filters and filters['min_plays'] is not None:
            filtered_df = filtered_df[filtered_df['plays'] >= filters['min_plays']]

        if 'max_plays' in filters and filters['max_plays'] is not None:
            filtered_df = filtered_df[filtered_df['plays'] <= filters['max_plays']]

    return filtered_df


def get_up_aggregated_data(df):
    """按UP主聚合数据"""
    if df.empty:
        print("The data frame is empty and cannot be aggregated")
        return pd.DataFrame()

    # 确保必要的列存在
    if 'up_name' not in df.columns:
        print("Error: Missing up_name column, unable to aggregate data")
        print("Available Columns:", df.columns.tolist())
        return pd.DataFrame()

    print(f"Start aggregating data, number of raw data rows: {len(df)}")
    print(f"Number of UP owners: {df['up_name'].nunique()}")

    # 构建聚合配置 - 只使用实际存在的列
    agg_config = {}

    # 添加可用的列到聚合配置
    if 'domain' in df.columns:
        agg_config['domain'] = 'first'
        print("find domain")
    else:
        print("not find domain")

    if 'gender' in df.columns:
        agg_config['gender'] = 'first'
        print("find gender")
    else:
        print("not find gender 列")

    if 'plays' in df.columns:
        agg_config['plays'] = ['sum', 'mean', 'max']
        print("find plays")
    else:
        print("not find plays")

    if 'coins' in df.columns:
        agg_config['coins'] = ['sum', 'mean']
        print("find coins")
    else:
        print("not find coins")

    if 'likes' in df.columns:
        agg_config['likes'] = ['sum', 'mean']
        print("find likes")
    else:
        print("not find likes")

    if 'danmu' in df.columns:
        agg_config['danmu'] = ['sum', 'mean']
        print("find danmu")
    else:
        print("not find danmu")

    if 'video_title' in df.columns:
        agg_config['video_title'] = 'count'
        print("find video_title")
    elif 'video_count' in df.columns:
        agg_config['video_count'] = 'sum'
        print("find video_count")
    else:
        agg_config['up_name'] = 'count'
        print("Use up_name count as the number of videos")

    print(f"Aggregate Configuration: {agg_config}")

    # 按UP主分组，计算聚合指标
    try:
        up_aggregated = df.groupby('up_name').agg(agg_config).round(2)
        print(f"Data shape after aggregation: {up_aggregated.shape}")

        # 扁平化列名
        up_aggregated.columns = ['_'.join(col).strip() for col in up_aggregated.columns.values]
        up_aggregated = up_aggregated.reset_index()

        print(f"Column names after flattening: {up_aggregated.columns.tolist()}")

        # 重命名列 - 修复列名映射
        column_mapping = {}
        if 'video_title_count' in up_aggregated.columns:
            column_mapping['video_title_count'] = 'video_count'
        elif 'up_name_count' in up_aggregated.columns:
            column_mapping['up_name_count'] = 'video_count'
        elif 'video_count_first' in up_aggregated.columns:
            column_mapping['video_count_first'] = 'video_count'

        # 修复领域和性别列名
        if 'domain_first' in up_aggregated.columns:
            column_mapping['domain_first'] = 'domain'
        if 'gender_first' in up_aggregated.columns:
            column_mapping['gender_first'] = 'gender'

        if 'plays_sum' in up_aggregated.columns:
            column_mapping['plays_sum'] = 'total_plays'
        if 'plays_mean' in up_aggregated.columns:
            column_mapping['plays_mean'] = 'avg_plays'
        if 'plays_max' in up_aggregated.columns:
            column_mapping['plays_max'] = 'max_plays'
        if 'coins_sum' in up_aggregated.columns:
            column_mapping['coins_sum'] = 'total_coins'
        if 'coins_mean' in up_aggregated.columns:
            column_mapping['coins_mean'] = 'avg_coins'
        if 'likes_sum' in up_aggregated.columns:
            column_mapping['likes_sum'] = 'total_likes'
        if 'likes_mean' in up_aggregated.columns:
            column_mapping['likes_mean'] = 'avg_likes'
        if 'danmu_sum' in up_aggregated.columns:
            column_mapping['danmu_sum'] = 'total_danmu'
        if 'danmu_mean' in up_aggregated.columns:
            column_mapping['danmu_mean'] = 'avg_danmu'

        up_aggregated = up_aggregated.rename(columns=column_mapping)
        print(f"Renamed column: {up_aggregated.columns.tolist()}")

        # 计算综合得分
        if not up_aggregated.empty:
            score_components = []
            weights = []

            if 'total_plays' in up_aggregated.columns:
                if up_aggregated['total_plays'].max() > up_aggregated['total_plays'].min():
                    normalized_plays = (up_aggregated['total_plays'] - up_aggregated['total_plays'].min()) / (
                                up_aggregated['total_plays'].max() - up_aggregated['total_plays'].min())
                else:
                    normalized_plays = up_aggregated['total_plays'] * 0
                score_components.append(normalized_plays)
                weights.append(0.2)

            if 'total_coins' in up_aggregated.columns:
                if up_aggregated['total_coins'].max() > up_aggregated['total_coins'].min():
                    normalized_coins = (up_aggregated['total_coins'] - up_aggregated['total_coins'].min()) / (
                                up_aggregated['total_coins'].max() - up_aggregated['total_coins'].min())
                else:
                    normalized_coins = up_aggregated['total_coins'] * 0
                score_components.append(normalized_coins)
                weights.append(0.3)

            if 'total_likes' in up_aggregated.columns:
                if up_aggregated['total_likes'].max() > up_aggregated['total_likes'].min():
                    normalized_likes = (up_aggregated['total_likes'] - up_aggregated['total_likes'].min()) / (
                                up_aggregated['total_likes'].max() - up_aggregated['total_likes'].min())
                else:
                    normalized_likes = up_aggregated['total_likes'] * 0
                score_components.append(normalized_likes)
                weights.append(0.3)

            if 'total_danmu' in up_aggregated.columns:
                if up_aggregated['total_danmu'].max() > up_aggregated['total_danmu'].min():
                    normalized_danmu = (up_aggregated['total_danmu'] - up_aggregated['total_danmu'].min()) / (
                                up_aggregated['total_danmu'].max() - up_aggregated['total_danmu'].min())
                else:
                    normalized_danmu = up_aggregated['total_danmu'] * 0
                score_components.append(normalized_danmu)
                weights.append(0.2)

            if score_components and sum(weights) > 0:
                total_score = sum(comp * weight for comp, weight in zip(score_components, weights)) / sum(weights)
                up_aggregated['comprehensive_score'] = total_score.round(4)
                print("Overall score calculation completed")

        print(f"Final aggregated data shape: {up_aggregated.shape}")
        if not up_aggregated.empty:
            print(f"Aggregated Data Preview:\n{up_aggregated.head()}")

        return up_aggregated

    except Exception as e:
        print(f"Failed to aggregate data for the uploader: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()


def get_data_summary(df):
    """获取数据摘要"""
    up_aggregated = get_up_aggregated_data(df)

    summary = {
        'total_videos': len(df),
        'total_up': len(up_aggregated) if not up_aggregated.empty else 0,
        'domains': df['domain'].nunique() if 'domain' in df.columns else 0,
        'avg_plays_per_video': df['plays'].mean() if 'plays' in df.columns else 0,
        'avg_plays_per_up': up_aggregated[
            'avg_plays'].mean() if not up_aggregated.empty and 'avg_plays' in up_aggregated.columns else 0,
        'total_plays': up_aggregated[
            'total_plays'].sum() if not up_aggregated.empty and 'total_plays' in up_aggregated.columns else 0
    }
    return summary