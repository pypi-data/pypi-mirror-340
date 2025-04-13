import asyncio
import logging
from xecution.common.enums import Exchange, KlineType, Mode, Symbol
from xecution.models.config import OrderConfig, RuntimeConfig
from xecution.models.topic import KlineTopic
from xecution.services.exchange.binance_service import BinanceService
from xecution.services.exchange.bybit_service import BybitService
from xecution.services.exchange.okx_service import OkxService

class BaseEngine:
    """Base engine that initializes BinanceService and processes on_candle_closed and on_datasource_update."""

    def __init__(self, config: RuntimeConfig):
        self.config = config
        self.data_map = {}  # Local data storage for kline data
        self.binance_service = BinanceService(config, self.data_map)  # Pass data_map to BinanceService
        self.bybit_service = BybitService(config, self.data_map)  # Pass data_map to BybitService
        self.okx_service = OkxService(config, self.data_map)  # Pass data_map to OkxService

    async def on_candle_closed(self, kline_topic: KlineTopic):
        """Handles closed candle data"""

    async def on_order_update(self, order):
        """Handles order status"""

    async def on_datasource_update(self, datasource_topic):
        """Handles updates from external data sources."""

    async def start(self):
        """Starts BinanceService and behaves differently based on the runtime mode."""
        try:
            await self.binance_service.get_klines(self.on_candle_closed)

            if self.config.mode == Mode.Live or self.config.mode == Mode.Testnet:
                await self.binance_service.check_connection()
                while True:
                    await asyncio.sleep(1)  # Keep the loop alive
            else:
                logging.info("Backtest mode completed. Exiting.")
        except ConnectionError as e:
                logging.error(f"Connection check failed: {e}")
        
    async def place_order(self, order_config: OrderConfig):
        await self.binance_service.place_order(order_config)
        
    async def get_account_info(self):
        return await self.binance_service.get_account_info()

    async def set_hedge_mode(self, is_hedge_mode: bool):
        return await self.binance_service.set_hedge_mode( is_hedge_mode)

    async def set_leverage(self, symbol: Symbol, leverage: int):
        return await self.binance_service.set_leverage(symbol, leverage)
    
    async def get_position_info(self, symbol: Symbol):
        return await self.binance_service.get_position_info(symbol)
    
    async def get_wallet_balance(self):
        return await self.binance_service.get_wallet_balance()

    async def get_current_price(self,symbol: Symbol):
        if self.config.exchange == Exchange.Binance:
            return await self.binance_service.get_current_price(symbol)
        elif self.config.exchange == Exchange.Bybit:
            return await self.bybit_service.get_current_price(symbol)
        elif self.config.exchange == Exchange.Okx:
            return await self.okx_service.get_current_price(symbol)
        else:
            logging.error("Unknown exchange")
            return None
        
    async def get_order_book(self,symbol:Symbol):
        if self.config.exchange == Exchange.Binance:
            return await self.binance_service.get_order_book(symbol)
        else:
            logging.error("Unknown exchange")
            return None

    async def listen_order_status(self,kline_topic: KlineTopic):
        if self.config.exchange == Exchange.Binance:
            return await self.binance_service.listen_order_status(self.on_order_update,kline_topic)
        else:
            logging.error("Unknown exchange")
            return None
