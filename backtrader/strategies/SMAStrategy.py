import backtrader as bt


class SMAStrategy(bt.Strategy):
    params = (
        ('SMA1', 36),  # Default value for SMA1
        ('SMA2', 220),  # Default value for SMA2
    )

    def __init__(self):
        # Initialize SMA indicators
        self.sma1 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.SMA1)
        self.sma2 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.SMA2)
        # Track position
        self.position_flag = None

    def next(self):
        # Get available cash
        cash = self.broker.getcash()

        # Get current price
        price = self.data.close[0]
        
        # Get commission from the broker (assuming percentage commission)
        commission_rate = self.broker.getcommissioninfo(self.data).p.commission

        # Calculate the cost per share including commission
        cost_per_share = price * (1 + commission_rate)

        # Calculate the maximum number of shares that can be bought with the available cash
        size = cash // cost_per_share

        # Execute buy order with calculated size if a buy signal is triggered
        if self.sma1 > self.sma2 and not self.position and size > 0:
            self.buy(size=size)  # Buy max shares accounting for commission

        # If SMA1 crosses below SMA2, exit position by selling all shares
        elif self.sma1 < self.sma2 and self.position:
            self.sell(size=self.position.size)  # Sell all shares

    def stop(self):
        # This function is called at the end of the backtest or optimization
        final_value = self.broker.getvalue()
        print(f'SMA1: {self.params.SMA1}, SMA2: {self.params.SMA2} -> Final Value: {final_value}')
