# --------------------------------------------------------- 抽象父类 --------------------------------------------------- 
# 定义抽象基类

from abc import ABC, abstractmethod

class TechnicalAnalysis(ABC):
    @abstractmethod
    def fit(self, *args, **kwargs):
        """计算指标数据的方法"""
        pass

    @abstractmethod
    def get_data(self):
        """获取计算结果数据的方法"""
        pass

    @abstractmethod
    def plot(self, show: bool, save: bool, save_path: str = None):
        """绘制图表的方法"""
        pass
        
