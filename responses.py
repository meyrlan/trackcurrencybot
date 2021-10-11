from binance_class import BinanceAPI

def sample_responses(message, second_):
    message = str(message).lower()

    if message in ("hey", "hi", "hello"):
        return "Hey! How do you do?"

    symbol_first = str(message).upper()
    symbol_second = second_
    symbol = f"{symbol_first}{symbol_second}"
    _binance_obj = BinanceAPI(p_symbol_first=symbol_first, p_symbol_second=symbol_second)

    if _binance_obj.check_client_build_ok():
        _out = _binance_obj.general_get_symbol_avg_price()
        ans = ""
        if _out[0] == 'OK':
            ans += (f"Price of 1 {symbol_first} in {symbol_second}: {_out[1]}\n")
            # ans += (f"{chr(10)}\n")
            return ans

    return "I don't understand you!"