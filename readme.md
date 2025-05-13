# Function calling 实践

## 结构

agent_main.py 是agent的主要内容，运行这个文件即可
function_schema.json 是编写的函数结构json信息，向函数库中补充函数需要向这个文件中添加xinxi
generated.py 这是agent使用编写函数功能时默认的保存路径，这些默认路径是在指定函数的json结构中提供的description中的prompt提供的
prompt.md 有一些测试时使用到的一些prompt
tools.py 函数库中的函数的具体实现
excel_data.xlsx是通过tools中的函数随机生成的用于测试功能的excel文件。
