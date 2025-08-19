from PySide6.QtCore import QMargins, QPoint, Qt, QPointF
from PySide6.QtGui import QPainter, QColor, QFont, QPen
from PySide6 import QtCharts

from uiUtils.Charts.chartUtils import Font
import numpy as np
            

class Trend(QtCharts.QLineSeries):
    def __init__(self,
                name: str = None,
                line_color: str = None,
                line_width: int = 1,
            ) -> None:
        
        super().__init__()
        self.set_name(name)
        self.set_line_color(line_color)
        self.set_line_width(line_width)

    def set_name(self, name):
        self.name = name
        if self.name:
            self.setName(name)

    def click_connector(self, func):
        self.clicked.connect( lambda qpoint: func(qpoint.toTuple()
                                    )
                                    )
    
    def select_point_by_pos(self, pos:tuple[int]):
        points = self.pointsVector()
        #middle_idx = int(len(points) // 2)
        min_dist = np.inf
        selected_idx = -1
        for idx, point in enumerate(points):
            dist = abs(point.x() - pos[0])
            if dist < min_dist:
                selected_idx = idx
                min_dist = dist
            else:
                break

        self.selectPoint(selected_idx)

                
            
    
    def set_line_color(self, color):
        self.line_color = color
        if self.line_color:
            pen = self.pen()
            pen.setColor(QColor(self.line_color))
            self.setPen(pen)

    def set_line_width(self, width):
        self.line_width = width
        if self.line_width:
            pen = self.pen()
            pen.setWidth(self.line_width)
            self.setPen(pen)

    def clear_trend(self):
        self.clear()

    def add_data(self, axisX_values, axisY_values):
        assert len(axisX_values)==len(axisY_values)
        for x, y in zip(axisX_values, axisY_values):
            self.append(QPointF(x, y))
            
            

class selectedPoint(QtCharts.QLineSeries):
    def __init__(self,
                color: str = None,
                line_width: int = None,
                show_label:bool = False
            ) -> None:
        
        super().__init__()
        self.set_line_color(color)
        self.set_line_width(line_width)
        self.show_label = show_label

    def set_line_color(self, color):
        self.line_color = color
        if self.line_color:
            pen = self.pen()
            pen.setColor(QColor(self.line_color))
            self.setPen(pen)
    
    
    def set_line_width(self, width):
        self.line_width = width
        if self.line_width:
            pen = self.pen()
            pen.setWidth(self.line_width)
            self.setPen(pen)

    def show_point(self, point):
        self.clear()
        self.append(QPointF(*point))
        self.selectAllPoints()
        if self.show_label:
            self.pointLabelsVisible()
        

    




class LineChart(QtCharts.QChartView):
    def __init__(self, 
                parent=None,
                chart_title: str = None,
                chart_title_color: str = None,
                chart_title_font: object = None,
                axisX_label: str = None,
                axisY_label: str = None,
                chart_background_color: str = None,
                chart_legend: bool = False,
                chart_legend_alignment: str = 'TOP',
                chart_legend_color: str = None,
                axis_color: str = None,
                axis_font: object = None,
                axisX_grid: bool = False,
                axisY_grid: bool = False,
                axisX_grid_color: str = None,
                axisY_grid_color: str = None,
                axisX_range: tuple = None,
                axisY_range: tuple = None,
                axisX_tickCount: str = 5,
                axisY_tickCount: str = 5,
                animation: bool = True,
                ):

        self.chart:QtCharts.QChart = QtCharts.QChart()
        super().__init__(self.chart, parent)
        self.chart.legend().setVisible(False)
        

        self.__set_axis()

        self.setup_chart()

        if chart_title:
            self.set_chart_title(chart_title)
        if chart_title_color:
            self.set_chart_title_color(chart_title_color)
        if chart_title_font:
            self.set_chart_title_font(chart_title_font)

        if chart_background_color:
            self.set_background_color(chart_background_color)

        self.set_legend(chart_legend)
        self.set_legend_alignment(chart_legend_alignment)
        if chart_legend_color:
            self.set_chart_legend_color(chart_legend_color)

        self.set_axisX_label(axisX_label)
        self.set_axisY_label(axisY_label)

        self.set_axis_color(axis_color)
        self.set_axis_font(axis_font)
        self.set_axis_grid(axisX_grid, axisY_grid)
        self.set_axis_grid_color(axisX_grid_color, axisY_grid_color)

        self.set_axisX_range(axisX_range)
        self.set_axisY_range(axisY_range)

        self.set_axisX_tickCount(axisX_tickCount)
        self.set_axisY_tickCount(axisY_tickCount)

        self.set_animation(animation)

    def set_chart_title(self, title):
        self.chart.setTitle(title)

    def set_chart_title_font(self, font):
        assert(isinstance(font, Font))
        font = QFont(font.font, font.font_size, QFont.Bold if font.bold else QFont.Normal)
        self.chart.setTitleFont(font)
    

    def set_chart_title_color(self, color):
        self.chart.setTitleBrush(QColor(color))

    def set_background_color(self, background_color: str) -> None:
        self.chart.setBackgroundBrush(QColor(background_color))

    def set_legend(self, legend):
        self.chart.legend().setVisible(legend)

    def set_chart_legend_color(self, color):
        self.chart.legend().setLabelBrush(QColor(color))

    def set_legend_alignment(self, alignment):
        assert alignment in ['TOP', 'BOTTOM', 'LEFT', 'RIGHT']
        if alignment == "TOP":
            self.chart.legend().setAlignment(Qt.AlignTop)
        elif alignment == "BOTTOM":
            self.chart.legend().setAlignment(Qt.AlignBottom)
        elif alignment == "LEFT":
             self.chart.legend().setAlignment(Qt.AlignLeft)
        elif alignment == "RIGHT":
             self.chart.legend().setAlignment(Qt.AlignRight)

    def __set_axis(self):
        self.axisX = QtCharts.QValueAxis()
        self.chart.addAxis(self.axisX, Qt.AlignBottom)

        self.axisY = QtCharts.QValueAxis()
        self.chart.addAxis(self.axisY, Qt.AlignLeft)

    def set_axisX_label(self, label):
        self.axisX_label = label
        if self.axisX_label and hasattr(self, 'axisX'):
            self.axisX.setTitleText(self.axisX_label)

    def set_axisY_label(self, label):
        self.axisY_label = label
        if self.axisY_label and hasattr(self, 'axisY'):
            self.axisY.setTitleText(self.axisY_label)

    def set_axis_color(self, color):
        self.axis_color = color
        if self.axis_color and hasattr(self, 'axisX') and hasattr(self, 'axisY'):
            self.axisX.setTitleBrush(QColor(self.axis_color))
            self.axisX.setLabelsColor(QColor(self.axis_color))
            self.axisY.setTitleBrush(QColor(self.axis_color))
            self.axisY.setLabelsColor(QColor(self.axis_color))

    def set_axis_font(self, font):
        self.axis_font = font
        if self.axis_font and hasattr(self, 'axisX') and hasattr(self, 'axisY'):
            assert(isinstance(self.axis_font, Font))
            font = QFont(self.axis_font.font, self.axis_font.font_size, QFont.Bold if self.axis_font.bold else QFont.Normal)
            self.axisX.setTitleFont(font)
            self.axisY.setTitleFont(font)

    def set_axis_grid(self, axisX_grid, axisY_grid):
        self.axisX_grid = axisX_grid
        self.axisY_grid = axisY_grid
        if hasattr(self, 'axisX'):
            self.axisX.setGridLineVisible(self.axisX_grid)
        if hasattr(self, 'axisY'):
            self.axisY.setGridLineVisible(self.axisY_grid)

    def set_axis_grid_color(self, axisX_grid_color, axisY_grid_color):
        self.axisX_grid_color = axisX_grid_color
        self.axisY_grid_color = axisY_grid_color
        if self.axisX_grid_color and hasattr(self, 'axisX'):
            self.axisX.setGridLineColor(self.axisX_grid_color)
        if self.axisY_grid and hasattr(self, 'axisY'):
            self.axisY.setGridLineColor(self.axisY_grid_color)

    def set_axisX_range(self, range):
        self.axisX_range = range
        if self.axisX_range and hasattr(self, 'axisX'):
            self.axisX.setRange(*self.axisX_range)

    def set_axisY_range(self, range):
        self.axisY_range = range
        if self.axisY_range and hasattr(self, 'axisY'):
            self.axisY.setRange(*self.axisY_range)

    def set_axisX_tickCount(self, tickCount):
        self.axisX_tickCount = tickCount
        if self.axisX_tickCount and hasattr(self, 'axisX'):
            self.axisX.setTickCount(self.axisX_tickCount)

    def set_axisY_tickCount(self, tickCount):
        self.axisY_tickCount = tickCount
        if self.axisY_tickCount and hasattr(self, 'axisY'):
            self.axisY.setTickCount(self.axisY_tickCount)

    def set_animation(self, animation):
        if animation:
            self.chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        else:
            self.chart.setAnimationOptions(QtCharts.QChart.NoAnimation)

    def add_trend(self, series):
        self.chart.addSeries(series)
        series.attachAxis(self.axisX)
        series.attachAxis(self.axisY)

        

    def setup_chart(self):
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        self.chart.setBackgroundRoundness(0)
        self.chart.setContentsMargins(-9, -9, -9, -9)
        self.chart.legend().hide()
        self.setRenderHint(QPainter.Antialiasing)
    

    def remove_all_trends(self,):
        self.chart.removeAllSeries()

    
