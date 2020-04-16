'''
客户段
'''

from socket import *
from multiprocessing import Process
import sys

ADDR = ("0.0.0.0", 8888)


# 接收消息
def recv_msg(s):
    while True:
        data, addr = s.recvfrom(6666)
        print(data.decode()+"\n发言",end="")  # 打印字符窜


def send_msg(s, name):  # name参数用来匹配服务端字典这样节省服务端循环便利
    count = 0
    while True:
        try:
            msg = input("发言:")
        except KeyboardInterrupt:  # 在强制退出的时候也可以正常打印退出内容
            msg = "quit"
        if msg == "quit":
            # 拼接 “Q name”
            q_msg = "Q " + name
            s.sendto(q_msg.encode(), ADDR)
            # 关闭进程
            sys.exit("退出聊天室")

        elif msg == "给力":

            x_msg = "X "+name
            s.sendto(x_msg.encode(),ADDR)
            count += 1
            if count == 3:
                sys.exit("您已被踢出聊天室")



        # s_msg --->"C 张三 发送的消息"
        s_msg = "C %s %s" % (name, msg)
        s.sendto(s_msg.encode(), ADDR)


def main():
    s = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input("请输入姓名:")
        msg = "L " + name  # 定协议L表示发送姓名请求
        s.sendto(msg.encode(), ADDR)
        data, addr = s.recvfrom(120)
        if data.decode() == "OK":
            print("您已进入聊天室")
            break
        else:
            print("%s名字已存在" % data.decode())

    # 创建套接字父进程处理发送消息，子进成处理接收消息
    p = Process(target=recv_msg, args=(s,))
    p.daemon = True  # 父子进程同时退出
    p.start()  # 启动进程

    send_msg(s, name)  # 发送消息


if __name__ == '__main__':
    main()
