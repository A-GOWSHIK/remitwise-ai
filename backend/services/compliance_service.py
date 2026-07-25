"""
RemitWise AI – Compliance Service
====================================
Loads country compliance rules from the local JSON file and exposes
structured query functions for country rules, documents, KYC, and AML.
"""

import logging
from typing import Any, Dict, List, Optional

from config import settings
from utils.file_loader import load_json_file
from utils.validators import validate_country_code

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _load_rules() -> List[Dict[str, Any]]:
    """Load and return the raw compliance rules list from disk (cached)."""
    data = load_json_file(settings.COMPLIANCE_FILE)
    return data.get("compliance_rules", [])


def _find_rule(country_code: str) -> Optional[Dict[str, Any]]:
    """
    Look up a compliance rule by two-letter country code (case-insensitive).

    Returns None when the country is not in the local dataset.
    """
    code = validate_country_code(country_code)
    for rule in _load_rules():
        if rule.get("country_code", "").upper() == code:
            return rule
    return None


# ---------------------------------------------------------------------------
# Public service functions
# ---------------------------------------------------------------------------

def get_country_rules(country_code: str) -> Optional[Dict[str, Any]]:
    """
    Return the full compliance profile for a country.

    Parameters
    ----------
    country_code:
        ISO 3166-1 alpha-2 country code (e.g. ``"US"``, ``"IN"``).

    Returns
    -------
    dict | None
        Full compliance rule record, or *None* if the country is not in the
        local dataset.
    """
    rule = _find_rule(country_code)
    if rule is None:
        logger.warning("get_country_rules('%s') → not found in dataset", country_code)
    else:
        logger.info("get_country_rules('%s') → found", country_code)
    return rule


def get_required_documents(country_code: str) -> List[Dict[str, Any]]:
    """
    Return the list of required/optional documents for a country.

    Parameters
    ----------
    country_code:
        ISO 3166-1 alpha-2 country code.

    Returns
    -------
    list[dict]
        Document requirement records from the compliance dataset.

    Raises
    ------
    ValueError
        When the country code is not found in the local dataset.
    """
    rule = _find_rule(country_code)
    if rule is None:
        raise ValueError(
            f"No compliance data found for country code: '{country_code.upper()}'. "
            "The country may not yet be in the local dataset."
        )
    docs = rule.get("required_documents", [])
    logger.info(
        "get_required_documents('%s') → %d document types", country_code, len(docs)
    )
    return docs


def get_kyc_requirements(country_code: str) -> Dict[str, Any]:
    """
    Return KYC-specific requirements for a country.

    Parameters
    ----------
    country_code:
        ISO 3166-1 alpha-2 country code.

    Returns
    -------
    dict
        ``{"country_code", "country_name", "kyc_required", "mandatory_documents",
           "optional_documents", "risk_level", "regulatory_framework"}``

    Raises
    ------
    ValueError
        When the country code is not found.
    """
    rule = _find_rule(country_code)
    if rule is None:
        raise ValueError(
            f"No compliance data found for country code: '{country_code.upper()}'."
        )

    docs = rule.get("required_documents", [])
    mandatory = [d for d in docs if d.get("mandatory", False)]
    optional = [d for d in docs if not d.get("mandatory", False)]

    result = {
        "country_code": rule["country_code"],
        "country_name": rule.get("country_name"),
        "kyc_required": rule.get("kyc_required", False),
        "mandatory_documents": mandatory,
        "optional_documents": optional,
        "risk_level": rule.get("risk_level"),
        "regulatory_framework": rule.get("regulatory_framework", []),
        "notes": rule.get("notes"),
    }
    logger.info("get_kyc_requirements('%s') → kyc_required=%s", country_code, result["kyc_required"])
    return result


def get_aml_requirements(country_code: str) -> Dict[str, Any]:
    """
    Return AML-specific requirements for a country.

    Parameters
    ----------
    country_code:
        ISO 3166-1 alpha-2 country code.

    Returns
    -------
    dict
        ``{"country_code", "country_name", "aml_required",
           "sanctions_screening", "transaction_limits", "risk_level", "notes"}``

    Raises
    ------
    ValueError
        When the country code is not found.
    """
    rule = _find_rule(country_code)
    if rule is None:
        raise ValueError(
            f"No compliance data found for country code: '{country_code.upper()}'."
        )

    result = {
        "country_code": rule["country_code"],
        "country_name": rule.get("country_name"),
        "aml_required": rule.get("aml_required", False),
        "sanctions_screening": rule.get("sanctions_screening", False),
        "transaction_limits": rule.get("transaction_limits", {}),
        "risk_level": rule.get("risk_level"),
        "regulatory_framework": rule.get("regulatory_framework", []),
        "notes": rule.get("notes"),
    }
    logger.info(
        "get_aml_requirements('%s') → aml_required=%s, sanctions=%s",
        country_code, result["aml_required"], result["sanctions_screening"],
    )
    return result


def list_all_countries() -> List[Dict[str, Any]]:
    """
    Return a summary of all countries present in the compliance dataset.

    Returns
    -------
    list[dict]
        Each item: ``{"country_code", "country_name", "region", "risk_level",
                       "kyc_required", "aml_required", "sanctions_screening"}``
    """
    rules = _load_rules()
    summary = [
        {
            "country_code": r.get("country_code"),
            "country_name": r.get("country_name"),
            "region": r.get("region"),
            "risk_level": r.get("risk_level"),
            "kyc_required": r.get("kyc_required"),
            "aml_required": r.get("aml_required"),
            "sanctions_screening": r.get("sanctions_screening"),
        }
        for r in rules
    ]
    logger.info("list_all_countries() → %d countries", len(summary))
    return summary
