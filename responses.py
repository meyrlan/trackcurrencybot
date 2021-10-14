from binance_class import BinanceAPI

def sample_responses(message, second_):
    message = str(message).lower()

    symbol_first = str(message).upper()
    symbol_second = second_
    symbol = f"{symbol_first}{symbol_second}"
    print(symbol_first + " " + symbol_second)
    _binance_obj = BinanceAPI(p_symbol_first=symbol_first, p_symbol_second=symbol_second)

    if _binance_obj.check_client_build_ok():
        _out = _binance_obj.general_get_symbol_avg_price()
        ans = ""
        print("Okay")
        if _out[0] == 'OK':
            ans += (f"1 {symbol_first} = {_out[1]} {symbol_second}")
            return ans

    cur = symbol_first
    symbol_first = symbol_second
    symbol_second = cur

    symbol = f"{symbol_first}{symbol_second}"
    print(symbol_first + " " + symbol_second)
    _binance_obj = BinanceAPI(p_symbol_first=symbol_first, p_symbol_second=symbol_second)

    if _binance_obj.check_client_build_ok():
        _out = _binance_obj.general_get_symbol_avg_price()
        ans = ""
        print("Okay")
        if _out[0] == 'OK':
            ans += (f"1 {symbol_second} = {1 / _out[1]} {symbol_first}")
            return ans

    return "I don't understand you!"