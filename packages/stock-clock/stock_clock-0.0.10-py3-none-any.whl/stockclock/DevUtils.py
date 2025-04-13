#%%
# coding: utf-8
from asyncio import sleep
import requests
import os
import polars as pl
from pathlib import Path
import numpy as np
import csv
from datetime import datetime
import pymysql
import polars as pl
from sqlalchemy import create_engine
from typing import Literal
from pathlib import Path
from csmarapi.CsmarService import CsmarService
from pymysql import Error
print(
    """
    ****************** Notice ******************   
    This is a toolkit for Stock-Clock developers. 
    Therefore, it's strongly recommended that 
    ordinary users do not use the classes in the 
    DevUtils file. If you have any problems, 
    please contact us at stockclock@126.com.
    ********************************************
    """
)
#%%
# ======== 数据获取工具-通过各种api接口获得免费的数据 ========
class StockDataGetUtils:
    # 数据设置  
    # 构造函数
    def __init__(self):
        pass


    # ======  聚合数据api  ======
    # 指数数据
    @classmethod
    def juhedata_index(cls,api_keys_list:list,stock_type:str=None)->dict:
        """
        说明：
        type:0代表上证综合指数，1代表深证成份指数(输入此字段时,gid字段不起作用)
        """
        for key in api_keys_list:
            # 基本参数配置
            apiUrl = 'http://web.juhe.cn/finance/stock/hs'  # 接口请求URL
            # 接口请求入参配置
            requestParams = {
                'key': key,
                'gid': '',
                'type': stock_type,
            }
            # 发起接口网络请求
            response = requests.get(apiUrl, params=requestParams)
            # 解析响应结果
            if response.status_code == 200:
                responseResult = response.json()
                # 网络请求成功。可依据业务逻辑和接口文档说明自行处理。
                result = responseResult['result']
                error_code = responseResult['error_code']

                # 错误码解析
                if error_code == 0 and type(result) == dict:
                    # 判断最大和最小数据是否弄反了（接口的bug）
                    if float(result['highPri']) < float(result['lowpri']):
                        # 反了的话就交换回来
                        result['highPri'],result['lowpri'] = result['lowpri'],result['highPri']
                    result_interpret = {   
                        'name':result['name'],
                        'time':result['time'],
                        'dealNum':int(result['dealNum']), # 返回的单位是手（百股），
                        'dealPrice':float(result['dealPri']), # 单位是元，
                        'openPrice':float(result['openPri']),
                        'highPrice':float(result['highPri']),
                        'lowPrice':float(result['lowpri']),
                        'nowPrice':float(result['nowpri'])
                    } 
                    print('请求成功，返回指数数据')
                    return result_interpret

                else:
                    error_dict = {
                        '10001':  '错误的请求KEY',
                        '10002':	'该KEY无请求权限',
                        '10003':	'KEY过期',	
                        '10004':	'错误的OPENID',	
                        '10005':	'应用未审核超时，请提交认证',	
                        '10007':	'未知的请求源',	
                        '10008':	'被禁止的IP',	
                        '10009':	'被禁止的KEY',
                        '10011':	'当前IP请求超过限制',	
                        '10012':	'请求超过次数限制',
                        '10013':	'测试KEY超过请求限制',	
                        '10014':	'系统内部异常(调用充值类业务时，请务必联系客服或通过订单查询接口检测订单，避免造成损失)',	
                        '10020':	'接口维护',	
                        '10021':	'接口停用',	
                        '202101': '参数错误',
                        '202102': '查询不到结果',
                        '202103': '网络异常'
                    }
                    print(f'请求成功，但结果的错误码为：{error_code},更换api尝试')
            else:
                print(response.status_code)
                # 网络异常等因素，解析结果异常。可依据业务逻辑自行处理。
                print('请求异常')
                return
        print('所有api尝试完毕,仍然失败')
        return   
    
    # 聚合数据api-股票数据
    @classmethod
    def juhedata_stock(cls,api_keys_list:list, gid:str=None)->dict:
        """
        说明：
        gid:股票代码，需要市场头+证券号，如
        sh601881（中国银河）
        """
        for apiKey in api_keys_list:
        # 基本参数配置
            apiUrl = 'http://web.juhe.cn/finance/stock/hs'  # 接口请求URL
            # 接口请求入参配置
            requestParams = {
                'key': apiKey,
                'gid': gid,
                'type': ''
            }

            # 发起接口网络请求
            response = requests.get(apiUrl, params=requestParams)

            # 解析响应结果
            if response.status_code == 200:
                responseResult = response.json()
                result = responseResult['result']
                error_code = responseResult['error_code']
                
                if error_code == 0:
                    data_dict = result[0]
                    data = data_dict['data']
                    # 解析result
                    result_dict = {
                            'date':data['date'],
                            'time':data['time'],
                            'gid':data['gid'],
                            'name':data['name'],
                            'openPrice':data['todayStartPri'],
                            'highPrice':data['todayMax'],
                            'lowPrice':data['todayMin'],
                            'nowPrice':data['nowPri'],
                            'dealNum':data['traAmount'],
                            'dealPrice':data['traNumber']
                    }
                    print('请求成功，返回数据')
                    return result_dict 
                else:
                    error_dict = {
                        '0': f'请求成功，但是类型为{type(result)}',
                        '10001':  '错误的请求KEY',
                        '10002':	'该KEY无请求权限',
                        '10003':	'KEY过期',	
                        '10004':	'错误的OPENID',	
                        '10005':	'应用未审核超时，请提交认证',	
                        '10007':	'未知的请求源',	
                        '10008':	'被禁止的IP',	
                        '10009':	'被禁止的KEY',
                        '10011':	'当前IP请求超过限制',	
                        '10012':	'请求超过次数限制',
                        '10013':	'测试KEY超过请求限制',	
                        '10014':	'系统内部异常(调用充值类业务时，请务必联系客服或通过订单查询接口检测订单，避免造成损失)',	
                        '10020':	'接口维护',	
                        '10021':	'接口停用',	
                        '202101': '参数错误',
                        '202102': '查询不到结果',
                        '202103': '网络异常'
                    }
                    print(f'请求成功，但结果的错误码为：{error_dict[str(error_code)]},更换api尝试')
            else:
                # 网络异常等因素，解析结果异常。可依据业务逻辑自行处理。     
                print(response.status_code)
                print('请求异常')
                return
        print('请求结束')
        return
    
    # ====== 麦蕊数据 ====== 
    # 1. 麦蕊数据-个股数据
    @classmethod
    def mairui_stock_data(cls,
                        gid:str,
                        freq:Literal['5m','15m','30m','60m','dn','dq','dh','wn','wq','wh','mn','mq','mh','yn','yq','yh'],
                        license_list:list)->dict:
        """
        麦瑞数据的股票日度数据 \\ 
        API接口：http://api.mairui.club/hszb/fsjy/股票代码(如000001)/分时级别/您的licence \\
        备用接口：http://api1.mairui.club/hszb/fsjy/股票代码(如000001)/分时级别/您的licence \\
        接口说明：根据《股票列表》得到的股票代码以及分时级别获取分时交易数据，交易时间从远到近排序。\\
        目前 分时级别 支持5分钟、15分钟、30分钟、60分钟、日周月年级别（包括前后复权），
        对应的值分别是 5m（5分钟）、15m（15分钟）、30m（30分钟）、60m（60分钟）、dn(日线未复权)、dq（日线前复权）、
        dh（日线后复权）、wn(周线未复权)、wq（周线前复权）、wh（周线后复权）、
        mn(月线未复权)、mq（月线前复权）、mh（月线后复权）、yn(年线未复权)、yq（年线前复权）、yh（年线后复权） 。 \\
        数据更新：分钟级别数据盘中更新，分时越小越优先更新，如5分钟级别会每5分钟更新，15分钟级别会每15分钟更新，以此类推，日线及以上级别每天16:00更新。\\ 

        参数： \\
        gid: 股票代码 \\ 
        freq: 分时级别 \\
        license_list: 证书的 \\ 
        （为了维护方便，没有向juhe数据一样提供license_list）

        响应结果
        {'d': '2025-03-21',  日期\\ 
        'o': 11.49, 开盘\\
        'h': 11.52, 最高\\
        'l': 11.39, 最低\\
        'c': 11.42, 收盘\\
        'v': 1376389, 成交量\\
        'e': 1576151833.21, 成交额\\
        'zf': 1.13, 振幅\\
        'hs': 0.71, 换手率\\
        'zd': -0.61, 涨跌幅\\
        'zde': -0.07, 涨跌额\\
        'ud': '2025-03-22 01:52:35'} 返回时间\\
        返回值：符合数据库的dict
        """
        url1 = f'http://api.mairui.club/hszb/fsjy/{gid}/{freq}'
        url2 = f'http://api1.mairui.club/hszb/fsjy/{gid}/{freq}'

        # 分别使用两个接口进行尝试
        for licenses in license_list:
            for base_url in [url1,url2]: 
                req_url = f'{base_url}/{licenses}'
                try:
                    response = requests.get(req_url)
                    if response.status_code == 200:
                        # 解析json 
                        data = response.json()
                        if isinstance(data, dict):
                            # 替换成数据库的字段名 
                            data.pop('ud')
                            data['date'] = data.pop('d')
                            data['gid'] = gid
                            data['openPrice'] = data.pop('o')
                            data['highPrice'] = data.pop('h')
                            data['lowPrice'] = data.pop('l')
                            data['nowPrice'] = data.pop('c')
                            data['dealNum'] = data.pop('v')
                            data['dealPrice'] = data.pop('e')
                            data['amplitude'] = data.pop('zf')
                            data['turnover'] = data.pop('hs')
                            data['percentageChange'] = data.pop('zd')
                            data['priceChange'] = data.pop('zde')

                            # 返回字典数据
                            return data
                        else:
                            print(f'请求 {gid} 成功，但是返回的数据类型为 {type(data)}')
                            continue
                    else:
                        print(f"请求 {gid} 失败，状态码: {response.status_code}")
                        continue
                except requests.RequestException as e:
                    print(f"请求 {gid} 时发生异常: {e}，尝试更换url")
                    continue
            print(f'所有url尝试完毕，仍然失败,尝试更换证书') 
            continue
        print('所有证书尝试完毕，仍然失败') 

    # 2.麦蕊数据-股票列表(周更)
    @classmethod
    def mairui_stock_list(cls,license_list:list):
        """
        麦瑞数据的股票列表 \\
        API接口：http://api.mairui.club/hslt/list/您的licence \\
        备用接口：http://api1.mairui.club/hslt/list/您的licence \\ 
        周更，每周六执行

        响应结果：
        返回应该是字典组成的list
        dm	string	股票的六位交易代码，例如：601398 gid \\
        mc	string	股票名称，例如：工商银行 name gid \\
        jys	string	交易所，"sh"表示上证，"sz"表示深证 market \\
        """
        url1 = f'http://api.mairui.club/hslt/list'
        url2 = f'http://api1.mairui.club/hslt/list'

        # 分别使用两个接口进行尝试
        for license in license_list:
            for base_url in [url1,url2]: 
                req_url = f'{base_url}/{license}'
                try:
                    response = requests.get(req_url)
                    if response.status_code == 200:
                        # 解析json 
                        data = response.json()
                        # 返回字典数据
                        return data
                    else:
                        print(f"请求股票列表失败，状态码: {response.status_code}")
                except requests.RequestException as e:
                    print(f"请求异常: {e}，尝试更换url")
            print(f'所有url尝试完毕，仍然失败,尝试更换证书') 
        print('所有证书尝试完毕，仍然失败') 

    # 3.迈瑞数据-财务数据
    @classmethod
    def mairui_finance_data(cls,
                            license_list:list,
                            finance_data_type:Literal['profitability','operatingCapability','growthCapability','solvencyCapability','cashFlow','performanceReport','performanceForecast','performanceExpressReport','profitBreakdown'],
                            year:int,
                            quarter:Literal['1','2','3','4']):
        """
        麦瑞数据的股票财务数据  

        - 盈利能力（profitability）
        API接口：http://api.mairuiapi.com/hicw/yl/年度(如2020)/季度(如1)/您的licence
        备用接口：http://api1.mairuiapi.com/hicw/yl/年度(如2020)/季度(如1)/您的licence  

        - 运营能力（operatingCapability）
        API接口：http://api.mairuiapi.com/hicw/yy/年度(如2020)/季度(如1)/您的licence
        备用接口：http://api1.mairuiapi.com/hicw/yy/年度(如2020)/季度(如1)/您的licence  

        - 成长能力（growthCapability）
        API接口：http://api.mairuiapi.com/hicw/cz/年度(如2020)/季度(如1)/您的licence
        备用接口：http://api1.mairuiapi.com/hicw/cz/年度(如2020)/季度(如1)/您的licence 

        - 偿债能力（solvencyCapability）
        API接口：http://api.mairuiapi.com/hicw/cznl/年度(如2020)/季度(如1)/您的licence
        备用接口：http://api1.mairuiapi.com/hicw/cznl/年度(如2020)/季度(如1)/您的licence

        - 现金流量（cashFlow）
        API接口：http://api.mairuiapi.com/hicw/xj/年度(如2020)/季度(如1)/您的licence
        备用接口：http://api1.mairuiapi.com/hicw/xj/年度(如2020)/季度(如1)/您的licence 

        - 业绩报表（performanceReport）
        API接口：http://api.mairuiapi.com/hicw/yjbb/年度(如2020)/季度(如1)/您的licence
        备用接口：http://api1.mairuiapi.com/hicw/yjbb/年度(如2020)/季度(如1)/您的licence

        - 业绩预告（performanceForecast）
        API接口：http://api.mairuiapi.com/hicw/yjyg/年度(如2020)/季度(如1)/您的licence
        备用接口：http://api1.mairuiapi.com/hicw/yjyg/年度(如2020)/季度(如1)/您的licence

        - 业绩快报（performanceExpressReport）
        API接口：http://api.mairuiapi.com/hicw/yjkb/年度(如2020)/季度(如1)/您的licence
        备用接口：http://api1.mairuiapi.com/hicw/yjkb/年度(如2020)/季度(如1)/您的licence

        - 利润细分（profitBreakdown）
        API接口：http://api.mairuiapi.com/hicw/lr/您的licence
        备用接口：http://api1.mairuiapi.com/hicw/lr/您的licence
        """
        # 定义url字典:
        url_dict = {
            'profitability': ['http://api.mairuiapi.com/hicw/yl/',
                            'http://api1.mairuiapi.com/hicw/yl/'],
            'operatingCapability': ['http://api.mairuiapi.com/hicw/yy/',
                            'http://api1.mairuiapi.com/hicw/yy/'],
            'growthCapability': ['http://api.mairuiapi.com/hicw/cz/',
                            'http://api1.mairuiapi.com/hicw/cz/'],
            'solvencyCapability': ['http://api.mairuiapi.com/hicw/cznl/',
                            'http://api1.mairuiapi.com/hicw/cznl/'],
            'cashFlow': ['http://api.mairuiapi.com/hicw/xj/',
                            'http://api1.mairuiapi.com/hicw/xj/'],
            'performanceReport': ['http://api.mairuiapi.com/hicw/yjbb/',
                            'http://api1.mairuiapi.com/hicw/yjbb/'],
            'performanceForecast': ['http://api.mairuiapi.com/hicw/yjyg/',
                            'http://api1.mairuiapi.com/hicw/yjyg/'],
            'performanceExpressReport': ['http://api.mairuiapi.com/hicw/yjkb/',
                            'http://api1.mairuiapi.com/hicw/yjkb/'],
            'profitBreakdown': ['http://api.mairuiapi.com/hicw/lr/',
                                'http://api1.mairuiapi.com/hicw/lr/']
        }
        # 获取传入的接口 
        url_head1 = url_dict[finance_data_type][0]
        url_head2 = url_dict[finance_data_type][1] 
        url1 = f'{url_head1}{year}/{quarter}'
        url2 = f'{url_head2}{year}/{quarter}'
        
        for licenses in license_list:
            for base_url in [url1,url2]:
                req_url = f'{base_url}/{licenses}'
                try:
                    response = requests.get(req_url)
                    if response.status_code == 200:
                        # 解析json
                        data = response.json()
                        # 由于返回的是列表，不对data进行处理，放在主函数中处理  
                        if isinstance(data, list) and len(data) > 0:
                            return data
                        else:
                            print(f'请求 {req_url} 成功，但是类型或长度有误')
                    else:
                        print(f"请求财务数据失败，状态码: {response.status_code}")
                except requests.RequestException as e:
                    print(f"请求异常: {e}，尝试更换url")
            print(f'所有url尝试完毕，仍然失败,尝试更换证书')
        print('所有证书尝试完毕，仍然失败')
        return

    
    # 3.麦蕊数据-指数列表
    @classmethod
    def mairui_mairui_index_list(cls,
                                 license_list:list):
        """
        API接口：http://api.mairui.club/zs/all/您的licence
        备用接口：http://api1.mairui.club/zs/all/您的licence
        """
        url1 = f'http://api.mairui.club/zs/all'
        url2 = f'http://api1.mairui.club/zs/all'

        # 分别使用两个接口进行尝试
        for license in license_list:
            for base_url in [url1,url2]: 
                req_url = f'{base_url}/{license}'
                try:
                    response = requests.get(req_url)
                    if response.status_code == 200:
                        # 解析json 
                        data = response.json()
                        # 返回字典数据
                        return data
                    else:
                        print(f"请求股票列表失败，状态码: {response.status_code}")
                except requests.RequestException as e:
                    print(f"请求异常: {e}，尝试更换url")
            print(f'所有url尝试完毕，仍然失败,尝试更换证书') 
        print('所有证书尝试完毕，仍然失败') 

    # 4.麦蕊数据-指数数据
    @classmethod
    def mairui_index_data(cls,
                        gid:str,
                        license_list:list)->dict:
        """
        API接口：http://api.mairui.club/zs/sssj/指数代码(如sh000001)/您的licence
        备用接口：http://api1.mairui.club/zs/sssj/指数代码(如sh000001)/您的licence 

        gid：指数代码
        license_list: 证书  \\
        

        返回结果： 
        只能返回实时数据
        t : 时间（实时数据） time
        h : 最高指数 highPrice 
        l : 最低指数 lowPrice 
        o : 开盘指数 openPrice 
        p : 当前指数 nowPrice  
        cje : 成交额 元 dealPrice 
        v : 成交量 手 dealNum
        """
        url1 = f'http://api.mairui.club/zs/sssj'
        url2 = f'http://api1.mairui.club/zs/sssj'

        # 分别使用两个接口进行尝试
        for license in license_list:
            for base_url in [url1,url2]: 
                req_url = f'{base_url}/{gid}/{license}'
                try:
                    response = requests.get(req_url)
                    if response.status_code == 200:
                        # 解析json 
                        data = response.json()

                        if isinstance(data, dict):
                            # 替换成数据库的字段名
                            result_data = {}
                            result_data['time'] = data.pop('t')
                            result_data['gid'] = gid
                            result_data['openPrice'] = data.pop('o')
                            result_data['highPrice'] = data.pop('h')
                            result_data['lowPrice'] = data.pop('l')
                            result_data['nowPrice'] = data.pop('p')
                            result_data['dealPrice'] = data.pop('cje')
                            result_data['dealNum'] = data.pop('v')

                        # 返回字典数据
                            return result_data
                    else:
                        print(f"请求指数列表失败，状态码: {response.status_code}")
                except requests.RequestException as e:
                    print(f"请求异常: {e}，尝试更换url")
            print(f'所有url尝试完毕，仍然失败,尝试更换证书') 
        print('所有证书尝试完毕，仍然失败')     

    # 5.麦蕊数据-指数大盘
    @classmethod
    def mairui_base(cls,
                    license_list:list)->dict:
        """
        API接口：http://api.mairui.club/zs/lsgl/您的licence
        备用接口：http://api1.mairui.club/zs/lsgl/您的licence

        gid：指数代码
        license_list: 证书  \\
        

        返回结果： 
        只能返回实时数据
        totalUp: 上涨总数  
        totalDown: 下跌总数 
        zt 涨停总数 
        dt 跌停总股数 
        upAToB 涨幅在A-B的数量
        downAToB 跌幅在A-B的数量
        """
        url1 = f'http://api.mairui.club/zs/lsgl'
        url2 = f'http://api1.mairui.club/zs/lsgl'

        # 分别使用两个接口进行尝试
        for license in license_list:
            for base_url in [url1,url2]: 
                req_url = f'{base_url}/{license}'
                try:
                    response = requests.get(req_url)
                    if response.status_code == 200:
                        # 解析json 
                        data = response.json()

                        if isinstance(data, dict):
                            # 替换成数据库的字段名
                            data['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            data['limitUp'] = data.pop('zt')
                            data['limitDown'] = data.pop('dt')
                            data['up8ToLimitUp'] = data.pop('up8ToZt')
                            data['down8ToLimitDown'] = data.pop('down8ToDt')                            

                        # 返回字典数据
                            return data
                    else:
                        print(f"请求指数列表失败，状态码: {response.status_code}")
                except requests.RequestException as e:
                    print(f"请求异常: {e}，尝试更换url")
            print(f'所有url尝试完毕，仍然失败,尝试更换证书') 
        print('所有证书尝试完毕，仍然失败')

    # 6.麦蕊数据 - 行业
    @classmethod
    def mairui_industry(cls,
                        gid,
                        license_list:list):
        """
        API接口：http://api.mairui.club/hszg/zg/股票代码(如000001)/您的licence
        备用接口：http://api1.mairui.club/hszg/zg/股票代码(如000001)/您的licence

        返回值不是字典，因此不做修改，返回值
        """
        url1 = 'http://api.mairui.club/hszg/zg'
        url2 = 'http://api1.mairui.club/hszg/zg'

        # 分别使用两个接口进行尝试
        for licenses in license_list:
            for base_url in [url1,url2]: 
                req_url = f"{base_url}/{gid}/{licenses}"
                try:
                    response = requests.get(req_url)
                    if response.status_code == 200:
                        # 解析json 
                        data = response.json()
                        return data
                    else:
                        print(f"请求指数列表失败，状态码: {response.status_code}")
                except requests.RequestException as e:
                    print(f"请求异常: {e}，尝试更换url")
            print(f'所有url尝试完毕，仍然失败,尝试更换证书') 
        print('所有证书尝试完毕，仍然失败')


    # ====== csmar ======
    @classmethod
    def csmar_data(cls,
                         account:str,
                         password:str,
                         columns:list,
                         condition:str,
                         table_name:str,
                         start_time:str,
                         end_time:str):
        """
        由于csmar的api接口由统一的api接口提供，因此不在函数内做清洗，请在调用后再清洗

        参数设定：  
        account:账号
        password:密码
        columns:列名 list 参考csmar的文档  
        condition: 条件，必须要填，类似WHERE后的句子，可以使用恒正确的条件来查询所有  
        table_name:表名
        start_time:开始时间
        end_time:结束时间
        """
        csmar = CsmarService()
        csmar.login(account, password)
        try:
            data = csmar.query(columns, condition, table_name, start_time, end_time)
            return data
        except:
            raise ValueError('csmar数据获取失败')

        



#======== 保存数据工具-将数据保存到mysql或其他路径 ========
class DataSaveUtils:
    def __init__(self):
        pass

    
    # 工具：将csv储存为mysql
    # ====== 将csv添加到数据表 ======
    @classmethod
    def csv_to_mysql(cls, 
                     sql_config_dict:dict, 
                     csv_file: str,
                     table_name:str):
        """
        将csv数据插入到 MySQL 表中， \\
        插入前确保csv列名和表列名一致 \\
        参数设置 csv_file: csv文件路径 \\

        sql_config_dict配置 \\
        :param host: MySQL 主机地址，默认localhost \\
        :param port: 端口号，默认3306 \\
        :param user: MySQL 用户名 \\
        :param password: MySQL 密码 \\
        :param database: 数据库名 \\
        :param cursorclass,默认 pymysql.cursors.DictCursor \\
        :param charset, 默认 utf8mb4 \\
 
        table_name: 目标表名
        """

        host = sql_config_dict.get('host','localhost')
        port = sql_config_dict.get('port',3306)
        user = sql_config_dict['user']
        password = sql_config_dict['password']
        database = sql_config_dict['database']
        charset = sql_config_dict.get('charset','utf8mb4')
        cursorclass = sql_config_dict.get('cursorclass',pymysql.cursors.DictCursor)
    
        try:
            # 连接到 MySQL 数据库
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                charset=charset,
                cursorclass=cursorclass,
                port=port
            )
            print("成功连接到数据库")
        except pymysql.Error as err:
            print(f"连接数据库时出错: {err}")
            return

        try:
            # 打开 CSV 文件
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader)  # 获取 CSV 文件的标题行
                print("成功读取 CSV 文件")

                try:
                    with connection.cursor() as cursor:
                        # 插入数据
                        placeholders = ', '.join(['%s'] * len(headers))
                        insert_query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({placeholders})"
                        for row in reader:
                            cursor.execute(insert_query, row)
                        connection.commit()
                        print("数据插入成功")
                except pymysql.Error as err:
                    print(f"插入数据时出错: {err}")
        except FileNotFoundError:
            print(f"未找到 CSV 文件: {csv_file}")
        finally:
            # 关闭数据库连接
            connection.close()


    # ====== 将字典数据插入到 MySQL 表中 ======
    @classmethod
    def dict_to_mysql(cls, sql_config_dict: dict, data_dict: dict,table_name:str):
        """
        将字典数据插入到 MySQL 表中，
        插入前确保dict键名和表列名一致

        sql_config_dict配置 \\
        :param host: MySQL 主机地址，默认localhost \\
        :param port: 端口号，默认3306 \\
        :param user: MySQL 用户名 \\
        :param password: MySQL 密码 \\
        :param database: 数据库名 \\
        :param cursorclass,默认 pymysql.cursors.DictCursor \\
        :param charset, 默认 utf8mb4 \\
 
        table_name: 目标表名
        """
        host = sql_config_dict.get('host', 'localhost')
        port = sql_config_dict.get('port', 3306)
        user = sql_config_dict['user']
        password = sql_config_dict['password']
        database = sql_config_dict['database']
        charset = sql_config_dict.get('charset', 'utf8mb4')
        cursorclass = sql_config_dict.get('cursorclass', pymysql.cursors.DictCursor)

        try:
            # 连接到 MySQL 数据库
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                charset=charset,
                cursorclass=cursorclass,
                port=port
            )

            with connection.cursor() as cursor:
                # 构建插入语句
                columns = ', '.join(data_dict.keys())
                placeholders = ', '.join(['%s'] * len(data_dict))
                insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                values = tuple(data_dict.values())

                # 执行插入语句
                cursor.execute(insert_query, values)

            # 提交事务
            connection.commit()
            print(f"成功插入数据到 {table_name} 表")
        except pymysql.Error as err:
            print(f"插入数据时出错: {err}")
        finally:
            # 关闭数据库连接
            if connection:
                connection.close()

        # 旧版本
        """
        host = sql_config_dict.get('host','localhost')
        port = sql_config_dict.get('port','3306')
        user = sql_config_dict['user']
        password = sql_config_dict['password']
        database = sql_config_dict['database']
        charset = sql_config_dict.get('charset','utf8mb4')
        cursorclass = sql_config_dict.get('cursorclass',pymysql.cursors.DictCursor)

        try:
            # 连接到 MySQL 数据库
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                charset=charset,
                cursorclass=cursorclass,
                port=port
            )

            with connection.cursor() as cursor:
                for key, value in data_dict.items():
                    if isinstance(value, (datetime, str)):
                        try:
                            if isinstance(value, str):
                                value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                            datetime_column = key
                            break
                        except ValueError:
                            continue

                # 构建插入语句
                columns = ', '.join(data_dict.keys())
                placeholders = ', '.join(['%s'] * len(data_dict))
                insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                values = tuple(data_dict.values())

                # 执行插入语句
                cursor.execute(insert_query, values)

            # 提交事务
            connection.commit()
            print(f"成功插入数据到 {table_name} 表")
        except pymysql.Error as err:
            print(f"插入数据时出错: {err}")
        finally:
            # 关闭数据库连接
            if connection:
                connection.close()
        """


    # 将polars插入的mysql中
    @classmethod
    def insert_polars_df_to_mysql(cls,
                                  dataframe:pl.DataFrame,
                                  sql_config_dict:dict,
                                  table_name:str):
        """
        将polars数据插入到 MySQL 表中，
        插入前确保dict键名和表列名一致

        sql_config_dict配置 \\
        :param host: MySQL 主机地址，默认localhost \\
        :param port: 端口号，默认3306 \\
        :param user: MySQL 用户名 \\
        :param password: MySQL 密码 \\
        :param database: 数据库名 \\
        :param cursorclass,默认 pymysql.cursors.DictCursor \\
        :param charset, 默认 utf8mb4 \\
 
        table_name: 目标表名
        """
        host = sql_config_dict.get('host', 'localhost')
        port = sql_config_dict.get('port', 3306)
        user = sql_config_dict['user']
        password = sql_config_dict['password']
        database = sql_config_dict['database']
        charset = sql_config_dict.get('charset', 'utf8mb4')
        cursorclass = sql_config_dict.get('cursorclass', pymysql.cursors.DictCursor)

        try:
            # 建立数据库连接
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                charset=charset,
                cursorclass=cursorclass
            )

            if connection.open:
                cursor = connection.cursor()
                # 获取 DataFrame 的列名
                columns = ', '.join(dataframe.columns)
                # 生成占位符
                placeholders = ', '.join(['%s'] * len(dataframe.columns))
                # 生成插入语句
                insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

                # 将 DataFrame 转换为元组列表
                data = [tuple(row) for row in dataframe.rows()]

                # 执行插入操作
                cursor.executemany(insert_query, data)
                connection.commit()
                print(f"{cursor.rowcount} 条记录插入成功。")

        except Error as e:
            print(f"错误: {e}")
        finally:
            if connection.open:
                cursor.close()
                connection.close()
                print("数据库连接已关闭。")



#%%
# ======== mysql工具，用于除了保存外的其他mysql操作 ========
class MySQLUtils:
    def __init__(self):
        pass

    # ====== 执行mysql脚本 ======
    @classmethod
    def execute_mysql_script(cls,
                             sql_config_dict:dict, 
                             script_path:str):
        """
        执行mysql脚本

        sql_config_dict配置 \\
        :param host: MySQL 主机地址，默认localhost \\
        :param port: 端口号，默认3306 \\
        :param user: MySQL 用户名 \\
        :param password: MySQL 密码 \\
        :param database: 数据库名 \\
        :param cursorclass,默认 pymysql.cursors.DictCursor \\
        :param charset, 默认 utf8mb4 \\
        """
        host = sql_config_dict.get('host', 'localhost')
        port = sql_config_dict.get('port', 3306)
        user = sql_config_dict['user']
        password = sql_config_dict['password']
        database = sql_config_dict['database']
        charset = sql_config_dict.get('charset', 'utf8mb4')
        cursorclass = sql_config_dict.get('cursorclass', pymysql.cursors.DictCursor)

        try:
            # 连接到 MySQL 数据库
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                charset=charset,
                cursorclass=cursorclass
            )
            print("成功连接到数据库")

            try:
                with open(script_path, 'r', encoding='utf-8') as file:
                    # 读取 SQL 脚本内容
                    sql_script = file.read()
                    # 按分号分割 SQL 语句
                    sql_commands = sql_script.split(';')

                    with connection.cursor() as cursor:
                        for command in sql_commands:
                            if command.strip():
                                # 执行 SQL 语句
                                cursor.execute(command)
                        # 提交事务
                        connection.commit()
                        print("SQL 脚本执行成功")
            except FileNotFoundError:
                print(f"未找到 SQL 脚本文件: {script_path}")
            except pymysql.Error as err:
                print(f"执行 SQL 脚本时出错: {err}")
        except pymysql.Error as err:
            print(f"连接数据库时出错: {err}")
        finally:
            if connection:
                # 关闭数据库连接
                connection.close()
    
    # ====== 读取mysql数据为polars-df ======
    @classmethod
    def read_mysql(cls,sql_config_dict:dict, sql_query:str)->pl.DataFrame:
        """
        从获取sql_query的请求结果

        sql_config_dict配置 \\
        :param host: MySQL 主机地址，默认localhost \\
        :param port: 端口号，默认3306 \\
        :param user: MySQL 用户名 \\
        :param password: MySQL 密码 \\
        :param database: 数据库名 \\
        :param cursorclass,默认 pymysql.cursors.DictCursor \\
        :param charset, 默认 utf8mb4 \\
        """
        host = sql_config_dict.get('host', 'localhost')
        port = sql_config_dict.get('port', 3306)
        user = sql_config_dict['user']
        password = sql_config_dict['password']
        database = sql_config_dict['database']

        # 构建数据库连接字符串
        engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

        # 构建完整的 SQL 查询语句
        sql_query

        # 从数据库中读取数据
        df = pl.read_database(sql_query, engine)

        # 返回df
        return df

    # ====== 将polars-df同步到mysql(更新) ======
    def sync_polars_df_to_mysql(df: pl.DataFrame, 
                                sql_config_dict: dict, 
                                table_name: str,
                                col_list:list):
        """
        将 polars DataFrame 中的数据同步到 MySQL 表中。

        df: polars DataFrame，包含要同步的数据。 \\

        :sql_config_dict配置 \\
        :param host: MySQL 主机地址，默认localhost \\
        :param port: 端口号，默认3306 \\
        :param user: MySQL 用户名 \\
        :param password: MySQL 密码 \\
        :param database: 数据库名 \\
        :param cursorclass,默认 pymysql.cursors.DictCursor \\
        :param charset, 默认 utf8mb4 \\
                
        table_name: 目标 MySQL 表的名称。
        col_list:更新的基准列
        """
        # 构建数据库连接字符串
        host = sql_config_dict['host']
        user = sql_config_dict['user']
        password = sql_config_dict['password']
        database = sql_config_dict['database']
        port = sql_config_dict.get('port', 3306)
        engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

        # 从 MySQL 表中读取数据
        query = f"SELECT * FROM {table_name}"
        mysql_df = pl.read_database(query, engine)

        try:
            # 找出 DataFrame 中有而 MySQL 表中没有的数据，指定连接列
            new_rows = df.join(mysql_df, on=col_list, how='anti')

            # 找出 MySQL 表中有而 DataFrame 中没有的数据，指定连接列
            deleted_rows = mysql_df.join(df, on=col_list, how='anti')
        except:
            raise ValueError('col_list列名错误')

        try:
            # 插入新数据到 MySQL 表
            if not new_rows.is_empty():
                new_rows.write_database(table_name, engine, if_table_exists='append')
                print(f"成功插入 {len(new_rows)} 条新记录到 {table_name} 表。")
            else:
                print('没有新股票插入')
        except:
            print('新股票插入错误')
        
        # 从 MySQL 表中删除不存在的数据
        if not deleted_rows.is_empty():
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            try:
                with connection.cursor() as cursor:
                    # 暂时禁用外键约束
                    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                    for row in deleted_rows.iter_rows(named=True):
                        conditions = " AND ".join([f"{col} = %s" for col in row.keys()])
                        delete_query = f"DELETE FROM {table_name} WHERE {conditions}"
                        cursor.execute(delete_query, tuple(row.values()))
                    # 提交事务
                    connection.commit()
                    # 启用外键约束
                    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                    print(f"成功从 {table_name} 表中删除 {len(deleted_rows)} 条记录。")
            except pymysql.Error as err:
                print(f"删除数据时出错: {err}")
            finally:
                connection.close()
        else:
            print('没有旧股票删除')
    @classmethod
    def execute_sql(cls,sql_config_dict, sql):
        """
        根据数据库配置信息执行 SQL 语句

        :param config: 数据库配置字典，包含 host, user, password, database, port 等信息
        :param sql: 要执行的 SQL 语句
        :return: 执行结果
        """
        try:
            host = sql_config_dict.get('host', 'localhost')
            port = sql_config_dict.get('port', 3306)
            user = sql_config_dict['user']
            password = sql_config_dict['password']
            database = sql_config_dict['database']
            charset = sql_config_dict.get('charset', 'utf8mb4')
            cursorclass = sql_config_dict.get('cursorclass', pymysql.cursors.DictCursor)

            # 连接到数据库
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port,
                charset=charset,
                cursorclass=cursorclass
            )
            print("成功连接到数据库")

            with connection.cursor() as cursor:
                # 执行 SQL 语句
                cursor.execute(sql)
                if sql.strip().lower().startswith('select'):
                    # 如果是 SELECT 语句，获取查询结果
                    result = cursor.fetchall()
                else:
                    # 对于其他语句（如 INSERT, UPDATE, DELETE 等），提交事务
                    connection.commit()
                    result = "操作成功"
                return result
        except pymysql.Error as err:
            print(f"执行 SQL 语句时出错: {err}")
            return None
        finally:
            if connection:
                # 关闭数据库连接
                connection.close()
     
