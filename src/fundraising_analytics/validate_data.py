from collections.abc import Mapping

import polars as pl


def validate_tables(tables: Mapping[str, pl.DataFrame]) -> pl.DataFrame:
    donors, gifts = tables["donors"], tables["gifts"]
    solicitations, costs = tables["solicitations"], tables["outreach_costs"]
    known_donors = set(donors["donor_id"].to_list())
    known_codes = set(solicitations["solicitation_code"].to_list())
    gift_codes = {x for x in gifts["solicitation_code"].to_list() if x is not None}
    cost_delta = costs.with_columns(
        (
            pl.col("creative_cost")
            + pl.col("printing_cost")
            + pl.col("distribution_cost")
            + pl.col("platform_cost")
            - pl.col("total_cost")
        )
        .abs()
        .alias("delta")
    )
    rows = [
        (
            "Warning",
            "gifts",
            "duplicate_gift_id",
            gifts.height - gifts["gift_id"].n_unique(),
            "Gift IDs repeated.",
        ),
        (
            "Warning",
            "gifts",
            "unknown_solicitation_code",
            len(gift_codes - known_codes),
            "Codes absent from solicitation table.",
        ),
        (
            "Error",
            "gifts",
            "orphan_donor_id",
            len(set(gifts["donor_id"].to_list()) - known_donors),
            "Donor IDs absent from donor table.",
        ),
        (
            "Error",
            "gifts",
            "nonpositive_gift",
            gifts.filter(pl.col("gift_amount") <= 0).height,
            "Gift amount is not positive.",
        ),
        (
            "Error",
            "outreach_costs",
            "cost_components_do_not_reconcile",
            cost_delta.filter(pl.col("delta") > 0.011).height,
            "Cost components differ from total.",
        ),
    ]
    return pl.DataFrame(
        rows,
        schema=["severity", "table_name", "check_name", "affected_rows", "explanation"],
        orient="row",
    )
