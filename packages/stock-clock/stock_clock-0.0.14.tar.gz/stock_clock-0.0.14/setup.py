import setuptools

with open("/www/files/Stock/stock-clock/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stock-clock",
    version="0.0.14",
    author="Qi Yueran",
    author_email="stockclock@126.com",
    description="Utils for Stock-Clock",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=['stockclock','stockclock.Technical','stockclock.Sample']),  # 修改1/3：直接指定包名
    package_dir={'stockclock': 'stockclock'},  # 修改2/3：映射目录名称
        install_requires=[
        'requests>=2.28',        # API请求
        'polars[all]>=0.19',     # 数据处理（包含所有扩展）
        'pymysql>=1.1',          # MySQL驱动
        'sqlalchemy>=2.0',       # 数据库ORM
        'numpy>=1.24',           # 数值计算
        'mysql-connector-python>=8.0',  # MySQL官方驱动
        'python-dotenv>=1.0',    # 环境变量管理
        'typing-extensions>=4.5' # 类型提示支持
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
