import streamlit as st
import pandas as pd

# 设置页面标题
st.title('关键词数据分析')

# 文件上传
uploaded_file = st.file_uploader("上传关键词 CSV 文件", type=["csv"])

if uploaded_file is not None:
    # 读取 CSV 文件
    df = pd.read_csv(uploaded_file)
    
    # 显示原始数据
    st.subheader("原始数据")
    st.write(df)

    # 根据 ABA 分组
    def categorize_aba(aba):
        if aba <= 50000:
            return '0-50000'
        elif 50000 < aba <= 100000:
            return '50000-100000'
        elif 100000 < aba <= 200000:
            return '100000-200000'
        else:
            return '>200000'
    
    df['ABA Group'] = df['ABA'].apply(categorize_aba)

    # 分组显示数据
    st.subheader("按 ABA 分组的数据")
    
    # 展示每个 ABA 组的数据
    for group in ['0-50000', '50000-100000', '100000-200000', '>200000']:
        st.write(f"**ABA 组: {group}**")
        st.write(df[df['ABA Group'] == group])

    # 筛选最具竞争力的关键词：ABA 高、CPC、Clicks Share、Conversion Share 低
    st.subheader("最具竞争力的关键词（按 CPC、Clicks Share、Conversion Share 排序）")
    
    competitive_keywords = df[(df['CPC'] != '-') & (df['Clicks Share'] != '-') & (df['Conversion Share'] != '-')]
    competitive_keywords = competitive_keywords.sort_values(by=['ABA', 'CPC', 'Clicks Share', 'Conversion Share'], ascending=[True, True, True, True])

    st.write(competitive_keywords[['Keywords', 'ABA', 'CPC', 'Clicks Share', 'Conversion Share']])
else:
    st.write("请上传一个 CSV 文件。")
