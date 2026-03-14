import  json

# 写入json文件
data = {"name":"张三",
        "age":18,
        "sex":"男",
        "hobbies":["football","swimming"]
}
with open("./resources/data.json","w",encoding="utf-8") as f:
    # ensure_ascii=False : 默认输出为True，确保输出ascii编码；设置成False，输出为中文
    # indent=4 : 缩进4个空格
    json.dump(data,f,ensure_ascii=False,indent=4)

# 读取json文件
with open("./resources/data.json","r",encoding="utf-8") as f:
    data = json.load(f)
    print(data)
    print(type(data))