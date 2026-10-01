# Data dictionary

All records are synthetic. Dates cover 2022–2025 for gifts. Money is in US dollars.

## Relationships

`donors.donor_id` → `gifts.donor_id`; `solicitations.solicitation_code` → `gifts.solicitation_code` and `outreach_costs.solicitation_code`; `gifts.gift_id` → `website_sources.gift_id`.

## donors.csv

Grain: one person. Primary key: `donor_id`. Fields: `join_date` (date), `state_group`, `age_band`, `membership_status`, `acquisition_source` (categories), `email_opt_in`, `mail_opt_in`, `household_member`, `volunteer` (Boolean), and `event_attendance_count` (integer). `age_band` may be missing.

## gifts.csv

Grain: one gift transaction before controlled duplicate rows. Primary key: `gift_id`. Fields: `donor_id`, `gift_date`, `gift_amount`, `payment_method`, `gift_type`, `solicitation_code`, `online`, `recurring_gift`, and `soft_credit`. `solicitation_code` may be missing or unmatched for training.

## solicitations.csv

Grain: one outreach instance. Primary key: `solicitation_code`. Fields: `channel`, `campaign_name`, `send_date`, `fiscal_year`, `audience_segment`, and `purpose`.

## outreach_costs.csv

Grain: one cost record per solicitation. Key: `solicitation_code`. Fields: `recipient_count`, `creative_cost`, `printing_cost`, `distribution_cost`, `platform_cost`, and `total_cost`. Total cost equals the component sum.

## website_sources.csv

Grain: one response per unique online gift. Key: `gift_id`. `source_response_raw` is the donor's varied self-report and may be missing. `source_category_clean` is the normalized training category.
