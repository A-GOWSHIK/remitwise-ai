"""
RemitWise AI – Exchange Service
=================================
All interaction with the Frankfurter API is encapsulated here.
Routes and agents should call these functions – never call the external API
directly from a route handler.
"""

import logging
from datetime import date
from typing import Any, Dict, List, Optional

import requests
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout, Timeout

from config import settings
from utils.validators import validate_currency, validate_date_range, validate_date_string

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Execute a GET request against the Frankfurter base URL.

    Parameters
    ----------
    path:
        URL path, e.g. ``"/latest"`` or ``"/2024-01-01"``
    params:
        Optional query-string parameters.

    Returns
    -------
    dict
        Parsed JSON response body.

    Raises
    ------
    requests.exceptions.Timeout
        When the upstream server does not respond within the configured timeout.
    requests.exceptions.ConnectionError
        When the network is unreachable.
    requests.exceptions.HTTPError
        When the upstream returns a 4xx / 5xx status code.
    """
    url = f"{settings.FRANKFURTER_BASE_URL}{path}"
    logger.debug("GET %s params=%s", url, params)

    try:
        response = requests.get(
            url,
            params=params,
            timeout=settings.HTTP_TIMEOUT_SECONDS,
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        return response.json()

    except ReadTimeout as exc:
        logger.error("Read timeout calling Frankfurter: %s", exc)
        raise Timeout(
            f"Frankfurter API timed out after {settings.HTTP_TIMEOUT_SECONDS}s."
        ) from exc
    except Timeout as exc:
        logger.error("Timeout calling Frankfurter: %s", exc)
        raise
    except ConnectionError as exc:
        logger.error("Network error calling Frankfurter: %s", exc)
        raise
    except HTTPError as exc:
        logger.error(
            "HTTP error from Frankfurter: status=%s body=%s",
            exc.response.status_code,
            exc.response.text[:200],
        )
        raise


# ---------------------------------------------------------------------------
# Public service functions
# ---------------------------------------------------------------------------

def get_latest_rate(
    base: str,
    target: str,
) -> Dict[str, Any]:
    """
    Fetch the latest exchange rate between two currencies.

    Parameters
    ----------
    base:
        Source currency code (e.g. ``"USD"``).
    target:
        Target currency code (e.g. ``"INR"``).

    Returns
    -------
    dict
        ``{"base": str, "target": str, "rate": float, "date": str, "amount": float}``

    Raises
    ------
    ValueError
        For unsupported or identical currency codes.
    requests.exceptions.RequestException
        On network or HTTP errors.
    """
    base = validate_currency(base)
    target = validate_currency(target)

    if base == target:
        raise ValueError("Base and target currency must differ.")

    data = _get("/latest", params={"from": base, "to": target, "amount": 1})
    rate = data["rates"][target]

    logger.info("Latest rate %s→%s = %.6f", base, target, rate)
    return {
        "base": base,
        "target": target,
        "rate": rate,
        "date": data.get("date"),
        "amount": data.get("amount", 1),
        "source": "Frankfurter API",
    }


def get_historical_rates(
    base: str,
    target: str,
    start_date: str,
    end_date: str,
) -> Dict[str, Any]:
    """
    Fetch historical exchange rates for a date range.

    Parameters
    ----------
    base:
        Source currency code.
    target:
        Target currency code.
    start_date:
        Start of the range, format ``YYYY-MM-DD``.
    end_date:
        End of the range, format ``YYYY-MM-DD``.

    Returns
    -------
    dict
        ``{"base", "target", "start_date", "end_date", "rates": {date: rate}, "count"}``

    Raises
    ------
    ValueError
        For invalid inputs.
    requests.exceptions.RequestException
        On network or HTTP errors.
    """
    base = validate_currency(base)
    target = validate_currency(target)

    if base == target:
        raise ValueError("Base and target currency must differ.")

    start, end = validate_date_range(start_date, end_date)
    path = f"/{start}..{end}"

    data = _get(path, params={"from": base, "to": target, "amount": 1})

    # Frankfurter returns {"rates": {"YYYY-MM-DD": {"TARGET": value}}}
    raw_rates: Dict[str, Dict[str, float]] = data.get("rates", {})
    flat_rates = {day: vals[target] for day, vals in raw_rates.items() if target in vals}

    logger.info(
        "Historical rates %s→%s from %s to %s: %d data points",
        base, target, start, end, len(flat_rates),
    )
    return {
        "base": base,
        "target": target,
        "start_date": str(start),
        "end_date": str(end),
        "rates": flat_rates,
        "count": len(flat_rates),
        "source": "Frankfurter API",
    }


def list_supported_currencies() -> Dict[str, Any]:
    """
    Return all currencies supported by the Frankfurter API.

    Returns
    -------
    dict
        ``{"currencies": {code: name}, "count": int}``

    Raises
    ------
    requests.exceptions.RequestException
        On network or HTTP errors.
    """
    data = _get("/currencies")
    logger.info("Fetched %d currencies from Frankfurter", len(data))
    return {
        "currencies": data,
        "count": len(data),
        "source": "Frankfurter API",
    }


def convert_amount(
    base: str,
    target: str,
    amount: float,
) -> Dict[str, Any]:
    """
    Convert a specific monetary amount using the latest exchange rate.

    Parameters
    ----------
    base:
        Source currency code.
    target:
        Target currency code.
    amount:
        Amount to convert (must be positive).

    Returns
    -------
    dict
        ``{"base", "target", "original_amount", "converted_amount", "rate", "date"}``
    """
    base = validate_currency(base)
    target = validate_currency(target)

    if base == target:
        raise ValueError("Base and target currency must differ.")
    if amount <= 0:
        raise ValueError("Amount must be a positive number.")

    data = _get("/latest", params={"from": base, "to": target, "amount": amount})
    converted = data["rates"][target]
    rate = converted / amount

    logger.info(
        "Converted %.2f %s → %.2f %s (rate=%.6f)",
        amount, base, converted, target, rate,
    )
    return {
        "base": base,
        "target": target,
        "original_amount": amount,
        "converted_amount": round(converted, 4),
        "rate": round(rate, 6),
        "date": data.get("date"),
        "source": "Frankfurter API",
    }
