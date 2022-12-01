import talib as ta
from dataclasses import dataclass#, field


#获得均线
def get_ma(data,param_text):
    ma_param = param_text.split(',')
    ma_param = list(map(int, ma_param))
    num = 1
    for i in range(0, len(ma_param), 2): #步长为2 刚好 一个是周期 一个是类型
        data['ma%s' % num] = ta.MA(data.close, timeperiod=ma_param[i], matype=ma_param[i+1])
        num = num + 1
    return num-1 # 返回均线数量

#获得布林线
@dataclass()
class bollbands():
    title='布林线参数'
    present='输入：格式为:周期数,上线标准差倍数,下线标准差倍数,matype'
    showtype = {'bbs_up': 'line','bbs_mid': 'line','bbs_low': 'line'}
    def_param = '20,2,2,0'
    @staticmethod
    def get(data,param_text):
        bbands_param = param_text.split(',')
        bbands_param = list(map(int, bbands_param))
        data['bbs_up'], data['bbs_mid'], data['bbs_low'] = ta.BBANDS(data.close, timeperiod=bbands_param[0],
            nbdevup=bbands_param[1], nbdevdn=bbands_param[2], matype=bbands_param[3])  # 上中下轨

#主图指标
def indk(ind_name):
    if ind_name=='bollbands':
        return bollbands

@dataclass()
class adx():
    title = '平均趋向指数'
    present = '参数输入：格式为:周期数'
    showtype={'adx':'line'}
    def_param='14'
    @staticmethod
    def get(data, param_text):
        adx_param=int(param_text)
        data['adx'] = ta.ADX(data.high, data.low, data.close, timeperiod=adx_param)

@dataclass()
class adxr():
    title = '平均趋向指数的趋向指数'
    present = '参数输入：格式为:周期数'
    showtype={'adxr':'line'}
    def_param='14'
    @staticmethod
    def get(data, param_text):
        adxr_param=int(param_text)
        data['adxr'] = ta.ADXR(data.high, data.low, data.close, timeperiod=adxr_param)

@dataclass()
class aroon():
    title = '阿隆指标'
    present = '参数输入：格式为:周期数'
    showtype={'aroondown':'line','aroonup':'line'}
    def_param='14'
    @staticmethod
    def get(data, param_text):
        aroon_param=int(param_text)
        data['aroondown'], data['aroonup'] = ta.AROON(data.high, data.low, timeperiod=aroon_param)
    @staticmethod
    def showname1():
        return 'aroondown','aroonup'
@dataclass()
class aroonosc():
    title = '阿隆振荡'
    present = '参数输入：格式为:周期数'
    showtype={'aroonosc':'line'}
    def_param='14'
    @staticmethod
    def get(data, param_text):
        aroonosc_param=int(param_text)
        data['aroonosc'] = ta.AROONOSC(data.high, data.low, timeperiod=aroonosc_param)

@dataclass()
class cci():
    title = 'CCI顺势指标'
    present = '参数输入：格式为:周期数'
    showtype={'cci':'line'}
    def_param='14'
    @staticmethod
    def get(data, param_text):
        cci_param=int(param_text)
        data['cci'] = ta.CCI(data.high, data.low, data.close, timeperiod=cci_param)

@dataclass()
class cmo():
    title = '钱德动量摆动指标'
    present = '参数输入：格式为:周期数'
    showtype={'cmo':'line'}
    def_param='14'
    @staticmethod
    def get(data, param_text):
        cmo_param=int(param_text)
        data['cmo'] = ta.CMO(data.close, timeperiod=cmo_param)


@dataclass()
class dx():
    title = 'DX动向指标或趋向指标 DMI指标'
    present = '参数输入：格式为:周期数'
    showtype={'dx':'line'}
    def_param='14'
    @staticmethod
    def get(data, param_text):
        dx_param=int(param_text)
        data['dx'] = ta.DX(data.high, data.low, data.close, timeperiod=dx_param)

@dataclass()
class macd():
    title = '平滑异同移动平均线'
    present = '参数输入：格式为:快线ma周期,慢线ma周期,信号周期'
    showtype={'macd_DIFF':'line','macd_DEA':'line','macd_Hist':'bar'}
    def_param='12,26,9'
    @staticmethod
    def get(data, param_text):
        macd_param = param_text.split(',')
        macd_param = list(map(int, macd_param))
        data['macd_DIFF'], data['macd_DEA'], data['macd_Hist'] = ta.MACD(data.close,
            fastperiod=macd_param[0], slowperiod=macd_param[1],signalperiod=macd_param[2])
        
@dataclass()
class macdext():
    title = '具有可控MA类型的MACD'
    present = '参数输入：格式为:快线ma周期,matype,慢线ma周期,matype,信号周期,matype'
    showtype={'macdext_DIFF':'line','macdext_DEA':'line','macdext_Hist':'bar'}
    def_param='12,0,26,0,9,0'
    @staticmethod
    def get(data, param_text):
        macdext_param = param_text.split(',')
        macdext_param = list(map(int, macdext_param))
        data['macdext_DIFF'], data['macdext_DEA'], data['macdext_Hist'] = ta.MACDEXT(data.close, fastperiod=macdext_param[0], fastmatype=macdext_param[1],
              slowperiod=macdext_param[2], slowmatype=macdext_param[3], signalperiod=macdext_param[4],signalmatype=macdext_param[5])

@dataclass()
class mfi():
    title = 'MFI资金流量指标'
    present = '参数输入：格式为:周期数'
    showtype={'mfi':'line'}
    def_param='14'
    @staticmethod
    def get(data, param_text):
        mfi_param=int(param_text)
        data['mfi'] = ta.MFI(data.high, data.low, data.close, data.volume, timeperiod=mfi_param)

@dataclass()
class minus_di():
    title = 'MINUS_DI下升动向值(与DX相似)'
    present = '参数输入：格式为:周期数'
    showtype={'minus_di':'line'}
    def_param='14'
    @staticmethod
    def get(data, param_text):
        minus_di_param=int(param_text)
        data['minus_di'] = ta.MINUS_DI(data.high, data.low, data.close, timeperiod=minus_di_param)
@dataclass()
class minus_dm():
    title = 'minus_dm下升动向值(与DX相似)'
    present = '参数输入：格式为:周期数'
    showtype={'minus_dm':'line'}
    def_param='14'
    @staticmethod
    def get(data, param_text):
        minus_dm_param=int(param_text)
        data['minus_dm'] = ta.MINUS_DM(data.high, data.low, timeperiod=minus_dm_param)

@dataclass()
class mom():
    title = 'MOM上升动向值Momentum 动量'
    present = '参数输入：格式为:周期数'
    showtype={'mom':'bar'}
    def_param='10'
    @staticmethod
    def get(data, param_text):
        mom_param=int(param_text)
        data['mom'] = ta.MOM(data.close, timeperiod=mom_param)
        
@dataclass()
class ppo():
    title = '价格震荡百分比指数'
    present = '参数输入：格式为:快线ma周期,慢线ma周期,matype'
    showtype={'ppo':'line'}
    def_param='12,26,0'
    @staticmethod
    def get(data, param_text):
        ppo_param = param_text.split(',')
        ppo_param = list(map(int, ppo_param))
        data['ppo'] = ta.PPO(data.close,fastperiod=ppo_param[0], slowperiod=ppo_param[1],matype=ppo_param[2])

@dataclass()
class roc():
    title = '变动率指标 ((price/prevPrice)-1)*100'
    present = '参数输入：格式为:周期数'
    showtype={'roc':'line'}
    def_param='10'
    @staticmethod
    def get(data, param_text):
        roc_param=int(param_text)
        data['roc'] = ta.ROC(data.close, timeperiod=roc_param)

@dataclass()
class rsi():
    title = 'RSI相对强弱指数'
    present = '参数输入：格式为:周期数'
    showtype={'rsi':'line'}
    def_param='14'
    @staticmethod
    def get(data, param_text):
        rsi_param=int(param_text)
        data['rsi'] = ta.RSI(data.close, timeperiod=rsi_param)

@dataclass()
class stoch():
    title = 'Stochastic KDJ指标中的KD指标'
    present = '参数输入：格式为:快Kma周期,慢Kma周期,慢Kmatype,慢Dma周期,慢Dmatype'
    showtype={'slowk':'line','slowd':'line'}
    def_param='5,3,0,3,0'
    @staticmethod
    def get(data, param_text):
        stoch_param = param_text.split(',')
        stoch_param = list(map(int, stoch_param))
        data['slowk'], data['slowd'] = ta.STOCH(data.high, data.low, data.close, fastk_period=stoch_param[0],
            slowk_period=stoch_param[1], slowk_matype=stoch_param[2], slowd_period=stoch_param[3], slowd_matype=stoch_param[4])

@dataclass()
class ultosc():
    title = 'ULTOSC终极波动指标'
    present = '参数输入：格式为:周期数,周期数,周期数'
    showtype={'ultosc':'line'}
    def_param='7,14,28'
    @staticmethod
    def get(data, param_text):
        ultosc_param = param_text.split(',')
        ultosc_param = list(map(int,ultosc_param))
        data['ultosc'] = ta.ULTOSC(data.high, data.low, data.close, timeperiod1=ultosc_param[0], timeperiod2=ultosc_param[1], timeperiod3=ultosc_param[2])

@dataclass()
class adosc():
    title = 'ADOSC震荡指标'
    present = '参数输入：格式为:快ma周期,慢ma周期'
    showtype={'adosc':'line'}
    def_param='3,10'
    @staticmethod
    def get(data, param_text):
        adosc_param = param_text.split(',')
        adosc_param = list(map(int,adosc_param))
        data['adosc'] = ta.ADOSC(data.high, data.low, data.close, data.volume, fastperiod=adosc_param[0], slowperiod=adosc_param[1])

'''
没加进来的：APO - 绝对价格振荡器 BOP均势指标 PLUS_DI-Plus PLUS_DM-Plus ROC一系列指标 STOCH一系列指标 TRIX指标 WILLR威廉指标
希尔伯特变换 等其他指标
'''
def ind_at(ind_name):
    if ind_name=='adx':
        return adx
    elif ind_name=='adxr':
        return adxr
    elif ind_name=='aroon':
        return aroon
    elif ind_name=='aroonosc':
        return aroonosc
    elif ind_name=='cci':
        return cci
    elif ind_name=='cmo':
        return cmo
    elif ind_name=='dx':
        return dx
    elif ind_name=='macd':
        return macd
    elif ind_name=='macdext':
        return macdext
    elif ind_name=='mfi':
        return mfi
    elif ind_name=='minus_di':
        return minus_di
    elif ind_name=='minus_dm':
        return minus_dm
    elif ind_name=='mom':
        return mom
    elif ind_name=='ppo':
        return ppo
    elif ind_name=='roc':
        return roc
    elif ind_name=='rsi':
        return rsi
    elif ind_name=='stoch':
        return stoch
    elif ind_name=='ultosc':
        return ultosc
    elif ind_name=='adosc':
        return adosc


indk_list=['','bollbands']
ind_at_list=['','adx','adxr','aroon','aroonosc','cci','cmo','dx','macd','macdext','mfi','minus_di','minus_dm',
             'mom','ppo', 'roc','rsi','stoch','ultosc','adosc']


