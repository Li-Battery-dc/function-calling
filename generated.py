# 导入所需的库
import pandas as pd


def calculate_correlation(excel_path, subject):
    # 读取 Excel 文件
    df = pd.read_excel(excel_path)
    
    # 筛选出数值列
    numeric_df = df.select_dtypes(include='number')
    
    # 检查指定科目是否存在于数值列中
    if subject not in numeric_df.columns:
        print(f'指定的科目 {subject} 不存在于数值数据中。')
        return None
    
    # 计算指定科目与其他数值列的相关系数
    correlations = numeric_df.corr()[subject]
    
    return correlations
