"""
ftp 客户端
c/s模式   发送请求 获取结果
"""

from socket import *
from time import sleep

ADDR = ('127.0.0.1',8800)

class FTPClient:
    def __init__(self,sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b'L') # 发送请求
        # 等待回复 YES NO
        data = self.sockfd.recv(128).decode()
        if data == "YES":
            # 接收文件列表
            data = self.sockfd.recv(4096)
            print(data.decode())
        else:
            print("获取文件列表失败")


    #处理下载文件
    def do_get(self,filename):
        #G filename -->文件格式
        data = "G "+filename#发送自定协议
        self.sockfd.send(data.encode())
        data = self.sockfd.recv(120)
        #如果发送过来的是yes就写入文件
        if data.decode() == "YES":
            f = open(filename,"wb")
            while True:
                data, = self.sockfd.recv(1024)
                #给文件最后发送一个标识符用于服务端结束循环
                if data == b"##":
                    f.write(data)

        else:
            print("文件不存在")


    def do_put(self,filename):
        #破获一个错误，如果文件不错在或者输入了其他内容就同一回复
        try:
            f= open(filename,"wb")
        except:
            print("上传文件不存在")
            return
        #在输入的时候可以添加任何路径
        filename = filename.split("/")[-1]
        data = "P "+filename
        self.sockfd.send(data.encode())#发送请求
        data = self.sockfd.recv(120).decode()#等待回复
        if data == "YES":
            while True:
                data = f.read(1024)
                if not data:
                    sleep(0.1)
                    self.sockfd.send(b"##")
                    break
                self.sockfd.send(data)
            f.close()

        else:
            print("文件已存在")





# 链接服务端
def main():
    s = socket()
    s.connect(ADDR)

    # 实例化对象
    ftp = FTPClient(s)

    while True:
        print("================命令选项==================")
        print("=======          list                ===")
        print("=======         get file             ===")
        print("=======         put file             ===")
        print("=======          quit                ===")
        print("=========================================")

        cmd = input("请输入命令:")
        if cmd == "list":
            ftp.do_list()

        if cmd[:3] == "get":
            filename = cmd.split(" ")[-1]
            ftp.do_get(filename)

        if cmd[:3] == "put":
            filename = cmd.split(" ")[-1]
            ftp.do_put(filename)


if __name__ == '__main__':
    main()