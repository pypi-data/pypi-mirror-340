from market_listener import MarketListener
from kingstar_client import KingstarClient
import time

class MyMarketListener(MarketListener): #继承监听器
    def on_subscribe_tick_data(self,flow_no):
        print('成功订阅了行情！')
    def on_tick(self,flow_no,ticks): #返回的tick，也是个实体类
        for tick in  ticks: #
            print(flow_no,tick.gtick2json())


if __name__ == "__main__":
    client = KingstarClient("ws://10.74.16.48:20002", "kingstar", "kingstar") #初始化
    client.add_listener(MyMarketListener()) #注册获取数据的回调类
    client.connect()  # 登陆，有自动重登机制，但是不会自动重新订阅

    client.subscribe_tick('SHFE','Future',['ag2506','ag2508']) # 订阅，入参为这3项必填，合约代码可传数组
    # client.subscribe_tick('SHFE', 'Future', 'ag2508')
    time.sleep(10)
    # client.close()
    client.unsubscribe_tick('SHFE','Future',['ag2506','ag2508'])
    while True: # 整个订阅机制都是子线程运行，如果需要持续接收tick，主线程需要手动维持运行
        time.sleep(1)