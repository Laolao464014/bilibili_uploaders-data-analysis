# 应用配置
APP_CONFIG = {
    'page_title': 'B站UP主合作价值分析平台',
    'page_icon': '📊',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# 数据配置
DATA_CONFIG = {
    'original_file': 'bilibili_data.xlsx',
    'cleaned_file': 'cleaned_bilibili_data.xlsx',
    'cache_time': 3600
}

# 分析权重配置
WEIGHTS = {
    'plays': 0.2,
    'coins': 0.3,
    'likes': 0.3,
    'danmu': 0.2
}

# 默认筛选条件
DEFAULT_FILTERS = {
    'domains': [],
    'genders': [],
    'min_plays': 0,
    'max_plays': float('inf')
}