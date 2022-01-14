from FtxProcessor import FtxProcessor

ftx=FtxProcessor()
TRADING_FEES=0.14*2  #open+close fee *2

def return_only_with_spot(spot_market,future_market):
    _to_return=[]
    for future in future_market:
        spot_eqv=future.split(":")[0]
        if(spot_eqv in spot_market):
            _to_return.append(future)
    return _to_return

def get_futures(exchange_interface):
    futures=[]
    markets=exchange_interface.getMarkets()
    for i in markets:
        pair= i.split("/")
        if "USD:USD-" in pair[1]:
            futures.append(i)
    return futures

def get_spot(exchange_interface):
    futures=[]
    markets=exchange_interface.getMarkets()
    for i in markets:
        pair= i.split("/")
        if "USD" == pair[1]:
            futures.append(i)
    return futures

def compare_price(exchange,futures):
    _to_return=[]
    for future in futures:
        price_future=exchange.getActualPrice(future)
        price_spot  =exchange.getActualPrice(future.split(":")[0])
        premium_percent=((price_future-price_spot)/(price_spot))*100
        if premium_percent>0:
            _to_return.append([future,premium_percent*(1-TRADING_FEES)])
            #print(future,price_future,price_spot,float(premium_percent))
    _ordered = sorted(_to_return, key=lambda x: x[1],reverse=True)
    return _ordered       

def plot_results(array):
    print("FUTURE","%PREMIUM")
    for i in array:
        print(i[0],i[1])

spread=compare_price(ftx,return_only_with_spot(get_spot(ftx),get_futures(ftx)))
plot_results(spread)

