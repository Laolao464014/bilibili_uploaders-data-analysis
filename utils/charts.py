import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_scatter_plot(df, x_col, y_col, color_col, size_col=None, title=""):
    """创建散点图"""
    required_cols = [x_col, y_col, color_col]
    if size_col:
        required_cols.append(size_col)

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"警告: 缺少列 {missing_cols}，无法创建散点图")
        return create_empty_plot(title)

    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        size=size_col,
        hover_name='up_name' if 'up_name' in df.columns else None,
        title=title,
        size_max=30
    )
    return fig


def create_bar_chart(df, x_col, y_col, title=""):
    """创建柱状图"""
    if x_col not in df.columns or y_col not in df.columns:
        print(f"警告: 缺少列 {x_col} 或 {y_col}，无法创建柱状图")
        return create_empty_plot(title)

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=title,
        text_auto='.2f'
    )
    return fig


def create_pie_chart(df, names_col, values_col, title=""):
    """创建饼图"""
    if names_col not in df.columns or values_col not in df.columns:
        print(f"警告: 缺少列 {names_col} 或 {values_col}，无法创建饼图")
        return create_empty_plot(title)

    pie_data = df[[names_col, values_col]].copy()
    pie_data = pie_data.dropna()

    fig = px.pie(
        pie_data,
        names=names_col,
        values=values_col,
        title=title
    )
    return fig


def create_pie_chart_from_series(series, title=""):
    """从Series创建饼图（用于value_counts结果）"""
    if series.empty:
        return create_empty_plot(title)

    pie_data = series.reset_index()
    pie_data.columns = ['category', 'count']

    fig = px.pie(
        pie_data,
        names='category',
        values='count',
        title=title
    )
    return fig


def create_time_series(df, date_col, value_cols, title=""):
    """创建时间序列图"""
    if date_col not in df.columns:
        return create_empty_plot(title)

    fig = go.Figure()

    for col in value_cols:
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df[date_col],
                y=df[col],
                name=col,
                mode='lines+markers'
            ))

    fig.update_layout(title=title)
    return fig


def create_empty_plot(title="暂无数据"):
    """创建空图表"""
    fig = go.Figure()
    fig.add_annotation(
        text=title,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=20)
    )
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    return fig