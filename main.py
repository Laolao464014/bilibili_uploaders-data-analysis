import streamlit as st
from config import APP_CONFIG
from PIL import Image
import os


def main():
    # 应用配置
    st.set_page_config(**APP_CONFIG)

    st.sidebar.markdown("**Course: Data Visualization 2025**")
    st.sidebar.markdown("**Prof. Mano Mathew**")
    st.sidebar.markdown("student:xinqian zhou")
    st.sidebar.markdown("student:ID 20252033")
    st.sidebar.markdown("github ID:Laolao464014")
    st.sidebar.markdown("[Check out this LinkedIn](https://www.linkedin.com/in/manomathew/)", unsafe_allow_html=True)
    # 在侧边栏左上角添加Logo
    with st.sidebar:
        # 创建两列布局来并排显示两个Logo
        col1, col2 = st.columns([1, 1])

        with col1:
            try:
                # 加载并显示第一个Logo - 路径更新到assets文件夹
                if os.path.exists("assets/WUT-Logo.png"):
                    wut_logo = Image.open("assets/WUT-Logo.png")
                    st.image(wut_logo, use_container_width=True, caption="WUT")
                else:
                    st.error("assets/WUT-Logo.png not found")
            except Exception as e:
                st.error(f"Error loading WUT logo: {e}")

        with col2:
            try:
                # 加载并显示第二个Logo - 路径更新到assets文件夹
                if os.path.exists("assets/efrei.png"):
                    efrei_logo = Image.open("assets/efrei.png")
                    st.image(efrei_logo, use_container_width=True, caption="EFREI")
                else:
                    st.error("assets/efrei.png not found")
            except Exception as e:
                st.error(f"Error loading EFREI logo: {e}")

        # 添加一些间距
        st.markdown("---")

    # 主页面内容
    st.title("🎯 Bilibili UP Owner Collaboration Value Analysis Platform")
    st.markdown("""
    ## Welcome to the Bilibili UP Creator Data Analysis Platform！

    **Main Functions:**

    📊 **data overview** - View data summary and basic distribution
    📈 **in-depths_analysis** - Deeply explore data relationships and trends  
    🤝 **uploaders_recommand** - Intelligent Recommendation Based on Multi-Dimensional Ratings

    **Data Description:**
    - Each row of data represents a single video or multiple videos from a content creator.
    - The system will automatically aggregate and analyze by UP host.
    - Supports filtering by category, gender, number of plays, etc.

    **Usage Process:**
    1. Select the page in the left sidebar
    2. Filter data using the filter
    3. View interactive charts and analysis results
    4. Get personalized collaboration suggestions for creators

    **Analysis Dimension:**
    - **Video aspect**: Single video playback and interaction data
    - **From the perspective of the content creator**: Total views, average views, number of videos, stability
    - **Domain level**: Cross-disciplinary comparative analysis
    """)

    # 添加一些整体统计信息
    try:
        from utils.data_loader import load_data, get_up_aggregated_data
        df = load_data()
        if not df.empty:
            up_aggregated = get_up_aggregated_data(df)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                # 正确计算总视频数：使用video_count列的总和
                if 'video_count' in df.columns:
                    total_videos = df['video_count'].sum()  # 直接从原始数据计算
                else:
                    total_videos = len(df)  # 如果没有video_count列，回退到行数
                st.metric("Total number of videos", total_videos)
            with col2:
                st.metric("Total number of UP owners", len(up_aggregated))
            with col3:
                st.metric("Coverage area", df['domain'].nunique() if 'domain' in df.columns else 0)
            with col4:
                # 使用正确的总视频数计算人均视频数
                if 'video_count' in df.columns:
                    total_videos = df['video_count'].sum()
                else:
                    total_videos = len(df)
                avg_videos = total_videos / len(up_aggregated) if len(up_aggregated) > 0 else 0
                st.metric("Average number of videos per person", f"{avg_videos:.1f}")
    except Exception as e:
        st.info("Please prepare the data first to view the statistics.")


if __name__ == "__main__":
    main()