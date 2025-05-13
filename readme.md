# Function calling 实践

## 结构

agent_main.py 是agent的主要内容，运行这个文件即可

function_schema.json 是编写的函数结构json信息，向函数库中补充函数需要向这个文件中添加xinxi

generated.py 这是agent使用编写函数功能时默认的保存路径，这些默认路径是在指定函数的json结构中提供的description中的prompt提供的

prompt.md 有一些测试时使用到的一些prompt

tools.py 函数库中的函数的具体实现

excel_data.xlsx是通过tools中的函数随机生成的用于测试功能的excel文件。

## 说明

agent中使用的模型API接口内置在我的环境变量中，如果要使用这个agent需要前往[火山引擎文档](https://www.volcengine.com/docs/82379/)中注册账号并获取API，然后打开对应模型的服务。

天气查询函数中的API保存在我没有上传到git的txt文件中。若需要使用可以在[Qweather和风天气文档](https://dev.qweather.com/docs/)中按照指引获取api，
