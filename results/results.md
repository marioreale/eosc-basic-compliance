# EOSC Node Landing Page compliance — checklist v3.0

Run `live-2026-09-24-no-italy` · 2026-09-24T19:39:15+00:00 · 12 nodes · one page request per node plus 32 followed link(s) in total (depth 1).

> **This is not a compliance statement.** Points marked 🟠 review are ones this tool refuses to guess at: they either turn on a judgement ("clearly state") or quantify over things this tool does not enumerate ("all research resources").

**Node names.** 13 approved node name(s) were used, from the official list committed with the checklist (`checklist/approved-names.txt`, sha256 `871161a50fcb…`), as an unscoped list: a match shows the name appears on the page but not that it is that node's own name. Separator glyphs are treated as interchangeable, so a page writing “EOSC Node - X” satisfies a list writing “EOSC Node | X”.

> **Skipped by request.** eosc-it was left out of this run with --skip: not fetched, not assessed and not shown below. This table does not cover every configured node.

🟢 PASS — satisfied, with evidence · 🔴 **FAIL** — violated, with evidence · 🟠 review — a human must decide · 🟣 ERROR — could not be assessed

| Node | 1 | 1R | 2 | 3 | 4 | 5a | 5b | 5c | 6 | 7 |
|---|---|---|---|---|---|---|---|---|---|---|
| BBMRI-ERIC | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟠 review | 🟢 PASS | 🟢 PASS | 🟢 PASS |
| CERN | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟢 PASS |
| EOSC Node Czechia | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS |
| EOSC DTO (D4Science) | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| Data Terra | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS |
| EOSC Finland | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| PaNOSC | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS |
| EUDAT | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| EGI | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| GÉANT | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS |
| EBRAINS | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🔴 **FAIL** | 🟠 review | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS |
| EOSC Node Slovakia | 🟢 PASS | 🟠 review | 🟠 review | 🟠 review | 🟢 PASS | 🟠 review | 🟢 PASS | 🟢 PASS | 🟢 PASS | 🟢 PASS |

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
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the name found is this node's own — an approved name was found in the page body, but the list supplied is unscoped, so it does not say which node the name belongs to.
  - EOSC-referencing image asset(s): 1
  - img: eosc node - bbmri-eric logo
  - approved name matched from the unscoped list: "EOSC Node | BBMRI-ERIC" (the page writes it "EOSC Node - BBMRI-ERIC") — the list does not say which name belongs to which node, so this does not establish it is this node's own name
  - *Reviewer action:* Confirm the EOSC logo is visible without scrolling. Confirm the matched name is this node's own; the list supplied does not say.
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
<https://eosc-auth.cern.ch/login>

- **1** 🟠 review — HTTP 200 but only 127 characters rendered. The page may require JavaScript the tool did not execute, or may be a shell.
  - HTTP 200
  - text length: 127
  - *Reviewer action:* Open the page in a browser and confirm content is served anonymously.
- **1R** 🟠 review — Not assessable in full: it quantifies over every resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 1 distinct external host(s) linked from the landing page
  - cern.service-now.com (Contact Support, Privacy policy)
  - EOSC AAI indicators seen: myaccessid
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "Welcome to CERN-EOSC-NODE Sign in with EOSC Local credentials Not a member? Apply for an account Privacy policy Contact Support..."
  - no organisation-like names matched by pattern
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — No EOSC-referencing image asset was found in the markup. This is NOT proof of absence: a logo shown as a CSS background image, an SVG sprite reference, or a file named without "eosc" would all be missed by this check.
  - 0 image/SVG element(s) examined, none referencing EOSC
  - mentions of EOSC in page text: 2
  - NONE of the 13 approved name(s) for this node appear in the page body — note the <title> is not searched
  - *Reviewer action:* Look at the page (or its screenshot) and confirm whether an EOSC logo is visibly displayed.
- **4** 🟠 review — No link to eosc.eu was found, but the page yielded too little to conclude absence: the document is essentially empty (127 chars of text in total)
  - 6 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-cern/ but is not linked from here
  - *Reviewer action:* Open the page, dismiss any consent banner, and look for a link to the node's entry under eosc.eu/building-the-eosc-federation.
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 6 outbound link(s) on the landing page
  - main text length: 127 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟠 review — No pointer to an Acceptable Use Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 6 link(s) examined, none matching an Acceptable Use Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for an Acceptable Use Policy.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 6 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** 🟢 PASS — The landing page links to a route identified as a helpdesk or user support.
  - "Contact Support" -> https://cern.service-now.com/service-portal?id=functional_element&name=WLCG-IAM
  - *Reviewer action:* Confirm the route reaches the node's user support. A helpdesk behind a sign-in form is still a means of contact, but note it.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en_US"
  - detected language: en (confidence 0.97)

### EOSC Node Czechia
<https://www.eosc.cz/en/about-eosc-cz/eosc-node-czechia>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 3769 characters of text rendered
  - redirects followed: 2
- **1R** 🟠 review — Not assessable in full: it quantifies over every resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 4 distinct external host(s) linked from the landing page
  - bsky.app
  - www.linkedin.com (LinkedIn)
  - www.muni.cz (Masaryk University)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - meta description: "Through the Czech EOSC Node, European researchers can access computing resources, data, repositories, and secure AI and LLM tools through a single sign-on and a single point of access."
  - opening main text: "You are here: Home EOSC Node Czechia EOSC Node Czechia Through the Czech EOSC Node, European researchers can access computing resources, data, repositories, and secure AI and LLM tools through a single sign-on and a single point of access. What Is the EOSC Federation? The EOSC Federation enables researchers to access trustworthy and secure data, software, services and other digital resources acros..."
  - organisation-like names found: Masaryk University
  - about page one level down: https://www.eosc.cz/en/about-eosc-cz/contact (HTTP 200) opening text: "You are here: Home Contact Contact Contact for media Mgr. Bc. xxxxx correspondence Address: xxxxxx@ics.muni.cz phone: +420xxxxxxx General contacts Contact: info@eosc.cz EOSC CZ Training Centre: events@eosc.cz Correspondence address of the EOS..."
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — No EOSC-referencing image asset was found in the markup. This is NOT proof of absence: a logo shown as a CSS background image, an SVG sprite reference, or a file named without "eosc" would all be missed by this check.
  - 4 image/SVG element(s) examined, none referencing EOSC
  - mentions of EOSC in page text: 31
  - approved name matched from the unscoped list: "EOSC Node | Czechia" (the page writes it "EOSC Node Czechia") — the list does not say which name belongs to which node, so this does not establish it is this node's own name
  - *Reviewer action:* Look at the page (or its screenshot) and confirm whether an EOSC logo is visibly displayed.
- **4** 🟢 PASS — Links to a specific node entry under eosc.eu/building-the-eosc-federation.
  - "DETAILED DESCRIPTION OF EOSC NODE CZECHIA" -> https://eosc.eu/building-the-eosc-federation/eosc-node-czechia
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 73 outbound link(s) on the landing page
  - main text length: 2115 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟠 review — No pointer to an Acceptable Use Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 73 link(s) examined, none matching an Acceptable Use Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for an Acceptable Use Policy.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 73 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** 🟠 review — A contact page exists and offers a way to get in touch, but nothing on it identifies a helpdesk specifically. A link labelled "support" was found, but that word alone does not identify a helpdesk: it also labels funding programmes and service catalogues. The checklist asks for the node helpdesk, and general enquiries may not satisfy that.
  - "Contact" -> https://www.eosc.cz/en/about-eosc-cz/contact
  - "National Support" -> https://www.eosc.cz/en/projects/national-support
  - "Contact" -> https://www.eosc.cz/en/about-eosc-cz/contact
  - followed: https://www.eosc.cz/en/about-eosc-cz/contact -> HTTP 200
  - *Reviewer action:* Confirm whether any route reaches the node's user support, not a general mailbox or an unrelated service.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en"
  - detected language: en (confidence 1.0)

### EOSC DTO (D4Science)
<https://eosc-dto.d4science.org/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 12319 characters of text rendered
- **1R** 🟠 review — Not assessable in full: it quantifies over every resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 5 distinct external host(s) linked from the landing page
  - doi.org (EOSC-Marine project)
  - ec.europa.eu (EU H2020 programme)
  - support.d4science.org (Helpdesk, Open a Node helpdesk request)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "A thematic node of the European Open Science Cloud EOSC Node | European Digital Twin Ocean Federating marine data, research environments, analytical services and computing resources for collaborative, FAIR and reproducible ocean science. Sign in with EOSC AAI Explore Resource Catalogue Explore Services Explore Research Environments This Node Landing Page is publicly accessible without login. Prote..."
  - organisation-like names found: AUP Consortium; CNR; CNR CNR; ERIC; European Research Executive Agency; OGS HCMR EMSO-ERIC ETT University
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
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 57 outbound link(s) on the landing page
  - main text length: 12097 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟢 PASS — The landing page links to an Acceptable Use Policy, and the target was fetched and reads like a policy document.
  - "D4Science Access and Acceptable Use Policy" -> https://www.d4science.org/policies/access-and-acceptable-use
  - "AUP" -> https://www.d4science.org/policies/access-and-acceptable-use
  - followed: https://www.d4science.org/policies/access-and-acceptable-use -> HTTP 200, 5461 chars, title: Access and Acceptable Use Policy | D4Science
  - policy wording found: Policy, Responsib, authorized, comply
  - *Reviewer action:* Confirm it covers all the node's resources and is in English.
- **5c** 🟠 review — A user access policy is mentioned in the page text but not as a followable link.
  - text mentions: Access Polic, UAP, User Access Polic
  - *Reviewer action:* Find where a User Access Policy is actually published and confirm it is reachable.
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
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — it was looked for and not found in the page body, which is not proof of absence, since the <title> is not searched.
  - EOSC-referencing image asset(s): 1
  - img: eosc node data terra environment
  - NONE of the 13 approved name(s) for this node appear in the page body — the phrase "EOSC Node" does occur 3 times, but never followed by an approved name — note the <title> is not searched
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
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — it was looked for and not found in the page body, which is not proof of absence, since the <title> is not searched.
  - EOSC-referencing image asset(s): 1
  - img: EOSCNode_Finland-1-1-scaled.jpg
  - NONE of the 13 approved name(s) for this node appear in the page body — note the <title> is not searched
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
  - "Prerequisites and responsibilities for a CSC project manager" -> https://research.csc.fi/terms-of-use/prerequisites-for-a-project-manager/
  - followed: https://research.csc.fi/terms-of-use/ -> HTTP 200, 16560 chars, title: Terms of use - Services for Research
  - policy wording found: Terms, comply, conditions, permitted
  - *Reviewer action:* Confirm it covers all the node's resources and is in English.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 85 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
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
- **1R** 🟠 review — Not assessable in full: it quantifies over every resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML. One level of crawling narrows this but cannot close it.
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
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 123 outbound link(s) on the landing page
  - main text length: 7846 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟠 review — No pointer to an Acceptable Use Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 123 link(s) examined, none matching an Acceptable Use Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for an Acceptable Use Policy.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 123 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
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
- **1R** 🟠 review — Not assessable in full: it quantifies over every resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML. One level of crawling narrows this but cannot close it.
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
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 11 outbound link(s) on the landing page
  - main text length: 742 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟢 PASS — The landing page links to an Acceptable Use Policy, and the target was fetched and reads like a policy document.
  - "EUDAT AUP" -> https://www.eudat.eu/eudat-cdi-aup
  - followed: https://www.eudat.eu/eudat-cdi-aup -> HTTP 200, 3101 chars, title: EUDAT CDI Acceptable Use Policy and Conditions of Use | EUDAT
  - policy wording found: Conditions, You shall, permitted, policy
  - *Reviewer action:* Confirm it covers all the node's resources and is in English.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 11 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
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
  - NONE of the 13 approved name(s) for this node appear in the page body — note the <title> is not searched
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

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 9805 characters of text rendered
  - redirects followed: 1
- **1R** 🟠 review — Not assessable in full: it quantifies over every resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML. One level of crawling narrows this but cannot close it.
  - 27 distinct external host(s) linked from the landing page
  - careers.geant.org (Careers)
  - clouds.geant.org (About the GÉANT Cloud Frameworks, Above-the-Net Services Incubator, Clouds)
  - community.geant.org (Community Award, Community Programme, GÉANT Community)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** 🟠 review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - meta description: "The GÉANT EOSC Node provides trusted digital infrastructure that enables researchers across Europe to discover, access and use research resources seamlessly."
  - opening main text: "Home . Projects . GÉANT EOSC Node GÉANT EOSC Node The GÉANT EOSC Node is GÉANT's contribution to the EOSC Federation, providing trusted digital infrastructure that enables researchers across Europe to discover, access and use research resources seamlessly. GÉANT Service Catalogue The catalogue provides an overview of the GÉANT services onboarded into the EOSC Federation. GÉANT Node Acceptable Use ..."
  - organisation-like names found: Association; Security Operations Centre
  - about page one level down: https://geant.org/contact (HTTP 200) opening text: "Home . Contact Contact Get in touch, learn more or request support. GDPR For questions related to our Privacy Notice and how GÉANT processes your personal data. Contact us General enquiries Submit a general enquiry, and we will put you in contact with the appr..."
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** 🟠 review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the name found is this node's own — an approved name was found in the page body, but the list supplied is unscoped, so it does not say which node the name belongs to.
  - EOSC-referencing image asset(s): 1
  - img: EOSCNode-GEANT-300x59.jpg
  - approved name matched from the unscoped list: "EOSC Node | GÉANT" (the page writes it "EOSC Node GÉANT") — the list does not say which name belongs to which node, so this does not establish it is this node's own name
  - *Reviewer action:* Confirm the EOSC logo is visible without scrolling. Confirm the matched name is this node's own; the list supplied does not say.
- **4** 🔴 **FAIL** — Links only to the building-the-eosc-federation index, which the checklist explicitly excludes. The node's own dedicated entry is required.
  - "An evolving European federation enabling researchers to discover, access, share and reuse data and resources." -> https://eosc.eu/building-the-eosc-federation
  - "A ‘system of systems’ to find and access data and services for research and innovation in Europe." -> https://eosc.eu/building-the-eosc-federation
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-geant/ but is not linked from here
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 124 outbound link(s) on the landing page
  - main text length: 6097 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟢 PASS — The landing page links to what appears to be an Acceptable Use Policy. The link target was not fetched (it was not selected when this evidence was collected), so this is a pointer, not a verified document.
  - "This policy defines the rules that govern your access to and use of the resources and services of the “GÉANT Node”." -> https://geant.org/projects/geant-eosc-node/geant-node-acceptable-use-policy/
  - *Reviewer action:* Open the link and confirm the target really is an Acceptable Use Policy, in English. Collecting the evidence again would fetch it.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 124 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** 🟢 PASS — A page reached from the landing page identifies a helpdesk or user support route.
  - "Contact" -> https://geant.org/contact
  - "Contact To find out more about the GÉANT EOSC Node get in touch via the contact form." -> https://geant.org/contact/
  - followed: https://geant.org/contact -> HTTP 200
  - helpdesk wording on that page: helpdesk
  - *Reviewer action:* Confirm the route reaches the node's user support.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en-US"
  - detected language: en (confidence 1.0)

### EBRAINS
<https://ebrains.eu/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 6641 characters of text rendered
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
  - NONE of the 13 approved name(s) for this node appear in the page body — note the <title> is not searched
  - *Reviewer action:* Look at the page (or its screenshot) and confirm whether an EOSC logo is visibly displayed.
- **4** 🔴 **FAIL** — No link to eosc.eu was found on the landing page.
  - 127 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-ebrains-ri/ but is not linked from here
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 127 outbound link(s) on the landing page
  - main text length: 4781 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟠 review — No pointer to an Acceptable Use Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 127 link(s) examined, none matching an Acceptable Use Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for an Acceptable Use Policy.
- **5c** 🟠 review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 127 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** 🟠 review — A contact page exists and offers a way to get in touch, but nothing on it identifies a helpdesk specifically. A link labelled "support" was found, but that word alone does not identify a helpdesk: it also labels funding programmes and service catalogues. The checklist asks for the node helpdesk, and general enquiries may not satisfy that.
  - "EBRAINS Support for EuroHPC Applications" -> https://ebrains.eu/data-tools-services/computing-infrastructure/ebrains-support-for-eurohpc-applications
  - "Media Contact" -> https://ebrains.eu/news-events/media/media-contact
  - "Contact Us" -> https://ebrains.eu/contact
  - followed: https://ebrains.eu/data-tools-services/computing-infrastructure/ebrains-support-for-eurohpc-applications -> HTTP 200
  - *Reviewer action:* Confirm whether any route reaches the node's user support, not a general mailbox or an unrelated service.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en"
  - detected language: en (confidence 1.0)

### EOSC Node Slovakia
<https://eosc.sk/>

- **1** 🟢 PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 8448 characters of text rendered
- **1R** 🟠 review — Not assessable in full: it quantifies over every resource reachable through the landing page, including through intermediate pages, and whether a given login is genuinely EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML. One level of crawling narrows this but cannot close it.
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
- **5a** 🟠 review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 45 outbound link(s) on the landing page
  - main text length: 8448 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** 🟢 PASS — The landing page links to what appears to be an Acceptable Use Policy. The link target was not fetched (it is a PDF document, which the tool does not download or read), so this is a pointer, not a verified document.
  - "Terms of Use (incl. AUP and UAP)" -> https://eosc.sk/docs/eosc_sk_tou.pdf
  - *Reviewer action:* Open the PDF and confirm it is an Acceptable Use Policy, in English. No --depth setting will fetch it.
- **5c** 🟢 PASS — The landing page links to what appears to be a User Access Policy. The link target was not fetched (it is a PDF document, which the tool does not download or read), so this is a pointer, not a verified document.
  - "Terms of Use (incl. AUP and UAP)" -> https://eosc.sk/docs/eosc_sk_tou.pdf
  - *Reviewer action:* Open the PDF and confirm it is a User Access Policy, in English. No --depth setting will fetch it.
- **6** 🟢 PASS — The landing page links to a route identified as a helpdesk or user support.
  - "Open helpdesk" -> https://hd.eosc.sk
  - "HELPDESK" -> https://hd.eosc.sk
  - *Reviewer action:* Confirm the route reaches the node's user support. A helpdesk behind a sign-in form is still a means of contact, but note it.
- **7** 🟢 PASS — The main content is English and the page declares English.
  - declared lang attribute: "en"
  - detected language: en (confidence 1.0)
