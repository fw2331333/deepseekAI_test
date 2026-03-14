# 打开文件
f = open("./resources/test.txt","r",encoding="utf-8") # ./可省略

# 读取文件

content = f.read()
print(content)

# con = f.readlines()
# for i in con:
#     print(i)

# 关闭文件
f.close()

# 写文件
f1 = open("./resources/test.txt","w",encoding="utf-8")
try:
    # 写入内容
    f1.write("测试内容1\n")
    f1.write("测试内容2\n")
    f1.write("测试内容3\n")

finally:
    f1.close()

with open("./resources/test.txt","r",encoding="utf-8") as f2:
    content1 = f2.read()
    print(content)