# backend/core/utils/product_enrichment.py
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger("product_enrich")


# ==========================================================
# Module-aware mock database
# ==========================================================
MOCK_DB = {
    "Crop": {
        "Roundup": {
            "manufacturer": "Bayer CropScience",
            "active_ingredient": "Glyphosate 480 g/L",
            "composition": "Isopropylamine salt of glyphosate",
            "product_website": "https://www.cropscience.bayer.com/",
            "safety_precautions": "Avoid contact with skin and eyes. PHI: 14 days.",
        },
        "YaraMila Cereal": {
            "manufacturer": "Yara International",
            "active_ingredient": None,
            "composition": "NPK 25-5-5",
            "product_website": "https://www.yara.com/",
            "safety_precautions": "Store in a cool dry place.",
        },
    },
    "Poultry": {
        "Hendrix Broiler Feed": {
            "manufacturer": "Hendrix Genetics",
            "active_ingredient": None,
            "composition": "Protein 22%, Energy 3000 kcal/kg",
            "product_website": "https://www.hendrix-genetics.com/",
            "safety_precautions": "Store dry and cool, feed according to age.",
        },
        "Nobilis ND Vaccine": {
            "manufacturer": "MSD Animal Health",
            "active_ingredient": "Live Newcastle Disease Virus",
            "composition": "Vaccine suspension",
            "product_website": "https://www.msd-animal-health.com/",
            "safety_precautions": "Handle carefully, follow cold chain instructions.",
        },
    },
    "Livestock": {
        "Coccivet": {
            "manufacturer": "Zoetis",
            "active_ingredient": "Coccidiostat 5%",
            "composition": "Feed additive for cattle and sheep",
            "product_website": "https://www.zoetis.com/",
            "safety_precautions": "Use as instructed, avoid overdosage.",
        },
    },
    "Aquaculture": {
        "Shrimp Grower Feed": {
            "manufacturer": "Skretting",
            "active_ingredient": None,
            "composition": "Protein 35%, Lipid 5%, Vitamins and minerals",
            "product_website": "https://www.skretting.com/",
            "safety_precautions": "Store in dry, ventilated area. Avoid contamination.",
        },
        "AquaVita Vitamin Mix": {
            "manufacturer": "Cargill Aqua Nutrition",
            "active_ingredient": None,
            "composition": "Vitamin and mineral mix for fish/shrimp",
            "product_website": "https://www.cargill.com/aqua-nutrition",
            "safety_precautions": "Mix according to instructions; store dry.",
        },
    }
}


# ==========================================================
# Main enrichment function
# ==========================================================
def enrich_product_info(item_name: str, module_type: str = "Crop") -> dict:
    """
    Enrich product info from live sources or fallback mock_db.
    module_type: Crop | Poultry | Livestock | Aquaculture
    """
    result = {
        "manufacturer": None,
        "active_ingredient": None,
        "composition": None,
        "product_website": None,
        "safety_precautions": None,
    }

    q = item_name.strip()

    # === Attempt live search (optional, polite) ===
    try:
        search_url = f"https://www.bing.com/search?q={requests.utils.quote(q + ' manufacturer active ingredient')}"
        headers = {"User-Agent": "Mozilla/5.0 (compatible; FarmSyn/1.0)"}
        r = requests.get(search_url, headers=headers, timeout=6)
        if r.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r.text, "html.parser")
            a = soup.find("a", href=True)
            if a and a["href"]:
                href = a["href"]
                known_manufacturers = ["bayer", "yara", "syngenta", "bayercrop", "corteva", "hendrix", "msd", "zoetis", "skretting", "cargill"]
                if any(k in href.lower() for k in known_manufacturers):
                    result["product_website"] = href
                    try:
                        r2 = requests.get(href, headers=headers, timeout=6)
                        if r2.status_code == 200:
                            s2 = BeautifulSoup(r2.text, "html.parser")
                            text = s2.get_text(separator=" ").strip()
                            if "active ingredient" in text.lower():
                                result["active_ingredient"] = "See manufacturer page"
                            if "ph" in text.lower() or "pre-harvest interval" in text.lower():
                                result["safety_precautions"] = "See manufacturer page (contains PHI/safety info)"
                    except Exception as e:
                        logger.debug("Product page fetch failed: %s", e)
    except Exception as e:
        logger.debug("Search step failed: %s", e)

    # === Fallback to mock DB ===
    module_db = MOCK_DB.get(module_type, {})
    if not any(result.values()) and module_db.get(item_name):
        result.update(module_db[item_name])

    return result


# ==========================================================
# Wrapper for routers
# ==========================================================
def get_product_details(item_name: str, module_type: str = "Crop") -> dict:
    return enrich_product_info(item_name, module_type)
