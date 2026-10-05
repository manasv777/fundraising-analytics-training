"""Create deterministic, privacy-safe fundraising training data."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import numpy as np
import polars as pl

from .config import RAW_DATA_DIR

SEED = 20261001


def _dates(rng: np.random.Generator, start: date, end: date, count: int) -> list[date]:
    span = (end - start).days
    return [start + timedelta(days=int(value)) for value in rng.integers(0, span + 1, count)]


def _donors(rng: np.random.Generator) -> pl.DataFrame:
    n = 3_000
    states = np.array(["NC", "VA", "PA", "NY", "TN", "GA", "OH", "Other"])
    acquisition = np.array(["Website", "Event", "Magazine", "Friend", "Direct mail", "Unknown"])
    age = np.array(["Under 35", "35-49", "50-64", "65+", None], dtype=object)
    return pl.DataFrame(
        {
            "donor_id": [f"D{i:06d}" for i in range(1, n + 1)],
            "join_date": _dates(rng, date(2010, 1, 1), date(2025, 10, 31), n),
            "state_group": rng.choice(
                states, n, p=[0.20, 0.14, 0.12, 0.10, 0.08, 0.07, 0.07, 0.22]
            ),
            "age_band": rng.choice(age, n, p=[0.08, 0.18, 0.31, 0.35, 0.08]),
            "membership_status": rng.choice(
                ["Active", "Lapsed", "Prospect"], n, p=[0.55, 0.27, 0.18]
            ),
            "acquisition_source": rng.choice(
                acquisition, n, p=[0.29, 0.13, 0.18, 0.12, 0.18, 0.10]
            ),
            "email_opt_in": rng.random(n) < 0.72,
            "mail_opt_in": rng.random(n) < 0.83,
            "household_member": rng.random(n) < 0.24,
            "volunteer": rng.random(n) < 0.15,
            "event_attendance_count": rng.poisson(0.8, n),
        }
    ).with_columns(pl.col("join_date").cast(pl.Date))


def _solicitations() -> pl.DataFrame:
    rows: list[dict[str, object]] = []
    for year in range(2022, 2026):
        specs = [
            (f"REN{year}A", "Renewal", f"Spring renewal {year}", date(year, 2, 10), "Prior donors"),
            (f"REN{year}B", "Renewal", f"Fall renewal {year}", date(year, 8, 15), "Lapsing donors"),
            (
                f"EOY{year}",
                "Year-end letter",
                f"Year-end appeal {year}",
                date(year, 11, 15),
                "All mailable donors",
            ),
            (f"MAG{year}S", "Magazine", f"Spring magazine {year}", date(year, 4, 1), "Members"),
            (f"MAG{year}F", "Magazine", f"Fall magazine {year}", date(year, 9, 1), "Members"),
            (
                f"WEB{year}S",
                "Website",
                f"Spring web campaign {year}",
                date(year, 5, 1),
                "Digital audience",
            ),
            (
                f"WEB{year}G",
                "Website",
                f"Giving Tuesday {year}",
                date(year, 11, 25),
                "Digital audience",
            ),
        ]
        for code, channel, name, sent, audience in specs:
            rows.append(
                {
                    "solicitation_code": code,
                    "channel": channel,
                    "campaign_name": name,
                    "send_date": sent,
                    "fiscal_year": year,
                    "audience_segment": audience,
                    "purpose": "General support",
                }
            )
    rows.append(
        {
            "solicitation_code": "MAG2025TEST",
            "channel": "Magazine",
            "campaign_name": "Unsent training comparison",
            "send_date": date(2025, 12, 20),
            "fiscal_year": 2025,
            "audience_segment": "Test holdout",
            "purpose": "General support",
        }
    )
    return pl.DataFrame(rows).with_columns(pl.col("send_date").cast(pl.Date))


def _gift_date(rng: np.random.Generator, year: int, channel: str) -> date:
    if channel == "Year-end letter":
        month = int(rng.choice([11, 12], p=[0.25, 0.75]))
    elif channel == "Renewal":
        month = int(rng.choice([2, 3, 8, 9], p=[0.30, 0.20, 0.30, 0.20]))
    elif channel == "Magazine":
        month = int(rng.choice([4, 5, 9, 10]))
    elif channel == "Website":
        month = int(
            rng.choice(
                range(1, 13),
                p=[0.05, 0.05, 0.06, 0.06, 0.07, 0.06, 0.06, 0.06, 0.07, 0.10, 0.16, 0.20],
            )
        )
    else:
        month = int(
            rng.choice(
                range(1, 13),
                p=[0.06, 0.05, 0.06, 0.07, 0.07, 0.07, 0.07, 0.06, 0.07, 0.10, 0.14, 0.18],
            )
        )
    day = int(rng.integers(1, 29))
    return date(year, month, day)


def _gifts(
    rng: np.random.Generator, donors: pl.DataFrame, solicitations: pl.DataFrame
) -> pl.DataFrame:
    unique_n = 8_988
    donor_ids = donors["donor_id"].to_numpy()
    popularity = rng.lognormal(0, 0.8, len(donor_ids))
    popularity /= popularity.sum()
    chosen_donors = rng.choice(donor_ids, unique_n, p=popularity)
    years = rng.choice([2022, 2023, 2024, 2025], unique_n, p=[0.21, 0.23, 0.26, 0.30])
    channels = rng.choice(
        ["Renewal", "Year-end letter", "Magazine", "Website", "Unattributed"],
        unique_n,
        p=[0.26, 0.27, 0.15, 0.26, 0.06],
    )
    tiers = rng.choice(["standard", "mid", "2500", "5000"], unique_n, p=[0.76, 0.19, 0.03, 0.02])
    standard = np.array([25, 35, 50, 75, 100, 150, 250, 500], dtype=float)
    mid = np.array([750, 1000, 1250, 1500, 2000], dtype=float)
    major25 = np.array([2500, 3000, 3500, 4000], dtype=float)
    major5 = np.array([5000, 7500, 10000, 15000, 25000], dtype=float)
    amounts = [
        float(
            rng.choice(
                standard
                if t == "standard"
                else mid
                if t == "mid"
                else major25
                if t == "2500"
                else major5
            )
        )
        for t in tiers
    ]
    codes_by_year_channel: dict[tuple[int, str], list[str]] = {}
    send_date_by_code: dict[str, date] = {}
    for row in solicitations.iter_rows(named=True):
        if row["solicitation_code"] == "MAG2025TEST":
            continue
        codes_by_year_channel.setdefault((row["fiscal_year"], row["channel"]), []).append(
            row["solicitation_code"]
        )
        send_date_by_code[row["solicitation_code"]] = row["send_date"]
    codes: list[str | None] = []
    dates: list[date] = []
    for year, channel in zip(years, channels, strict=True):
        if channel == "Unattributed":
            dates.append(_gift_date(rng, int(year), str(channel)))
            codes.append(None)
        else:
            chosen_code = str(rng.choice(codes_by_year_channel[(int(year), str(channel))]))
            send_date = send_date_by_code[chosen_code]
            last_day = min(45, (date(int(year), 12, 31) - send_date).days)
            dates.append(send_date + timedelta(days=int(rng.integers(1, last_day + 1))))
            if rng.random() < 0.055:
                codes.append(None)
            elif rng.random() < 0.012:
                codes.append(f"LEGACY{year}")
            else:
                codes.append(chosen_code)
    gift_types = [
        str(x)
        for x in rng.choice(
            ["One-time", "Recurring", "Tribute"], unique_n, p=[0.78, 0.17, 0.05]
        )
    ]
    payment_methods = [
        str(x)
        for x in rng.choice(
            ["Card", "Check", "ACH", "Stock"], unique_n, p=[0.51, 0.35, 0.11, 0.03]
        )
    ]
    for index, channel in enumerate(channels):
        if channel == "Website":
            payment_methods[index] = str(rng.choice(["Card", "ACH"], p=[0.85, 0.15]))
    frame = pl.DataFrame(
        {
            "gift_id": [f"G{i:07d}" for i in range(1, unique_n + 1)],
            "donor_id": chosen_donors,
            "gift_date": dates,
            "gift_amount": amounts,
            "payment_method": payment_methods,
            "gift_type": gift_types,
            "solicitation_code": codes,
            "online": [str(x) == "Website" for x in channels],
            "recurring_gift": [gift_type == "Recurring" for gift_type in gift_types],
            "soft_credit": rng.random(unique_n) < 0.025,
        }
    ).with_columns(pl.col("gift_date").cast(pl.Date))
    duplicates = frame.sample(n=12, seed=SEED).with_columns(pl.col("payment_method"))
    return pl.concat([frame, duplicates])


def _costs(rng: np.random.Generator, solicitations: pl.DataFrame) -> pl.DataFrame:
    rows = []
    for row in solicitations.iter_rows(named=True):
        channel = row["channel"]
        recipients = int(
            rng.integers(1500, 4200) if channel != "Website" else rng.integers(5000, 12000)
        )
        creative = round(float(rng.uniform(400, 1800)), 2)
        printing = (
            round(recipients * float(rng.uniform(0.25, 0.62)), 2) if channel != "Website" else 0.0
        )
        distribution = (
            round(recipients * float(rng.uniform(0.25, 0.55)), 2) if channel != "Website" else 0.0
        )
        platform = round(float(rng.uniform(250, 1100)), 2) if channel == "Website" else 0.0
        rows.append(
            {
                "solicitation_code": row["solicitation_code"],
                "recipient_count": recipients,
                "creative_cost": creative,
                "printing_cost": printing,
                "distribution_cost": distribution,
                "platform_cost": platform,
                "total_cost": round(creative + printing + distribution + platform, 2),
            }
        )
    return pl.DataFrame(rows)


def _website_sources(rng: np.random.Generator, gifts: pl.DataFrame) -> pl.DataFrame:
    online = gifts.unique("gift_id").sort("gift_id").filter(pl.col("online"))
    raw_values = np.array(
        [
            "Google",
            "google search",
            "Magazine",
            "Our magazine",
            "Friend",
            "friend or family",
            "Social media",
            "Facebook",
            "Event",
            "Other",
            None,
        ],
        dtype=object,
    )
    raw = rng.choice(
        raw_values,
        online.height,
        p=[0.16, 0.10, 0.12, 0.07, 0.10, 0.07, 0.10, 0.06, 0.07, 0.10, 0.05],
    )

    def clean(value: object) -> str:
        if value is None:
            return "Missing"
        text = str(value).lower()
        if "google" in text:
            return "Search"
        if "magazine" in text:
            return "Magazine"
        if "friend" in text or "family" in text:
            return "Friend or family"
        if "social" in text or "facebook" in text:
            return "Social media"
        if "event" in text:
            return "Event"
        return "Other"

    return pl.DataFrame(
        {
            "gift_id": online["gift_id"],
            "source_response_raw": raw,
            "source_category_clean": [clean(x) for x in raw],
        }
    )


def generate_all(seed: int = SEED, output_dir: Path = RAW_DATA_DIR) -> dict[str, pl.DataFrame]:
    rng = np.random.default_rng(seed)
    donors = _donors(rng)
    solicitations = _solicitations()
    gifts = _gifts(rng, donors, solicitations)
    first_gifts = gifts.group_by("donor_id").agg(
        pl.col("gift_date").min().alias("first_gift_date")
    )
    donors = (
        donors.join(first_gifts, on="donor_id", how="left")
        .with_columns(
            pl.when(pl.col("first_gift_date").is_not_null())
            .then(pl.min_horizontal("join_date", "first_gift_date"))
            .otherwise(pl.col("join_date"))
            .alias("join_date")
        )
        .drop("first_gift_date")
    )
    costs = _costs(rng, solicitations)
    website_sources = _website_sources(rng, gifts)
    tables = {
        "donors": donors,
        "gifts": gifts,
        "solicitations": solicitations,
        "outreach_costs": costs,
        "website_sources": website_sources,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, frame in tables.items():
        frame.write_csv(output_dir / f"{name}.csv")
    return tables


if __name__ == "__main__":
    for table, data in generate_all().items():
        print(f"{table}.csv: {data.height:,} rows")
