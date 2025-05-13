from openai import OpenAI
import os
import json
import time
import numpy as np
from tools import handle_excel, write_file, call_function, get_weather

# 具体使用的API已经被保存在了我的环境变量中
client = OpenAI(
    api_key=os.environ.get("ARK_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)
model = "doubao-1-5-pro-32k-250115"

# 初始化system prompt
messages = [
    {
        "role": "system",
        "content": "你是一个智能助手，你应该完成用户的要求。如果用户要求你编写或调用函数来完成这个任务，你可以调用这些函数，否则不要这么做。",
    }
]
with open("function_schema.json", "r", encoding="utf-8") as file:
    schemas = json.load(file)

handle_excel_schema = schemas["handle_excel_schema"]
write_file_schema = schemas["write_file_schema"]
call_func_schema = schemas["call_function_schema"]
get_weather_schema = schemas["get_weather_schema"]
tools = [
    handle_excel_schema,
    write_file_schema,
    call_func_schema,
    get_weather_schema
]
available_tools = {
    "handle_excel": handle_excel,
    "write_file": write_file,
    "call_function": call_function,
    "get_weather": get_weather,
}

def main():
    while True:
        prompt = input("我能帮你做什么？(exit退出)\n")
        if prompt.lower() == "exit":
            break
        messages.append({"role": "user", "content": prompt})

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.8,
            tools=tools,
        )

        response = completion.choices[0].message

        if response.tool_calls:
            messages.append(response)

            for tool_call in response.tool_calls: 
                args = json.loads(tool_call.function.arguments)
                func_name = tool_call.function.name
                if func_name == "write_file":
                    print("调用了write_file函数")
                    messages.append(
                        {
                            "role" : "system",
                            "content": "注意你在调用write_file函数的时候要保证写入的内容是一个可以运行的函数，不要包含'''python '''这样的显示格式内容。如果需要写入多个函数，将它们内嵌在一个main函数中，例如def main(params):\n    def fun1():\n   def fun2:\n ...:main函数的主要逻辑"
                        }
                    )
                elif func_name == "call_function":
                    print("调用了call_function函数")
                elif func_name == "handle_excel":
                    print("调用了handle_excel函数")
                elif func_name == "cal_corrlation":
                    print("调用了cal_corrlation函数")
                elif func_name == "get_weather":
                    print("调用了get_weather函数")
                res = available_tools[func_name](**args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": res,
                    "name": tool_call.function.name,
                })

            final_response = client.chat.completions.create(
                model=model,
                messages=messages,
            ).choices[0].message.content
            messages.append({
                "role": "assistant",
                "content": final_response,
            })
            print(final_response)

        else:
            print(response.content)
            messages.append({
                "role": "assistant",
                "content": response.content,
            })

if __name__ == "__main__":
    main()
