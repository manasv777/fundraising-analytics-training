# Data dictionary

These files contain synthetic practice records. Monetary values are US dollars. Gift dates span January 2022 through December 2025. Read each table's **grain** first: it tells you what one row represents and helps you avoid multiplying gift revenue during joins.

## How the tables connect

```text
donors.donor_id ──< gifts.donor_id
solicitations.solicitation_code ──< gifts.solicitation_code
solicitations.solicitation_code ── outreach_costs.solicitation_code
gifts.gift_id ── website_sources.gift_id (website gifts only)
```

`──<` means one record can match many records. A donor can make many gifts. Gift IDs have a few intentional duplicate rows, so deduplicate only after examining them. Some gift solicitation codes are blank or unmatched on purpose; a left join should preserve those gifts.

## `donors.csv`

**Grain:** one synthetic person. **Key:** `donor_id`. **Rows:** 3,000.

| Field | Type | Meaning | Missing? |
| --- | --- | --- | --- |
| `donor_id` | Text | Synthetic person ID | No |
| `join_date` | Date | First date in this synthetic donor record | No |
| `state_group` | Text | State or `Other` grouping | No |
| `age_band` | Text | Broad age category | Yes |
| `membership_status` | Text | `Active`, `Lapsed`, or `Prospect` in the synthetic snapshot | No |
| `acquisition_source` | Text | Recorded way this person entered the database | No |
| `email_opt_in` | Boolean | Whether email contact is allowed in this synthetic snapshot | No |
| `mail_opt_in` | Boolean | Whether postal contact is allowed | No |
| `household_member` | Boolean | Household grouping flag | No |
| `volunteer` | Boolean | Volunteer flag in the synthetic snapshot | No |
| `event_attendance_count` | Integer | Synthetic event count in the snapshot | No |

The profile fields are a snapshot, not a history of how they changed. Do not assume volunteer status, opt-in, or event count was known at an earlier model cutoff date.

## `gifts.csv`

**Grain:** one gift transaction before intentional duplicate rows. **Intended key:** `gift_id`. **Rows:** 9,000, including a few duplicate gift IDs.

| Field | Type | Meaning | Missing? |
| --- | --- | --- | --- |
| `gift_id` | Text | Transaction identifier | No |
| `donor_id` | Text | Person who made the gift; joins to `donors` | No |
| `gift_date` | Date | Date the gift was recorded | No |
| `gift_amount` | Number | Gift amount in dollars | No |
| `payment_method` | Text | Card, check, ACH, or stock | No |
| `gift_type` | Text | One-time, recurring, or tribute label | No |
| `solicitation_code` | Text | Recorded campaign code; may be blank or legacy/unmatched | Yes |
| `online` | Boolean | Website-gift indicator in the synthetic data | No |
| `recurring_gift` | Boolean | Recurring-payment indicator | No |
| `soft_credit` | Boolean | Training flag for a soft-credit gift | No |

`recurring_gift` mirrors whether `gift_type` is `Recurring`. A blank or unmatched code is an attribution question, not a zero-dollar gift.

## `solicitations.csv`

**Grain:** one outreach campaign. **Key:** `solicitation_code`. **Rows:** 29.

| Field | Type | Meaning | Missing? |
| --- | --- | --- | --- |
| `solicitation_code` | Text | Campaign identifier used on gifts and cost rows | No |
| `channel` | Text | Renewal, year-end letter, magazine, or website | No |
| `campaign_name` | Text | Readable campaign label | No |
| `send_date` | Date | Campaign start or send date | No |
| `fiscal_year` | Integer | Training year assigned to the campaign | No |
| `audience_segment` | Text | Intended outreach audience | No |
| `purpose` | Text | Campaign purpose | No |

One campaign is an intentional zero-response example. A coded gift follows its matched campaign's send date.

## `outreach_costs.csv`

**Grain:** one cost record per campaign. **Key:** `solicitation_code`. **Rows:** 29.

| Field | Type | Meaning | Missing? |
| --- | --- | --- | --- |
| `solicitation_code` | Text | Joins to `solicitations` | No |
| `recipient_count` | Integer | Synthetic people reached or contacted | No |
| `creative_cost` | Number | Design or content cost | No |
| `printing_cost` | Number | Print cost; zero for website | No |
| `distribution_cost` | Number | Postage or distribution; zero for website | No |
| `platform_cost` | Number | Digital platform cost; generally zero for mail | No |
| `total_cost` | Number | Sum of the four cost fields | No |

The website `recipient_count` is a synthetic reach number. Confirm its real-world denominator before comparing website response rates with mailed appeals.

## `website_sources.csv`

**Grain:** one response per unique website gift. **Key:** `gift_id`. The corresponding gift has `online == True`.

| Field | Type | Meaning | Missing? |
| --- | --- | --- | --- |
| `gift_id` | Text | Joins to `gifts` | No |
| `source_response_raw` | Text | Donor's self-elected answer, with spelling and wording variation | Yes |
| `source_category_clean` | Text | Normalized practice category | No |

Try normalizing the raw answers yourself before comparing them with `source_category_clean`. These answers indicate what donors selected; they do not prove which outreach caused a gift.
