import os
from Ashare import *
import pandas as pd

# 1. 从环境变量获取参数，如果没有则使用默认值（方便本地调试）
target_stock = os.environ.get('STOCK_CODE', 'sh600900')
start_date_str = os.environ.get('START_DATE', '2024-09-18')
# 【新增】获取周期参数，默认为日线 '1d'
frequency = os.environ.get('FREQUENCY', '1d')

def run_task():
    print(f"开始获取 {target_stock} 的历史数据...")
    print(f"起始时间设定为: {start_date_str}")
    print(f"设定周期为: {frequency}")
    
    try:
        # 2. 获取数据 (传入动态的 frequency 变量)
        df = get_price(target_stock, frequency=frequency)
        
        if df is None or df.empty:
            print(f"未能获取到 {target_stock} 的数据，请检查代码输入是否正确。")
            return

        # 3. 处理日期索引
        df.index = pd.to_datetime(df.index)
        
        # 4. 按日期过滤
        df_filtered = df[df.index >= start_date_str]

        if df_filtered.empty:
            print(f"日期范围内 ({start_date_str} 至今) 没有找到数据。")
            return

        # 5. 打印结果预览
        print(f"成功获取数据：从 {df_filtered.index.min().strftime('%Y-%m-%d %H:%M:%S')} 到 {df_filtered.index.max().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"共计 {len(df_filtered)} 条K线记录。")

        # 6. 动态命名文件：股票代码_周期_起始日期.csv (加入周期防止文件名冲突)
        # 例如：sh600900_15m_2024-09-18.csv
        output_file = f"{target_stock}_{frequency}_{start_date_str}.csv"
        
        df_filtered.to_csv(output_file, encoding='utf-8-sig')
        print(f"\n文件已成功保存为: {output_file}")

    except Exception as e:
        print(f"运行出错: {e}")

if __name__ == "__main__":
    run_task()
