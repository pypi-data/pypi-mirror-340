import os 
from dotenv import load_dotenv  # 新增导入
load_dotenv('/www/files/Stock/PyScript/.env')
load_dotenv('/home/frank/files/programs/StockClock/mnt/Stock/PyScript/.env')  # 默认加载当前目录的.env文件

import sys
sys.path.append('/www/files/Stock')
sys.path.append('/home/frank/files/programs/StockClock/mnt/Stock') 

from Utils.DataUtils.StockDataUtils import *
from Utils.AnalyzeUtils.Technical import *
from Utils.AnalyzeUtils.Sentiment import *  
from Utils.AnalyzeUtils.Technical.Trend import * 

import requests 
import polars as pl   

def load_sample_data()->pl.DataFrame:
    """用于获取一个示例数据集 \\
    该数据是沪深300指数的日度收盘价和交易额
    - date 日期 
    - closePrice 收盘价(点数) 
    - dealNum 成交量(手) 
    """
    return pl.read_parquet('./technicalSample.parquet').with_columns(pl.col('date').cast(pl.Date)).sort('date')
    
