# EOSC Node Landing Page compliance — checklist v3.2

Run `web-14` · 2026-09-28T23:59:12+00:00 · 13 nodes · one page request per node plus 63 followed link(s), then 60 second-hop page(s) (depth 2).

> **This is not a compliance statement.** Points marked 🟠 review are ones this tool refuses to guess at: they either turn on a judgement ("clearly state") or quantify over things this tool does not enumerate ("all Node Exchange research resources").

**Node names.** 13 approved node name(s) were used, from the official list committed with the checklist (`checklist/approved-names.txt`, sha256 `46af586bc693…`), as an unscoped list: a match shows the name appears on the page but not that it is that node's own name. Separator glyphs are treated as interchangeable, so a page writing “EOSC Node - X” satisfies a list writing “EOSC Node | X”.

🟢 PASS — satisfied, with evidence · 🔴 **FAIL** — violated, with evidence · 🟠 review — a human must decide · 🟣 ERROR — could not be assessed

This run was collected at `--depth=2`, so it is reported twice: once using only the landing page and its direct links, and once using the second hop as well. Both tables come from the **same capture** — the shallow view is the deep evidence with the second-hop pages set aside, not a separate run — so any difference between them is the hop itself and not the passage of time.

### Results at depth 1

Landing page plus links that can settle a checklist point (policies, contact, about). This is the default the tool ships with.

130 cells: 🟢 52 PASS · 🔴 10 FAIL · 🟠 68 review.

| Node | 1 | 1R | 2 | 3 | 4 | 5a | 5b | 5c | 6 | 7 |
|---|---|---|---|---|---|---|---|---|---|---|
| BBMRI-ERIC | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS | 🟢 PASS | 🟢 PASS |
| CERN | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS | 🟢 PASS | 🟢 PASS |
| EOSC Node Czechia | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| EOSC DTO (D4Science) | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| Data Terra | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🔴 **FAIL** | 🔴 **FAIL** | 🟠 review | 🟢 PASS |
| EOSC Finland | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| PaNOSC | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS |
| EUDAT | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| EGI | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| GÉANT | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS |
| EOSC Node Poland | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| EOSC Node Italy | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🔴 **FAIL** | 🟢 PASS |
| EOSC Node Slovakia | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS | 🟢 PASS | 🟢 PASS |

### Results at depth 2

The same evidence plus 60 page(s) reached one further hop out, under a shared run budget.

130 cells: 🟢 52 PASS · 🔴 10 FAIL · 🟠 68 review.

| Node | 1 | 1R | 2 | 3 | 4 | 5a | 5b | 5c | 6 | 7 |
|---|---|---|---|---|---|---|---|---|---|---|
| BBMRI-ERIC | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS | 🟢 PASS | 🟢 PASS |
| CERN | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS | 🟢 PASS | 🟢 PASS |
| EOSC Node Czechia | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| EOSC DTO (D4Science) | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| Data Terra | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🔴 **FAIL** | 🔴 **FAIL** | 🟠 review | 🟢 PASS |
| EOSC Finland | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| PaNOSC | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS |
| EUDAT | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| EGI | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| GÉANT | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS |
| EOSC Node Poland | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| EOSC Node Italy | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🔴 **FAIL** | 🟢 PASS |
| EOSC Node Slovakia | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS | 🟢 PASS | 🟢 PASS |

### What the second hop changed

**No verdict changed.** The second hop fetched 60 page(s) and left all 130 cells exactly as depth 1 had them.

That is a finding, not a failure of the deeper crawl. The points still marked 🟠 review are not shallow-crawl artefacts: they turn on a judgement ("clearly state") or quantify over things no crawl enumerates ("all Node Exchange research resources offered by the Node"). Fetching more pages cannot settle either kind, which is why depth 1 remains the default.

#### Pages the second hop fetched

| Node | Point it was followed for | Page | Served |
|---|---|---|---|
| BBMRI-ERIC | 2 | <https://www.bbmri-eric.eu/news-events/bbmri-eric-at-the-integrating-research-and-healthcare-for-rare-diseases-workshop-in-malta/jel_workshop_malta/> | 200 |
| BBMRI-ERIC | 5s | <https://www.bbmri-eric.eu/services/other-services/> | 200 |
| BBMRI-ERIC | 5s | <https://www.bbmri-eric.eu/services/quality-management/> | 200 |
| BBMRI-ERIC | 5s | <https://www.bbmri-eric.eu/elsi/> | 200 |
| BBMRI-ERIC | 2 | <https://www.bbmri-eric.eu/national-nodes/> | 200 |
| BBMRI-ERIC | 5s | <https://www.bbmri-eric.eu/services/the-code-of-conduct-for-health-research/> | 200 |
| BBMRI-ERIC | 5s | <https://www.bbmri-eric.eu/services/isber-biobank-collaboration/> | 200 |
| BBMRI-ERIC | 5s | <https://www.bbmri-eric.eu/services/standardisation/> | 200 |
| BBMRI-ERIC | 5s | <https://www.bbmri-eric.eu/esli> | 200 |
| CERN | 2 | <https://eosc.cern/about/collaboration> | 200 |
| CERN | 5b | <https://eosc.cern/policies/aup> | 200 |
| CERN | 5c | <https://eosc.cern/policies/uap> | 200 |
| CERN | 2 | <https://eosc.cern/about/technology> | 200 |
| EOSC Node Czechia | 2 | <https://www.eosc.cz/en/about-eosc-cz/eosc-cz-in-data> | 200 |
| EOSC Node Czechia | 2 | <https://www.eosc.cz/en/about-eosc-cz/secretariat-eosc-cz> | 200 |
| EOSC Node Czechia | 2 | <https://www.eosc.cz/en/about-eosc-cz/templates-eosc-cz> | 200 |
| EOSC Node Czechia | 2 | <https://www.eosc.cz/en/about-eosc-cz/acknowledgement-and-citation> | 200 |
| EOSC Node Czechia | 6 | <https://dmp.eosc.cz/en/> | 200 |
| EOSC Node Czechia | 2 | <https://www.eosc.cz/en/about-eosc-cz/faq> | 200 |
| EOSC DTO (D4Science) | 5b | <https://www.d4science.org/policies/terms-of-use> | 200 |
| EOSC DTO (D4Science) | 6 | <https://www.d4science.org/support> | 200 |
| EOSC DTO (D4Science) | 5p | <https://www.d4science.org/policies> | 200 |
| EOSC DTO (D4Science) | 5s | <https://eosc-dto.d4science.org/service-catalogue-organization/eoscnodedto-catalogue> | 200 |
| EOSC DTO (D4Science) | 5b | <https://www.d4science.org/terms-of-use> | 404 |
| EOSC DTO (D4Science) | 5p | <https://www.d4science.org/cookie-policy> | 200 |
| EOSC DTO (D4Science) | 6 | <https://www.d4science.org/contact-us> | 403 |
| EOSC DTO (D4Science) | 2 | <https://www.d4science.org/about-us> | 200 |
| Data Terra | 5s | <https://www.data-terra.org/offre-de-services/> | 200 |
| EOSC Finland | 5p | <https://research.csc.fi/policies/> | 200 |
| EOSC Finland | 5s | <https://research.csc.fi/service-break> | 200 |
| EOSC Finland | 5p | <https://research.csc.fi/policies/dmpol/> | 200 |
| EOSC Finland | 5s | <https://research.csc.fi/resources/> | 200 |
| EOSC Finland | 6 | <https://research.csc.fi/training/csc-research-support-coffee-every-wednesday-at-1400-finnish-time/> | 200 |
| EOSC Finland | 5p | <https://research.csc.fi/policies/pid-policy/> | 200 |
| EOSC Finland | 5s | <https://research.csc.fi/resources/applying-for-resources/> | 200 |
| EOSC Finland | 5s | <https://research.csc.fi/resources/applying-for-resources/extremely-large-resources/> | 200 |
| EOSC Finland | 5s | <https://research.csc.fi/resources/quotas/> | 200 |
| EOSC Finland | 5s | <https://research.csc.fi/cloud-computing/> | 200 |
| EOSC Finland | 6 | <https://research.csc.fi/service/advanced-support/> | 200 |
| EOSC Finland | 5s | <https://research.csc.fi/sensitive-data/> | 200 |
| PaNOSC | 2 | <https://www.panosc.eu/about-panosc/photon-and-neutron-competence-centre/> | 200 |
| PaNOSC | 2 | <https://www.panosc.eu/services/pan-software-catalogue/> | 200 |
| PaNOSC | 5s | <https://www.panosc.eu/services/data-catalogue/> | 200 |
| EUDAT | 5b | <https://eudat.eu/eudat-cdi-aup/data-protection-and-privacy-policies> | 200 |
| EUDAT | 6 | <https://www.eudat.eu/catalogue> | 200 |
| EUDAT | 5s | <https://portal.eudat.eu/catalog> | 200 |
| EUDAT | 6 | <https://eudat.eu/contact-support-request> | 200 |
| EUDAT | 2 | <https://docs.eudat.eu/b2access/about/> | 200 |
| EUDAT | 6 | <https://www.eudat.eu/contact-support-request> | 200 |
| EUDAT | 2 | <https://www.eudat.eu/about> | 200 |
| EUDAT | 2 | <https://eudat.eu/about> | 200 |
| EUDAT | 5p | <https://eudat.eu/service-catalogue/b2safe> | 200 |
| EGI | 5p | <https://www.egi.eu/privacy-policy/> | 200 |
| EGI | 5s | <https://www.egi.eu/services/business/> | 200 |
| EGI | 5s | <https://www.egi.eu/services/federation/> | 200 |
| EGI | 2 | <https://www.egi.eu/egi-federation/> | 200 |
| EGI | 5s | <https://www.egi.eu/service-contracts/> | 200 |
| EGI | 5s | <https://www.egi.eu/resources/> | 200 |
| EGI | 5s | <https://www.egi.eu/service/cloud-compute/> | 200 |
| EOSC Node Poland | 5s | <https://eosc.pl/?undefined=> | 200 |


## What each column means

Full requirement text and the reasoning behind each verdict: [checklist v3.2 explained](checklist-v3.2.html).

| Column | Question it answers | Can a tool decide it? |
|---|---|---|
| **1** | Is the landing page itself reachable without logging in (or via EOSC AAI)? | yes, by inspection |
| **1R** | Are the resources the landing page points to also public or behind EOSC AAI? | no, human judgement |
| **2** | Does the page state the node's scope, its intended users, and who runs it? | no, human judgement |
| **3** | Is the EOSC logo shown, together with the official Tripartite-approved node name? | partly |
| **4** | Does the page link to this node's own entry on eosc.eu (not the homepage or the index)? | yes, by inspection |
| **5a** | Is there an English purpose description for each research resource, on the NLP (or a page it links to) and in the EOSC Catalogue? | no, human judgement |
| **5b** | Is an Acceptable Use Policy (AUP) linked from the landing page or a page it links to (and in the Catalogue)? | partly |
| **5c** | Is a User Access Policy (UAP) linked from the landing page or a page it links to (and in the Catalogue)? | partly |
| **6** | Is there a way to contact the node's helpdesk? | partly |
| **7** | Is the landing page in English? | yes, by inspection |

## Points in full

**1 — NLP is publicly accessible, or reachable via EOSC AAI login** (decidable by inspection)  
The NLP [...] must be either publicly accessible without login, or accessible via login through the EOSC AAI. "Accessible via login through the EOSC AAI" means the page presents a login button or link pointing to the Node's EOSC AAI-compliant access mechanism, integrated and verified under requirement [P.2] of the Production 1.0 Checklist for EOSC Nodes, v1.4.

> Anonymous reachability is directly observable: fetch the URL without credentials and see whether the content is served. Branch (b) only matters when (a) fails.

**1R — Node Exchange resources linked from the NLP are public or behind EOSC AAI** (needs a human)  
[The NLP, and] every Node Exchange resource it links to, directly or via intermediate pages, must be either publicly accessible without login, or accessible via login through the EOSC AAI.

> Not decidable by inspection, and one level of link following does not close the gap. The requirement quantifies over every resource reachable from the page "directly or via intermediate pages", which is unbounded; this tool follows at most one level, and only links that can settle a specific point. Even with full traversal it would still require confirming that each login encountered is genuinely EOSC AAI rather than a local or institutional IdP, and whether a given login is EOSC AAI compliant is settled under requirement [P.2] of the Production 1.0 Checklist, not by reading HTML. Nor can a script tell which linked resources are Node Exchange resources. The tool reports how many followed pages were served anonymously and lists the outbound resource links it found, so a reviewer has a work list.

**2 — Scope, intended users and responsible organisation are stated** (needs a human)  
Clearly state the Node's scope, intended users and responsible organisation. (It is up to the Node to feature all the organisations involved).

> "Clearly state" is a judgement about whether prose communicates three things to a researcher. A keyword match would produce confident nonsense in both directions. The tool extracts the candidate passages and names the reviewer must read.

**3 — EOSC logo and official Tripartite-approved node name are visible** (partly decidable)  
Clearly and visibly show the EOSC logo and the official Tripartite-approved name of the Node.

> Presence of an EOSC logo image is checkable, with caveats: a logo rendered as a CSS background or inlined SVG sprite can be missed, and "clearly and visibly" is a judgement. The Tripartite-approved name is NOT checkable without the authoritative list of approved node names, which the tool does not have; supply it via --approved-names to turn this into a real check.

**4 — Link to the node's own dedicated page on eosc.eu** (decidable by inspection)  
Include a link to the Node's own dedicated page on the eosc.eu website — the Node's entry under eosc.eu/building-the-eosc-federation, not the eosc.eu homepage or the index page itself.

> Fully decidable and the sharpest point in the checklist: an href under eosc.eu/building-the-eosc-federation/ with a path segment beyond the index. The checklist explicitly excludes both the homepage and the index, so those are matched and rejected rather than ignored.

**5a — Purpose description in English, on the NLP (or a page it links to) and in the Catalogue, for each Node Exchange resource** (needs a human)  
For all Node Exchange research resources offered by the Node to EOSC users, a purpose description must be accessible in English both on the NLP presenting the resource to the users (directly on the NLP itself or via intermediate web pages linked by the NLP) and via the link to the resource's entry in the EOSC Catalogue [...], i.e. in the Metadata about the Resource in the Service or Research Products Metadata catalogues.

> Requires enumerating "all Node Exchange research resources offered by the Node", which is not derivable from the landing page alone, and reading each description; the Catalogue metadata half is not read by this tool at all. The tool reports the page's size and link count so a reviewer has a starting point.

**5b — Acceptable Use Policy (AUP) on the NLP or a page it links to, and in the Catalogue, for each Node Exchange resource** (partly decidable)  
For all Node Exchange research resources offered by the Node to EOSC users, the Acceptable Use Policy (AUP) must be accessible in English both on the NLP presenting the resource to the users (directly on the NLP itself or via intermediate web pages linked by the NLP) and via the link to the resource's entry in the EOSC Catalogue [...]. AUP/UAP can be provided via specific product licenses in the case of datasets, archives, software, i.e. non-Services resources. AUP and UAP can be provided through the same, single document. AUP and UAP do not necessarily need to be unique per service.

> The NLP half is checkable: a pointer to an AUP on the landing page or on a linked page the tool read (a policies, legal, services or resources page, followed for that purpose), and whether the target is served and reads like a policy. Since v3.2 its absence is a FAIL, because being in the Catalogue alone no longer suffices -- except when the NLP links to a User Access Policy (possibly one document for both) or to a licence (allowed for non-service resources), when the DOM did not arrive, or when the landing page links to a policies or services page the tool did not read; those are MANUAL_REVIEW. A policy named in the text without a link is recorded but does not count. Pages on other sites are not followed. A PASS covers the NLP half only: that the policy covers every resource presented, and that it is also in each resource's Catalogue metadata, remain a reviewer's check.

**5c — User Access Policy (UAP) on the NLP or a page it links to, and in the Catalogue, for each Node Exchange resource** (partly decidable)  
For all Node Exchange research resources offered by the Node to EOSC users, the User Access Policy (UAP) must be accessible in English both on the NLP presenting the resource to the users (directly on the NLP itself or via intermediate web pages linked by the NLP) and via the link to the resource's entry in the EOSC Catalogue [...]. AUP/UAP can be provided via specific product licenses in the case of datasets, archives, software, i.e. non-Services resources. AUP and UAP can be provided through the same, single document. AUP and UAP do not necessarily need to be unique per service.

> Same rule as 5b, with the roles swapped: a link to an Acceptable Use Policy turns a missing UAP into MANUAL_REVIEW, because the checklist allows one document for both. The two are still recognised separately -- an "Access Policy" is matched for 5c, an "Acceptable Use Policy" or "Terms of use" for 5b -- so a page that links only one of them gets a PASS on that point and a review on the other, not two PASSes.

**6 — Means of contacting the node helpdesk** (partly decidable)  
Provide means of contacting the Node helpdesk.

> A contact route (mailto:, contact/support/helpdesk page, contact form) is checkable. Whether it reaches a *helpdesk* rather than a generic press or info address is a judgement, so a generic-looking contact is flagged rather than passed silently.

**7 — The NLP itself is in English** (decidable by inspection)  
The NLP itself is in English. Other pages need not be, except for the information required by item 5.

> Statistical language detection over the page's main text, cross-checked against the declared lang attribute. Both are reported, because a mismatch between what a page declares and what it actually contains is itself worth seeing. The exception for item 5 information is assessed under 5a-5c, whose requirements already demand English.

## Detail

### BBMRI-ERIC
<https://www.bbmri-eric.eu/eosc-node-bbmri-eric/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 7094 characters of text rendered
- **1R** 🟠 review — Not assessable in full: it quantifies over every Node Exchange resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled under requirement [P.2] of the Production 1.0 Checklist rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 6 distinct external host(s) linked from the landing page
  - directory.bbmri-eric.eu (Directory)
  - negotiator.bbmri-eric.eu (Negotiator)
  - open-science-cloud.ec.europa.eu (European Open Science Cloud (EOSC))
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "­ EOSC Node - BBMRI-ERIC - BBMRI-ERIC Fonts A A Contrast A A Newsletter sign-up I give permission for BBMRI-ERIC to send me their newsletter and emails about subjects which they think may be of interest to me. I can unsubscribe from all emails at any time. I understand that my information will be processed according to BBMRI-ERIC's privacy notice . Leave this field empty if you're human: FAQ Downl..."
  - organisation-like names found: CSC; EOSC4CANCER EPND EPPerMed ERDERA ERIC; ERIC; European Research Infrastructure Consortium
  - about page one level down: https://www.bbmri-eric.eu/about/ (HTTP 200) opening text: "­ About us - BBMRI-ERIC Fonts A A Contrast A A Newsletter sign-up I give permission for BBMRI-ERIC to send me their newsletter and emails about subjects which they think may be of interest to me. I can unsubscribe from all emails at any time. I understand that..."
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the name found is this node's own — an approved name was found in the page body, but the list supplied is unscoped, so it does not say which node the name belongs to.
  - EOSC-referencing image asset(s): 1
  - img: eosc node - bbmri-eric logo
  - approved name matched from the unscoped list: "EOSC Node | BBMRI-ERIC" (the page writes it "EOSC Node - BBMRI-ERIC") — the list does not say which name belongs to which node, so this does not establish it is this node's own name
  - *Reviewer action:* Confirm the EOSC logo is visible without scrolling. Confirm the matched name is this node's own; the list supplied does not say.
- **4** 🟢 PASS — Links to a specific node entry under eosc.eu/building-the-eosc-federation.
  - "See the dedicated page on the EOSC website" -> https://eosc.eu/building-the-eosc-federation/eosc-node-bbmri-eric/
- **5a** 🟠 review — Quantifies over "all Node Exchange research resources offered by the Node", which cannot be enumerated from the landing page alone. Since checklist v3.2 each resource's purpose description must be on the NLP that presents it (directly or on a page the NLP links to) and in the resource's metadata in the EOSC Catalogue; the tool reads neither the resource list nor the Catalogue.
  - 84 outbound link(s) on the landing page
  - main text length: 7094 characters
  - *Reviewer action:* List the node's Node Exchange resources, then confirm each has an English purpose description on the NLP (or a page it links to) and in its EOSC Catalogue metadata.
- **5b** 🟢 PASS — The landing page does not link to an Acceptable Use Policy itself, but a page it links to does. Checklist v3.2 accepts the policy on the NLP or on intermediate pages linked by the NLP. The policy page itself was not fetched, so this is a pointer, not a verified document.
  - landing page -> https://www.bbmri-eric.eu/services/access-policies/ ("Access Policies")
  - via https://www.bbmri-eric.eu/services/access-policies/: "Acceptable Use Policy of BBMRI-ERIC Services" -> https://www.bbmri-eric.eu/wp-content/uploads/BBMRI-ERIC-AUP-IT-Services-1_3.pdf
  - *Reviewer action:* Confirm the policy covers every Node Exchange resource the landing page presents, and is in English. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **5c** 🟢 PASS — The landing page links to a User Access Policy, and the target was fetched and reads like a policy document.
  - "Access Policies" -> https://www.bbmri-eric.eu/services/access-policies/
  - followed: https://www.bbmri-eric.eu/services/access-policies/ -> HTTP 200, 8923 chars, title: Access Policies - BBMRI-ERIC
  - policy wording found: Policy, You may, conditions
  - *Reviewer action:* Confirm it covers all the node's resources and is in English. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **6** 🟢 PASS — A page reached from the landing page identifies a helpdesk or user support route.
  - "Services & Support" -> https://www.bbmri-eric.eu/services-support/
  - "Contact" -> https://www.bbmri-eric.eu/contact/
  - followed: https://www.bbmri-eric.eu/contact/ -> HTTP 200
  - helpdesk wording on that page: helpdesk
  - *Reviewer action:* Confirm the route reaches the node's user support.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en-GB"
  - detected language: en (confidence 1.0)

### CERN
<https://eosc.cern/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 5969 characters of text rendered
- **1R** 🟠 review — Not assessable in full: it quantifies over every Node Exchange resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled under requirement [P.2] of the Production 1.0 Checklist rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 9 distinct external host(s) linked from the landing page
  - cern.ch (CERN ↗, Directory)
  - eosc-webui.rucioit.cern.ch (Rucio Data Management Scientific Data Management system providing a complete and scalable solution for managing large volumes of data across globally distributed centres.)
  - eosc.cernbox.cern.ch (CERNBox Storage Cloud sync and share service allowing users to store and share data seamlessly across all their devices.)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - meta description: "CERN Node for the EOSC Federation - Research, Analyses, Repositories"
  - opening main text: "EOSC Federation · First wave Node The CERN Node for Open Science Integrating CERN's world-class research services and FAIR data into the European Open Science Cloud, enabling reproducible workflows, open datasets, and cross-disciplinary collaboration for researchers everywhere. Get Started Explore Services Try an Analysis What is the CERN Node? Part of the European Open Science Cloud Federation Th..."
  - organisation-like names found: Competence Centre; Durham University; EOSC Association
  - about page one level down: https://eosc.cern/about/cern-node#stages (HTTP 200) opening text: "The CERN Node A first-wave node of the EOSC Federation The CERN Node strengthens the EOSC Federation by providing high-TRL services and technology essential for high-energy physics and interdisciplinary research. It integrates CERN's established platforms, inc..."
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — it was looked for and not found in the page body, which is not proof of absence, since the <title> is not searched.
  - EOSC-referencing image asset(s): 2
  - img: EOSC Node CERN
  - img: EOSC Node CERN
  - NONE of the 13 approved name(s) for this node appear in the page body — note the <title> is not searched
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** 🟢 PASS — Links to a specific node entry under eosc.eu/building-the-eosc-federation.
  - "CERN Node on eosc.eu ↗" -> https://eosc.eu/building-the-eosc-federation/eosc-node-cern
- **5a** 🟠 review — Quantifies over "all Node Exchange research resources offered by the Node", which cannot be enumerated from the landing page alone. Since checklist v3.2 each resource's purpose description must be on the NLP that presents it (directly or on a page the NLP links to) and in the resource's metadata in the EOSC Catalogue; the tool reads neither the resource list nor the Catalogue.
  - 39 outbound link(s) on the landing page
  - main text length: 5456 characters
  - *Reviewer action:* List the node's Node Exchange resources, then confirm each has an English purpose description on the NLP (or a page it links to) and in its EOSC Catalogue metadata.
- **5b** 🟢 PASS — The landing page does not link to an Acceptable Use Policy itself, but a page it links to does. Checklist v3.2 accepts the policy on the NLP or on intermediate pages linked by the NLP. The policy page was fetched too.
  - landing page -> https://eosc.cern/policies ("Policies")
  - via https://eosc.cern/policies: "Acceptable Use Policy and Conditions of Use The rules you agree to when you use the Node’s services." -> https://eosc.cern/policies/aup
  - via https://eosc.cern/services: "Acceptable Use Policy" -> https://eosc.cern/policies/aup
  - via https://eosc.cern/policies/aup: "Acceptable Use Policy — CERN Node" -> https://eosc.cern/policies/aup
  - *Reviewer action:* Confirm the policy covers every Node Exchange resource the landing page presents, and is in English. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **5c** 🟢 PASS — The landing page does not link to a User Access Policy itself, but a page it links to does. Checklist v3.2 accepts the policy on the NLP or on intermediate pages linked by the NLP. The policy page was fetched too.
  - landing page -> https://eosc.cern/policies ("Policies")
  - via https://eosc.cern/policies: "User Access Policy Who can use the services, and how you get access to them." -> https://eosc.cern/policies/uap
  - via https://eosc.cern/services: "User Access Policy" -> https://eosc.cern/policies/uap
  - via https://eosc.cern/policies/uap: "User Access Policy — CERN Node" -> https://eosc.cern/policies/uap
  - *Reviewer action:* Confirm the policy covers every Node Exchange resource the landing page presents, and is in English. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **6** 🟢 PASS — A page reached from the landing page identifies a helpdesk or user support route.
  - "Contact" -> https://eosc.cern/contact
  - followed: https://eosc.cern/contact -> HTTP 200
  - helpdesk wording on that page: Helpdesk, ticket
  - *Reviewer action:* Confirm the route reaches the node's user support.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en"
  - detected language: en (confidence 1.0)

### EOSC Node Czechia
<https://www.eosc.cz/en/about-eosc-cz/eosc-node-czechia>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 5675 characters of text rendered
  - redirects followed: 2
- **1R** 🟠 review — Not assessable in full: it quantifies over every Node Exchange resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled under requirement [P.2] of the Production 1.0 Checklist rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 7 distinct external host(s) linked from the landing page
  - bsky.app
  - nma.eosc.cz (National Metadata Directory)
  - www.cesnet.cz (Acceptable Use Policy, Privacy Notice)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - meta description: "Through the Czech EOSC Node, European researchers can access computing resources, data, repositories, and secure AI and LLM tools through a single sign-on and a single point of access."
  - opening main text: "You are here: Home EOSC Node Czechia EOSC Node Czechia Through the Czech EOSC Node, European researchers can access computing resources, data, repositories, and secure AI and LLM tools through a single sign-on and a single point of access. Scope EOSC Node Czechia provides a national entry point to selected Czech research data, repositories, computing resources and digital services integrated into ..."
  - organisation-like names found: Masaryk University; Technical University
  - about page one level down: https://www.eosc.cz/en/about-eosc-cz/contact (HTTP 200) opening text: "You are here: Home Contact Contact Contact for media Mgr. Bc. XXXXX XXXXX correspondence Address: XXXXX@ics.muni.cz phone: +420 XXXXXX General contacts Contact: info@eosc.cz EOSC CZ Training Centre: events@eosc.cz Correspondence address of the EOSC-CZ project ..."
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — No EOSC-referencing image asset was found in the markup. This is NOT proof of absence: a logo shown as a CSS background image, an SVG sprite reference, or a file named without "eosc" would all be missed by this check.
  - 4 image/SVG element(s) examined, none referencing EOSC
  - mentions of EOSC in page text: 47
  - approved name matched from the unscoped list: "EOSC Node | Czechia" (the page writes it "EOSC Node Czechia") — the list does not say which name belongs to which node, so this does not establish it is this node's own name
  - *Reviewer action:* Look at the page (or its screenshot) and confirm whether an EOSC logo is visibly displayed.
- **4** 🔴 **FAIL** — Links only to the building-the-eosc-federation index, which the checklist explicitly excludes. The node's own dedicated entry is required.
  - "EOSC Federation" -> https://eosc.eu/building-the-eosc-federation
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-czechia/ but is not linked from here
- **5a** 🟠 review — Quantifies over "all Node Exchange research resources offered by the Node", which cannot be enumerated from the landing page alone. Since checklist v3.2 each resource's purpose description must be on the NLP that presents it (directly or on a page the NLP links to) and in the resource's metadata in the EOSC Catalogue; the tool reads neither the resource list nor the Catalogue.
  - 78 outbound link(s) on the landing page
  - main text length: 4021 characters
  - *Reviewer action:* List the node's Node Exchange resources, then confirm each has an English purpose description on the NLP (or a page it links to) and in its EOSC Catalogue metadata.
- **5b** 🟢 PASS — The landing page links to what appears to be an Acceptable Use Policy. The link target was not fetched (it is on another site, which the tool does not follow), so this is a pointer, not a verified document.
  - "Acceptable Use Policy" -> https://www.cesnet.cz/en/cesid-aup
  - *Reviewer action:* Open the link and confirm the target really is an Acceptable Use Policy, in English. No --depth setting will fetch it. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the NLP, but it links to an Acceptable Use Policy. Checklist v3.2 allows the AUP and the UAP to be provided through the same, single document, so this may satisfy the point.
  - 78 link(s) on the landing page examined, none matching a User Access Policy
  - 12 linked page(s) read, none linking to a User Access Policy: https://www.eosc.cz/en/about-eosc-cz/contact, https://www.eosc.cz/en/projects/national-support, https://www.eosc.cz/en/about-eosc-cz, https://www.eosc.cz/en/about-eosc-cz/initiative-eosc-cz, https://www.eosc.cz/en/projects/czech-academic-and-research-discovery-services-cards ...
  - named in the text without a link: Access conditions
  - an Acceptable Use Policy: "Acceptable Use Policy" -> https://www.cesnet.cz/en/cesid-aup
  - *Reviewer action:* Open the linked an Acceptable Use Policy and confirm it also serves as a User Access Policy for every Node Exchange resource the page presents. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **6** 🟢 PASS — The landing page links to a route identified as a helpdesk or user support.
  - "support@eosc.cz" -> mailto:support@eosc.cz
  - "support@eosc.cz" -> mailto:support@eosc.cz
  - *Reviewer action:* Confirm the route reaches the node's user support. A helpdesk behind a sign-in form is still a means of contact, but note it.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en"
  - detected language: en (confidence 1.0)

### EOSC DTO (D4Science)
<https://eosc-dto.d4science.org/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 12326 characters of text rendered
- **1R** 🟠 review — Not assessable in full: it quantifies over every Node Exchange resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled under requirement [P.2] of the Production 1.0 Checklist rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 5 distinct external host(s) linked from the landing page
  - doi.org (EOSC-Marine project)
  - ec.europa.eu (EU H2020 programme)
  - support.d4science.org (Helpdesk, Open a Node helpdesk request)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "A thematic node of the European Open Science Cloud EOSC Node | European Digital Twin Ocean Federating marine data, research environments, analytical services and computing resources for collaborative, FAIR and reproducible ocean science. Sign in with EOSC AAI Explore Resource Catalogue Explore Services Explore Research Environments This Node Landing Page is publicly accessible without login. Prote..."
  - organisation-like names found: AUP Consortium; CNR; CNR CNR; ERIC; European Research Executive Agency; OGS HCMR EMSO-ERIC ETT University
  - about page one level down: https://www.d4science.org/about-us (HTTP 200) opening text: "D4Science is a digital infrastructure designed to offer diverse communities of practices a comprehensive suite of services through tailored and co-created virtual research environments promoting collaboration and innovation. It is operated as a not-for-profit ..."
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — it was looked for and not found in the page body, which is not proof of absence, since the <title> is not searched.
  - EOSC-referencing image asset(s): 1
  - img: Official logo of EOSC Node European Digital Twin Ocean
  - NONE of the 13 approved name(s) for this node appear in the page body — the phrase "EOSC Node" does occur 5 times, but never followed by an approved name — note the <title> is not searched
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** 🟢 PASS — Links to a specific node entry under eosc.eu/building-the-eosc-federation.
  - "View the dedicated Node page on eosc.eu →" -> https://eosc.eu/building-the-eosc-federation/eosc-node-digital-twin-of-the-ocean
  - "Open the official Node entry →" -> https://eosc.eu/building-the-eosc-federation/eosc-node-digital-twin-of-the-ocean
  - "Node page in EOSC Federation" -> https://eosc.eu/building-the-eosc-federation/eosc-node-digital-twin-of-the-ocean
- **5a** 🟠 review — Quantifies over "all Node Exchange research resources offered by the Node", which cannot be enumerated from the landing page alone. Since checklist v3.2 each resource's purpose description must be on the NLP that presents it (directly or on a page the NLP links to) and in the resource's metadata in the EOSC Catalogue; the tool reads neither the resource list nor the Catalogue.
  - 57 outbound link(s) on the landing page
  - main text length: 12097 characters
  - *Reviewer action:* List the node's Node Exchange resources, then confirm each has an English purpose description on the NLP (or a page it links to) and in its EOSC Catalogue metadata.
- **5b** 🟢 PASS — The landing page links to an Acceptable Use Policy, and the target was fetched and reads like a policy document.
  - "D4Science Access and Acceptable Use Policy" -> https://www.d4science.org/policies/access-and-acceptable-use
  - "AUP" -> https://www.d4science.org/policies/access-and-acceptable-use
  - followed: https://www.d4science.org/policies/access-and-acceptable-use -> HTTP 200, 5461 chars, title: Access and Acceptable Use Policy | D4Science
  - policy wording found: Policy, Responsib, authorized, comply
  - *Reviewer action:* Confirm it covers all the node's resources and is in English. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the NLP, but it links to an Acceptable Use Policy. Checklist v3.2 allows the AUP and the UAP to be provided through the same, single document, so this may satisfy the point.
  - 57 link(s) on the landing page examined, none matching a User Access Policy
  - 13 linked page(s) read, none linking to a User Access Policy: https://www.d4science.org/policies/access-and-acceptable-use, https://eosc-dto.d4science.org/terms-of-use, https://support.d4science.org/projects/eosc-node-eu-dto-support/issues/new, https://www.d4science.org/policies/privacy-and-data-protection, https://eosc-dto.d4science.org/cookie-policy ...
  - named in the text without a link: Access Polic, UAP, User Access Polic
  - an Acceptable Use Policy: "D4Science Access and Acceptable Use Policy" -> https://www.d4science.org/policies/access-and-acceptable-use
  - *Reviewer action:* Open the linked an Acceptable Use Policy and confirm it also serves as a User Access Policy for every Node Exchange resource the page presents. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **6** 🟢 PASS — The landing page links to a route identified as a helpdesk or user support.
  - "Open a Node helpdesk request" -> https://support.d4science.org/projects/eosc-node-eu-dto-support/issues/new
  - "Helpdesk" -> https://support.d4science.org/projects/eosc-node-eu-dto-support/issues/new
  - *Reviewer action:* Confirm the route reaches the node's user support. A helpdesk behind a sign-in form is still a means of contact, but note it.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en-US"
  - detected language: en (confidence 1.0)

### Data Terra
<https://www.data-terra.org/eosc/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 19620 characters of text rendered
- **1R** 🟠 review — Not assessable in full: it quantifies over every Node Exchange resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled under requirement [P.2] of the Production 1.0 Checklist rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 38 distinct external host(s) linked from the landing page
  - cnes.fr
  - fr.linkedin.com
  - intranet.data-terra.org
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "Accueil The EOSC Node f... The EOSC Node for the Earth system and environmental sciences (under construction) The EOSC node’s digital gateway plays a crucial role in connecting research organizations to the broader European ecosystem. It serves as a single-entry point to the European Open Science Cloud (EOSC), facilitating access to open science resources and services across Europe. The DATA TERRA..."
  - no organisation-like names matched by pattern
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — it was looked for and not found in the page body, which is not proof of absence, since the <title> is not searched.
  - EOSC-referencing image asset(s): 1
  - img: eosc node data terra environment
  - NONE of the 13 approved name(s) for this node appear in the page body — the phrase "EOSC Node" does occur 3 times, but never followed by an approved name — note the <title> is not searched
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** 🔴 **FAIL** — No link to eosc.eu was found on the landing page.
  - 93 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-data-terra/ but is not linked from here
- **5a** 🟠 review — Quantifies over "all Node Exchange research resources offered by the Node", which cannot be enumerated from the landing page alone. Since checklist v3.2 each resource's purpose description must be on the NLP that presents it (directly or on a page the NLP links to) and in the resource's metadata in the EOSC Catalogue; the tool reads neither the resource list nor the Catalogue.
  - 93 outbound link(s) on the landing page
  - main text length: 5739 characters
  - *Reviewer action:* List the node's Node Exchange resources, then confirm each has an English purpose description on the NLP (or a page it links to) and in its EOSC Catalogue metadata.
- **5b** 🔴 **FAIL** — No pointer to an Acceptable Use Policy was found on the landing page. None of the 3 linked page(s) the tool read links to it either, and the landing page links to no other policies, legal, services or resources page. Checklist v3.2 requires it on the NLP, directly or via intermediate pages linked by the NLP, for every Node Exchange resource the page presents, as well as in each resource's EOSC Catalogue metadata; being in the Catalogue alone is not enough.
  - 93 link(s) on the landing page examined, none matching an Acceptable Use Policy
  - 3 linked page(s) read, none linking to an Acceptable Use Policy: https://www.data-terra.org/contact-acces/, https://www.data-terra.org/services/, https://www.data-terra.org/offre-de-services/
  - *Reviewer action:* Confirm on the live page, then ask the node to link an Acceptable Use Policy from the NLP or a page it links to, for each of its resources (one document may cover all of them, and may be the same as the other policy).
- **5c** 🔴 **FAIL** — No pointer to a User Access Policy was found on the landing page. None of the 3 linked page(s) the tool read links to it either, and the landing page links to no other policies, legal, services or resources page. Checklist v3.2 requires it on the NLP, directly or via intermediate pages linked by the NLP, for every Node Exchange resource the page presents, as well as in each resource's EOSC Catalogue metadata; being in the Catalogue alone is not enough.
  - 93 link(s) on the landing page examined, none matching a User Access Policy
  - 3 linked page(s) read, none linking to a User Access Policy: https://www.data-terra.org/contact-acces/, https://www.data-terra.org/services/, https://www.data-terra.org/offre-de-services/
  - *Reviewer action:* Confirm on the live page, then ask the node to link a User Access Policy from the NLP or a page it links to, for each of its resources (one document may cover all of them, and may be the same as the other policy).
- **6** 🟠 review — The contact or support pages reached from the landing page do not identify a helpdesk. The checklist asks for the node helpdesk, and general enquiries may not satisfy that.
  - "Contact & accès" -> https://www.data-terra.org/contact-acces/
  - "Contact & accès" -> https://www.data-terra.org/contact-acces/
  - followed: https://www.data-terra.org/contact-acces/ -> HTTP 200
  - *Reviewer action:* Confirm whether any route reaches the node's user support, not a general mailbox or an unrelated service.
- **7** 🟢 PASS — The main content is English. The page declares "fr-FR", which is a metadata inconsistency worth fixing but does not breach point 7.
  - declared lang attribute: "fr-FR"
  - detected language: en (confidence 1.0)
  - *Reviewer action:* Suggest the node correct its lang attribute.

### EOSC Finland
<https://eosc.fi/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 3315 characters of text rendered
  - redirects followed: 1
- **1R** 🟠 review — Not assessable in full: it quantifies over every Node Exchange resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled under requirement [P.2] of the Production 1.0 Checklist rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 10 distinct external host(s) linked from the landing page
  - csc.fi (Detailed contact information (External link), Directions (External link), Main website – csc.fi (External link))
  - docs.csc.fi (Applications catalogue (External link), Docs CSC - User guides (External link), User guides (External link))
  - etsin.fairdata.fi (Etsin (External link))
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "EOSC Finland Pilot Node Dataset-as-a-Service EOSC Finland - Tools for service providers and data managers EOSC Finland for researchers More about the EOSC Federation and the Finnish Pilot Node MyAccessID - a new way to access CSC services Discover services Browse services in the EOSC federation available for researchers with a Finnish affiliation or project. Service catalogue Start using services ..."
  - organisation-like names found: Browse CSC; CSC; Copyright CSC; Docs CSC; Espoo Life Science Center; IT Center
  - about page one level down: https://research.csc.fi/eosc-the-finnish-candidate-node/short-definition-of-eosc-and-the-federation-and-the-finnish-candidate-node/ (HTTP 200) opening text: "EOSC Finland Pilot Node Dataset-as-a-Service EOSC Finland - Tools for service providers and data managers EOSC Finland for researchers More about the EOSC Federation and the Finnish Pilot Node MyAccessID - a new way to access CSC services More about the EOSC F..."
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — it was looked for and not found in the page body, which is not proof of absence, since the <title> is not searched.
  - EOSC-referencing image asset(s): 1
  - img: EOSCNode_Finland-1-1-scaled.jpg
  - NONE of the 13 approved name(s) for this node appear in the page body — note the <title> is not searched
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** 🔴 **FAIL** — No link to eosc.eu was found on the landing page.
  - 85 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-finland/ but is not linked from here
- **5a** 🟠 review — Quantifies over "all Node Exchange research resources offered by the Node", which cannot be enumerated from the landing page alone. Since checklist v3.2 each resource's purpose description must be on the NLP that presents it (directly or on a page the NLP links to) and in the resource's metadata in the EOSC Catalogue; the tool reads neither the resource list nor the Catalogue.
  - 85 outbound link(s) on the landing page
  - main text length: 823 characters
  - *Reviewer action:* List the node's Node Exchange resources, then confirm each has an English purpose description on the NLP (or a page it links to) and in its EOSC Catalogue metadata.
- **5b** 🟢 PASS — The landing page links to an Acceptable Use Policy, and the target was fetched and reads like a policy document.
  - "Terms of use" -> https://research.csc.fi/terms-of-use/
  - "Prerequisites and responsibilities for a CSC project manager" -> https://research.csc.fi/terms-of-use/prerequisites-for-a-project-manager/
  - followed: https://research.csc.fi/terms-of-use/ -> HTTP 200, 16556 chars, title: Terms of use - Services for Research
  - policy wording found: Terms, comply, conditions, permitted
  - *Reviewer action:* Confirm it covers all the node's resources and is in English. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the NLP, but it links to an Acceptable Use Policy. Checklist v3.2 allows the AUP and the UAP to be provided through the same, single document, so this may satisfy the point.
  - 85 link(s) on the landing page examined, none matching a User Access Policy
  - 20 linked page(s) read, none linking to a User Access Policy: https://research.csc.fi/terms-of-use/, https://research.csc.fi/terms-of-use/prerequisites-for-a-project-manager/, https://research.csc.fi/support, https://research.csc.fi/eosc-the-finnish-candidate-node/short-definition-of-eosc-and-the-federation-and-the-finnish-candidate-node/, https://research.csc.fi/terms-of-use/data-processing-agreement/ ...
  - an Acceptable Use Policy: "Terms of use" -> https://research.csc.fi/terms-of-use/
  - an Acceptable Use Policy: "Prerequisites and responsibilities for a CSC project manager" -> https://research.csc.fi/terms-of-use/prerequisites-for-a-project-manager/
  - *Reviewer action:* Open the linked an Acceptable Use Policy and confirm it also serves as a User Access Policy for every Node Exchange resource the page presents. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **6** 🟢 PASS — The landing page links to a route identified as a helpdesk or user support.
  - "Service Desk" -> https://research.csc.fi/support
  - "Service Desk" -> https://research.csc.fi/support
  - *Reviewer action:* Confirm the route reaches the node's user support. A helpdesk behind a sign-in form is still a means of contact, but note it.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en-US"
  - detected language: en (confidence 1.0)

### PaNOSC
<https://eosc.panosc.eu/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 7846 characters of text rendered
  - redirects followed: 2
- **1R** 🟠 review — Not assessable in full: it quantifies over every Node Exchange resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled under requirement [P.2] of the Production 1.0 Checklist rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 40 distinct external host(s) linked from the landing page
  - aiidalab-qe.readthedocs.io (AiiDAlab Quantum ESPRESSO (QE) app)
  - api.whatsapp.com
  - archive.materialscloud.org (Materials Cloud Archive)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "Menu About About PaNOSC Node PaNOSC project (2018-2022) European Research Infrastructures FAIR Principles Contact Science Cluster About Members Services Photon and Neutron Competence Centre PaNOSC data policy framework PaN OSCARS funded projects PaNOSC Node About Services Training Project (2018-2022) Services Data E-learning platform Use Cases Video Women in science Materials Branding Material Pub..."
  - organisation-like names found: EOSC Association; Institut; Lund University; Neutron Competence Centre; Paul Scherrer Institute
  - about page one level down: https://www.panosc.eu/about-panosc/ (HTTP 200) opening text: "Menu About About PaNOSC Node PaNOSC project (2018-2022) European Research Infrastructures FAIR Principles Contact Science Cluster About Members Services Photon and Neutron Competence Centre PaNOSC data policy framework PaN OSCARS funded projects PaNOSC Node Ab..."
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — it was looked for and not found in the page body, which is not proof of absence, since the <title> is not searched.
  - EOSC-referencing image asset(s): 3
  - img: EOSCNodePaNOSC_ColourPos-scaled.png
  - img: EOSC Federation User Forum
  - img: European Open Science Cloud
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** 🔴 **FAIL** — Links only to the building-the-eosc-federation index, which the checklist explicitly excludes. The node's own dedicated entry is required.
  - "Building the EOSC Federation" -> https://eosc.eu/eosc-about/building-the-eosc-federation/
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-panosc/ but is not linked from here
- **5a** 🟠 review — Quantifies over "all Node Exchange research resources offered by the Node", which cannot be enumerated from the landing page alone. Since checklist v3.2 each resource's purpose description must be on the NLP that presents it (directly or on a page the NLP links to) and in the resource's metadata in the EOSC Catalogue; the tool reads neither the resource list nor the Catalogue.
  - 123 outbound link(s) on the landing page
  - main text length: 7846 characters
  - *Reviewer action:* List the node's Node Exchange resources, then confirm each has an English purpose description on the NLP (or a page it links to) and in its EOSC Catalogue metadata.
- **5b** 🟠 review — No pointer to an Acceptable Use Policy was found on the pages the tool read, but the landing page links to pages that may carry it (a policies, legal, services or resources page) which were not read. Checklist v3.2 accepts the policy on intermediate pages linked by the NLP.
  - 123 link(s) on the landing page examined, none matching an Acceptable Use Policy
  - 10 linked page(s) read, none linking to an Acceptable Use Policy: https://www.panosc.eu/contact/, https://www.panosc.eu/about-panosc/, https://www.panosc.eu/about-european-research-infrastructures/, https://www.panosc.eu/data/panosc-data-policy-framework/, https://www.panosc.eu/privacy-policy/ ...
  - not read: "PaNOSC node services" -> https://services.panosc.eu
  - *Reviewer action:* Open those pages and look for an Acceptable Use Policy for each resource. Collecting the evidence again at depth 1 or more would read them.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the pages the tool read, but the landing page links to pages that may carry it (a policies, legal, services or resources page) which were not read. Checklist v3.2 accepts the policy on intermediate pages linked by the NLP.
  - 123 link(s) on the landing page examined, none matching a User Access Policy
  - 10 linked page(s) read, none linking to a User Access Policy: https://www.panosc.eu/contact/, https://www.panosc.eu/about-panosc/, https://www.panosc.eu/about-european-research-infrastructures/, https://www.panosc.eu/data/panosc-data-policy-framework/, https://www.panosc.eu/privacy-policy/ ...
  - not read: "PaNOSC node services" -> https://services.panosc.eu
  - *Reviewer action:* Open those pages and look for a User Access Policy for each resource. Collecting the evidence again at depth 1 or more would read them.
- **6** 🟠 review — A contact page exists and offers a way to get in touch, but nothing on it identifies a helpdesk specifically. The checklist asks for the node helpdesk, and general enquiries may not satisfy that.
  - "Contact" -> https://www.panosc.eu/contact/
  - "Contact us" -> https://www.panosc.eu/contact/
  - "Contact" -> https://www.panosc.eu/contact/
  - followed: https://www.panosc.eu/contact/ -> HTTP 200
  - *Reviewer action:* Confirm whether any route reaches the node's user support, not a general mailbox or an unrelated service.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en-GB"
  - detected language: en (confidence 1.0)

### EUDAT
<https://portal.eudat.eu/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 1130 characters of text rendered
  - redirects followed: 1
- **1R** 🟠 review — Not assessable in full: it quantifies over every Node Exchange resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled under requirement [P.2] of the Production 1.0 Checklist rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 3 distinct external host(s) linked from the landing page
  - docs.eudat.eu (Set up your workspace Read about the first steps in becoming an EUDAT Node user., User Guides Browse guides on how to best use the EUDAT Node services.)
  - eudat.eu (Service catalogue Browse the EUDAT Node services you can order, no account needed.)
  - www.eudat.eu (Accessibility Statement, EUDAT AUP, FAQs)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "Welcome to the EUDAT Portal Empowering open and collaborative research. The EUDAT Node brings together services, resources, and communities to support FAIR data management, cross-border collaboration, and interoperable scientific workflows within the EOSC ecosystem. Find information about EUDAT Services and how to best utilise the EUDAT Node workspace, a platform built for better research and limi..."
  - organisation-like names found: EUDAT Ltd
  - about page one level down: https://docs.eudat.eu (HTTP 200) opening text: "EUDAT Documentation Documentation Documentation Table of contents Welcome to the EUDAT Documentation service Documentation Feedback Interested in EUDAT services B2ACCESS B2ACCESS Overview Assurance Concepts For Users For Users Enabling MFA Updating Email List ..."
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the name found is this node's own — an approved name was found in the page body, but the list supplied is unscoped, so it does not say which node the name belongs to.
  - EOSC-referencing image asset(s): 2
  - img: EOSC Node
  - img: EOSC Node
  - approved name matched from the unscoped list: "EOSC Node | EUDAT" (the page writes it "EOSC Node EUDAT") — the list does not say which name belongs to which node, so this does not establish it is this node's own name
  - *Reviewer action:* Confirm the EOSC logo is visible without scrolling. Confirm the matched name is this node's own; the list supplied does not say.
- **4** 🟢 PASS — Links to a specific node entry under eosc.eu/building-the-eosc-federation.
  - "EOSC Node EUDAT" -> https://eosc.eu/building-the-eosc-federation/eosc-node-eudat
- **5a** 🟠 review — Quantifies over "all Node Exchange research resources offered by the Node", which cannot be enumerated from the landing page alone. Since checklist v3.2 each resource's purpose description must be on the NLP that presents it (directly or on a page the NLP links to) and in the resource's metadata in the EOSC Catalogue; the tool reads neither the resource list nor the Catalogue.
  - 11 outbound link(s) on the landing page
  - main text length: 742 characters
  - *Reviewer action:* List the node's Node Exchange resources, then confirm each has an English purpose description on the NLP (or a page it links to) and in its EOSC Catalogue metadata.
- **5b** 🟢 PASS — The landing page links to an Acceptable Use Policy, and the target was fetched and reads like a policy document.
  - "EUDAT AUP" -> https://www.eudat.eu/eudat-cdi-aup
  - followed: https://www.eudat.eu/eudat-cdi-aup -> HTTP 200, 3101 chars, title: EUDAT CDI Acceptable Use Policy and Conditions of Use | EUDAT
  - policy wording found: Conditions, You shall, permitted, policy
  - *Reviewer action:* Confirm it covers all the node's resources and is in English. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the NLP, but it links to an Acceptable Use Policy. Checklist v3.2 allows the AUP and the UAP to be provided through the same, single document, so this may satisfy the point.
  - 11 link(s) on the landing page examined, none matching a User Access Policy
  - 14 linked page(s) read, none linking to a User Access Policy: https://www.eudat.eu/eudat-cdi-aup, https://portal.eudat.eu/helpdesk, https://docs.eudat.eu, https://www.eudat.eu/privacy-policy, https://eudat.eu/catalogue ...
  - an Acceptable Use Policy: "EUDAT AUP" -> https://www.eudat.eu/eudat-cdi-aup
  - an Acceptable Use Policy via https://www.eudat.eu/eudat-cdi-aup: "EUDAT CDI Acceptable Use Policy and Conditions of Use | EUDAT" -> https://www.eudat.eu/eudat-cdi-aup
  - *Reviewer action:* Open the linked an Acceptable Use Policy and confirm it also serves as a User Access Policy for every Node Exchange resource the page presents. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **6** 🟢 PASS — The landing page links to a route identified as a helpdesk or user support.
  - "Helpdesk Ask the EUDAT support team a question or report a problem." -> https://portal.eudat.eu/helpdesk
  - *Reviewer action:* Confirm the route reaches the node's user support. A helpdesk behind a sign-in form is still a means of contact, but note it.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en"
  - detected language: en (confidence 1.0)

### EGI
<https://www.egi.eu/egi-node>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 6638 characters of text rendered
- **1R** 🟠 review — Not assessable in full: it quantifies over every Node Exchange resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled under requirement [P.2] of the Production 1.0 Checklist rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 5 distinct external host(s) linked from the landing page
  - bsky.app
  - github.com
  - www.linkedin.com
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "EGI for EOSC EGI Node Operated by the EGI Foundation on behalf of the EGI Federation, the Node provides scalable compute, storage, data management and advanced digital research services for data-intensive science. It delivers EOSC Core and Federating Capabilities including AAI, catalogue, monitoring, accounting, helpdesk and application deployment management, while supporting multi-node use cases ..."
  - organisation-like names found: About About Us EGI Foundation; About EGI Foundation; EGI Digital Innovation Hub Foundation; EGI Foundation; EGI Infrastructure EGI Community Foundation
  - about page one level down: https://www.egi.eu/about/ (HTTP 200) opening text: "EGI: Open Ecosystem for Research and Innovation We support data-intensive research with a wide range of advanced computing services EGI is the federation of computing and storage resource providers united by a mission of delivering advanced computing and data ..."
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — No EOSC-referencing image asset was found in the markup. This is NOT proof of absence: a logo shown as a CSS background image, an SVG sprite reference, or a file named without "eosc" would all be missed by this check.
  - 40 image/SVG element(s) examined, none referencing EOSC
  - mentions of EOSC in page text: 23
  - NONE of the 13 approved name(s) for this node appear in the page body — note the <title> is not searched
  - *Reviewer action:* Look at the page (or its screenshot) and confirm whether an EOSC logo is visibly displayed.
- **4** 🔴 **FAIL** — No link to eosc.eu was found on the landing page.
  - 167 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-egi/ but is not linked from here
- **5a** 🟠 review — Quantifies over "all Node Exchange research resources offered by the Node", which cannot be enumerated from the landing page alone. Since checklist v3.2 each resource's purpose description must be on the NLP that presents it (directly or on a page the NLP links to) and in the resource's metadata in the EOSC Catalogue; the tool reads neither the resource list nor the Catalogue.
  - 167 outbound link(s) on the landing page
  - main text length: 4451 characters
  - *Reviewer action:* List the node's Node Exchange resources, then confirm each has an English purpose description on the NLP (or a page it links to) and in its EOSC Catalogue metadata.
- **5b** 🟢 PASS — The landing page links to an Acceptable Use Policy, and the target was fetched and reads like a policy document.
  - "terms of use" -> https://www.egi.eu/terms-of-use/
  - followed: https://www.egi.eu/terms-of-use/ -> HTTP 200, 2362 chars, title: Terms of Use - EGI
  - policy wording found: Conditions, Policy, Terms, You shall
  - *Reviewer action:* Confirm it covers all the node's resources and is in English. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the NLP, but it links to an Acceptable Use Policy. Checklist v3.2 allows the AUP and the UAP to be provided through the same, single document, so this may satisfy the point.
  - 167 link(s) on the landing page examined, none matching a User Access Policy
  - 12 linked page(s) read, none linking to a User Access Policy: https://www.egi.eu/terms-of-use/, https://www.egi.eu/contact-us/, https://www.egi.eu/about/, https://www.egi.eu/services/, https://www.egi.eu/services/research/ ...
  - named in the text without a link: Access Polic
  - an Acceptable Use Policy: "terms of use" -> https://www.egi.eu/terms-of-use/
  - *Reviewer action:* Open the linked an Acceptable Use Policy and confirm it also serves as a User Access Policy for every Node Exchange resource the page presents. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **6** 🟢 PASS — A page reached from the landing page identifies a helpdesk or user support route.
  - "Contact Us" -> https://www.egi.eu/contact-us/
  - "Contact Us" -> https://www.egi.eu/contact-us/
  - followed: https://www.egi.eu/contact-us/ -> HTTP 200
  - helpdesk wording on that page: support[at]egi
  - *Reviewer action:* Confirm the route reaches the node's user support.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en"
  - detected language: en (confidence 1.0)

### GÉANT
<https://geant.org/geant-eosc-node/>

- **1** 🟠 review — HTTP 403 to this tool's anonymous request, with no login affordance found. This is most likely bot protection reacting to an automated client rather than an access policy, so it is not treated as a failure: a browser may well be served normally. It could not be verified either way.
  - HTTP 403
  - bot-protection wording seen: Cloudflare, Just a moment, Ray ID
  - final URL: https://geant.org/geant-eosc-node/?ki-cf-botcl=1
  - *Reviewer action:* Open the URL in a normal browser. If it loads, this point passes and the block was bot protection. If it demands a login, confirm that the login is EOSC AAI compliant, as verified under requirement [P.2] of the Production 1.0 Checklist.
- **1R** 🟠 review — Not assessable in full: it quantifies over every Node Exchange resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled under requirement [P.2] of the Production 1.0 Checklist rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 1 distinct external host(s) linked from the landing page
  - www.cloudflare.com (Cloudflare, Privacy)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "geant.org Performing security verification This website uses a security service to protect against malicious bots. This page is displayed while the website verifies you are not a bot. Verification successful. Waiting for geant.org to respond..."
  - no organisation-like names matched by pattern
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — No EOSC-referencing image asset was found in the markup. This is NOT proof of absence: a logo shown as a CSS background image, an SVG sprite reference, or a file named without "eosc" would all be missed by this check.
  - 1 image/SVG element(s) examined, none referencing EOSC
  - mentions of EOSC in page text: 0
  - NONE of the 13 approved name(s) for this node appear in the page body — note the <title> is not searched
  - *Reviewer action:* Look at the page (or its screenshot) and confirm whether an EOSC logo is visibly displayed.
- **4** 🟠 review — No link to eosc.eu was found, but the page yielded too little to conclude absence: only 5 DOM element(s) captured (2 link(s), 1 image(s), 2 control(s)) — too little structure to treat the document as delivered
  - 2 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-geant/ but is not linked from here
  - *Reviewer action:* Open the page, dismiss any consent banner, and look for a link to the node's entry under eosc.eu/building-the-eosc-federation.
- **5a** 🟠 review — Quantifies over "all Node Exchange research resources offered by the Node", which cannot be enumerated from the landing page alone. Since checklist v3.2 each resource's purpose description must be on the NLP that presents it (directly or on a page the NLP links to) and in the resource's metadata in the EOSC Catalogue; the tool reads neither the resource list nor the Catalogue.
  - 2 outbound link(s) on the landing page
  - main text length: 241 characters
  - *Reviewer action:* List the node's Node Exchange resources, then confirm each has an English purpose description on the NLP (or a page it links to) and in its EOSC Catalogue metadata.
- **5b** 🟠 review — No pointer to an Acceptable Use Policy was found, but the page yielded too little to conclude absence: only 5 DOM element(s) captured (2 link(s), 1 image(s), 2 control(s)) — too little structure to treat the document as delivered
  - 2 link(s) on the landing page examined, none matching an Acceptable Use Policy
  - *Reviewer action:* Open the page, dismiss any consent banner, and look for an Acceptable Use Policy linked for each resource the page presents.
- **5c** 🟠 review — No pointer to a User Access Policy was found, but the page yielded too little to conclude absence: only 5 DOM element(s) captured (2 link(s), 1 image(s), 2 control(s)) — too little structure to treat the document as delivered
  - 2 link(s) on the landing page examined, none matching a User Access Policy
  - *Reviewer action:* Open the page, dismiss any consent banner, and look for a User Access Policy linked for each resource the page presents.
- **6** 🟠 review — No contact route was found, but the page yielded too little to conclude absence: only 5 DOM element(s) captured (2 link(s), 1 image(s), 2 control(s)) — too little structure to treat the document as delivered
  - 2 link(s) examined
  - *Reviewer action:* Open the page, dismiss any consent banner, and look for a helpdesk or support contact.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en-US"
  - detected language: en (confidence 1.0)

### EOSC Node Poland
<https://eosc.pl/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 5496 characters of text rendered
  - redirects followed: 1
- **1R** 🟠 review — Not assessable in full: it quantifies over every Node Exchange resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled under requirement [P.2] of the Production 1.0 Checklist rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 13 distinct external host(s) linked from the landing page
  - creativecommons.org (Public domain)
  - data.eosc.pl (Work with data)
  - eosc.gov.pl (About, eosc.gov.pl EOSC.gov.pl is an initiative of the Polish EOSC partnership that supports the development of open science in Poland. It provides information on national EOSC-related activities and serves as a space for sharing experiences and good practices among institutions involved in open science.)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "Polish Open Science Platform We support the development of Polish science and innovation by offering modern tools and access to unique research data. All Resources Datasets Publications Software Services Data sources Catalogues Providers Organisations Interoperability Guidelines Trainings Browse Exact match What can you explore on our platform? Explore the catalogue Find the resources you need qui..."
  - organisation-like names found: Academic Computer Centre; EOSC Association EOSC Association; Institute; Interdisciplinary Centre; Networking Center; University
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — it was looked for and not found in the page body, which is not proof of absence, since the <title> is not searched.
  - EOSC-referencing image asset(s): 4
  - img: EOSC Beyond
  - img: eosc.gov.pl
  - img: EOSC Association
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** 🔴 **FAIL** — Links to eosc.eu but not to the node's dedicated page under building-the-eosc-federation. The checklist excludes the homepage.
  - "EOSC Association EOSC Association brings together institutions and organisations committed to building an open scientific ecosystem in Europe. It supports collaboration, common standards, and the development of sustainable infrastructure that improves access to research data, tools, and services." -> https://eosc.eu/
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-poland/ but is not linked from here
- **5a** 🟠 review — Quantifies over "all Node Exchange research resources offered by the Node", which cannot be enumerated from the landing page alone. Since checklist v3.2 each resource's purpose description must be on the NLP that presents it (directly or on a page the NLP links to) and in the resource's metadata in the EOSC Catalogue; the tool reads neither the resource list nor the Catalogue.
  - 35 outbound link(s) on the landing page
  - main text length: 5075 characters
  - *Reviewer action:* List the node's Node Exchange resources, then confirm each has an English purpose description on the NLP (or a page it links to) and in its EOSC Catalogue metadata.
- **5b** 🟢 PASS — The landing page links to an Acceptable Use Policy, and the target was fetched and reads like a policy document.
  - "Terms of use" -> https://eosc.pl/terms-of-use
  - followed: https://eosc.pl/terms-of-use -> HTTP 200, 6530 chars, title: Polish Open Science Platform
  - policy wording found: Conditions, Policy, You shall, authorized
  - *Reviewer action:* Confirm it covers all the node's resources and is in English. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the NLP, but it links to an Acceptable Use Policy. Checklist v3.2 allows the AUP and the UAP to be provided through the same, single document, so this may satisfy the point.
  - 35 link(s) on the landing page examined, none matching a User Access Policy
  - 5 linked page(s) read, none linking to a User Access Policy: https://eosc.pl/terms-of-use, https://eosc.pl/privacy-policy, https://eosc.pl/search/all_collection?q=*, https://eosc.pl/search/data_source, https://eosc.pl/?undefined=
  - an Acceptable Use Policy: "Terms of use" -> https://eosc.pl/terms-of-use
  - an Acceptable Use Policy via https://eosc.pl/terms-of-use: "Polish Open Science Platform" -> https://eosc.pl/terms-of-use
  - *Reviewer action:* Open the linked an Acceptable Use Policy and confirm it also serves as a User Access Policy for every Node Exchange resource the page presents. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **6** 🟢 PASS — The landing page links to a route identified as a helpdesk or user support.
  - "support@eosc.pl" -> mailto:support@eosc.pl
  - "support@eosc.pl" -> mailto:support@eosc.pl
  - *Reviewer action:* Confirm the route reaches the node's user support. A helpdesk behind a sign-in form is still a means of contact, but note it.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en"
  - detected language: en (confidence 1.0)

### EOSC Node Italy
<https://eoscnode-it.d4science.org/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 3254 characters of text rendered
- **1R** 🟠 review — Not assessable in full: it quantifies over every Node Exchange resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled under requirement [P.2] of the Production 1.0 Checklist rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 7 distinct external host(s) linked from the landing page
  - eoscnode-it.d4science.org:443 (EOSC-IT-Node Gateway)
  - www.cnr.it (cnr)
  - www.cookieyes.com (Cookieyes logo)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "The Italian gateway to explore, engage, and enrich research collaborations and contribute to the European Open Science Cloud (EOSC). Sign In This image was generated with the assistance of AI..."
  - no organisation-like names matched by pattern
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — it was looked for and not found in the page body, which is not proof of absence, since the <title> is not searched.
  - EOSC-referencing image asset(s): 1
  - img: EOSC-IT-Node Gateway
  - NONE of the 13 approved name(s) for this node appear in the page body — note the <title> is not searched
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** 🔴 **FAIL** — No link to eosc.eu was found on the landing page.
  - 15 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-italy/ but is not linked from here
  - note: a cookie-consent overlay dominates the captured text (main text only 191 chars; markers: Accept All, Reject All, We value your privacy); only 15 links captured, low for a landing page; only 191 characters of main text captured — the DOM was nonetheless complete, so absence stands
- **5a** 🟠 review — Quantifies over "all Node Exchange research resources offered by the Node", which cannot be enumerated from the landing page alone. Since checklist v3.2 each resource's purpose description must be on the NLP that presents it (directly or on a page the NLP links to) and in the resource's metadata in the EOSC Catalogue; the tool reads neither the resource list nor the Catalogue.
  - 15 outbound link(s) on the landing page
  - main text length: 191 characters
  - *Reviewer action:* List the node's Node Exchange resources, then confirm each has an English purpose description on the NLP (or a page it links to) and in its EOSC Catalogue metadata.
- **5b** 🟢 PASS — The landing page links to an Acceptable Use Policy, and the target was fetched and reads like a policy document.
  - "Terms of Use" -> https://eoscnode-it.d4science.org/terms-of-use
  - followed: https://eoscnode-it.d4science.org/terms-of-use -> HTTP 200, 8785 chars, title: Terms of Use - D4Science Infrastructure Gateway
  - policy wording found: Terms, comply, conditions, policy
  - *Reviewer action:* Confirm it covers all the node's resources and is in English. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the NLP, but it links to an Acceptable Use Policy. Checklist v3.2 allows the AUP and the UAP to be provided through the same, single document, so this may satisfy the point.
  - 15 link(s) on the landing page examined, none matching a User Access Policy
  - 4 linked page(s) read, none linking to a User Access Policy: https://eoscnode-it.d4science.org/terms-of-use, https://eoscnode-it.d4science.org/cookie-policy, https://www.d4science.org/policies/privacy-and-data-protection, https://eoscnode-it.d4science.org/catalogue-eoscnoteit-cloud
  - an Acceptable Use Policy: "Terms of Use" -> https://eoscnode-it.d4science.org/terms-of-use
  - an Acceptable Use Policy via https://eoscnode-it.d4science.org/terms-of-use: "Terms of Use - D4Science Infrastructure Gateway" -> https://eoscnode-it.d4science.org/terms-of-use
  - *Reviewer action:* Open the linked an Acceptable Use Policy and confirm it also serves as a User Access Policy for every Node Exchange resource the page presents. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **6** 🔴 **FAIL** — No contact route of any kind was found among the landing page's links: no mailto:, and no link labelled or addressed as contact, support or helpdesk.
  - 15 link(s) examined
  - note: a cookie-consent overlay dominates the captured text (main text only 191 chars; markers: Accept All, Reject All, We value your privacy); only 15 links captured, low for a landing page; only 191 characters of main text captured — the DOM was nonetheless complete, so absence stands
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en-US"
  - detected language: en (confidence 1.0)

### EOSC Node Slovakia
<https://eosc.sk/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 8227 characters of text rendered
- **1R** 🟠 review — Not assessable in full: it quantifies over every Node Exchange resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled under requirement [P.2] of the Production 1.0 Checklist rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 19 distinct external host(s) linked from the landing page
  - app.crepc.sk (CREPČ The Central Registry of Publications of Universities in the Slovak Republic [Slovak only])
  - app.creuc.sk (CREUČ The Central Registry of Artistic Activity of Universities in the Slovak Republic [Slovak only])
  - cvtisr.sk (CVTI SR Portal, CVTI SR WEB)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - meta description: "EOSC Node Slovakia - pilot entry point (MVP) to research resources and services of the Slovak national EOSC node."
  - opening main text: "Services Resources Use Cases Helpdesk Monitoring About Services Resources Use Cases Helpdesk Monitoring About EN / SK SSO login with EOSC SK AAI The production environment of EOSC SK AAI is deployed and validated. It provides single sign-on for the node based on the EOSC AAI architecture. Login will not be started from this page: it will be offered directly at the selected services as they are con..."
  - organisation-like names found: Comenius University; Contact Slovak Centre; European Open Science Cloud Association; Matej Bel University; Slovak Centre; Technical University
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the name found is this node's own — an approved name was found in the page body, but the list supplied is unscoped, so it does not say which node the name belongs to.
  - EOSC-referencing image asset(s): 6
  - img: EOSC
  - img: EOSC
  - img: Service catalogue sc.eosc.sk
  - *Reviewer action:* Confirm the EOSC logo is visible without scrolling. Confirm the matched name is this node's own; the list supplied does not say.
- **4** 🟢 PASS — Links to a specific node entry under eosc.eu/building-the-eosc-federation.
  - "EOSC Node Slovakia (EOSC-A)" -> https://eosc.eu/building-the-eosc-federation/eosc-node-slovakia
- **5a** 🟠 review — Quantifies over "all Node Exchange research resources offered by the Node", which cannot be enumerated from the landing page alone. Since checklist v3.2 each resource's purpose description must be on the NLP that presents it (directly or on a page the NLP links to) and in the resource's metadata in the EOSC Catalogue; the tool reads neither the resource list nor the Catalogue.
  - 45 outbound link(s) on the landing page
  - main text length: 8227 characters
  - *Reviewer action:* List the node's Node Exchange resources, then confirm each has an English purpose description on the NLP (or a page it links to) and in its EOSC Catalogue metadata.
- **5b** 🟢 PASS — The landing page links to what appears to be an Acceptable Use Policy. The link target was not fetched (it is a PDF document, which the tool does not download or read), so this is a pointer, not a verified document.
  - "Terms of Use (incl. AUP and UAP)" -> https://eosc.sk/docs/eosc_sk_tou.pdf
  - *Reviewer action:* Open the PDF and confirm it is an Acceptable Use Policy, in English. No --depth setting will fetch it. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **5c** 🟢 PASS — The landing page links to what appears to be a User Access Policy. The link target was not fetched (it is a PDF document, which the tool does not download or read), so this is a pointer, not a verified document.
  - "Terms of Use (incl. AUP and UAP)" -> https://eosc.sk/docs/eosc_sk_tou.pdf
  - *Reviewer action:* Open the PDF and confirm it is a User Access Policy, in English. No --depth setting will fetch it. Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue, which this tool does not read.
- **6** 🟢 PASS — The landing page links to a route identified as a helpdesk or user support.
  - "Open helpdesk" -> https://hd.eosc.sk
  - "HELPDESK" -> https://hd.eosc.sk
  - *Reviewer action:* Confirm the route reaches the node's user support. A helpdesk behind a sign-in form is still a means of contact, but note it.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en"
  - detected language: en (confidence 1.0)
