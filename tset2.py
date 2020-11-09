import time
import datetime
import numpy as np
import pandas as pd
from ib_insync import *

import time
import bokeh
bokeh.sampledata.download()
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from  bokeh.sampledata.stocks import MSFT
from bokeh.models import HoverTool
from math import pi

def Ibconnect():  # 检查网络链接
    for i in range(0, 30, 1):
        try:
            b = ib.connect('127.0.0.1', 7497, clientId=i, timeout=0.2)  # # 超时0.2秒,目的是连接不成功快速进行下一次尝试
            # print(b)
        except:
            print('尝试联网失败：clientId=%s' % (i))
        else:  # 联网成功
            # time.sleep(0.3)  # 等待测试连接超时，然后重新连接
            for j in range(i + 1, 30, 1):  # 重新建立一个连接
                try:
                    b = ib.connect('127.0.0.1', 7497, clientId=i, timeout=0)  # 由于测试连接0.2秒太短，需要重新设置连接超时时间保证后面的程序可以正常连接
                except:
                    print('尝试联网失败：clientId=%s' % (i))

                else:
                    print('联网成功：clientId=%s' % (j))
                    return True
def Get_Data(contract, dur, barsize, endTime):
    '''不设置结束时间'''
    # Price_Ag = ib.reqHistoricalData(
    #     contract, endDateTime='', durationStr=dur,
    #     barSizeSetting=barsize, whatToShow='MIDPOINT', useRTH=False)
    '''设置结束时间'''
    Price_Ag = ib.reqHistoricalData(
        contract, endDateTime=endTime, durationStr=dur,
        barSizeSetting=barsize, whatToShow='MIDPOINT', useRTH=False)

    df = util.df(Price_Ag)
    return df

if __name__ == '__main__':
    '''
             durationStr: Time span of all the bars. Examples:
                                '60 S', '30 D', '13 W', '6 M', '10 Y'.
                barSizeSetting: Time period of one bar. Must be one of:
                                '1 secs', '5 secs', '10 secs' 15 secs', '30 secs',
                                '1 min', '2 mins', '3 mins', '5 mins', '10 mins', '15 mins',
                                '20 mins', '30 mins',
                                '1 hour', '2 hours', '3 hours', '4 hours', '8 hours',
                                '1 day', '1 week', '1 month'.
            '''
    dur = '1 D'
    barsize1 = '1 min'
    barsize2 = '10 mins'
    endtime = ''
    # endtime = '20201103 12:00:00'
    # dur2 = '5 D'
    # barsize2 = '10 mins'
    # endtime2 = ''
    # endtime2 = '20200405 00:00:00'

    now = time.strftime("%Y%m%d%H%M%S", time.localtime())
    output_file("log_lines_%s.html"% (str(now)[0:17]))

    df=pd.DataFrame(MSFT)[:50]
    df['date']=pd.to_datetime(df['date'])
    inc=df.close>df.open
    dec=df.open>df.close
    open=np.array(df['open'])
    opem=open.tolist()
    w=23*60*3000#一天的时间用毫秒展示
    #工具条
    # 创建数据 → 包含四个标签
    hover = HoverTool(tooltips=[
        ("index", "$index"),
        ("open", "@opem"),
        ("high", "@high"),
        ("low", "@df.low"),
        ("close", "@df.close"),
        ("(x,y)", "($x, $y)"),
    ])
    # 设置标签显示内容
    # $index：自动计算 → 数据index
    # $x：自动计算 → 数据x值
    # $y：自动计算 → 数据y值
    # @A：显示ColumnDataSource中对应字段值
    TOOLS=[hover,'crosshair,pan,wheel_zoom,box_zoom,zoom_in, xzoom_in, yzoom_in,zoom_out, xzoom_out, yzoom_out,reset,save']
    TOOLTIPS=[(),(),]
    #画布
    # opts=dict(plot_width=1000,plot_height=50)
    p=figure(x_axis_type='datetime',tools=TOOLS,plot_width=1000,plot_height=650,title='Price',toolbar_location="below",
           toolbar_sticky=False)

    # 工具栏位置："above"，"below"，"left"，"right"
    #其它

    p.xaxis.major_label_orientation=pi/4
    p.grid.grid_line_alpha=0.3
    #绘图
    p.segment(df.date,df.high,df.date,df.low,color='black') #箱线图
    p.vbar(df.date[inc],w,df.open[inc],df.close[inc],fill_color='#F2583E',line_color='black')
    p.vbar(df.date[dec], w, df.open[dec], df.close[dec], fill_color='#D5E1DD', line_color='black')
    # p.line(x=df.date,y=df.high,legend='A',line_width=2)
    # 显示结果
    show(p)

