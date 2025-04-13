# 技术分析类
# 导入库
from .__init__ import TechnicalAnalysis
import polars as pl
import pandas as pd
import numpy as np
from typing import List
from typing import Literal
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px



"""技术分析类的编写说明：   
开发者在添加类之前请**一定仔细**阅读！   \\ 

技术分析类的方法： \\
Technica中，每一个指标对应一个类，用于生成类的对应数据，以及该指标的衍生指标 \\  
在构造函数中，传入计算该类的所需超参数,并且初始化所有变量 \\ 

每个类需要继承TechnicalAnalysis抽象类，并且实现fit，get_*，plot*方法 \\
fit方法，参数传入对应的数据data，并需要指明time_col和price_col，即指定时间和所需要的价格，如果需要多个价格数据，可以使用前缀,后缀的方式写参数名  \\  
fit方法生成指标对应的数据，其中时间列统一命名为time，price,其他列命名方式为首字母大写或简写（Narrow MA etc.） \\  
fit方法实质上就是为传入的data，生成对应指标的列  
get_data 方法，返回对应的数据，*为数据名   
plot 方法，需要传入show和save参数，用于控制是否显示图像和是否保存图像，save为True时，需要传入save_path参数，用于指定保存路径，保存路径为路径+文件名.格式 \\  

其余方法各自实现 \\   
如果有多个plot方法，可以使用前缀，如kline_plot   \\  
最好使用plotly，保存为html格式，可以交互 \\ 
其他衍生指标方法:以detect/calculate等为前缀，**仅**使用本类的属性就可以计算出的指标，如布林通道->布林通道收窄指标，无需添加类的属性，返回值即可  \\  
如果某一衍生指标需要多个其他指标构成，则单独写成一个类，再在类中调用其他类的(衍生)指标，便于维护  \\ 

当前已有的类(开发后请对应补充）： \\

 ------ 趋势分析 ------
1. BollingerBrand类，用于计算布林带数据 - 衍生指标 1.布林带收窄（用于判断趋势or震荡）  \\ 
2. MA类，用于计算多个窗口的移动平均 - 衍生指标 1.均线排列，用于识别上涨下跌 2.均线交叉，用于识别趋势开端 3.均线斜率，用于识别上涨下跌  \\  
3. DI类


"""

# --------------------------------------------------------- 趋势分析指标 --------------------------------------------------- #
#%%


# ======== 布林带 ======== 
class BollingerBrand(TechnicalAnalysis):
    # 构造函数，传入参数
    def __init__(self, 
                 window:int=20,
                 m:float=2):
        """
        布林通道分析工具，用于衡量价格波动性和识别超买/超卖状态 \\
        
        参数说明：
        window: 移动平均周期（默认20个时间单位），建议与交易周期匹配（如20日线）\\ 
        m     : 标准差倍数（默认2），决定通道宽度，数值越大通道越宽 \\   
        由于使用了移动平均，在统计历史指标的时候，统计x天的指标需要至少保留window+x天的数据  
        
        主要方法： \\
        fit()       : 计算布林通道（需传入包含价格和时间列的数据） \\
        plot()      : 可视化布林通道与价格走势 \\
        get_*()     : 获取计算结果数据 \\
        
        fit计算结果包含： \\
        - MA  : 移动平均线（中轨） \\
        - Upper : 上轨（MA + m*σ） \\
        - Lower : 下轨（MA - m*σ） \\ 

        衍生方法：\\ 
        detect_narrow: 返回一个polars的df，用于比较当前通道宽度和前若干日的通道宽度的分位数，判断是否收窄，Narrow列为false表示没收窄，true表示收窄 \\ S
        """
        self.window = window 
        self.m = m
        self.bollinger_brand_data = None
    
    # 计算布林带
    def fit(self,
            data:pl.DataFrame,
            price_col:str,
            time_col:str):
        """
        输入： \\
        data: 数据 \\ 
        price_col: 价格列 \\
        time_col: 时间列 \\
        
        初始化布林带数据bollinger_brand_data polars df  \\
        - time 时间 （Technical库中所有的时间均为time）   \\ 
        - price 价格 （Technical库中所有的时间均为price或price+前后缀） \\
        - MA 移动平均线（中轨） \\
        - Upper 上轨（MA + m*σ） \\
        - Lower 下轨（MA - m*σ） \\ 

        用bollinger_brand_data方法获取计算结果数据 \\
        """
        # 计算布林通道
        self.bollinger_brand_data = (
            data. 
                select(
                    pl.col(time_col).alias('time'),
                    pl.col(price_col).alias('price'),
                ). 
                with_columns(
                    pl.col('price').rolling_mean(self.window).alias('MA'),
                    pl.col('price').rolling_std(self.window).alias('STD'),
                ).
                with_columns(
                    (pl.col('MA') + self.m * pl.col('STD')).alias('Upper'),
                    (pl.col('MA') - self.m * pl.col('STD')).alias('Lower'),
                ).
                drop_nulls()
        )

    # 绘制图像
    def plot(self,
             show:bool,
             save:bool,
             save_path:str=None):
        """
        show: 是否显示图像 
        save: 是否保存图像
        save_path: 保存路径（需要.html格式）
        """
        if self.bollinger_brand_data is None:
            print("请先调用 fit 方法计算布林带。")
            return
        
        # 创建交互式图表
        fig = go.Figure()
        
        # 添加价格线
        fig.add_trace(go.Scatter(
            x=self.bollinger_brand_data['time'],
            y=self.bollinger_brand_data['price'],
            name='Price',
            line=dict(color='#1f77b4', width=2)
        ))
        
        # 添加布林带中轨
        fig.add_trace(go.Scatter(
            x=self.bollinger_brand_data['time'],
            y=self.bollinger_brand_data['MA'],
            name='MA',
            line=dict(color='#2ca02c', width=1.5)
        ))
        
        # 添加上下轨道（虚线）
        fig.add_trace(go.Scatter(
            x=self.bollinger_brand_data['time'],
            y=self.bollinger_brand_data['Upper'],
            name='Upper',
            line=dict(color='#d62728', width=1.5, dash='dot')
        ))
        
        fig.add_trace(go.Scatter(
            x=self.bollinger_brand_data['time'],
            y=self.bollinger_brand_data['Lower'],
            name='Lower',
            line=dict(color='#ff7f0e', width=1.5, dash='dot')
        ))
        
        # 填充布林带区域
        fig.add_trace(go.Scatter(
            x=self.bollinger_brand_data['time'],
            y=self.bollinger_brand_data['Upper'],
            fill=None,
            mode='lines',
            line=dict(width=0),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=self.bollinger_brand_data['time'],
            y=self.bollinger_brand_data['Lower'],
            fill='tonexty',
            mode='lines',
            line=dict(width=0),
            fillcolor='rgba(173,216,230,0.2)',
            showlegend=False
        ))
        
        # 设置图表布局
        fig.update_layout(
            title='Bollinger Bands (布林通道)',
            xaxis_title='Time',
            yaxis_title='Price',
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            width=1400,
            height=700,
            hovermode='x unified',
            showlegend=True
        )
        
        # 处理保存和显示
        if save:
            if not save_path.endswith('.html'):
                save_path += '.html'
            fig.write_html(save_path)
            
        if show:
            fig.show()
    
    # 获取布林带数据
    def get_data(self)->pl.DataFrame:
        """
        获取布林带数据
        """
        if self.bollinger_brand_data is not None:
            return self.bollinger_brand_data
        else:
            print('请先初始化')
            return None

    # 收窄判断
    def detect_narrow(self,
               window:int=100,
               quantile:float=0.2)->pl.DataFrame | None:
        """
        收窄判断：判断布林带是否收窄 \\
        原理：判断布林带是否收窄，即判断上轨和下轨之间的距离是否小于一定阈值 \\
        输入参数：
        window: 移动平均周期（默认100个时间单位），建议与交易周期匹配（如100日线） \\
        quantile:分位数，小数，若当日的带宽小于前window天的第quantile分位数，则认为收窄 \\
        
        输出：一个polars的df： \\
        - date: 日期 \\
        - BindWidth: 带宽 \\
        - Narrow: 布尔值，True表示收窄，False表示不收窄  
        """
        if self.bollinger_brand_data is None:
            print("请先调用 fit 方法计算布林带。")
            return None
        
        # 计算布林带宽度
        narrow = (
            self.bollinger_brand_data. 
                with_columns(
                    (pl.col('Upper') - pl.col('Lower')).alias('BandWidth')
                ).
                with_columns(
                    pl.col('BandWidth').
                    rolling_quantile(
                        quantile=quantile, 
                        window_size=window, 
                        interpolation='nearest'
                    ).
                    alias('Quantile')
                ). 
                with_columns(
                    (pl.col('BandWidth') <= pl.col('Quantile')).alias('Narrow')
                ). 
                select(
                    pl.col(['time','BandWidth','Quantile','Narrow'])
                ). 
                drop_nulls()
        )

        return narrow 

    def detect_break(self) -> pl.DataFrame:
        '''检验是否有向上或向下突破'''
        # 修复1：所有条件必须用括号明确优先级
        reg = (
            ((pl.col('price') <= pl.col('Upper')) & (pl.col('price').shift(1) > pl.col('Upper').shift(1)))
            | 
            ((pl.col('price') >= pl.col('Lower')) & (pl.col('price').shift(1) < pl.col('Lower').shift(1)))
        )
        breakpoint = (
            self.bollinger_brand_data.
                with_columns(
                    pl.when(
                        # 修复2：向上突破条件（每个子条件单独括号）
                        ((pl.col('price') >= pl.col('Upper')) & ((pl.col('price').shift(1) < pl.col('Upper').shift(1))))
                    ).
                    then(1).
                    when(
                        # 修复3：向下突破条件
                        ((pl.col('price') <= pl.col('Lower')) & ((pl.col('price').shift(1) > pl.col('Lower').shift(1))))
                    ).
                    then(-1).
                    when(reg).
                    then(0).
                    otherwise(2). # 无变化，标记为2
                    alias('Break')
                ).    
                select(pl.col(['time', 'Break']))
            )   
        return breakpoint


# ======== 移动平均线 ========
class MA(TechnicalAnalysis):
    # 构造函数，传入参数
    def __init__(self, 
                 windows_list:List[int],
                 method:Literal['SMA','EMA'],
                 alpha:float=None):
        """
        移动平均分析工具，用于平滑价格，用于识别趋势 \\  
        
        参数说明：
        window_list: 移动平均周期的列表，可以传入多个整数，以便计算多个窗口期的移动平均线 \\ 
        method: 计算移动平均的方法，有SMA和EMA两种方法，即简单移动平均和加权移动平均 \\   
        alpha: 如果设置使用EMA方法，则需要传入alpha参数，用于计算加权移动平均的权重，默认为2/(window+1) \\
        由于使用了移动平均，在统计历史指标的时候，统计x天的指标需要至少保留window+x天的数据  \\
        
        主要方法： \\
        fit()   : 计算多条移动均线（需传入data，price列，time列） \\
        plot()  : 可视化布林通道与价格走势 \\
        get_*() : 获取计算结果数据 \\
        
        fit计算结果包含： \\
        - EMA_{window} 或 SMA_{window}

        衍生方法：\\ 
        detect_cross: MACD指标，传入慢线long和快线short，返回一个df，记录是否出现金叉或死叉 \\  
        detect_alignment: 传入列名列表，计算MA排列指标，传入多条均线，返回一个df，记录是否出现均线排列 \\  
        calculate_slope: 计算每天的均线斜率，返回一个df，记录每天的均线斜率 \\
        """
        self.windows_list = windows_list
        self.method = method
        self.alpha = None
        if self.method == 'EMA':
            self.alpha = alpha

        self.ma_data = None
    
    # 计算移动平均线的方法
    class __fitUtils__:
        def __init__(self):
            pass

        # SMA方法
        @classmethod
        def __SMA__(cls,
                    data:pl.DataFrame,
                    price_col:str,
                    time_col:str,
                    windows_list:List[int]):
            """
            data: 数据
            price_col: 价格列
            time_col: 时间列
            window: 窗口大小
            """
            ma_data = (
                data.
                    select(
                        pl.col(time_col).alias('time'),
                        pl.col(price_col).alias('price'),
                    ).
                    with_columns(
                        [
                            pl.col('price').rolling_mean(window).alias(f'SMA_{window}')
                            for window in windows_list
                        ]
                    ). 
                    drop_nulls()
            )
            return ma_data
        
        # EMA方法
        @classmethod
        def __EMA__(cls,
                    data: pl.DataFrame,
                    price_col: str,
                    time_col: str,
                    windows_list: List[int],
                    alpha: float = None):  # 改为可选参数
            """
            data: 输入数据（需按时间排序）
            price_col: 价格列名（如"close"）
            time_col: 时间列名（如"date"）
            windows_list: 时间窗口列表（单位：数据点个数）
            alpha: 平滑因子（可选，默认根据窗口计算）
            """
            ma_data = (
                data
                .select(
                    pl.col(time_col).alias('time'),
                    pl.col(price_col).alias('price')
                )
                .with_columns([
                    # EMA计算公式：EMA_t = α * price_t + (1-α) * EMA_{t-1}
                    pl.col("price").ewm_mean(
                        alpha=alpha if alpha is not None else 2/(window+1),  # 自动计算默认alpha
                        adjust=False  # 使用精确递推公式
                    ).alias(f"EMA_{window}")
                    for window in windows_list
                ])
                .drop_nulls()
            )

            return ma_data
        


    def fit(self,
            data:pl.DataFrame,
            time_col:str,
            price_col:str):
        """
        data: 数据 "
        time_col: 时间列
        price_col: 价格列
        """
        if self.method == 'SMA':
            self.ma_data = self.__fitUtils__.__SMA__(data,price_col,time_col,self.windows_list)
        elif self.method == 'EMA':
            self.ma_data = self.__fitUtils__.__EMA__(data,price_col,time_col,self.windows_list,self.alpha)
        
    
    def plot(self, 
             show: bool, 
             save: bool, 
             save_path: str = None):
        """
        绘制移动平均线图表
        show: 是否显示图像
        save: 是否保存图像
        save_path: 保存路径（需要.html格式）
        """
        if self.ma_data is None:
            print("请先调用 fit 方法计算移动平均线。")
            return
        
        # 创建交互式图表
        fig = go.Figure()
        
        # 添加价格线（始终显示）
        fig.add_trace(go.Scatter(
            x=self.ma_data['time'],
            y=self.ma_data['price'],
            name='Price',
            line=dict(color='#1f77b4', width=2)
        ))
        
        # 自动生成颜色序列（最多支持10条均线）
        colors = px.colors.qualitative.Plotly
        ma_columns = [col for col in self.ma_data.columns 
                     if col.startswith(('SMA_', 'EMA_'))]
        
        # 添加各条移动平均线
        for idx, col in enumerate(ma_columns):
            fig.add_trace(go.Scatter(
                x=self.ma_data['time'],
                y=self.ma_data[col],
                name=f'{col}',
                line=dict(
                    color=colors[idx % len(colors)],
                    width=1.5,
                    dash='dot' if self.method == 'EMA' else 'solid'
                )
            ))
        
        # 设置图表布局
        fig.update_layout(
            title=f'{self.method} Moving Averages (移动平均线)',
            xaxis_title='Time',
            yaxis_title='Price',
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            width=1400,
            height=700,
            hovermode='x unified',
            showlegend=True
        )
        
        # 处理保存和显示
        if save:
            if not save_path.endswith('.html'):
                save_path += '.html'
            fig.write_html(save_path)
            
        if show:
            fig.show()
        pass


    # 返回数据
    def get_data(self)->pl.DataFrame:
        """
        获取均线数据
        列： 
        time 时间  
        price 原始价格
        SMA_... / EMA_ ... 窗口对应值
        """
        if self.ma_data is not None:
            return self.ma_data
        else:
            print('请先用fit方法初始化')
            return None

    # 金叉和死叉的检验
    def detect_cross(self, short: str, long: str) -> pl.DataFrame:
        """
        检测金叉/死叉信号
        :param short: 短期均线列名（如'SMA_5'）
        :param long: 长期均线列名（如'SMA_20'）
        :return: 包含日期和信号标记的DataFrame（1=金叉，-1=死叉）
        """
        if self.ma_data is None:
            print("请先调用 fit 方法计算移动平均线。")
            return None
        
        # 验证列是否存在
        if short not in self.ma_data.columns or long not in self.ma_data.columns:
            missing = [col for col in [short, long] if col not in self.ma_data.columns]
            print(f"错误：列 {missing} 不存在于计算结果中")
            print(f"可用列：{self.ma_data.columns}")
            return None
        
        cross_data = (
            self.ma_data.
                with_columns([
                    # 获取前一日数值
                    pl.col(short).shift(1).alias("_prev_short"),
                    pl.col(long).shift(1).alias("_prev_long")
                ]).
                with_columns(
                    # 金叉条件：前日短<长 & 当日短>长
                    pl.when(
                        (pl.col("_prev_short") < pl.col("_prev_long")) &
                        (pl.col(short) > pl.col(long))
                    ).
                    then(1).
                    # 死叉条件：前日短>长 & 当日短<长
                    when(
                        (pl.col("_prev_short") > pl.col("_prev_long")) &
                        (pl.col(short) < pl.col(long))
                    ).
                    then(-1).
                    # 无信号标记为0，也可用.fill_null(0)
                    otherwise(0).
                    alias("Signal")
                ).
                select([
                    pl.col("time"), 
                    pl.col("Signal").fill_null(0)  # 处理首行空值
                ])
                # 可选：过滤有信号的日期
                # .filter(pl.col("Signal") != 0)
        )
        
        return cross_data

    def detect_alignment(self, cols: List[str]) -> pl.DataFrame:
        """
        判断均线排列方向
        :param cols: 需要判断排列顺序的均线列名列表（按短期到长期顺序传入）
                     示例：['MA_5', 'MA_10', 'MA_20'] \\ 
        :return: 包含日期和排列方向的DataFrame（1=多头，-1=空头，0=无序） \\ 
        """
        if self.ma_data is None:
            print("请先调用 fit 方法计算移动平均线。")
            return None

        # 参数校验
        if len(cols) < 2:
            print("错误：至少需要传入两个均线列")
            return None
        
        missing_cols = [col for col in cols if col not in self.ma_data.columns]
        if missing_cols:
            print(f"错误：列 {missing_cols} 不存在")
            print(f"可用列：{self.ma_data.columns}")
            return None

        # 生成排列条件
        long_conditions = [
            (pl.col(cols[i]) > pl.col(cols[i+1])) 
            for i in range(len(cols)-1)
        ]
        short_conditions = [
            (pl.col(cols[i]) < pl.col(cols[i+1]))
            for i in range(len(cols)-1)
        ]

        # 合并条件（所有相邻均线都满足关系）
        is_long = long_conditions[0]
        for cond in long_conditions[1:]:
            is_long = is_long & cond

        is_short = short_conditions[0]
        for cond in short_conditions[1:]:
            is_short = is_short & cond

        return (
            self.ma_data
            .with_columns(
                pl.when(is_long).then(1)
                .when(is_short).then(-1)
                .otherwise(0)
                .alias("Alignment")
            )
            .select([
                pl.col("time"),
                pl.col("Alignment")
            ])
        )

    def calculate_slope(self, 
        cols: List[str],
        window: int = 5,
        method: Literal["diff", "regression"] = "diff"
    ) -> pl.DataFrame:
        """
        计算均线斜率（变化率）
        
        :param cols: 需要计算斜率的均线列名列表（如['SMA_5', 'EMA_20']）
        :param window: 计算窗口大小（单位：数据点个数）
        :param method: 计算方法
        - diff：差分法（简单快速）(斜率 = (当前值 - N天前值)/N)
        - regression：线性回归斜率（更精确但计算量大）
        :return: 包含日期和斜率列的DataFrame
        """
        if self.ma_data is None:
            print("请先调用 fit 方法计算移动平均线。")
            return None

        # 验证列存在性
        missing_cols = [col for col in cols if col not in self.ma_data.columns]
        if missing_cols:
            print(f"错误：列 {missing_cols} 不存在")
            print(f"可用列：{self.ma_data.columns}")
            return None

        # 定义不同计算模式
        def _diff_slope(col: str):
            """差分法计算斜率"""
            return (pl.col(col) - pl.col(col).shift(window)) / window

        def _regression_slope(col: str):
            """线性回归斜率（需安装numpy）"""
            return pl.col(col).rolling_map(
                lambda s: np.polyfit(np.arange(len(s)), s, 1)[0] if len(s) >=2 else None,
                window
            )

        # 选择计算方法
        slope_func = _diff_slope if method == "diff" else _regression_slope

        slope = (
            self.ma_data
            .select([
                pl.col("time"),
                *[
                    slope_func(col).round(4).alias(f"{col}_slope")
                    for col in cols
                ]
            ])
            .drop_nulls()  # 去除初始窗口的null值
        )

        return slope
    
    def calculate_divergence(self,short:str,long:str)->pl.DataFrame:
        """
        计算均线发散度  
        计算short和long之间的距离分位数
        """
        div_data = (
            self.ma_data.
                select(
                    pl.col(['time',short,long])
                ). 
                select(
                    pl.col('time'),
                    ((pl.col(short) - pl.col(long))/pl.col(long)).alias(f'{long}_and_{short}_divergence')
                )
        )
        return div_data

# ======== 趋势检验类DI ========
class DI(TechnicalAnalysis):
    # DI(趋势指标的计算)
    def __init__(self,
                 window:int=14):
        """
        DI类 
        """
        # 计算DI 
        self.window = window
        self.TR_data = None
        self.DM_data = None
        self.ATR_data = None
        self.DI_data = None
    # 计算TR
    class __fitUtils__:
        # 用于筛选列
        @classmethod
        def select_col(cls,
                       data:pl.DataFrame,
                       time_col:str,
                       open_price_col:str,
                       high_price_col:str,
                       low_price_col:str,
                       close_price_col:str,
                    )->pl.DataFrame:
            
            select_data = (
                data. 
                    select(
                        pl.col(time_col).alias('time'),
                        pl.col(open_price_col).alias('open_price'),
                        pl.col(high_price_col).alias('high_price'),
                        pl.col(low_price_col).alias('low_price'),
                        pl.col(close_price_col).alias('close_price')
                    )
            )
            return select_data

        # 用于计算TR,DI的函数
        @classmethod
        def TR(cls,
                select_data:pl.DataFrame)->pl.DataFrame:
            
            TR = (
                select_data.
                    drop_nulls().
                    with_columns(
                        (pl.col('high_price') - pl.col('low_price')).abs().alias('H-L'),
                        (pl.col('high_price') - pl.col('close_price').shift(1)).abs().shift(1).alias('H-PC'),
                        (pl.col('low_price') - pl.col('close_price').shift(1)).abs().shift(1).alias('L-PC')
                    ).
                    with_columns(
                        pl.max_horizontal(['H-L','H-PC','L-PC']).alias('TR')
                    ).
                    select(
                        pl.col('time','TR')
                    ).
                    sort('time')
            )

            return TR

        @classmethod
        def DM(cls,
               select_data:pl.DataFrame)->pl.DataFrame:
            
            DM = (
                select_data. 
                    drop_nulls().
                    with_columns(
                        pl.when(
                            pl.col('high_price') > pl.col('high_price').shift(1)
                        ).
                        then(
                            pl.col('high_price') - pl.col('high_price').shift(1)
                        ).
                        otherwise(0).
                        alias('+DM'),
                    ).
                    with_columns(
                        pl.when(
                            pl.col('low_price') < pl.col('low_price').shift(1)
                        ). 
                        then(
                            pl.col('low_price').shift(1) - pl.col('low_price')
                        ). 
                        otherwise(0).
                        alias('-DM')
                    ). 
                    select(
                        pl.col(['time','+DM','-DM'])
                    ).
                    sort('time')
            )

            return DM
        
        @classmethod
        def ATR(cls,
                window:int,
                TR_data:pl.DataFrame)->pl.DataFrame:
            # 计算ATR
            ATR = (
                TR_data. 
                    with_columns(
                        pl.col('TR').rolling_mean(window).alias('ATR')
                    ). 
                    drop('TR').
                    drop_nulls()
            )

            return ATR
        
        @classmethod
        def DI(cls,
               DM_data:pl.DataFrame,
               ATR_data:pl.DataFrame)->pl.DataFrame:
            # 计算+DI和-DI
            # 合并MA和ATR
            DI = (
                DM_data.join(
                    ATR_data, how='inner', 
                    on = 'time'
                ).
                drop_nulls().
                with_columns(
                    (pl.col('+DM') / pl.col('ATR') * 100).alias('+DI'),
                    (pl.col('-DM') / pl.col('ATR') * 100).alias('-DI')
                ). 
                select(
                    pl.col(['time','+DI','-DI'])
                ). 
                sort('time')
            )

            return DI
        
        
    def fit(self,
            data:pl.DataFrame,
            time_col:str,
            open_price_col:str,
            high_price_col:str,
            low_price_col:str,
            close_price_col:str,
            )->pl.DataFrame:
        """
        data: 数据
        time_col: 时间列
        open_price_col: 开盘价列
        high_price_col: 最高价列
        low_price_col: 最低价列
        close_price_col: 收盘价列
        """
        # 筛选列
        select_data = self.__fitUtils__.select_col(data,time_col,open_price_col,high_price_col,low_price_col,close_price_col)
        # 计算TR
        self.TR_data = self.__fitUtils__.TR(select_data)
        print('== TR计算完毕 ==')
        # 计算DM
        self.DM_data = self.__fitUtils__.DM(select_data)
        print('== DM计算完毕 ==')
        # 计算ATR
        self.ATR_data = self.__fitUtils__.ATR(self.window,self.TR_data)
        print('== ATR计算完毕 ==')
        # 计算DI
        self.DI_data = self.__fitUtils__.DI(self.DM_data,self.ATR_data)
        print('== DI计算完毕 ==')
    
    
    def get_data(self)->pl.DataFrame:
        """
        获取DI数据
        """
        if self.DI_data is not None:
            return self.DI_data
        else:
            print('请先用fit方法初始化')
            return None
    
    def plot(self,
             show:bool,
             save:bool,
             save_path:str=None):
        raise NotImplementedError("没有实现DI的plot方法")
        
        
    




# 计算ADX
class ADX:
    def __init__(self,
            window:int=14):
        """
        windows:SMA的窗口,经典选择是14
        """ 
        self.window = window
        self.ADX_data = None

    def fit(self,
            di_data:pl.DataFrame,
            time_col:str='time',
            plus_di_col:str='+DI',
            min_di_col:str='-DI'):
        """
        传入一个di形式的data  
        需要有三列：time,+DI,-DI
        """
        # 计算+DI和-DI的SMA
        self.ADX_data = (
            di_data.
                select(
                    pl.col(time_col).alias('time'),
                    pl.col(plus_di_col).alias('+DI'),
                    pl.col(min_di_col).alias('-DI')
                ).
                with_columns(
                    pl.col('+DI').rolling_mean(self.window).alias('+DI_SMA'),
                    pl.col('-DI').rolling_mean(self.window).alias('-DI_SMA')
                ). 
                drop_nulls().
                with_columns(
                    ((pl.col('+DI_SMA')-pl.col('-DI_SMA')).abs() * 100 / (pl.col('+DI_SMA') + pl.col('-DI_SMA'))).alias('ADX')
                ). 
                select(
                    pl.col(['time','ADX'])
                ). 
                sort('time')
        )

    def get_ADX_data(self)->pl.DataFrame:
        """返回ADX数据
        """
        return self.ADX_data


# ------------------------------------------------------------------------ 震荡分析指标 --------------------------------------------------- #