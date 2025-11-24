import streamlit as st
import pandas as pd
import sys
import os

# 添加utils目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.data_loader import load_data, get_filtered_data, get_up_aggregated_data
from utils.charts import create_scatter_plot, create_bar_chart


def main():
    st.set_page_config(
        page_title="In-Depth Analysis - Bilibili Analytics Platform",
        page_icon="📈"
    )

    st.title("📈 Deep Data Analysis")

    df = load_data()
    if df.empty:
        st.error("Data loading failed")
        return

    # 侧边栏筛选器 - 与数据概览页面保持一致
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
            "Range of views per video",
            min_value=float(df['plays'].min()),
            max_value=float(df['plays'].max()),
            value=(float(df['plays'].min()), float(df['plays'].max()))
        )
    else:
        min_plays, max_plays = 0, 1000000
        st.sidebar.warning("Playback sequence does not exist")

    # 应用筛选 - 与数据概览页面保持一致
    filters = {
        'domains': selected_domains,
        'genders': selected_gender,
        'min_plays': min_plays,
        'max_plays': max_plays
    }

    filtered_df = get_filtered_data(df, filters)
    up_aggregated = get_up_aggregated_data(filtered_df)

    # 关键指标 - 与数据概览页面保持一致
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # 正确计算视频数量：使用video_count列的总和
        if 'video_count' in filtered_df.columns:
            total_videos = filtered_df['video_count'].sum()
        else:
            total_videos = len(filtered_df)
        st.metric("Number of videos", total_videos)
    with col2:
        st.metric("Number of UP owners", len(up_aggregated))
    with col3:
        avg_plays_per_video = filtered_df['plays'].mean() if 'plays' in filtered_df.columns else 0
        st.metric("Average Views per Video", f"{avg_plays_per_video:.0f}")
    with col4:
        if 'video_count' in filtered_df.columns:
            total_videos = filtered_df['video_count'].sum()
        else:
            total_videos = len(filtered_df)
        avg_videos_per_up = total_videos / len(up_aggregated) if len(up_aggregated) > 0 else 0
        st.metric("Average number of videos per UP owner", f"{avg_videos_per_up:.1f}")

    tab1, tab2, tab3 = st.tabs(["Video creator analysis", "Video Analysis", "Domain Comparison"])

    with tab1:
        st.subheader("Comprehensive Influence Analysis of UP Owner")

        if not up_aggregated.empty and all(
                col in up_aggregated.columns for col in ['total_plays', 'comprehensive_score', 'domain']):
            # 确保有视频数量列用于散点图大小
            size_col = 'video_count' if 'video_count' in up_aggregated.columns else None

            fig_scatter = create_scatter_plot(
                up_aggregated,
                'total_plays',
                'comprehensive_score',
                'domain',
                size_col,
                "Relationship Between a Uploader's Total Views and Overall Score"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

            # 添加综合得分排名
            st.subheader("Top 10 UP Owners by Overall Score")
            display_cols = ['up_name', 'domain', 'comprehensive_score']
            if 'video_count' in up_aggregated.columns:
                display_cols.append('video_count')
            if 'total_plays' in up_aggregated.columns:
                display_cols.append('total_plays')

            top_up = up_aggregated.nlargest(10, 'comprehensive_score')[display_cols]
            st.dataframe(top_up, use_container_width=True)

        else:
            st.warning("Unable to perform a comprehensive analysis of the UP creator due to missing necessary data.")

    with tab2:
        st.subheader("Video Data Analysis")

        if all(col in filtered_df.columns for col in ['plays', 'coins', 'likes']):
            # 播放数TOP 5视频 - 使用与数据概览一致的计数方式
            top_videos = filtered_df.nlargest(5, 'plays')

            # 确保获取到足够的视频数据
            if len(top_videos) >= 5:
                display_count = 5
            else:
                display_count = len(top_videos)
                st.warning(f"only find {display_count} datas of video")

            if 'video_title' in top_videos.columns:
                display_data = top_videos[['video_title', 'plays']].head(display_count)
                # 创建水平柱状图，确保所有项目可见
                fig_plays = create_bar_chart(
                    display_data,
                    'plays',
                    'video_title',
                    "Top 5 Videos by Views"
                )
                # 调整图表高度以确保所有项目显示
                fig_plays.update_layout(height=400)
            else:
                display_data = top_videos[['up_name', 'plays']].head(display_count)
                fig_plays = create_bar_chart(
                    display_data,
                    'plays',
                    'up_name',
                    "播放数TOP 5视频"
                )
                fig_plays.update_layout(height=400)

            st.plotly_chart(fig_plays, use_container_width=True)

            # 视频数据统计 - 与数据概览页面计数方式一致
            col1, col2 = st.columns(2)
            with col1:
                st.write("Video Play Count Statistics:")
                if 'plays' in filtered_df.columns:
                    # 使用与数据概览一致的计数方式
                    if 'video_count' in filtered_df.columns:
                        total_count = filtered_df['video_count'].sum()
                    else:
                        total_count = len(filtered_df)

                    plays_stats = filtered_df['plays'].describe()
                    # 创建统计表格，确保count值与数据概览一致
                    stats_data = {
                        'Statistical indicators': ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'],
                        'Numerical value': [
                            total_count,  # 使用与数据概览一致的计数
                            f"{plays_stats['mean']:.0f}",
                            f"{plays_stats['std']:.0f}",
                            f"{plays_stats['min']:.0f}",
                            f"{plays_stats['25%']:.0f}",
                            f"{plays_stats['50%']:.0f}",
                            f"{plays_stats['75%']:.0f}",
                            f"{plays_stats['max']:.0f}"
                        ]
                    }
                    stats_df = pd.DataFrame(stats_data)
                    st.dataframe(stats_df, use_container_width=True, hide_index=True)
                else:
                    st.write("Playback sequence does not exist")

            with col2:
                st.write("Video Interaction Data Statistics:")
                numeric_cols = [col for col in ['coins', 'likes', 'danmu'] if col in filtered_df.columns]
                if numeric_cols:
                    # 使用与数据概览一致的计数方式
                    if 'video_count' in filtered_df.columns:
                        total_count = filtered_df['video_count'].sum()
                    else:
                        total_count = len(filtered_df)

                    interaction_stats = filtered_df[numeric_cols].describe()
                    # 创建互动数据统计表
                    interaction_data = []
                    for col in numeric_cols:
                        col_stats = filtered_df[col].describe()
                        interaction_data.append({
                            'Indicator': col,
                            'count': total_count,  # 使用与数据概览一致的计数
                            'Mean': f"{col_stats['mean']:.0f}",
                            'Maximum value': f"{col_stats['max']:.0f}"
                        })
                    interaction_df = pd.DataFrame(interaction_data)
                    st.dataframe(interaction_df, use_container_width=True, hide_index=True)
                else:
                    st.write("No interactive data columns available")
        else:
            st.warning("Unable to analyze video data")

    with tab3:
        st.subheader("Cross-domain Performance Comparison")

        if not up_aggregated.empty and 'domain' in up_aggregated.columns:
            # 选择可用的数值列
            available_numeric_cols = [col for col in ['total_plays', 'avg_plays', 'video_count', 'comprehensive_score']
                                      if col in up_aggregated.columns]

            if available_numeric_cols:
                metrics_by_domain = up_aggregated.groupby('domain')[available_numeric_cols].mean().reset_index()

                st.subheader("Average Performance of Content Creators in Various Fields")
                st.dataframe(
                    metrics_by_domain,
                    use_container_width=True
                )

                # 可视化第一个数值列的对比
                if len(available_numeric_cols) > 0:
                    first_numeric = available_numeric_cols[0]
                    fig_comparison = create_bar_chart(
                        metrics_by_domain,
                        'domain',
                        first_numeric,
                        f"contrast of {first_numeric} of each domain"
                    )
                    st.plotly_chart(fig_comparison, use_container_width=True)
            else:
                st.warning("Countless value columns are available for comparison")
        else:
            st.warning("Missing domain information or uploader data")


if __name__ == "__main__":
    main()
