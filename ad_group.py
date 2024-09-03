import pandas as pd
import streamlit as st

# 设置网页标题
st.title("SKU Performance Analysis")

# 文件上传
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # 读取上传的文件
    data = pd.read_csv(uploaded_file)

    # 计算转化率和表现指标
    data['Conversion_Rate'] = data['Orders'] / data['Clicks']
    data['Performance'] = data['CTR'] * data['Conversion_Rate'] / data['ACOS']

    # 设定阈值
    high_performance_threshold = data['Performance'].quantile(0.75)
    low_performance_threshold = data['Performance'].quantile(0.25)

    # 分类函数
    def classify_performance(row):
        if row['Performance'] >= high_performance_threshold:
            return 'High Performance'
        elif row['Performance'] <= low_performance_threshold:
            return 'Low Performance'
        else:
            return 'Medium Performance'

    # 应用分类
    data['Group'] = data.apply(classify_performance, axis=1)

    # 显示结果表格
    st.write("Classified Data")
    st.dataframe(data[['SKU', 'ASIN', 'CTR', 'Conversion_Rate', 'ACOS', 'Group']])

    # 提供下载选项
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button("Download Classified Data", csv, "classified_data.csv", "text/csv")
