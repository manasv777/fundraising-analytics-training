"""Member 3 lesson: summarize and chart monthly revenue (3–4 hours)."""

import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

from fundraising_analytics.config import OUTPUT_DIR
from fundraising_analytics.load_data import load_tables
from fundraising_analytics.metrics import deduplicate_gifts, monthly_revenue

out = OUTPUT_DIR / "member_3"
out.mkdir(parents=True, exist_ok=True)
monthly = monthly_revenue(deduplicate_gifts(load_tables()["gifts"]))
monthly.write_csv(out / "monthly_revenue.csv")
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(monthly["month"].to_list(), monthly["revenue"].to_list(), color="#287271", linewidth=2)
ax.set(title="Monthly fundraising revenue", xlabel="Month", ylabel="Revenue")
ax.yaxis.set_major_formatter(StrMethodFormatter("${x:,.0f}"))
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
fig.savefig(out / "monthly_revenue.png", dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(11, 5))
ax.bar(monthly["month"].to_list(), monthly["gift_count"].to_list(), color="#D98C5F", width=20)
ax.set(title="Monthly gift count", xlabel="Month", ylabel="Gifts")
ax.grid(axis="y", alpha=0.25)
fig.tight_layout()
fig.savefig(out / "monthly_gift_count.png", dpi=160)
plt.close(fig)
print(f"Wrote monthly table and two charts to {out}")
