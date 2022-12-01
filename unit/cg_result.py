
import pandas as pd
import numpy as np
def culretcum(data):
    # data['baseret'] = data['open'].pct_change().shift(-1)  #离散收益# 用开盘价 开盘买入开盘卖出 计算当天持有收益
    data['baseret'] = ( np.log(data['open'] / data['open'].shift(1)) ).shift(-1) #连续收益#开盘价计算出的return要往前移
    # data['baseret_cum'] = (data['baseret'] + 1).cumprod() #离散收益
    data['baseret_cum'] = data['baseret'].cumsum().apply(np.exp) #连续收益
    data['straret'] = data['baseret'] * data['signal']
    # data['straret_cum'] = (data['straret'] + 1).cumprod() #离散收益
    data['straret_cum'] = data['straret'].cumsum().apply(np.exp) #连续收益
    # 当收益率的数字很大的时候，np.exp(连续)和cumprod(离散)得出的结果差别很大！！国外用连续多 国内A股也有用离散的
    data = data[:-1]  # 把最后一天删去 因为最后一天没有下一天的开盘价 不能计算return
    return data
def magetall(datas, name,yeardays=251,downtime=True,pltshow=True):  # 获得策略相关信息完整版
    data = datas.copy()  # 不影响原来的数据，后面循环每次都要用原来的数据

    #     data.dropna(inplace=True)     #去掉空值，NaN  #在这个策略里不能用这个 因为有参数有空值
    baselastret = data['baseret_cum'].iloc[-1]  # 获得基准最终收益
    stralastret = data['straret_cum'].iloc[-1]  # 获得策略最终收益
    extrlastret = stralastret - baselastret  # 最终超额收益

    baseyrisk = data['baseret'].std() * (yeardays ** 0.5)  # 基准年化风险
    strayrisk = data[data['signal'] != 0]['straret'].std() * (yeardays ** 0.5)  # 策略年化风险 仅计算持仓时间内

    baseannualret = baselastret ** (yeardays / len(data)) - 1  # 基准年化收益率
    if len(data[data['signal'] != 0]) !=0:  # 这是为了防止分母是0报错
        straannualret = stralastret ** (yeardays / len(data[data['signal'] != 0])) - 1  # 策略年化收益率 仅计算持仓时间内
    else:  # 没有信号的情况下收益就是0
        straannualret = 0

    sharperatio = (straannualret - 0.03) / strayrisk  # 夏普比率,设r=0.03

    data['cummax'] = data['straret_cum'].cummax()  # 计算累计最大值，用于计算回撤
    data['drawdown'] = (data['cummax'] - data['straret_cum']) / data['cummax']  # 计算回撤百分比
    if downtime==True:
        print('最大回撤发生时间：' + data.iloc[data[['drawdown']].idxmax(axis=0)]['Datetime'].values[0])  #打印出发生最大回撤的时间
    maxdrawdown = data['drawdown'].max()  # 最大回撤 从最高点跌到反弹回原位之前的最低点的最大百分比

    # 计算胜率和完整交易次数
    totaltradenum = 0
    winnum = 0
    lastopennum = 0
    for i in range(len(data)):
        if '-q' not in data.loc[i, 'remark'] and data.loc[i, 'remark'] != '' and lastopennum == 0:  # 开仓位置
            opennum = i
            lastopennum = opennum
        #         print(1)
        if data.loc[i, 'remark'] == '-q':  # 平仓位置
            totaltradenum = totaltradenum + 1
            lastopennum = 0
            #         print(i,opennum-1)
            if data.loc[i, 'straret_cum'] > data.loc[opennum - 1, 'straret_cum']:  # 盈利的位置
                winnum = winnum + 1
        elif '-q' in data.loc[i, 'remark']:  # 仅持仓一天的位置
            totaltradenum = totaltradenum + 1
            lastopennum = 0
            #             print(3)
            if data.loc[i, 'straret_cum'] > data.loc[i - 1, 'straret_cum']:  # 盈利的位置 今天的净值大于昨天的净值
                winnum = winnum + 1
    if winnum !=0 and  totaltradenum !=0:
        winrate = winnum / totaltradenum
    else:
        winrate = 0
    result = {'策略净值': stralastret, '基准净值': baselastret, '超额收益': extrlastret, '持仓夏普比率': sharperatio,
              '持仓年化收益': straannualret,
              '基准年化收益': baseannualret, '持仓年化风险': strayrisk, '基准年化风险': baseyrisk,
              '实时最大回测': maxdrawdown, '策略胜率': winrate, '完整交易次数': totaltradenum}

    result = pd.DataFrame(result, index=[name]).round(4)  # 字典转成df 不设置index会出错

    data['Datetime'] = pd.to_datetime(data['Datetime'])  # 前面先不用 影响策略的循环，循环数量会增大。现在才用 方便画图
    data.set_index('Datetime', inplace=True)  # 现在才用 方便画图
    if pltshow==True:
        data[['baseret_cum', 'straret_cum']].plot(figsize=(18, 6), title=name)  # 画出收益图
        data[['straret_cum', 'cummax']].plot(figsize=(18, 6), title=name)  # 画出回撤图
    # plt.show()  	#把前面画的图像显示出来
    return result

