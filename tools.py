import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
import requests
import os
from urllib.parse import quote
rcParams['font.sans-serif'] = ['SimHei']

def handle_excel(excel_path, subject, save_path=None)->str:
    '''
    处理Excel文件，绘制指定科目的成绩分布饼图
    :param excel_path: Excel文件路径
    :param subject: 科目名称
    :param save_path: 保存路径，默认为None，表示不保存
    '''
    def get_score_distribution(df, subject):
        if subject not in df.columns:
            raise ValueError(f"科目 '{subject}' 不存在于 Excel 表中")

        scores = df[subject].dropna()
        bins = [0, 60, 70, 80, 90, 100]
        labels = ['0-59', '60-69', '70-79', '80-89', '90-100']
        distribution = pd.cut(scores, bins=bins, labels=labels, include_lowest=True)
        counts = distribution.value_counts().sort_index()
        return counts
    
    def draw_pie_chart(counts, subject,save_path=None):
        plt.figure(figsize=(6, 6))
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140)
        plt.title(f"{subject}成绩分布饼图")
        plt.axis('equal')
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, format='png')
        else:
            plt.show()

    df = pd.read_excel(excel_path)
    counts = get_score_distribution(df, subject)
    draw_pie_chart(counts, subject, save_path=save_path)

    message = f"科目 '{subject}' 的成绩分布已绘制为饼图"
    if save_path:
        message += f"，并保存至 {save_path}"
    else:
        message += "，请查看图表"
    return message

def generate_random_scores_excel(filename="excel_data.xlsx", num_students=100, random_seed=42):
    np.random.seed(random_seed)

    subjects = ['数学', '语文', '英语', '物理', '化学', '生物', '历史', '地理', '政治']
    data = {}

    for subject in subjects:
        # 生成 0-100 之间的随机成绩，并四舍五入为整数
        data[subject] = np.random.randint(40, 101, size=num_students)

    df = pd.DataFrame(data)
    df.index = [f"学生{i+1}" for i in range(num_students)]
    df.to_excel(filename, index_label="姓名")
    print(f"模拟成绩文件已保存为：{filename}")

def write_file(filename:str, code:str)->str:
    '''
    根据给定的json数据编写python源文件，编写函数完成用户要求的功能
    :param filename: 需要编辑的文件名
    :param code: 需要写入的代码内容
    '''
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
    return f"{filename} written successfully."
 

def call_function(filename, function_name, param_list)->str:
    '''
    调用指定的函数
    :param filename: 文件名
    :param function_name: 函数名称
    :param param_list: 被调用函数使用的参数列表
    '''
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location("module.name", filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        func = getattr(module, function_name)
        result = func(*param_list)

        if isinstance(result, np.generic):
            result = result.item()  # 转换为 Python 原生类型
        return f"Function '{function_name}' called successfully. Result: {result}"
    except Exception as e:
        return f"Error calling function '{function_name}': {e}"

def get_weather(city_name: str) -> str:
    # 从 weather_api.txt 文件中读取 API 密钥
    try:
        with open("weather_api.txt", "r", encoding="utf-8") as file:
            api_key = file.read().strip()
    except FileNotFoundError:
        return "无法找到 weather_api.txt 文件，请确保文件存在并包含 API 密钥。"
    
    city_name = quote(city_name)  # 对城市名称进行 URL 编码
    def get_id(location, ):

        url = f"https://nn44u8xkum.re.qweatherapi.com/geo/v2/city/lookup?location={location}&key={api_key}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data.get("code") == "200":
            return data["location"][0]["id"]
        else:
            raise Exception(f"无法获取城市ID：{data.get('code')}")

    def get_weather_by_id(location_id):
        url = f"https://nn44u8xkum.re.qweatherapi.com/v7/weather/now?location={location_id}&key={api_key}"
        response = requests.get(url)
        data = response.json()

        if data.get("code") != "200":
            return f"无法获取 '{city_name}' 的天气信息。"

        weather_info = data["now"]
        weather = weather_info["text"]
        temp = weather_info["temp"]
        feels_like = weather_info["feelsLike"]
        wind_dir = weather_info["windDir"]

        return (
            f"{city_name} 当前天气：{weather}，气温：{temp}°C，"
            f"体感温度：{feels_like}°C，风向：{wind_dir}。"
            
        )
    
    return get_weather_by_id(get_id(city_name))

if __name__ == "__main__":
    # json_data = {
    #     "filename": "generated.py",
    #     "functions": [
    #         {
    #         "name": "sub",
    #         "params": ["a", "b"],
    #         "body": "print( a + b)\n"
    #         }
    #     ]
    # }
    # generate_file(json_data["filename"], json_data["functions"])
    print(call_function("generated.py", "process_excel", ["excel_data.xlsx", "数学"]))