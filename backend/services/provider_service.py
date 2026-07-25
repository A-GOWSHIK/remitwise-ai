"""
RemitWise AI – Provider Service
=================================
Loads provider data from the local JSON file and exposes query functions.
"""

import logging
from typing import Any, Dict, List, Optional

from config import settings
from utils.file_loader import load_json_file

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _load_providers() -> List[Dict[str, Any]]:
    """Load and return the raw provider list from disk (cached)."""
    data = load_json_file(settings.PROVIDERS_FILE)
    return data.get("providers", [])


# ---------------------------------------------------------------------------
# Public service functions
# ---------------------------------------------------------------------------

def list_providers(active_only: bool = True) -> List[Dict[str, Any]]:
    """
    Return all providers, optionally filtered to active ones only.

    Parameters
    ----------
    active_only:
        When True (default), only providers whose ``active`` flag is True
        are returned.

    Returns
    -------
    list[dict]
        Provider records as loaded from ``providers.json``.
    """
    providers = _load_providers()
    if active_only:
        providers = [p for p in providers if p.get("active", True)]
    logger.info("list_providers(active_only=%s) → %d providers", active_only, len(providers))
    return providers


def get_provider_by_id(provider_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single provider by its unique identifier.

    Parameters
    ----------
    provider_id:
        The ``id`` field value from ``providers.json`` (e.g. ``"wise"``).

    Returns
    -------
    dict | None
        The provider record, or *None* if not found.
    """
    providers = _load_providers()
    normalised = provider_id.strip().lower()
    for provider in providers:
        if provider.get("id", "").lower() == normalised:
            logger.info("get_provider_by_id('%s') → found", provider_id)
            return provider
    logger.warning("get_provider_by_id('%s') → not found", provider_id)
    return None


def get_supported_corridors(
    from_country: Optional[str] = None,
    to_country: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Return corridors supported across all active providers.

    Optionally filter by sender and/or receiver country.

    Parameters
    ----------
    from_country:
        ISO 3166-1 alpha-2 sender country (e.g. ``"US"``). Case-insensitive.
    to_country:
        ISO 3166-1 alpha-2 receiver country (e.g. ``"IN"``). Case-insensitive.

    Returns
    -------
    list[dict]
        Each item: ``{"provider_id", "provider_name", "from", "to", "currencies"}``
    """
    providers = list_providers(active_only=True)
    results: List[Dict[str, Any]] = []

    fc = from_country.upper() if from_country else None
    tc = to_country.upper() if to_country else None

    for provider in providers:
        for corridor in provider.get("supported_corridors", []):
            corridor_from = corridor.get("from", "").upper()
            corridor_to = corridor.get("to", "").upper()

            if fc and corridor_from != fc:
                continue
            if tc and corridor_to != tc:
                continue

            results.append({
                "provider_id": provider["id"],
                "provider_name": provider["name"],
                "from": corridor_from,
                "to": corridor_to,
                "currencies": corridor.get("currencies", []),
            })

    logger.info(
        "get_supported_corridors(from=%s, to=%s) → %d corridors",
        from_country, to_country, len(results),
    )
    return results


def get_payment_methods(provider_id: str) -> List[str]:
    """
    Return the payment methods accepted by a specific provider.

    Parameters
    ----------
    provider_id:
        Provider identifier.

    Returns
    -------
    list[str]
        Payment method names.

    Raises
    ------
    ValueError
        When the provider is not found.
    """
    provider = get_provider_by_id(provider_id)
    if not provider:
        raise ValueError(f"Provider not found: '{provider_id}'")
    return provider.get("payment_methods", [])


def get_delivery_methods(provider_id: str) -> List[str]:
    """
    Return the delivery methods offered by a specific provider.

    Parameters
    ----------
    provider_id:
        Provider identifier.

    Returns
    -------
    list[str]
        Delivery method names.

    Raises
    ------
    ValueError
        When the provider is not found.
    """
    provider = get_provider_by_id(provider_id)
    if not provider:
        raise ValueError(f"Provider not found: '{provider_id}'")
    return provider.get("delivery_methods", [])


def compare_providers(
    from_country: str,
    to_country: str,
) -> List[Dict[str, Any]]:
    """
    Return a comparison of providers that support a given corridor.

    Includes fees, speed, payment and delivery methods, and rating.

    Parameters
    ----------
    from_country:
        Sender country code.
    to_country:
        Receiver country code.

    Returns
    -------
    list[dict]
        Provider comparison data sorted by rating descending.
    """
    corridors = get_supported_corridors(from_country=from_country, to_country=to_country)
    supporting_ids = {c["provider_id"] for c in corridors}

    providers = [p for p in list_providers() if p["id"] in supporting_ids]

    comparison = []
    for p in providers:
        comparison.append({
            "provider_id": p["id"],
            "provider_name": p["name"],
            "website": p.get("website"),
            "rating": p.get("rating"),
            "fees": p.get("fees"),
            "transfer_speed": p.get("transfer_speed"),
            "payment_methods": p.get("payment_methods", []),
            "delivery_methods": p.get("delivery_methods", []),
        })

    comparison.sort(key=lambda x: x.get("rating") or 0, reverse=True)
    logger.info(
        "compare_providers(%s→%s) → %d providers", from_country, to_country, len(comparison)
    )
    return comparison
