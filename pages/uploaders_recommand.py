import streamlit as st
import pandas as pd
import sys
import os

# 添加utils目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.data_loader import load_data, get_filtered_data, get_up_aggregated_data


def main():
    st.set_page_config(
        page_title="Recommended by the UP Owner - Bilibili Analysis Platform",
        page_icon="🤝"
    )

    st.title("🤝 Recommended Collaboration by the Uploader")

    df = load_data()
    if df.empty:
        st.error("Data loading failed")
        return

    # 修复筛选条件
    available_domains = df['domain'].unique() if 'domain' in df.columns else []
    available_genders = df['gender'].unique() if 'gender' in df.columns else []

    filters = {
        'domains': available_domains.tolist() if hasattr(available_domains, 'tolist') else list(available_domains),
        'genders': available_genders.tolist() if hasattr(available_genders, 'tolist') else list(available_genders)
    }

    filtered_df = get_filtered_data(df, filters)
    up_aggregated = get_up_aggregated_data(filtered_df)

    # 推荐参数设置
    st.sidebar.header("🎯 Recommended parameters")

    col1, col2 = st.columns(2)

    with col1:
        weight_total_plays = st.slider("Total Play Count Weight", 0.0, 1.0, 0.3, 0.1)
        weight_avg_plays = st.slider("Average Play Count Weight", 0.0, 1.0, 0.2, 0.1)

    with col2:
        weight_video_count = st.slider("Video Quantity Weight", 0.0, 1.0, 0.2, 0.1)
        weight_consistency = st.slider("Stability Weight", 0.0, 1.0, 0.3, 0.1)

    # 计算推荐分数
    if not up_aggregated.empty and all(
            col in up_aggregated.columns for col in ['total_plays', 'avg_plays', 'video_count']):
        # 归一化数据
        for col in ['total_plays', 'avg_plays', 'video_count']:
            if up_aggregated[col].max() > up_aggregated[col].min():
                up_aggregated[f'{col}_normalized'] = (
                        (up_aggregated[col] - up_aggregated[col].min()) /
                        (up_aggregated[col].max() - up_aggregated[col].min())
                )
            else:
                up_aggregated[f'{col}_normalized'] = 0.5

        # 计算稳定性分数
        up_aggregated['stability_score'] = up_aggregated['avg_plays'] / (
                    up_aggregated['total_plays'] / up_aggregated['video_count'] + 1)

        # 归一化稳定性分数
        if up_aggregated['stability_score'].max() > up_aggregated['stability_score'].min():
            up_aggregated['stability_normalized'] = (
                    (up_aggregated['stability_score'] - up_aggregated['stability_score'].min()) /
                    (up_aggregated['stability_score'].max() - up_aggregated['stability_score'].min())
            )
        else:
            up_aggregated['stability_normalized'] = 0.5

        total_weight = weight_total_plays + weight_avg_plays + weight_video_count + weight_consistency

        if total_weight > 0:
            up_aggregated['推荐分数'] = (
                    up_aggregated['total_plays_normalized'] * weight_total_plays +
                    up_aggregated['avg_plays_normalized'] * weight_avg_plays +
                    up_aggregated['video_count_normalized'] * weight_video_count +
                    up_aggregated['stability_normalized'] * weight_consistency
            )

    # 按领域推荐
    if not up_aggregated.empty and 'domain' in up_aggregated.columns:
        selected_domain = st.selectbox(
            "🎯 Select target field",
            options=up_aggregated['domain'].unique()
        )

        domain_up = up_aggregated[up_aggregated['domain'] == selected_domain]

        if '推荐分数' in domain_up.columns:
            top_up = domain_up.nlargest(10, '推荐分数')

            # 显示推荐结果
            st.subheader(f"🏆Top 10 Recommended Creators in the Field of {selected_domain}")

            display_columns = [col for col in ['up_name', 'video_count', 'total_plays', 'avg_plays', '推荐分数']
                               if col in top_up.columns]
            if display_columns:
                st.dataframe(
                    top_up[display_columns].sort_values('推荐分数', ascending=False),
                    use_container_width=True
                )

            # UP主详情查看
            st.subheader("🔍 UP Host Details Analysis")
            if 'up_name' in top_up.columns:
                selected_up = st.selectbox("Select the creator to view details", options=top_up['up_name'].values)

                if selected_up:
                    up_data = top_up[top_up['up_name'] == selected_up].iloc[0]

                    # 获取该UP主的原始视频数据
                    up_videos = filtered_df[filtered_df['up_name'] == selected_up]

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        if 'video_count' in up_data:
                            st.metric("Number of videos", f"{up_data['video_count']:.0f}")
                        if 'total_plays' in up_data:
                            st.metric("Total Plays", f"{up_data['total_plays']:.0f}")

                    with col2:
                        if 'avg_plays' in up_data:
                            st.metric("Average Play", f"{up_data['avg_plays']:.0f}")
                        if '推荐分数' in up_data:
                            st.metric("Average Play", f"{up_data['推荐分数']:.3f}")

                    with col3:
                        if not up_videos.empty and 'plays' in up_videos.columns:
                            max_play_video = up_videos.loc[up_videos['plays'].idxmax()]
                            st.metric("Top Played Video", f"{max_play_video['plays']:.0f}")
        else:
            st.warning("Unable to calculate recommendation score, please check the data columns")
    else:
        st.warning("Missing domain information or uploader data")


if __name__ == "__main__":
    main()