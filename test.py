import sys
import os
import signal
import uvicorn
from fastapi import FastAPI

class WebServer():

    app = FastAPI(title = 'Agnet WebServer', description = 'Agnet WebServer 接口文档', version='v1.0.0')
    queue = None

    # 启动
    def run(queue = None):

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
        #WebServer.queue.put(5500)

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


def run2(queue):
    sys.exit(WebServer.run(queue))

def main():
    run2(None)

    #print('QT结束')

    #os.kill(os.getpid(), signal.CTRL_C_EVENT)

    #p2.close()

    print('结束测试')


if __name__ == '__main__':

    # parser = argparse.ArgumentParser(description='')
    # parser.add_argument("-c", "--contract", required=True, help="contract address")
    # known_args = parser.parse_args()
    #multiprocessing.freeze_support()
    #f = open('a.txt', 'w')
    # sys.stdout = os.devnull
    # sys.stderr = os.devnull
    #os.devnull
    sys.exit(main())
