# Data Schema

The inventory JSON has a top-level `systems` array. Each system requires:
- `id`, `name`, `purpose`, `business_owner`, `technical_owner`, `provider`, `model`, `lifecycle`
- `jurisdictions` and `data_categories` arrays
- `dimensions` object with integer values 1–5 for `impact`, `data_sensitivity`, `autonomy`, `exposure`, `model_uncertainty`
- `last_review` in ISO `YYYY-MM-DD` format and positive `review_interval_days`
- `required_controls` array of control IDs
- `control_evidence` map from control ID to `status` (`implemented`, `planned`, `not_implemented`) and an `evidence` array.

Control catalogue entries require unique `id`, `title`, `domain`, `effectiveness` (1–3), `required` boolean, `frameworks` object, `owasp` array and a test description.

Evidence references in the sample are synthetic identifiers. In a real system, link to access-controlled evidence repositories and validate evidence scope, integrity, age and reviewer independence.
