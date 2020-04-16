'''
服务端
'''

from socket import *
from multiprocessing import Process

ADDR = ("0.0.0.0", 8888)
user = {}


# 处理发送过来的姓名
def do_login(s, name, address):
    if name in user or "管理" in name :
        s.sendto("用户名已存在".encode(), address)
    else:
        s.sendto(b"OK", address)  # 如果不存在就往客户端发送ok来表示用户创建成功
        msg = "欢迎%s进入聊天室" % name
        for i in user:
            s.sendto(msg.encode(), user[i])
        user[name] = address  # 把创建成功的用户信息添加到字典中


# "C 张三 发送的消息"
def do_chat(s,name,text):
    msg = "\n%s : %s"%(name,text)#张三：发送的内容
    for i in user:#遍历字典得到name对号入座
        if i !=name:#发送给除自己意外的所有客户端
            s.sendto(msg.encode(),user[i])

#退出功能
def do_quit(s,name):
    #先删除字典内容,这样就不用在遍历字典的时候多加一个条件
    del user[name]
    msg = "\n%s退出聊天室"%name
    for i in user:#遍历字典,发送给所有人
        s.sendto(msg.encode(),user[i])

def do_sensitivity(s,name):
    msg = "%s发送的内容含有敏感词汇予以警告,超过三次则踢出群聊"%name
    for i in user:
        s.sendto(msg.encode(),user[i])






def requesit(s):
    while True:
        data, addr = s.recvfrom(1024)  # 接受参量（内容）
        tmp = data.decode().split(" ",2)  # 解析协议“L”,"name"
        # 总分结构-->根据不同类型的请求来做出相应的判断
        # L表示发送的姓名
        if tmp[0] == "L":
            do_login(s, tmp[1], addr)
        # C表示发送的内容
        elif tmp[0] == "C":
            # "C 张三 发送的消息"
            do_chat(s,tmp[1],tmp[2])
        # D表示退出
        elif tmp[0] == "Q":
            #“Q name”
            do_quit(s,tmp[1])
            # X表示敏感词
        elif tmp[0] == "X":
            do_sensitivity(s,tmp[1])




def manger(s):
    msg = input("管理员消息")
    msg = "C 管理员 "+msg
    s.sendto(msg.encode(),ADDR)







# 结构搭建
def main():
    # 创建套接字
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)
    print("dengdai.....")
    requesit(s)


    p = Process(target=requesit,args=(s,))
    p.start()
    manger(s)
    p.join()


if __name__ == '__main__':
    main()
