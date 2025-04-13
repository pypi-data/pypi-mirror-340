"""Calc Server Module."""

from datetime import datetime

import requests

from .logger import logger


class CalcServer:
    """CalcServer Class."""

    def __init__(self, parent):
        """Class constructor."""
        self.base_url = parent.env.get("calc_server_url")

    def __post(self, endpoint, json=None):
        """Make Post Request.

        Args:
            endpoint (_type_): _description_
            json (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        res = requests.post(f"{self.base_url}{endpoint}", json=json, timeout=10)
        try:
            return res.json()
        except requests.JSONDecodeError as e:
            logger.error(
                f"JSON decode error for POST endpoint {endpoint}, res: {res}, {e}"
            )
            return res
        except Exception as e:
            logger.error(f"error in POST endpoint {endpoint}, res: {res}, {e}")
            raise

    def __get(self, endpoint, params=None):
        """Make Get Request.

        Args:
            endpoint (_type_): _description_
            params (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        res = requests.get(f"{self.base_url}{endpoint}", params=params, timeout=10)
        try:
            return res.json()
        except requests.JSONDecodeError as e:
            logger.error(
                f"JSON decode error for POST endpoint {endpoint}, res: {res}, {e}"
            )
            return res
        except Exception as e:
            logger.error(f"error in POST endpoint {endpoint}, res: {res}, {e}")
            raise

    def mark_price(self, positions, currency="ETH"):
        """Fetch positions Mark Price."""
        return self.__post(
            f"/price_list?currency={currency}",
            json=positions,
        )

    def get_mtm(self, positions, currency="ETH"):
        """Fetch positions Mark to Market."""
        return self.__post(
            f"/calc_mtm?currency={currency}",
            json=positions,
        )

    def get_greeks(self, positions, currency="ETH", ref_date=None):
        """Fetch positions greeks."""
        endpoint_date = "" if ref_date is None else f"&ref_date={ref_date}"
        return self.__post(
            f"/position_risk?currency={currency}{endpoint_date}",
            json=positions,
        )

    def market_snapshot(self, currency="ETH"):
        """Fetch market snapshot for a currency."""
        return self.__get(f"/market_snapshot?currency={currency}")

    def get_volsurface(self, currency="ETH"):
        """Fetch pickled vol surface."""
        response = self.__get(f"/volsurface_pickle?currency={currency}")
        response.raise_for_status()
        return response.content

    def get_volsurface_date(self, currency="ETH"):
        """Fetch vol surface anchor date."""
        res = self.__get(f"/vol_surface/date?currency={currency}")
        return datetime.fromisoformat(res)

    def get_spot_ladder(self, positions: list, spot_range: list = [-0.05, 0, 0.05], currency: str = "ETH"):
        """Fetch spot ladder."""
        payload = {
            "positions": positions,
            "spot_range": spot_range
}
        return self.__post(
            f"/risk_spot_ladder?currency={currency}",
            json=payload,
        )

