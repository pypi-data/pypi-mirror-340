from abc import ABC, abstractmethod
from typing import Any, ClassVar

from .event import (
    EVENT_ACCOUNT,
    EVENT_CONTRACT,
    EVENT_ORDER,
    EVENT_POSITION,
    EVENT_QUOTE,
    EVENT_TICK,
    EVENT_TRADE,
    Event,
    EventEngine,
)
from .object import (
    AccountData,
    BarData,
    CancelRequest,
    ContractData,
    Exchange,
    HistoryRequest,
    OrderData,
    OrderRequest,
    PositionData,
    QuoteData,
    QuoteRequest,
    SubscribeRequest,
    TickData,
    TradeData,
)


class BaseGateway(ABC):
    """
    Abstract base class for trading gateways.

    A gateway connects trading platform with brokerage APIs,
    providing standardized interface for:
    1. Market data subscription
    2. Order management
    3. Account information queries

    Implementation requirements:
    * Thread-safe and non-blocking
    * Must implement all abstractmethod
    * Must handle callbacks for on_tick, on_trade, on_order,
      on_position, on_account, on_contract
    """

    default_name: str = ""
    default_setting: ClassVar[dict[str, Any]] = {}
    exchanges: ClassVar[list[Exchange]] = []

    def __init__(self, event_engine: EventEngine, gateway_name: str = "") -> None:
        """
        Initialize a gateway instance.

        Args:
            event_engine: Event engine for pushing data updates
            gateway_name: Name of the gateway
        """
        self.event_engine = event_engine
        self.gateway_name = gateway_name

    def on_event(self, type: str, data: Any = None) -> None:
        """
        Push an event to event engine.

        Args:
            type: Event type string
            data: Event data object
        """
        event: Event = Event(type, data)
        self.event_engine.put(event)

    def on_tick(self, tick: TickData) -> None:
        """
        Push tick event.

        Args:
            tick: Tick data object
        """
        self.on_event(EVENT_TICK, tick)
        self.on_event(EVENT_TICK + tick.symbol, tick)

    def on_trade(self, trade: TradeData) -> None:
        """
        Push trade event.

        Args:
            trade: Trade data object
        """
        self.on_event(EVENT_TRADE, trade)
        self.on_event(EVENT_TRADE + trade.symbol, trade)

    def on_order(self, order: OrderData) -> None:
        """
        Push order event.

        Args:
            order: Order data object
        """
        self.on_event(EVENT_ORDER, order)
        self.on_event(EVENT_ORDER + order.orderid_with_gateway, order)

    def on_position(self, position: PositionData) -> None:
        """
        Push position event.

        Args:
            position: Position data object
        """
        self.on_event(EVENT_POSITION, position)
        self.on_event(EVENT_POSITION + position.symbol, position)

    def on_account(self, account: AccountData) -> None:
        """
        Push account event.

        Args:
            account: Account data object
        """
        self.on_event(EVENT_ACCOUNT, account)
        self.on_event(EVENT_ACCOUNT + account.accountid, account)

    def on_quote(self, quote: QuoteData) -> None:
        """
        Push quote event.

        Args:
            quote: Quote data object
        """
        self.on_event(EVENT_QUOTE, quote)
        self.on_event(EVENT_QUOTE + quote.symbol, quote)

    def on_contract(self, contract: ContractData) -> None:
        """
        Push contract event.

        Args:
            contract: Contract data object
        """
        self.on_event(EVENT_CONTRACT, contract)

    @abstractmethod
    def connect(self, setting: dict) -> None:
        """
        Connect to trading server.

        Implementation requirements:
        * Connect to server
        * Log connection status
        * Query account, position, orders, trades, contracts
        * Push data through on_* callbacks

        Args:
            setting: Connection settings
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Close connection to trading server.
        """
        pass

    @abstractmethod
    def subscribe(self, req: SubscribeRequest) -> None:
        """
        Subscribe to market data.

        Args:
            req: Subscription request object
        """
        pass

    @abstractmethod
    def send_order(self, req: OrderRequest) -> str:
        """
        Send new order to server.

        Implementation requirements:
        * Create OrderData from request
        * Assign unique orderid
        * Send to server
        * Return orderid for reference

        Args:
            req: Order request object

        Returns:
            str: Unique order ID
        """
        pass

    @abstractmethod
    def cancel_order(self, req: CancelRequest) -> None:
        """
        Cancel existing order.

        Args:
            req: Cancel request object
        """
        pass

    def send_quote(self, req: QuoteRequest) -> str:
        """
        Send quote to server.

        Args:
            req: Quote request object

        Returns:
            str: Quote ID
        """
        return ""

    @abstractmethod
    def cancel_quote(self, req: CancelRequest) -> None:
        """
        Cancel existing quote.

        Args:
            req: Cancel request object
        """
        pass

    @abstractmethod
    def query_account(self) -> None:
        """
        Query account balance from server.
        """
        pass

    @abstractmethod
    def query_position(self) -> None:
        """
        Query positions from server.
        """
        pass

    @abstractmethod
    def query_history(self, req: HistoryRequest) -> list[BarData]:
        """
        Query bar history data from server.

        Args:
            req: History request object

        Returns:
            List[BarData]: List of bar data
        """
        pass

    def get_default_setting(self) -> dict[str, Any]:
        """
        Get default connection settings.

        Returns:
            Dict[str, Any]: Default settings
        """
        return self.default_setting
