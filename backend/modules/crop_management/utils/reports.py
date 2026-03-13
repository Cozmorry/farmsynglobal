from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO
from datetime import datetime

from backend.modules.agronomy.service import list_agronomy_recommendations
from backend.models.crop_management import (
    CropBlock, Crop, Irrigation, FertilizerApplication, ChemicalApplication, Scouting
)
from backend.models.harvest import Harvest  # ensure you have this model
from backend.models.costs import Cost        # ensure you have this model

# ============================================================
# 1️⃣ Generate full crop report as a pandas DataFrame
# ============================================================
def generate_full_crop_report(db: Session, farm_id=None, block_id=None, crop_id=None) -> pd.DataFrame:
    """
    Generates a detailed crop report including activities, harvest, costs, and agronomy recommendations.
    """

    # Base query for crop blocks
    query = db.query(CropBlock).join(Crop)
    if farm_id:
        query = query.filter(CropBlock.farm_id == farm_id)
    if block_id:
        query = query.filter(CropBlock.id == block_id)
    if crop_id:
        query = query.filter(CropBlock.crop_id == crop_id)
    
    blocks = query.all()
    report_rows = []

    for block in blocks:
        crop = block.crop

        # Latest agronomy recommendation
        agronomy = (
            db.query(AgronomyRecommendation)
            .filter(AgronomyRecommendation.block_id == block.id)
            .order_by(AgronomyRecommendation.date_given.desc())
            .first()
        )

        # Activities
        irrigation_count = db.query(Irrigation).filter(Irrigation.block_id == block.id).count()
        fertilizer_count = db.query(FertilizerApplication).filter(FertilizerApplication.block_id == block.id).count()
        chemical_count = db.query(ChemicalApplication).filter(ChemicalApplication.block_id == block.id).count()
        scouting_count = db.query(Scouting).filter(Scouting.block_id == block.id).count()

        # Harvest
        harvests = db.query(Harvest).filter(Harvest.block_id == block.id).all()
        total_harvest_qty = sum(h.quantity for h in harvests)

        # Costs
        costs = db.query(Cost).filter(Cost.block_id == block.id).all()
        total_cost = sum(c.amount for c in costs)
        cost_per_unit = total_cost / total_harvest_qty if total_harvest_qty else 0

        report_rows.append({
            "farm_id": block.farm_id,
            "block_id": block.id,
            "block_name": block.name,
            "crop_id": crop.id,
            "crop_name": crop.name,
            "irrigation_count": irrigation_count,
            "fertilizer_count": fertilizer_count,
            "chemical_count": chemical_count,
            "scouting_count": scouting_count,
            "total_harvest_qty": total_harvest_qty,
            "total_cost": total_cost,
            "cost_per_unit": round(cost_per_unit, 2),
            "latest_agronomy_recommendation": agronomy.recommendation_text if agronomy else "N/A",
            "recommended_action": agronomy.recommended_action if agronomy else "N/A"
        })

    df = pd.DataFrame(report_rows)
    return df

# ============================================================
# 2️⃣ Generate Excel file from DataFrame
# ============================================================
def generate_excel_report(df: pd.DataFrame) -> BytesIO:
    """
    Convert a DataFrame into an Excel file stored in memory (BytesIO).
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Crop Report")
        writer.save()
    output.seek(0)
    return output



def generate_full_crop_report(db: Session, farm_id=None, block_id=None, crop_id=None) -> pd.DataFrame:
    """
    Generate a full crop report as a pandas DataFrame.
    Filters can be applied by farm_id, block_id, or crop_id.
    """
    query = db.query(models.Crop)

    if crop_id:
        query = query.filter(models.Crop.id == crop_id)
    if block_id:
        query = query.filter(models.Crop.block_id == block_id)
    if farm_id:
        query = query.join(models.Block).filter(models.Block.farm_id == farm_id)

    crops = query.all()

    # Build the report as a list of dicts
    report_data = []
    for crop in crops:
        block = crop.block
        farm = block.farm if block else None
        report_data.append({
            "farm_name": farm.name if farm else None,
            "block_name": block.name if block else None,
            "crop_name": crop.name,
            "crop_variety": crop.variety,
            "sowing_date": crop.sowing_date,
            "expected_harvest_date": crop.expected_harvest_date,
            "area": block.area if block else None
        })

    df = pd.DataFrame(report_data)
    return df

def generate_excel_report(df: pd.DataFrame) -> pd.io.excel._io.BytesIO:
    """
    Convert a pandas DataFrame into an Excel file (in memory) for download.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Crop Report")
        writer.save()
    output.seek(0)
    return output
