# -*- encoding:utf-8 -*-

import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.globals import ThemeType


class CreateChart(object):
    def __init__(self):
        self.initopts = opts.InitOpts(width="1000px",
                                      height="600px",
                                      theme=ThemeType.PURPLE_PASSION,  # 整体风格
                                      bg_color="#63686D")              # 背景颜色
        self.toolopts = opts.ToolBoxFeatureOpts(data_view=None,        # 工具箱选项设置
                                                data_zoom=None)
        self.toolboxopts = opts.ToolboxOpts(is_show=True,              # 是否展示工具框
                                            pos_left="90%",            # 工具框位置
                                            feature=self.toolopts)     # 工具框选项
        self.legendopts = opts.LegendOpts(pos_left="45%",
                                          pos_top="12%")               # 图例标签位置
        self.datazoomopts = opts.DataZoomOpts(is_show=True)            # 区域组件

    def line_chart(self, xaxis, yaxis):
        try:
            # 需要保证axis均是个{key:value,[value...]}的字典类型
            line_chart = Line(init_opts=self.initopts)
            line_chart.set_global_opts(
                toolbox_opts=self.toolboxopts,
                legend_opts=self.legendopts,
            )
            line_chart.add_xaxis(xaxis)
            for y in yaxis:
                for key, value in enumerate(y):
                    data_list = y[value].split(",")
                    line_chart.add_yaxis(value, data_list, is_smooth=True)
            return line_chart
        except Exception as error:
            print(error)
