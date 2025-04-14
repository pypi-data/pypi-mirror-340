import os
import polars as pl   

def technical_sample()->pl.DataFrame:
    """用于获取一个示例数据集 \\
    该数据是沪深300指数的日度收盘价和交易额
    - date 日期 
    - closePrice 收盘价(点数) 
    - dealNum 成交量(手) 
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))  # 获取脚本所在目录
    file_path = os.path.join(current_dir, 'technicalSample.parquet')  # 拼接绝对路径
    
    return pl.read_parquet(file_path).with_columns(pl.col('date').cast(pl.Date)).sort('date')
    
if __name__ == '__main__':
    print(technical_sample())