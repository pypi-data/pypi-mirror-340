from pathlib import Path
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def read_all_patterns(file_path):
    """
    Read all patterns from the text file into a list of lists.
    """
    patterns = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                values = line.strip().split(",")
                pattern = [float(val) for val in values]
                patterns.append(pattern)
        return patterns
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except ValueError as e:
        print(f"Error: Invalid data format in file: {e}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
def perc(new_value: float, old_value: float):
    return ((new_value - old_value) / old_value) * 100

def parse_volume(value: str) -> float:
    value = value.upper().replace(',', '').strip()
    if value.endswith('K'):
        return float(value[:-1]) * 1_000
    elif value.endswith('M'):
        return float(value[:-1]) * 1_000_000
    elif value.endswith('B'):
        return float(value[:-1]) * 1_000_000_000
    else:
        return float(value)
    
def data_loader(file_path: Path, close_column: str, volume_column: str):
    
    #load data
    df = pd.read_csv(file_path)

    #validate data 
    
    if df.isnull().sum().sum() > 0:
        raise ValueError("Invalid csv format!!")
    
    if close_column not in df.columns:
        raise ValueError(f"Close column '{close_column}' not found in the data.")
    
    if volume_column not in df.columns:
        raise ValueError(f"Volume column '{volume_column}' not found in the data.")
    
    # Clean close prices (remove commas and convert to float)
    close_data = df[close_column].astype(str).str.replace(',', '').astype(float).tolist()

    # Clean volumes (parse K, M, B)
    volume_data = df[volume_column].astype(str).apply(parse_volume).tolist()

    if len(close_data) != len(volume_data):
        raise ValueError("Both data have mismatched sizes!")
    
    return close_data, volume_data

def gen_pattern(close_data: list, volume_data: list, past_candles_no: int, future_candles_no: int, threshold_change: float, file_path: Path):
    
    pattern = []
    total_window = past_candles_no + future_candles_no
    
    for i in range(0, len(close_data) - total_window + 1):
        close_window = close_data[i:i + total_window]      
        volume_window = volume_data[i:i + total_window] 

        close_first_window = close_data[:past_candles_no]
        close_second_window = close_window[past_candles_no:]
        
        volume_first_window = volume_window[:past_candles_no]
        volume_second_window = volume_window[past_candles_no:]
        
        old_value = close_first_window[-1]
        new_value = close_second_window[-1]

        if old_value == 0 or old_value == new_value:
            change = 0
        else:
            change = perc(new_value, old_value)

        if change >= threshold_change or change <= -threshold_change:
            temp_pattern = []
            print(change)
            prev_close = 0
            prev_vol = 0

            for close in close_first_window:
                if prev_close == 0:
                    temp_pattern.append(0)
                    prev_close = close
                else:
                    change_close = perc(close,prev_close)
                    temp_pattern.append(change_close)
                    prev_close = close
            
            for vol in volume_first_window:
                if prev_vol == 0:
                    temp_pattern.append(0)
                    prev_vol = vol
                else:
                    change_vol = perc(vol,prev_vol)
                    temp_pattern.append(change_vol)
                    prev_vol = vol
        
            temp_pattern.append(change)
            pattern.append(temp_pattern)

            with open(file_path, 'w') as f:
                for pat in pattern:
                    line = ','.join(f"{x:.2f}" for x in pat)  # 6 decimal precision
                    f.write(line + '\n')
            
    return f"Pattern generation completed successfully! {len(pattern)} patterns saved to {file_path}"

def match_patterns(close_data: list, volume_data: list, pattern_text_file: Path, past_candles_no: int, close_confidence: float = None, volume_confidence: float = None):
    all_pattern = read_all_patterns(pattern_text_file)

    if len(close_data) != past_candles_no or len(volume_data) != past_candles_no:
        raise ValueError("invalid size of data!!")
    else:
        prev_close = 0
        pattern = []
        for close in close_data:
            if prev_close == 0:
                pattern.append(0)
                prev_close = close
            else:
                value = perc(close,prev_close)
                pattern.append(value)
                prev_close = close

        prev_vol = 0
        for vol in volume_data:
            if prev_vol == 0:
                pattern.append(0)
                prev_vol = vol
            else:
                value = perc(vol,prev_vol)
                pattern.append(value)
                prev_vol = vol
        
        price_part = pattern[:past_candles_no]
        volume_part = pattern[past_candles_no:]

        max_confidence_close = 0
        max_confidence_volume = 0
        pattern_index = 0

        for i, current_pattern in enumerate(all_pattern):
                stored_price_part = current_pattern[:past_candles_no]
                stored_volume_part = current_pattern[past_candles_no:-1]

                if len(current_pattern) < 10:
                    print(f"Warning: Pattern {i} has only {len(current_pattern)} elements, skipping.\n")
                    continue

                price_similarity = cosine_similarity([price_part], [stored_price_part])[0][0]
                volume_similarity = cosine_similarity([volume_part], [stored_volume_part])[0][0]
                
                if close_confidence is not None and volume_confidence is not None:
                    if price_similarity > close_confidence:
                        if price_similarity > max_confidence_close:
                            if volume_similarity > volume_confidence:
                                if volume_similarity > max_confidence_volume:
                                    max_confidence_close = price_similarity
                                    max_confidence_volume = volume_similarity
                                    pattern_index = i

                else:
                    if price_similarity > max_confidence_close:
                        if volume_similarity > max_confidence_volume:
                            max_confidence_close = price_similarity
                            max_confidence_volume = volume_similarity
                            pattern_index = i
        
        found_pattern = all_pattern[i]
        change = found_pattern[-1]
        print(f"Market Will go {change}% in future( Invest On Your Own Risk this is just experimental test!!)")
        return change

