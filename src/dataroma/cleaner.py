import re


def clean_historical_row(row):
    # Normalize quarter string
    quarter = re.sub(r"\s+", " ", row["quarter"]).strip()

    # Convert portfolio value to millions
    val_str = row["portfolio_value"].replace("$", "").strip()
    multiplier = 1000 if val_str.endswith("B") else 1
    value_num = float(re.sub(r"[MB]", "", val_str))

    return {
        "quarter": quarter,
        "portfolio_value_mil": round(value_num * multiplier, 2),
        "ticker": row["ticker"].strip(),
        "company": row["company"].strip(),
        "weight_pct": round(float(row["weight_pct"]), 2)
    }
