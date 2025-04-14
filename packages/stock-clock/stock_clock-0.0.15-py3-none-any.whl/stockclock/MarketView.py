import polars as pl
# 描述性统计工具类

# ====== 指数的描述性统计 ======
class indexDescriptionUtils:
    def __init__(self, index_data: pl.DataFrame):
        pass

    @classmethod
    def a(cls):
        pass
    
    @staticmethod
    def calculate_mcclellan(df):
        """计算麦克连振荡器 \\
        原理：\\
        1.以0轴为中心。MCL为正值时，是多头市场；MCL为负值时，是空头市场。 \\
        2.当MCL上涨至 50～ 100之间的超买区，曲线穿越此区后再度反转向下跌破 50时，可视为短期卖出讯号。\\
        3.当MCL下跌至-100～-170之间的超卖区，曲线穿越此区后再度反转向上突破-100时，可视为短期买进讯号。 \\
        4.MCL向上超越 80时，代表涨势变成快速上升行情。此时，不必急于卖出持股，如果趋势没有改变，指数一般会持续上涨一段时间。 \\
        """
        # 计算腾落值
        DIF = df['totalUp'] - df['totalDown']
        
        # 计算指数移动平均
        df['19d_ema'] = DIF.ewm(span=19, adjust=False).mean()
        df['39d_ema'] = DIF.ewm(span=39, adjust=False).mean()
        
        # 计算麦克连振荡器
        df['mcclellan_osc'] = df['19d_ema'] - df['39d_ema']
        
        return df

    '''''
    原理：1.以0轴为中心。MCL为正值时，是多头市场；MCL为负值时，是空头市场。
        2.当MCL上涨至 50～ 100之间的超买区，曲线穿越此区后再度反转向下跌破 50时，可视为短期卖出讯号。
        3.当MCL下跌至-100～-170之间的超卖区，曲线穿越此区后再度反转向上突破-100时，可视为短期买进讯号。
        4.MCL向上超越 80时，代表涨势变成快速上升行情。此时，不必急于卖出持股，如果趋势没有改变，指数一般会持续上涨一段时间。
    '''''


# ====== 股票的描述性统计 ====== 
class stockDescriptionUtils:
    def __init__(self, stock_data: pl.DataFrame):
        pass


# ====== 市场情绪 ======
