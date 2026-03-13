#backend/modules/agronomy/utils/reports.py
import pandas as pd
from .services import list_agronomy_recommendations

def generate_full_agronomy_report(db, block_id=None, crop_id=None):
    recs = list_agronomy_recommendations(db, block_id, crop_id)
    data = [
        {
            "id": r.id,
            "farm_id": r.farm_id,
            "block_id": r.block_id,
            "crop_id": r.crop_id,
            "recommendation_text": r.recommendation_text,
            "recommended_action": r.recommended_action,
            "date_given": r.date_given,
            "generated_by": r.generated_by,
            "source": r.source
        }
        for r in recs
    ]
    return pd.DataFrame(data)

def generate_excel_report(df: pd.DataFrame):
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Agronomy Report")
    output.seek(0)
    return output


