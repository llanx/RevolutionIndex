# Phase 3: Data Sourcing - Context

**Gathered:** 2026-03-03
**Status:** Ready for planning

<domain>
## Phase Boundary

Map every discovered variable from Phase 2's ranked catalog to freely available data sources, classify data availability, identify proxies for gaps, and produce a concrete inventory that constrains Phase 4 (Model Building) to what is empirically feasible. The inventory serves double duty as a methodology transparency document.

</domain>

<decisions>
## Implementation Decisions

### Data Source Scope
- **Primary sources:** US Government Open Data MCP's 37 federal APIs (FRED, BLS, BEA, Census, Treasury, CDC, etc.) — search these first for every variable
- **Secondary sources:** Free APIs or free downloads outside the MCP (e.g., WID.world, V-Dem, Freedom House, SIPRI) — used when MCP APIs don't cover a variable
- **Access requirements:** Free API with registration OK; free CSV/Excel downloads OK; no paid subscriptions
- **No hard cap** on number of non-MCP sources — cover all strong/moderate-evidence variables regardless of source count

### Proxy Variable Standards
- **Two tiers only:** Direct measure and strong proxy (literature-validated mapping). No weak/speculative proxies.
- **Strong proxy requirement:** Literature must explicitly support the variable-to-concept mapping (e.g., DW-NOMINATE scores validated as polarization measure)
- **Multiple proxies per variable:** Catalog all viable direct/strong-proxy measures per theoretical variable. Mark a recommended proxy but include alternatives. Final selection deferred to Phase 4.
- **Unmeasurable variables:** When a strong-evidence variable has no direct measure or strong proxy, document the gap, rank by theoretical importance, and flag for future work. Do not invent creative proxies.

### Historical Coverage Depth
- **Flexible start dates:** Accept whatever historical coverage each source provides. No minimum start year requirement.
- **Full metadata per source:** Document exact coverage window (start year, end year or "present"), update frequency, and any known gaps
- **Short series included:** Variables with data starting after 2000 are included if they measure strong-evidence concepts. Tag as "short series" so Phase 5 can run separate validation (full backtest on long series, recent-episodes-only on short series).
- **Frequency alignment:** Document native frequency only. Alignment decisions deferred to Phase 4.

### Inventory Output Format
- **Primary deliverable:** Structured markdown document — serves as both methodology reference and Phase 4 input
- **Machine-readable config** derived from markdown in Phase 4, not produced in Phase 3
- **Organization:** By theoretical domain (economic stress, political polarization, social cohesion, etc.) — matches Phase 2's literature review structure
- **Metadata per variable:** Variable name, theoretical concept mapped to, source name, API endpoint/download URL, series ID, native frequency, coverage window (start-end), proxy tier (direct/strong), known data gaps, API key required (y/n), rate limits, data license/terms, last verified date

### Claude's Recommendation
- **Proxy approach:** Claude recommended a three-tier system (direct/strong/weak). User opted for two tiers only (direct + strong proxy), excluding weak proxies for rigor.
- **Gap handling:** Claude recommended documenting and flagging unmeasurable gaps rather than searching for creative alternatives. User accepted.
- **Multiple proxies:** Claude recommended cataloging multiple proxies per variable with a recommended pick. User accepted. Final selection in Phase 4.
- **Short series:** Claude recommended including short series (post-2000) with tagging and split validation. User accepted.
- **Access notes:** Claude recommended including API key/rate limit/license metadata beyond the standard set. User accepted for transparency and to prevent Phase 4 blockers.
- **Organization:** Claude recommended grouping by theoretical domain over data source. User accepted for methodology transparency.

</decisions>

<specifics>
## Specific Ideas

- US Government Open Data MCP (https://lzinga.github.io/us-gov-open-data-mcp/) as the primary data discovery tool — 37 APIs, 18 work with no key
- Inventory document should be auditable by researchers/reviewers as a methodology appendix
- Phase 2's variable catalog already has preliminary "fed-data/other-data/unknown" tags from MCP cross-referencing — use these as a starting point, not from scratch

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 03-data-sourcing*
*Context gathered: 2026-03-03*
