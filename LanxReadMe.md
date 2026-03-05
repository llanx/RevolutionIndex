# What We Did This Session: Automating Variable Fetchers

## The Problem

The pipeline had 41 variables but only 12 (FRED API) auto-fetched. The remaining 29 required manually downloading CSV/XLSX files and placing them in the right directories. This made the pipeline impractical to run.

## What We Built

Created `models/fetchers.py` — a module with 25 automated fetcher functions that download, parse, and cache data for all 29 non-FRED variables. The pipeline now tries auto-fetch first and only falls back to manual download if it fails.

### Tier 1: No Authentication (8 fetchers)

These pull from public URLs with no API key needed.

| # | Variable | Source | How It Works |
|---|----------|--------|--------------|
| 3 | Congressional Polarization | VoteView | Downloads HSall_members.csv (~60MB), computes \|mean(R) - mean(D)\| DW-NOMINATE per Congress |
| 11 | Elite Factionalism | VoteView | Same CSV, computes max(SD_R, SD_D) per Congress |
| 15 | Racial Income Ratio | Census H-5 XLSX | Parses Black/White median household income, merges legacy (1967-2001) + modern (2002+) race categories |
| 20 | Middle-Class Income Share | Census H-2 XLSX | Sums 2nd+3rd+4th quintile income shares |
| 25 | Union Membership Rate | BLS Public Data API | POST requests with 20-year chunk pagination (series LUU0204899600) |
| 29 | Grumbach State Democracy Index | Harvard Dataverse | Downloads via Dataverse API (DOI: 10.7910/DVN/JNV3XO), computes state-averaged national score |
| 31 | Anti-System Vote Share | Harvard Dataverse | MIT Election Lab presidential returns (file id=10244938), computes third-party vote % |
| 38 | State Capacity (WGI) | World Bank REST API | GE.EST indicator for USA, no key needed |

### Tier 2: Free Registration (10 fetchers)

| # | Variable | Source | How It Works |
|---|----------|--------|--------------|
| 13 | Liberal Democracy Index | V-Dem (GitHub) | Downloads .RData via pyreadr, extracts USA rows |
| 21 | Judicial Independence | V-Dem | Same dataset, v2x_jucon column |
| 22 | Freedom of Expression | V-Dem | Same dataset, v2x_freexp_altinf column |
| 23 | Legislative Constraints | V-Dem | Same dataset, v2xlg_legcon column |
| 24 | Electoral Integrity | V-Dem | Same dataset, v2xel_frefair column |
| 32 | Executive Respects Constitution | V-Dem | Same dataset, v2exrescon column |
| 39 | Neighborhood Effects | V-Dem | Mean v2x_libdem across 32 OECD/NATO democracies per year |
| 12 | Protest Frequency | ACLED API | Monthly event count (needs ACLED_API_KEY + ACLED_EMAIL) |
| 36 | Protest Diffusion | ACLED API | Unique states with events per month |
| 37 | Prior Protest Experience | ACLED API | log(1 + cumulative events) monthly |

### Tier 3: Compiled Published Data (6 fetchers)

These variables come from surveys behind login walls (ANES, Gallup, WVS, PRRI). We compiled their aggregate values from peer-reviewed publications and hardcoded them as lookup tables.

| # | Variable | Obs | Range | Sources |
|---|----------|-----|-------|---------|
| 7 | Government Trust | 45 | 1958-2025 | ANES biennial + Pew supplements for off-years. Pew "Public Trust in Government" (2025), Hetherington (2005), ANES Guide 5A.1 |
| 4 | Affective Polarization | 18 | 1978-2020 | Feeling thermometer gap (in-party minus out-party). Iyengar et al. (2019), Tyler & Iyengar (2024), Boxell et al. (2024) |
| 42 | Political Efficacy | 28 | 1952-2020 | Average of VCF0613 + VCF0614 disagree %. ANES Guide External Efficacy Index, Craig et al. (1990) |
| 28 | Media Trust | 31 | 1972-2024 | Gallup "Trust in Mass Media" poll, % "great deal" or "fair amount". Gap 1977-1996 (question not asked) |
| 30 | Democratic Commitment | 5 | 1995-2017 | WVS US waves, % rating democracy 10/10 importance. Foa & Mounk (2016), WVS online analysis |
| 34 | Conspiratorial Thinking | 4 | 2021-2024 | PRRI QAnon tracking, % classified as "believers". PRRI American Values Survey reports |

### Also: Bright Line Watch (#41)

Best-effort fetcher that tries to scrape BLW survey data CSVs from their WordPress site. Returns None gracefully if URLs change (they're fragile).

## Bugs We Hit and Fixed

1. **BLS flat file 403** — `download.bls.gov` blocked direct downloads. Switched to BLS Public Data API with POST requests.
2. **MIT Election Lab GitHub 404** — All `raw.githubusercontent.com/MEDSL/` URLs were dead. Found the data on Harvard Dataverse instead.
3. **Grumbach SDI wrong DOI** — Initial DOI returned 404. Found correct DOI (10.7910/DVN/JNV3XO) and specific file IDs.
4. **Census H-5 section parsing** — Section labels didn't match expectations ("Black Alone (33)" not "BLACK"). Fixed by scanning for partial matches and merging legacy + modern race categories.
5. **V-Dem wrong file extension** — GitHub repo has `.RData` not `.rds`. Fixed URL.

## Pipeline Integration

Modified `models/pipeline.py` to call `try_auto_fetch(var)` before `load_manual_source(var)` in both Phase 2 (manual variables) and Phase 3 (constructed variables). Every fetcher is wrapped in try/except — failures return None and the pipeline continues.

## Caching

Each fetcher saves to `data/raw/var_{N}/auto_fetched.csv`. Freshness thresholds:
- 30 days default
- 7 days for ACLED (weekly updates)
- 90 days for V-Dem (annual updates)
- 365 days for compiled survey data (static lookup tables)

## Final Count

| Category | Count |
|----------|-------|
| FRED API (auto with key) | 12 |
| Fetchers in registry | 25 |
| Constructed (computed from FRED vars) | 4 |
| **Total coverable** | **41 of 41** |

Working out-of-the-box with just a FRED key: ~21 variables (12 FRED + 8 Tier 1 + 1 BLW best-effort). Add pyreadr: +7 V-Dem. Add ACLED key: +3 protest. The 6 compiled survey variables always work (hardcoded data).
