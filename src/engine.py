class DataFeed:
    def get_price(self, instrument):
        """Retrieve latest price for the given instrument."""
        raise NotImplementedError

class Broker:
    def send_order(self, order):
        """Send an order to the market."""
        raise NotImplementedError

class Gateway:
    """Trading interface, e.g. TqSdk or CTP."""

    def connect(self):
        raise NotImplementedError

    def send_order(self, order):
        raise NotImplementedError

class CTPGateway(Gateway):
    def connect(self):
        """Connect to the CTP interface."""
        # placeholder for actual CTP connection logic
        pass

    def send_order(self, order):
        # placeholder for sending order via CTP
        pass

class TqSdkGateway(Gateway):
    def connect(self):
        """Connect to the TqSdk interface."""
        pass

    def send_order(self, order):
        pass

class Strategy:
    def on_tick(self, data):
        """Strategy logic for each new market data tick."""
        raise NotImplementedError

class Order:
    def __init__(self, instrument: str, direction: str, volume: int, price: float):
        self.instrument = instrument
        self.direction = direction
        self.volume = volume
        self.price = price

class Account:
    def __init__(self, name: str, gateway: Gateway):
        self.name = name
        self.gateway = gateway
        self.positions = {}

    def connect(self):
        self.gateway.connect()

    def send_order(self, order: Order):
        self.gateway.send_order(order)

    def update_position(self, instrument: str, volume: int):
        self.positions[instrument] = self.positions.get(instrument, 0) + volume

class AccountManager:
    def __init__(self):
        self.accounts = {}

    def add_account(self, account: Account):
        self.accounts[account.name] = account

    def connect_all(self):
        for account in self.accounts.values():
            account.connect()

    def send_bulk_order(self, order: Order):
        for account in self.accounts.values():
            account.send_order(order)

class RiskManager:
    def check_order(self, account: Account, order: Order) -> bool:
        """Simple risk check example."""
        # placeholder for real risk logic
        return order.volume > 0 and order.price > 0

class Trader:
    def __init__(self, data_feed: DataFeed, account_manager: AccountManager, strategy: Strategy, risk: RiskManager):
        self.data_feed = data_feed
        self.account_manager = account_manager
        self.strategy = strategy
        self.risk = risk

    def run(self):
        self.account_manager.connect_all()
        while True:
            data = self.data_feed.get_price('DEFAULT')
            orders = self.strategy.on_tick(data) or []
            for order in orders:
                for account in self.account_manager.accounts.values():
                    if self.risk.check_order(account, order):
                        account.send_order(order)
