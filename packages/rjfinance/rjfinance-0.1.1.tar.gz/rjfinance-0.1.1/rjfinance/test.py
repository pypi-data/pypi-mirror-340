from main import data_loader
from main import gen_pattern
from main import match_patterns
file_path = r"D:\workdd==2\STOCK_PREDICTION\DATA\RAW_DATA\Nifty 50 Historical Data.csv"

# Specify the column names
close_column = "Close"
volume_column = "Vol."


close_data, volume_data = data_loader(file_path, close_column, volume_column)
print(type(close_data))

file_path = r"D:\workdd==2\STOCK_PREDICTION\DATA\RAW_DATA\Nifty 50 Historical Data.txt"

patterns = gen_pattern(close_data=close_data,volume_data=volume_data,past_candles_no=5,future_candles_no=3,threshold_change=1,file_path=file_path)

print(patterns)

close_data = [100.0, 100.15, 99.97, 100.20, 100.42]
volume_data = [1000.0, 670.0, 658.67, 885.83, 896.80]

file_path = r"D:\workdd==2\STOCK_PREDICTION\DATA\RAW_DATA\Nifty 50 Historical Data.txt"

match_patterns(close_data, volume_data, file_path, past_candles_no=5)
