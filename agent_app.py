import sys
import os
import signal
import uvicorn
import multiprocessing
from multiprocessing import Queue,Process
from PyQt5 import QtWidgets,QtCore,QtGui    # pip3 install PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *      # pip install PyQtWebEngine
from fastapi import FastAPI

class AgentClient(QMainWindow,):
    def __init__(self, url):
        super(AgentClient, self).__init__()
        self.setWindowTitle('Agent App')
        self.resize(1350,720)
        #self.setWindowIcon(QtGui.QIcon('./static/favicon.png'))
        
        self.browser = QWebEngineView()
        #Url = f'http://127.0.0.1:{port}/?apiKey=03AB7BAF-3E9C-4A54-9CE6-55741A8C98C8&custNo=00000'
        self.browser.setUrl(QtCore.QUrl(url))

        self.setCentralWidget(self.browser)

class WebServer():

    app = FastAPI(title = 'Agnet WebServer', description = 'Agnet WebServer 接口文档', version='v1.0.0')
    queue = None

    # 启动
    def run(queue : Queue = None):

        # 开启服务
        host = '127.0.0.1'
        port = 5500

        WebServer.queue = queue

        uvicorn.run(WebServer.app, host = host, port = port)
    
    # 添加在应用程序启动之前运行的函数
    @app.on_event("startup")
    async def startup_event():
        print("启动应用程序啦")
        # 进程间通信-消息队列
        WebServer.queue.put(5500)

    # 下载订单模板
    @app.get("/index", tags=['订单'])
    def order_download_template():
        # file_path = '../templates/Bulk Payout Template.xlsx'
        # filename = 'Bulk Payout Template.xlsx'
        # return FileResponse(path=file_path, filename=filename)

        return {
            "ret" : 0,
            'msg' : 'success'
        }

    
def run1(queue : Queue, pid : int):
    port = queue.get(True)

    url = f'http://127.0.0.1:{port}/index'
    #url = 'http://www.baidu.com'
    app = QApplication(sys.argv)
    gui = AgentClient(url)
    gui.show()
    #sys.exit(app.exec_())
    app.exec_()
    
    print('QT结束')
    os.kill(os.getpid(), signal.CTRL_C_EVENT)

def run2(queue):
    sys.exit(WebServer.run(queue))

def main():
    # 队列
    queue = Queue()

    p = Process(target=run1,args=(queue, os.getpid()))
    p.start()

    run2(queue)

    #print('QT结束')

    #os.kill(os.getpid(), signal.CTRL_C_EVENT)

    #p2.close()

    print('结束测试')


if __name__ == '__main__':

    # parser = argparse.ArgumentParser(description='')
    # parser.add_argument("-c", "--contract", required=True, help="contract address")
    # known_args = parser.parse_args()
    multiprocessing.freeze_support()
    sys.exit(main())
