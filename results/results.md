# EOSC Node Landing Page compliance — checklist v3.0

Run `2026-09-21-1738` · 2026-09-21T17:38:53+00:00 · 9 nodes · one page request per node plus 22 followed link(s), then 14 second-hop page(s) (depth 2).

> **This is not a compliance statement.** Points marked 🟠 review are ones this tool refuses to guess at: they either turn on a judgement ("clearly state") or quantify over things this tool does not enumerate ("all research resources").

**Node names.** 9 approved node name(s) were used, from the official list committed with the checklist (`checklist/approved-names.txt`, sha256 `57bf9093b096…`), as an unscoped list: a match shows the name appears on the page but not that it is that node's own name. Separator glyphs are treated as interchangeable, so a page writing “EOSC Node - X” satisfies a list writing “EOSC Node | X”.

🟢 PASS — satisfied, with evidence · 🔴 **FAIL** — violated, with evidence · 🟠 review — a human must decide · 🟣 ERROR — could not be assessed

This run was collected at `--depth=2`, so it is reported twice: once using only the landing page and its direct links, and once using the second hop as well. Both tables come from the **same capture** — the shallow view is the deep evidence with the second-hop pages set aside, not a separate run — so any difference between them is the hop itself and not the passage of time.

### Results at depth 1

Landing page plus links that can settle a checklist point (policies, contact, about). This is the default the tool ships with.

90 cells: 🟢 28 PASS · 🔴 7 FAIL · 🟠 55 review.

| Node | 1 | 1R | 2 | 3 | 4 | 5a | 5b | 5c | 6 | 7 |
|---|---|---|---|---|---|---|---|---|---|---|
| BBMRI-ERIC | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟠 review | 🟢 PASS | 🟢 PASS | 🟢 PASS |
| EOSC DTO (D4Science) | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🔴 **FAIL** | 🟢 PASS |
| Data Terra | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS |
| EOSC Finland | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| PaNOSC | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS |
| EUDAT | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| EGI | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| GÉANT | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review |
| EBRAINS | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟢 PASS |

### Results at depth 2

The same evidence plus 14 page(s) reached one further hop out, under a shared run budget.

90 cells: 🟢 28 PASS · 🔴 7 FAIL · 🟠 55 review.

| Node | 1 | 1R | 2 | 3 | 4 | 5a | 5b | 5c | 6 | 7 |
|---|---|---|---|---|---|---|---|---|---|---|
| BBMRI-ERIC | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟠 review | 🟢 PASS | 🟢 PASS | 🟢 PASS |
| EOSC DTO (D4Science) | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🔴 **FAIL** | 🟢 PASS |
| Data Terra | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS |
| EOSC Finland | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| PaNOSC | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS |
| EUDAT | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| EGI | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| GÉANT | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review |
| EBRAINS | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟢 PASS |

### What the second hop changed

**No verdict changed.** The second hop fetched 14 page(s) and left all 90 cells exactly as depth 1 had them.

That is a finding, not a failure of the deeper crawl. The points still marked 🟠 review are not shallow-crawl artefacts: they turn on a judgement ("clearly state") or quantify over things no crawl enumerates ("all research resources offered by the Node"). Fetching more pages cannot settle either kind, which is why depth 1 remains the default.

#### Pages the second hop fetched

| Node | Point it was followed for | Page | Served |
|---|---|---|---|
| BBMRI-ERIC | 2 | <https://www.bbmri-eric.eu/news-events/bbmri-eric-at-the-integrating-research-and-healthcare-for-rare-diseases-workshop-in-malta/jel_workshop_malta/> | 200 |
| BBMRI-ERIC | 2 | <https://www.bbmri-eric.eu/national-nodes/> | 200 |
| EOSC Finland | 6 | <https://research.csc.fi/training/csc-research-support-coffee-every-wednesday-at-1400-finnish-time/> | 200 |
| PaNOSC | 2 | <https://www.panosc.eu/about-panosc/photon-and-neutron-competence-centre/> | 200 |
| EUDAT | 5b | <https://eudat.eu/eudat-cdi-aup/data-protection-and-privacy-policies> | 200 |
| EUDAT | 6 | <https://www.eudat.eu/catalogue> | error |
| EUDAT | 6 | <https://eudat.eu/contact-support-request> | 200 |
| EUDAT | 2 | <https://docs.eudat.eu/b2access/about/> | 200 |
| EGI | 2 | <https://www.egi.eu/egi-federation/> | 200 |
| EBRAINS | 6 | <https://ebrains.eu/contact> | 200 |
| EBRAINS | 2 | <https://ebrains.eu/about/at-a-glance/mission> | 200 |
| EBRAINS | 2 | <https://ebrains.eu/about/at-a-glance/science-vision> | 200 |
| EBRAINS | 2 | <https://ebrains.eu/about/at-a-glance/ebrains-20> | 200 |
| EBRAINS | 2 | <https://ebrains.eu/about/at-a-glance/ethics-society> | 200 |


## What each column means

Full requirement text and the reasoning behind each verdict: [checklist v3.0 explained](checklist-v3.0.html).

| Column | Question it answers | Can a tool decide it? |
|---|---|---|
| **1** | Is the landing page itself reachable without logging in (or via EOSC AAI)? | yes, by inspection |
| **1R** | Are the resources the landing page points to also public or behind EOSC AAI? | no, human judgement |
| **2** | Does the page state the node's scope, its intended users, and who runs it? | no, human judgement |
| **3** | Is the EOSC logo shown, together with the official Tripartite-approved node name? | partly |
| **4** | Does the page link to this node's own entry on eosc.eu (not the homepage or the index)? | yes, by inspection |
| **5a** | Is there an English purpose description for the node's research resources? | no, human judgement |
| **5b** | Is an Acceptable Use Policy (AUP) reachable for those resources? | partly |
| **5c** | Is a User Access Policy (UAP) reachable for those resources? | partly |
| **6** | Is there a way to contact the node's helpdesk? | partly |
| **7** | Is the landing page in English? | yes, by inspection |

## Points in full

**1 — NLP is publicly accessible, or reachable via EOSC AAI login** (decidable by inspection)  
The Node Landing Page must either be (a) publicly accessible (anonymously, i.e. without the need for users to login) or (b) accessible via login through EOSC AAI.

> Anonymous reachability is directly observable: fetch the URL without credentials and see whether the content is served. Branch (b) only matters when (a) fails.

**1R — Resources pointed to by the NLP are public or behind EOSC AAI** (needs a human)  
All resources pointed by the Node Landing Page, thus exposed to EOSC users, either directly or through links through intermediate pages, must either be publicly accessible or accessible via login through EOSC AAI.

> Not decidable by inspection, and one level of link following does not close the gap. The requirement quantifies over every resource reachable from the page "either directly or through links through intermediate pages", which is unbounded; this tool follows at most one level, and only links that can settle a specific point. Even with full traversal it would still require confirming that each login encountered is genuinely EOSC AAI rather than a local or institutional IdP, and whether a given login is EOSC AAI compliant is settled during node enrolment with the EEN, not by reading HTML. The tool reports how many followed pages were served anonymously and lists the outbound resource links it found, so a reviewer has a work list.

**2 — Scope, intended users and responsible organization are stated** (needs a human)  
Clearly state the Node's scope, intended users and responsible organization. (It is up to the Node to feature all the organisations involved).

> "Clearly state" is a judgement about whether prose communicates three things to a researcher. A keyword match would produce confident nonsense in both directions. The tool extracts the candidate passages and names the reviewer must read.

**3 — EOSC logo and official Tripartite-approved node name are visible** (partly decidable)  
Clearly and visibly show the EOSC logo and the official Tripartite-approved name of the Node.

> Presence of an EOSC logo image is checkable, with caveats: a logo rendered as a CSS background or inlined SVG sprite can be missed, and "clearly and visibly" is a judgement. The Tripartite-approved name is NOT checkable without the authoritative list of approved node names, which the tool does not have; supply it via --approved-names to turn this into a real check.

**4 — Link to the node's own dedicated page on eosc.eu** (decidable by inspection)  
Provide a link to the Node's own dedicated page on the eosc.eu website — the Node's entry under eosc.eu/building-the-eosc-federation, not the eosc.eu homepage or the index page itself.

> Fully decidable and the sharpest point in the checklist: an href under eosc.eu/building-the-eosc-federation/ with a path segment beyond the index. The checklist explicitly excludes both the homepage and the index, so those are matched and rejected rather than ignored.

**5a — Purpose description accessible in English for research resources** (needs a human)  
For all research resources offered by the Node to EOSC users, a purpose description must be accessible in English either directly or via the link to the resource's entry in the EOSC Catalogue.

> Requires enumerating "all research resources offered by the Node", which is not derivable from the landing page alone and is not what this tool's single level of link following collects. Judging whether each description states a purpose is then a reading task, not a pattern match.

**5b — Acceptable Use Policy (AUP) accessible for research resources** (partly decidable)  
For all research resources offered by the Node, the Acceptable Use Policy (AUP) must be accessible in English either directly or via the resource's entry in the EOSC Catalogue.

> A pointer to an AUP on the landing page is checkable. "For all research resources" is not, without enumerating the resources. Absence of a pointer on the landing page is therefore reported as MANUAL_REVIEW, never FAIL: the policy may legitimately live on each resource's catalogue entry, which is exactly what the checklist permits.

**5c — User Access Policy (UAP) accessible for research resources** (partly decidable)  
For all research resources offered by the Node, the User Access Policy (UAP) must be accessible in English either directly or via the resource's entry in the EOSC Catalogue.

> Same reasoning as 5b. Note that AUP and UAP are distinct documents in this checklist and must not be conflated: an "Access Policy" satisfies 5c, an "Acceptable Use Policy" satisfies 5b, and many nodes publish only one.

**6 — Means of contacting the node helpdesk** (partly decidable)  
Provide means of contacting the Node helpdesk.

> A contact route (mailto:, contact/support/helpdesk page, contact form) is checkable. Whether it reaches a *helpdesk* rather than a generic press or info address is a judgement, so a generic-looking contact is flagged rather than passed silently.

**7 — The page is in English** (decidable by inspection)  
Be in English (Any other pages and information are not required to be strictly in English).

> Statistical language detection over the page's main text, cross-checked against the declared lang attribute. Both are reported, because a mismatch between what a page declares and what it actually contains is itself worth seeing.

## Detail

### BBMRI-ERIC
<https://www.bbmri-eric.eu/eosc-node-bbmri-eric/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 7100 characters of text rendered
- **1R** 🟠 review — Not assessable in full: it quantifies over every resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 6 distinct external host(s) linked from the landing page
  - directory.bbmri-eric.eu (Directory)
  - negotiator.bbmri-eric.eu (Negotiator)
  - open-science-cloud.ec.europa.eu (European Open Science Cloud (EOSC))
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "­ EOSC Node - BBMRI-ERIC - BBMRI-ERIC Fonts A A Contrast A A Newsletter sign-up I give permission for BBMRI-ERIC to send me their newsletter and emails about subjects which they think may be of interest to me. I can unsubscribe from all emails at any time. I understand that my information will be processed according to BBMRI-ERIC's privacy notice . Leave this field empty if you're human: FAQ Downl..."
  - organisation-like names found: CSC; EOSC4CANCER EPND EPPerMed ERDERA ERIC; ERIC; European Research Infrastructure Consortium
  - about page one level down: https://www.bbmri-eric.eu/about/ (HTTP 200) opening text: "Fonts A A Contrast A A Newsletter sign-up I give permission for BBMRI-ERIC to send me their newsletter and emails about subjects which they think may be of interest to me. I can unsubscribe from all emails at any time. I understand that my information will be ..."
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — the tool has no authoritative list of approved names.
  - EOSC-referencing image asset(s): 1
  - img: eosc node - bbmri-eric logo
  - approved name matched from the unscoped list: "EOSC Node | BBMRI-ERIC" (the page writes it "EOSC Node - BBMRI-ERIC") — the list does not say which name belongs to which node, so this does not establish it is this node's own name
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** 🟢 PASS — Links to a specific node entry under eosc.eu/building-the-eosc-federation.
  - "See the dedicated page on the EOSC website" -> https://eosc.eu/building-the-eosc-federation/eosc-node-bbmri-eric/
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 84 outbound link(s) on the landing page
  - main text length: 7100 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟠 review — An acceptable use policy is mentioned in the page text but not as a followable link.
  - text mentions: AUP
  - *Reviewer action:* Find where an Acceptable Use Policy is actually published and confirm it is reachable.
- **5c** 🟢 PASS — The landing page links to a User Access Policy, and the target was fetched and reads like a policy document.
  - "Access Policies" -> https://www.bbmri-eric.eu/services/access-policies/
  - followed: https://www.bbmri-eric.eu/services/access-policies/ -> HTTP 200, 8929 chars, title: Access Policies - BBMRI-ERIC
  - policy wording found: Policy, You may, conditions
  - *Reviewer action:* Confirm it covers all the node's resources and is in English.
- **6** 🟢 PASS — A support or helpdesk contact route is present.
  - "Services & Support" -> https://www.bbmri-eric.eu/services-support/
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en-GB"
  - detected language: en (confidence 1.0)

### EOSC DTO (D4Science)
<https://eosc-dto.d4science.org/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 4328 characters of text rendered
- **1R** 🟠 review — Not assessable in full: it quantifies over every resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 5 distinct external host(s) linked from the landing page
  - eosc-dto.d4science.org:443 (European-DTO Gateway)
  - open-science-cloud.ec.europa.eu (EOSC)
  - research-and-innovation.ec.europa.eu (HEU programme)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "EOSC Node | European Digital Twin Ocean This EOSC Thematic Node originated from the Blue-Cloud initiative, which de-facto piloted a marine thematic node to advance high-quality marine science Sign In Register Welcome! Access the rich world of this EOSC thematic node via the user-friendly D4Science platform . If you already have an account, simply sign in using your existing credentials, including ..."
  - no organisation-like names matched by pattern
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — the tool has no authoritative list of approved names.
  - EOSC-referencing image asset(s): 1
  - img: EOSC Node | European Digital Twin Ocean
  - NONE of the 9 approved name(s) for this node appear in the page body — the phrase "EOSC Node" does occur 2 times, but never followed by an approved name — note the <title> is not searched
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** 🔴 **FAIL** — No link to eosc.eu was found on the landing page.
  - 20 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-digital-twin-of-the-ocean/ but is not linked from here
  - note: a cookie-consent overlay dominates the captured text (main text only 530 chars; markers: Accept All, Reject All, This website uses cookies); only 20 links captured, low for a landing page; only 530 characters of main text captured — the DOM was nonetheless complete, so absence stands
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 20 outbound link(s) on the landing page
  - main text length: 530 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟢 PASS — The landing page links to an Acceptable Use Policy, and the target was fetched and reads like a policy document.
  - "Terms of Use" -> https://eosc-dto.d4science.org/terms-of-use
  - followed: https://eosc-dto.d4science.org/terms-of-use -> HTTP 200, 8785 chars, title: Terms of Use - D4Science Infrastructure Gateway
  - policy wording found: Terms, comply, conditions, policy
  - *Reviewer action:* Confirm it covers all the node's resources and is in English.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 20 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** 🔴 **FAIL** — No contact route of any kind was found among the landing page's links: no mailto:, and no link labelled or addressed as contact, support or helpdesk.
  - 20 link(s) examined
  - note: a cookie-consent overlay dominates the captured text (main text only 530 chars; markers: Accept All, Reject All, This website uses cookies); only 20 links captured, low for a landing page; only 530 characters of main text captured — the DOM was nonetheless complete, so absence stands
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en-US"
  - detected language: en (confidence 1.0)

### Data Terra
<https://www.data-terra.org/eosc/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 19620 characters of text rendered
- **1R** 🟠 review — Not assessable in full: it quantifies over every resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 38 distinct external host(s) linked from the landing page
  - cnes.fr
  - fr.linkedin.com
  - intranet.data-terra.org
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "Accueil The EOSC Node f... The EOSC Node for the Earth system and environmental sciences (under construction) The EOSC node’s digital gateway plays a crucial role in connecting research organizations to the broader European ecosystem. It serves as a single-entry point to the European Open Science Cloud (EOSC), facilitating access to open science resources and services across Europe. The DATA TERRA..."
  - no organisation-like names matched by pattern
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — the tool has no authoritative list of approved names.
  - EOSC-referencing image asset(s): 1
  - img: eosc node data terra environment
  - NONE of the 9 approved name(s) for this node appear in the page body — the phrase "EOSC Node" does occur 3 times, but never followed by an approved name — note the <title> is not searched
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** 🔴 **FAIL** — No link to eosc.eu was found on the landing page.
  - 93 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-data-terra/ but is not linked from here
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 93 outbound link(s) on the landing page
  - main text length: 5739 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟠 review — No pointer to an Acceptable Use Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 93 link(s) examined, none matching an Acceptable Use Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for an Acceptable Use Policy.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 93 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** 🟠 review — A contact route exists, but nothing identifies it as a helpdesk. The checklist asks specifically for the node helpdesk, and a general enquiries or press address does not obviously satisfy that.
  - "Contact & accès" -> https://www.data-terra.org/contact-acces/
  - "Contact & accès" -> https://www.data-terra.org/contact-acces/
  - *Reviewer action:* Confirm this contact route reaches the node's user support, not a general mailbox.
- **7** 🟢 PASS — The main content is English. The page declares "fr-FR", which is a metadata inconsistency worth fixing but does not breach point 7.
  - declared lang attribute: "fr-FR"
  - detected language: en (confidence 1.0)
  - *Reviewer action:* Suggest the node correct its lang attribute.

### EOSC Finland
<https://eosc.fi/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 3329 characters of text rendered
  - redirects followed: 1
- **1R** 🟠 review — Not assessable in full: it quantifies over every resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML. One level of crawling narrows this but cannot close it.
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
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — the tool has no authoritative list of approved names.
  - EOSC-referencing image asset(s): 1
  - img: EOSCNode_Finland-1-1-scaled.jpg
  - NONE of the 9 approved name(s) for this node appear in the page body — note the <title> is not searched
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** 🔴 **FAIL** — No link to eosc.eu was found on the landing page.
  - 85 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-finland/ but is not linked from here
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 85 outbound link(s) on the landing page
  - main text length: 823 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟢 PASS — The landing page links to an Acceptable Use Policy, and the target was fetched and reads like a policy document.
  - "Terms of use" -> https://research.csc.fi/terms-of-use/
  - followed: https://research.csc.fi/terms-of-use/ -> HTTP 200, 16560 chars, title: Terms of use - Services for Research
  - policy wording found: Terms, comply, conditions, permitted
  - *Reviewer action:* Confirm it covers all the node's resources and is in English.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 85 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** 🟢 PASS — A support or helpdesk contact route is present.
  - "Service Desk" -> https://research.csc.fi/support
  - "Service Desk" -> https://research.csc.fi/support
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en-US"
  - detected language: en (confidence 1.0)

### PaNOSC
<https://eosc.panosc.eu/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 7714 characters of text rendered
  - redirects followed: 2
- **1R** 🟠 review — Not assessable in full: it quantifies over every resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 37 distinct external host(s) linked from the landing page
  - aiidalab-qe.readthedocs.io (AiiDAlab Quantum ESPRESSO (QE) app)
  - api.whatsapp.com
  - archive.materialscloud.org (Materials Cloud Archive)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "Menu About About PaNOSC Node PaNOSC project (2018-2022) European Research Infrastructures FAIR Principles Contact Science Cluster About Members Services Photon and Neutron Competence Centre PaNOSC data policy framework PaN OSCARS funded projects PaNOSC Node About Services Training Project (2018-2022) Services Data E-learning platform Use Cases Video Women in science Materials Branding Material Pub..."
  - organisation-like names found: EOSC Association; Institut; Lund University; Neutron Competence Centre; Paul Scherrer Institute
  - about page one level down: https://www.panosc.eu/about-panosc/ (HTTP 200) opening text: "Menu About About PaNOSC Node PaNOSC project (2018-2022) European Research Infrastructures FAIR Principles Contact Science Cluster About Members Services Photon and Neutron Competence Centre PaNOSC data policy framework PaN OSCARS funded projects PaNOSC Node Ab..."
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — the tool has no authoritative list of approved names.
  - EOSC-referencing image asset(s): 3
  - img: EOSCNodePaNOSC_ColourPos-scaled.png
  - img: EOSC-Federation-logo.png
  - img: European Open Science Cloud
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** 🔴 **FAIL** — Links only to the building-the-eosc-federation index, which the checklist explicitly excludes. The node's own dedicated entry is required.
  - "Building the EOSC Federation" -> https://eosc.eu/eosc-about/building-the-eosc-federation/
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-panosc/ but is not linked from here
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 118 outbound link(s) on the landing page
  - main text length: 7714 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟠 review — No pointer to an Acceptable Use Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 118 link(s) examined, none matching an Acceptable Use Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for an Acceptable Use Policy.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 118 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** 🟠 review — A contact page exists and offers a way to get in touch, but nothing on it identifies a helpdesk specifically. The checklist asks for the node helpdesk, and general enquiries may not satisfy that.
  - followed: https://www.panosc.eu/contact/ -> HTTP 200
  - address given: mailto:contact@panosc.eu
  - address given: mailto:management@panosc.eu
  - *Reviewer action:* Confirm this reaches the node's user support, not a general mailbox.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en-GB"
  - detected language: en (confidence 1.0)

### EUDAT
<https://portal.eudat.eu/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 922 characters of text rendered
  - redirects followed: 1
- **1R** 🟠 review — Not assessable in full: it quantifies over every resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 2 distinct external host(s) linked from the landing page
  - docs.eudat.eu (Set up your workspace Read about the first steps in becoming an EUDAT Node user., User Guides Browse guides on how to best use the EUDAT Node for your research.)
  - www.eudat.eu (Accessibility Statement, EUDAT AUP, FAQs)
  - depth 1: 6 of 7 followed page(s) were served anonymously, so those are publicly accessible
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "EOSC Node Marketplace Welcome to the EUDAT Portal Find information about EUDAT Services and how to best utilise the EUDAT Node workspace, a platform built for better research and limitless science. Uncertain where to start? Service catalogue Browse the EUDAT Node services you can order, no account needed. Set up your workspace Read about the first steps in becoming an EUDAT Node user. User Guides ..."
  - organisation-like names found: EUDAT Ltd
  - about page one level down: https://docs.eudat.eu (HTTP 200) opening text: "EUDAT Documentation Documentation Documentation Table of contents Welcome to the EUDAT Documentation service Documentation Feedback Interested in EUDAT services B2ACCESS B2ACCESS Overview Assurance Concepts For Users For Users Enabling MFA Updating Email List ..."
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — the tool has no authoritative list of approved names.
  - EOSC-referencing image asset(s): 2
  - img: EOSC Node
  - img: EOSC Node
  - approved name matched from the unscoped list: "EOSC Node | EUDAT" (the page writes it "EOSC Node EUDAT") — the list does not say which name belongs to which node, so this does not establish it is this node's own name
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** 🟢 PASS — Links to a specific node entry under eosc.eu/building-the-eosc-federation.
  - "EOSC Node EUDAT" -> https://eosc.eu/building-the-eosc-federation/eosc-node-eudat
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 11 outbound link(s) on the landing page
  - main text length: 534 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟢 PASS — The landing page links to an Acceptable Use Policy, and the target was fetched and reads like a policy document.
  - "EUDAT AUP" -> https://www.eudat.eu/eudat-cdi-aup
  - followed: https://www.eudat.eu/eudat-cdi-aup -> HTTP 200, 3101 chars, title: EUDAT CDI Acceptable Use Policy and Conditions of Use | EUDAT
  - policy wording found: Conditions, You shall, permitted, policy
  - *Reviewer action:* Confirm it covers all the node's resources and is in English.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 11 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** 🟢 PASS — A support or helpdesk contact route is present.
  - "Helpdesk Ask the EUDAT support team a question or report a problem." -> https://portal.eudat.eu/helpdesk
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en"
  - detected language: en (confidence 1.0)

### EGI
<https://www.egi.eu/egi-node>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 6638 characters of text rendered
- **1R** 🟠 review — Not assessable in full: it quantifies over every resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML. One level of crawling narrows this but cannot close it.
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
  - NONE of the 9 approved name(s) for this node appear in the page body — note the <title> is not searched
  - *Reviewer action:* Look at the page (or its screenshot) and confirm whether an EOSC logo is visibly displayed.
- **4** 🔴 **FAIL** — No link to eosc.eu was found on the landing page.
  - 167 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-egi/ but is not linked from here
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 167 outbound link(s) on the landing page
  - main text length: 4451 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟢 PASS — The landing page links to an Acceptable Use Policy, and the target was fetched and reads like a policy document.
  - "terms of use" -> https://www.egi.eu/terms-of-use/
  - followed: https://www.egi.eu/terms-of-use/ -> HTTP 200, 2362 chars, title: Terms of Use - EGI
  - policy wording found: Conditions, Policy, Terms, You shall
  - *Reviewer action:* Confirm it covers all the node's resources and is in English.
- **5c** 🟠 review — A user access policy is mentioned in the page text but not as a followable link.
  - text mentions: Access Polic
  - *Reviewer action:* Find where a User Access Policy is actually published and confirm it is reachable.
- **6** 🟢 PASS — The contact page reached from the landing page identifies a support or helpdesk route.
  - "Contact Us" -> https://www.egi.eu/contact-us/
  - "Contact Us" -> https://www.egi.eu/contact-us/
  - followed: https://www.egi.eu/contact-us/ -> HTTP 200
  - helpdesk wording on that page: Support
  - *Reviewer action:* Confirm the route reaches the node's user support.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en"
  - detected language: en (confidence 1.0)

### GÉANT
<https://geant.org/geant-eosc-node/>

- **1** 🟠 review — HTTP 403 to this tool's anonymous request, with no login affordance found. This is most likely bot protection reacting to an automated client rather than an access policy, so it is not treated as a failure: a browser may well be served normally. It could not be verified either way.
  - HTTP 403
  - bot-protection wording seen: Just a moment
  - final URL: https://geant.org/geant-eosc-node/?ki-cf-botcl=1&__cf_chl_rt_tk=X05Sy.t37nU_vgBcL6YNwTlvx40ar7yO2_gAcJNYc2E-1789996062-1.0.1.1-NKqjBe7R838ToZ356YSM4RSXdHXkZVL3MHUu1WOel.8
  - *Reviewer action:* Open the URL in a normal browser. If it loads, this point passes and the block was bot protection. If it demands a login, confirm with the EEN that the login is EOSC AAI compliant.
- **1R** 🟠 review — Not assessable in full: it quantifies over every resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 0 distinct external host(s) linked from the landing page
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - no organisation-like names matched by pattern
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — No EOSC-referencing image asset was found in the markup. This is NOT proof of absence: a logo shown as a CSS background image, an SVG sprite reference, or a file named without "eosc" would all be missed by this check.
  - 0 image/SVG element(s) examined, none referencing EOSC
  - mentions of EOSC in page text: 0
  - 9 approved name(s) were supplied for this node, but no page body was captured (HTTP 403), so the name was not looked for
  - *Reviewer action:* Look at the page (or its screenshot) and confirm whether an EOSC logo is visibly displayed.
- **4** 🟠 review — No link to eosc.eu was found, but the page yielded too little to conclude absence: no links were captured at all, so the page yielded no link evidence
  - 0 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-geant/ but is not linked from here
  - *Reviewer action:* Open the page, dismiss any consent banner, and look for a link to the node's entry under eosc.eu/building-the-eosc-federation.
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 0 outbound link(s) on the landing page
  - main text length: 0 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟠 review — No pointer to an Acceptable Use Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 0 link(s) examined, none matching an Acceptable Use Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for an Acceptable Use Policy.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 0 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** 🟠 review — No contact route was found, but the page yielded too little to conclude absence: no links were captured at all, so the page yielded no link evidence
  - 0 link(s) examined
  - *Reviewer action:* Open the page, dismiss any consent banner, and look for a helpdesk or support contact.
- **7** 🟠 review — Only 0 characters of text were available — too little to detect a language.
  - declared lang attribute: "en-US"
  - *Reviewer action:* Open the page and confirm its content is in English.

### EBRAINS
<https://ebrains.eu/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 6693 characters of text rendered
- **1R** 🟠 review — Not assessable in full: it quantifies over every resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 5 distinct external host(s) linked from the landing page
  - bsky.app (Bluesky)
  - mastodon.social (Mastodon)
  - www.linkedin.com (LinkedIn)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - meta description: "An open research infrastructure that provides data, tools and services for brain-related research – from the molecular and cellular levels to the whole organ."
  - opening main text: "Built for Brain Breakthroughs Europe's Digital Infrastructure for Brain Research Explore data, tools and services EBRAINS RI EBRAINS is an open research infrastructure (RI) that provides data, tools and services for brain-related research – from the molecular and cellular levels to the whole organ. The EBRAINS infrastructure was originally built by the EU-funded Human Brain Project and is now adva..."
  - organisation-like names found: University
  - about page one level down: https://ebrains.eu/about (HTTP 200) opening text: "Breadcrumb Start > About About A Pioneering Ecosystem for Neuroscience Breakthroughs Digital Infrastructure for Brain Research Who we are EBRAINS is Europe’s digital infrastructure for brain research. It provides unique tools and data bringing together neurosc..."
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — No EOSC-referencing image asset was found in the markup. This is NOT proof of absence: a logo shown as a CSS background image, an SVG sprite reference, or a file named without "eosc" would all be missed by this check.
  - 51 image/SVG element(s) examined, none referencing EOSC
  - mentions of EOSC in page text: 0
  - NONE of the 9 approved name(s) for this node appear in the page body — note the <title> is not searched
  - *Reviewer action:* Look at the page (or its screenshot) and confirm whether an EOSC logo is visibly displayed.
- **4** 🔴 **FAIL** — No link to eosc.eu was found on the landing page.
  - 127 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-ebrains-ri/ but is not linked from here
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 127 outbound link(s) on the landing page
  - main text length: 4833 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟠 review — No pointer to an Acceptable Use Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 127 link(s) examined, none matching an Acceptable Use Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for an Acceptable Use Policy.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 127 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** 🟢 PASS — A support or helpdesk contact route is present.
  - "EBRAINS Support for EuroHPC Applications" -> https://ebrains.eu/data-tools-services/computing-infrastructure/ebrains-support-for-eurohpc-applications
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en"
  - detected language: en (confidence 1.0)
