import pandas as pd
import streamlit as st
import sys
import os

# 添加utils目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.data_loader import load_data, get_filtered_data, get_up_aggregated_data
from utils.charts import create_pie_chart, create_bar_chart, create_pie_chart_from_series


def main():
    st.set_page_config(
        page_title="Data Overview - Bilibili Analytics Platform",
        page_icon="📊"
    )

    st.title("📊 Data Overview")

    # 加载数据
    df = load_data()

    if df.empty:
        st.error("Data loading failed, please check the data file")
        return

    # 侧边栏筛选器
    st.sidebar.header("🔍 Data Filtering")

    # 获取可用的领域
    available_domains = df['domain'].unique() if 'domain' in df.columns else []
    available_genders = df['gender'].unique() if 'gender' in df.columns else []

    selected_domains = st.sidebar.multiselect(
        "Choose a creative field",
        options=available_domains,
        default=available_domains
    )

    selected_gender = st.sidebar.multiselect(
        "Select the gender of the UP owner",
        options=available_genders,
        default=available_genders
    )

    # 数值范围筛选
    if 'plays' in df.columns:
        min_plays, max_plays = st.sidebar.slider(
            "Range of views for a single video",
            min_value=float(df['plays'].min()),
            max_value=float(df['plays'].max()),
            value=(float(df['plays'].min()), float(df['plays'].max()))
        )
    else:
        min_plays, max_plays = 0, 1000000
        st.sidebar.warning("Playback sequence does not exist")

    # 应用筛选
    filters = {
        'domains': selected_domains,
        'genders': selected_gender,
        'min_plays': min_plays,
        'max_plays': max_plays
    }

    filtered_df = get_filtered_data(df, filters)

    # 获取UP主聚合数据
    up_aggregated = get_up_aggregated_data(filtered_df)

    # 关键指标
    # 关键指标
    # 关键指标
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # 正确计算视频数量：使用video_count列的总和
        if 'video_count' in filtered_df.columns:
            total_videos = filtered_df['video_count'].sum()  # 直接从筛选后的数据计算
        else:
            total_videos = len(filtered_df)  # 如果没有video_count列，回退到行数
        st.metric("Number of videos", total_videos)
    with col2:
        st.metric("Number of UP owners", len(up_aggregated))
    with col3:
        avg_plays_per_video = filtered_df['plays'].mean() if 'plays' in filtered_df.columns else 0
        st.metric("Average Views per Video", f"{avg_plays_per_video:.0f}")
    with col4:
        # 使用正确的总视频数计算平均视频数
        if 'video_count' in filtered_df.columns:
            total_videos = filtered_df['video_count'].sum()
        else:
            total_videos = len(filtered_df)
        avg_videos_per_up = total_videos / len(up_aggregated) if len(up_aggregated) > 0 else 0
        st.metric("Average number of videos per UP owner", f"{avg_videos_per_up:.1f}")

    # 领域分布图表
    # 领域分布图表
    if 'domain' in filtered_df.columns:
        col1, col2 = st.columns(2)

        with col1:
            # 修正：根据是否有video_count列来正确统计视频数量
            if 'video_count' in filtered_df.columns:
                # 如果有video_count列，按领域分组求和
                domain_video_count = filtered_df.groupby('domain')['video_count'].sum()
            else:
                # 如果没有video_count列，使用value_counts统计行数
                domain_video_count = filtered_df['domain'].value_counts()

            if not domain_video_count.empty:
                fig_pie = create_pie_chart_from_series(
                    domain_video_count,
                    "Distribution of video numbers across various fields"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No domain distribution data available")

        with col2:
            if not up_aggregated.empty and 'domain' in up_aggregated.columns:
                up_count_by_domain = up_aggregated['domain'].value_counts()
                if not up_count_by_domain.empty:
                    fig_bar = create_bar_chart(
                        up_count_by_domain.reset_index(),
                        'domain',
                        'count',
                        "Number of creators in each field"
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No UP host distribution data available")
            else:
                st.info("Unable to calculate the distribution of UP owners")

    # UP主数据表格
    st.subheader("up-loaders Data Summary (Top 20)")
    if not up_aggregated.empty:
        display_columns = [col for col in
                           ['up_name', 'domain', 'video_count', 'total_plays', 'avg_plays', 'comprehensive_score']
                           if col in up_aggregated.columns]
        if display_columns:
            top_up = up_aggregated.nlargest(20, 'total_plays')
            st.dataframe(top_up[display_columns], use_container_width=True)
        else:
            st.warning("No columns to display")
    else:
        st.warning("No UP host aggregation data available")

    # 原始数据预览
    st.subheader("Raw Data Preview (First 20 Records)")
    display_columns = [col for col in ['up_name', 'domain', 'video_title', 'plays', 'coins', 'likes']
                       if col in filtered_df.columns]
    if display_columns:
        st.dataframe(filtered_df[display_columns].head(20), use_container_width=True)
    else:
        st.warning("No columns to display")


if __name__ == "__main__":
    main()
