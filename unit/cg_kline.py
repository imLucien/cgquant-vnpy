#画出K线图和开平仓点位
from pyecharts.charts import Kline,Line,Scatter,Bar,Grid
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
import pandas as pd

# 有哪些：
# 查看期货行情K线图.ipynb 单K  搞定
# 查看期货行情K线图_jq.   K加交易量   搞定
# 玉米_多均线多策略组合系统  K加一个指标
# 黄金多均线多空策略   K加开平仓有策略分类标签
# btc多均线多头策略  K加开平仓加一个指标
# 五虎上将 沪深300.   K加开平仓加Y轴标签

#输入的：Datetime、高开低收都是首字母小写 均线：ma1 ma2等  没设置索引
#修改py包 notebook要退出重新打开才会生效

class drawkline():
	def __init__(self,data,name):  #参数好像不能用布尔值 会报错 所以用0和1
		self.data=data
		self.klinedate = data["Datetime"].apply(lambda x: str(x)).tolist()
		self.k_plot_value = data.apply(lambda record: [record['open'], record['close'], record['low'], record['high']],axis=1).tolist()
		self.name=name
		#.set_global_opts这个函数必须一次性把全部参数带进去，不带进去的就无效了,所以设置这么多参数
		self.init_opts=opts.InitOpts(width='990px', height='500px')
		self.yaxis_opts=opts.AxisOpts(is_scale=True, splitarea_opts=opts.SplitAreaOpts(areastyle_opts=opts.AreaStyleOpts(opacity=1)))
		self.xaxis_opts = opts.AxisOpts(is_scale=True, )
		self.title_opts = opts.TitleOpts(title="走势图")
		self.toolbox_opts = opts.ToolboxOpts()
		self.tooltip_opts = opts.TooltipOpts(
			trigger="axis", trigger_on="click", axis_pointer_type="cross",
			background_color="rgba(245, 245, 245, 0.8)",
			border_width=1, border_color="#ccc", textstyle_opts=opts.TextStyleOpts(color="#000"))
		self.brush_opts=opts.BrushOpts(x_axis_index="all", brush_link="all",
										  out_of_brush={"colorAlpha": 0.1}, brush_type="lineX", )
		self.axispointer_opts = opts.AxisPointerOpts(is_show=True, link=[{"xAxisIndex": "all"}],
			label=opts.LabelOpts(background_color="#777"), ) #设置坐标轴相互联动

		# 基本K线
		self.kline = (
			Kline(init_opts=self.init_opts)  # 设置图像大小
				.add_xaxis(self.klinedate).add_yaxis(self.name, self.k_plot_value)  # 显示的名称
		)

#主图 得到均线
	def drawma(self,num):
		# 均线
		ind_ma = (Line().add_xaxis(self.klinedate))
		for i in range(num):
			if i == 0:
				ind_ma.add_yaxis("ma%s" % (i + 1), self.data['ma%s' % (i + 1)], is_smooth=False,label_opts=opts.LabelOpts(is_show=False),
					is_hover_animation=False, )  # linestyle_opts=opts.LineStyleOpts(width=1, opacity=0.5)
			else:
				ind_ma.add_yaxis("ma%s" % (i + 1), self.data['ma%s' % (i + 1)], is_smooth=False,is_symbol_show=False)
		return ind_ma

#主图 在K线上画的指标
	def draw_indk(self,param_dict:dict):
		allunits = []  # 把画出来的各个单元都一起存到列表里
		for name, type in param_dict.items():
			if type=='line':
				line=(Line().add_xaxis(self.klinedate))
				line.add_yaxis(name, self.data[name], is_smooth=False,is_symbol_show=False)
				allunits.append(line)
		for i in range(len(allunits)):
			if i > 0:
				allunits[0].overlap(allunits[i])
		return allunits[0]  # 全部叠加到第一个上面

#主图核心 把各个图一起组合成主图
	def overlapkline(self,*args):
		for arg in args:
			self.kline.overlap(arg)
		return self.kline

# 画出仅有主图无副图的K线
	def kline_master(self,overlapkline):
		self.kline.set_global_opts(
			yaxis_opts=self.yaxis_opts,
			xaxis_opts=self.xaxis_opts,
			title_opts=self.title_opts,
			toolbox_opts=self.toolbox_opts,
			tooltip_opts=self.tooltip_opts,
			# 提示框配置项 ，点击显示十字光标
			brush_opts=self.brush_opts,  # 这是区域选择工具
			datazoom_opts=[opts.DataZoomOpts(is_show=False,type_="inside",xaxis_index=[0],range_start=90,range_end=100,),
						   opts.DataZoomOpts(is_show=True,type_="slider",xaxis_index=[0],range_start=90,range_end=100,)],
		) #slider是底下的移动边的意思，要增加才有的
		# klinemaster = overlapkline
		return overlapkline  #外部运用的时候再决定是render还是render_notebook

#副图 基础的画一个bar
	def _drawbar(self,barname):
		bar = (
			Bar()
				.add_xaxis(xaxis_data=self.klinedate)
				.add_yaxis(series_name=barname, yaxis_data=self.data[barname].apply(lambda x: str(x)).tolist(),
						   xaxis_index=1, yaxis_index=1, label_opts=opts.LabelOpts(is_show=False), )
				.set_global_opts(
				xaxis_opts=opts.AxisOpts(type_="category", is_scale=True, grid_index=1, boundary_gap=False,
										 axisline_opts=opts.AxisLineOpts(is_on_zero=False),
										 # X 轴或者 Y 轴的轴线是否在另一个轴的 0 刻度上，只有在另一个轴为数值轴且包含 0 刻度时有效
										 axistick_opts=opts.AxisTickOpts(is_show=False),  # 是否显示坐标轴刻度
										 # splitline_opts=opts.SplitLineOpts(is_show=False),#是否显示分割线 默认False
										 axislabel_opts=opts.LabelOpts(is_show=False),  # 是否显示标签
										 split_number=20, min_="dataMin", max_="dataMax",
										 ),
				yaxis_opts=opts.AxisOpts(
					grid_index=1, is_scale=True, split_number=2,
					axislabel_opts=opts.LabelOpts(is_show=False),
					axisline_opts=opts.AxisLineOpts(is_show=False),
					axistick_opts=opts.AxisTickOpts(is_show=False),
					# splitline_opts=opts.SplitLineOpts(is_show=False),
				),
				legend_opts=opts.LegendOpts(is_show=False),
			)
		)
		return bar

#副图 基础的画一条line
	def _drawline(self,linename):
		line = (
			Line()
				.add_xaxis(self.klinedate)
				.add_yaxis(linename, self.data[linename], xaxis_index=1, yaxis_index=1, is_symbol_show=False)
				.set_global_opts(
				xaxis_opts=opts.AxisOpts(
					is_scale=True,
					grid_index=1,
					axislabel_opts=opts.LabelOpts(is_show=False),
				),
				yaxis_opts=opts.AxisOpts(
					grid_index=1,
					is_scale=True,
				), legend_opts=opts.LegendOpts(is_show=False)
			)
		)
		return line

#主图 得到开平仓散点图 # 注意 需要 先overlap平仓再overlap开仓；这样同样位置开仓才能把平仓覆盖
	def makeocpos(self):
		# 开仓位置
		tradedate = self.data[(self.data['remark'] != '-q') & (self.data['remark'] != '')]["Datetime"].apply(
			lambda x: str(x)).tolist()  # df不能用not in
		tradeopen = self.data[(self.data['remark'] != '-q') & (self.data['remark'] != '')][
			['open', 'remark']].values.tolist()  # (data['remark'] != '-q')
		tradepos = (
			Scatter()
				.add_xaxis(tradedate)
				.add_yaxis('开仓', tradeopen,
						   label_opts=opts.LabelOpts(formatter=JsCode("function(params){return params.value[2];}")),
						   itemstyle_opts=opts.ItemStyleOpts(color='green', border_color='white'))
		)  # 散点的y轴必须是list.

		# 平仓位置 要少一天
		closedata = pd.DataFrame(columns=['Datetime','open'])
		for i in range(len(self.data) - 1):
			if '-q' in self.data.loc[i, 'remark']:
				closedata.loc[i + 1, 'Datetime'] = self.data.loc[i + 1, 'Datetime']
				closedata.loc[i + 1, 'open'] = self.data.loc[i + 1, 'open']
		closedate = closedata["Datetime"].apply(lambda x: str(x)).tolist()
		tradeclose = closedata['open'].tolist()
		closepos = (
			Scatter()
				.add_xaxis(closedate)
				.add_yaxis('平仓', tradeclose, label_opts=opts.LabelOpts(is_show=False),
						   itemstyle_opts=opts.ItemStyleOpts(color='blue'))
		)
		return tradepos,closepos

#副图 画一个基类单元 bar或者line
	def draw_unit(self,unit_name,unit_type) :
		if unit_type=='line':
			return self._drawline(unit_name)
		elif unit_type=='bar':
			return self._drawbar(unit_name)

#副图 画单个指标
	def draw_indicator(self,param_dict:dict):
		'''
		:param param_dict: {'macd_DIFF':'line','macd_DEA':'line','macd_Hist':'bar'}
		:return: 准备展示的图形
		'''
		allunits=[] #把画出来的各个单元都一起存到列表里
		for name,type in param_dict.items():
			allunits.append(self.draw_unit(name,type))
		for i in range(len(allunits)):
			if i>0:
				allunits[0].overlap(allunits[i])
		return allunits[0] #全部叠加到第一个上面


#画带一个副图的K线 即带一个指标
	def kline_ind1(self,overlapkline,indicator):
		'''
		:param indicator: 函数draw_indicator
		:return: 组合图形
		'''
		# 加一个副图的参数
		self.datazoom_opts1 = [
			opts.DataZoomOpts(is_show=False, type_="inside", xaxis_index=[0, 1], range_start=90, range_end=100, ),
			opts.DataZoomOpts(is_show=True, xaxis_index=[0, 1], type_="slider", pos_top="90%", range_start=90,range_end=100, ), ]

		self.kline.set_global_opts(
			yaxis_opts=self.yaxis_opts,
			xaxis_opts=self.xaxis_opts,
			title_opts=self.title_opts,
			toolbox_opts=self.toolbox_opts,
			tooltip_opts=self.tooltip_opts,
			brush_opts=self.brush_opts,
			datazoom_opts=self.datazoom_opts1,
			axispointer_opts=self.axispointer_opts,
			# 这个的作用是使得上下两图合在一起
		)

		grid_chart = Grid(init_opts=opts.InitOpts(width='990px', height='600px'))
		grid_chart.add(overlapkline, grid_opts=opts.GridOpts(height="55%"), )
		grid_chart.add(indicator, grid_opts=opts.GridOpts(pos_top="70%", height="19%"), )
		return grid_chart

#画带两个副图的K线 即带两个指标
	def kline_ind2(self,overlapkline,indicator1,indicator2):
		# 加两个副图的参数
		self.datazoom_opts2 = [
			opts.DataZoomOpts(is_show=False, type_="inside", xaxis_index=[0, 1, 2], range_start=90, range_end=100, ),
			opts.DataZoomOpts(is_show=False, xaxis_index=[0, 1, 2], type_="inside", pos_top="75%", range_start=90,range_end=100, ),
			opts.DataZoomOpts(is_show=True, xaxis_index=[0, 1, 2], type_="slider", pos_top="90%", range_start=90,range_end=100, )]

		self.kline.set_global_opts(
			yaxis_opts=self.yaxis_opts,
			xaxis_opts=self.xaxis_opts,
			title_opts=self.title_opts,
			toolbox_opts=self.toolbox_opts,
			tooltip_opts=self.tooltip_opts,
			brush_opts=self.brush_opts,
			datazoom_opts=self.datazoom_opts2,
			axispointer_opts=self.axispointer_opts,
			# 这个的作用是使得各个图合在一起
		)
		# overlap_kline_line = self.overlapkline()
		grid_chart = Grid(init_opts=opts.InitOpts(width='990px', height='700px'))  # top是从上到下的位置，height就是图的高
		grid_chart.add(overlapkline, grid_opts=opts.GridOpts(height="48%"), )
		grid_chart.add(indicator1, grid_opts=opts.GridOpts(pos_top="60%", height="14%"), )
		grid_chart.add(indicator2, grid_opts=opts.GridOpts(pos_top="75%", height="14%"), )
		return grid_chart