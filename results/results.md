# EOSC Node Landing Page compliance — checklist v3.0

Run `2026-09-17-1458` · 2026-09-17T14:58:24+00:00 · 9 nodes · one page request per node, no crawling.

> **This is not a compliance statement.** Points marked `review` are ones this tool refuses to guess at: they either turn on a judgement ("clearly state") or quantify over things a single page request cannot see ("all research resources").

| Node | 1 | 1R | 2 | 3 | 4 | 5a | 5b | 5c | 6 | 7 |
|---|---|---|---|---|---|---|---|---|---|---|
| BBMRI-ERIC | PASS | review | review | review | PASS | review | review | PASS | PASS | PASS |
| EOSC DTO (D4Science) | PASS | review | review | review | review | review | PASS | review | review | PASS |
| Data Terra | PASS | review | review | review | **FAIL** | review | review | review | review | PASS |
| EOSC Finland | PASS | review | review | review | **FAIL** | review | PASS | review | PASS | PASS |
| PaNOSC | PASS | review | review | review | **FAIL** | review | review | review | review | PASS |
| EUDAT | PASS | review | review | review | review | review | PASS | review | review | PASS |
| EGI | PASS | review | review | review | **FAIL** | review | PASS | review | review | PASS |
| GÉANT | PASS | review | review | review | **FAIL** | review | review | review | review | PASS |
| EBRAINS | PASS | review | review | review | **FAIL** | review | review | review | PASS | PASS |

## Points

**1 — NLP is publicly accessible, or reachable via EOSC AAI login** (decidable by inspection)  
The Node Landing Page must either be (a) publicly accessible (anonymously, i.e. without the need for users to login) or (b) accessible via login through EOSC AAI.

**1R — Resources pointed to by the NLP are public or behind EOSC AAI** (needs a human)  
All resources pointed by the Node Landing Page, thus exposed to EOSC users, either directly or through links through intermediate pages, must either be publicly accessible or accessible via login through EOSC AAI.

**2 — Scope, intended users and responsible organization are stated** (needs a human)  
Clearly state the Node's scope, intended users and responsible organization. (It is up to the Node to feature all the organisations involved).

**3 — EOSC logo and official Tripartite-approved node name are visible** (partly decidable)  
Clearly and visibly show the EOSC logo and the official Tripartite-approved name of the Node.

**4 — Link to the node's own dedicated page on eosc.eu** (decidable by inspection)  
Provide a link to the Node's own dedicated page on the eosc.eu website — the Node's entry under eosc.eu/building-the-eosc-federation, not the eosc.eu homepage or the index page itself.

**5a — Purpose description accessible in English for research resources** (needs a human)  
For all research resources offered by the Node to EOSC users, a purpose description must be accessible in English either directly or via the link to the resource's entry in the EOSC Catalogue.

**5b — Acceptable Use Policy (AUP) accessible for research resources** (partly decidable)  
For all research resources offered by the Node, the Acceptable Use Policy (AUP) must be accessible in English either directly or via the resource's entry in the EOSC Catalogue.

**5c — User Access Policy (UAP) accessible for research resources** (partly decidable)  
For all research resources offered by the Node, the User Access Policy (UAP) must be accessible in English either directly or via the resource's entry in the EOSC Catalogue.

**6 — Means of contacting the node helpdesk** (partly decidable)  
Provide means of contacting the Node helpdesk.

**7 — The page is in English** (decidable by inspection)  
Be in English (Any other pages and information are not required to be strictly in English).

## Detail

### BBMRI-ERIC
<https://www.bbmri-eric.eu/eosc-node-bbmri-eric/>

- **1** PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 7100 characters of text rendered
- **1R** review — Not assessable without following every resource link and confirming each login is EOSC AAI. This tool makes one request per node by design, and AAI compliance is verified during EEN enrolment rather than by reading a page.
  - 6 distinct external host(s) linked from the landing page
  - directory.bbmri-eric.eu (Directory)
  - negotiator.bbmri-eric.eu (Negotiator)
  - open-science-cloud.ec.europa.eu (European Open Science Cloud (EOSC))
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "­ EOSC Node - BBMRI-ERIC - BBMRI-ERIC Fonts A A Contrast A A Newsletter sign-up I give permission for BBMRI-ERIC to send me their newsletter and emails about subjects which they think may be of interest to me. I can unsubscribe from all emails at any time. I understand that my information will be processed according to BBMRI-ERIC's privacy notice . Leave this field empty if you're human: FAQ Downl..."
  - organisation-like names found: CSC; EOSC4CANCER EPND EPPerMed ERDERA ERIC; ERIC; European Research Infrastructure Consortium
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — the tool has no authoritative list of approved names.
  - EOSC-referencing image asset(s): 1
  - img: eosc node - bbmri-eric logo
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** PASS — Links to a specific node entry under eosc.eu/building-the-eosc-federation.
  - "See the dedicated page on the EOSC website" -> https://eosc.eu/building-the-eosc-federation/eosc-node-bbmri-eric/
- **5a** review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 84 outbound link(s) on the landing page
  - main text length: 7100 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** review — An acceptable use policy is mentioned in the page text but not as a followable link.
  - text mentions: AUP
  - *Reviewer action:* Find where an Acceptable Use Policy is actually published and confirm it is reachable.
- **5c** PASS — The landing page links to what appears to be a User Access Policy.
  - "Access Policies" -> https://www.bbmri-eric.eu/services/access-policies/
  - *Reviewer action:* Confirm the target really is a User Access Policy, is in English, and covers all the node's resources.
- **6** PASS — A support or helpdesk contact route is present.
  - "Services & Support" -> https://www.bbmri-eric.eu/services-support/
- **7** PASS — The main content is English and the page declares English.
  - declared lang attribute: "en-GB"
  - detected language: en (confidence 1.0)

### EOSC DTO (D4Science)
<https://eosc-dto.d4science.org/>

- **1** PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 4328 characters of text rendered
- **1R** review — Not assessable without following every resource link and confirming each login is EOSC AAI. This tool makes one request per node by design, and AAI compliance is verified during EEN enrolment rather than by reading a page.
  - 5 distinct external host(s) linked from the landing page
  - eosc-dto.d4science.org:443 (European-DTO Gateway)
  - open-science-cloud.ec.europa.eu (EOSC)
  - research-and-innovation.ec.europa.eu (HEU programme)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "EOSC Node | European Digital Twin Ocean This EOSC Thematic Node originated from the Blue-Cloud initiative, which de-facto piloted a marine thematic node to advance high-quality marine science Sign In Register Welcome! Access the rich world of this EOSC thematic node via the user-friendly D4Science platform . If you already have an account, simply sign in using your existing credentials, including ..."
  - no organisation-like names matched by pattern
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — the tool has no authoritative list of approved names.
  - EOSC-referencing image asset(s): 8
  - img: European-DTO Gateway
  - img: Page Icon
  - img: Page Icon
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** review — No link to eosc.eu was found, but the page did not fully render, so absence cannot be concluded: a cookie-consent overlay dominates the captured text (main text only 530 chars; markers: Accept All, Reject All, This website uses cookies); only 20 links captured, low for a landing page; only 530 characters of main text captured
  - 20 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-digital-twin-of-the-ocean/ but is not linked from here
  - *Reviewer action:* Open the page, dismiss any consent banner, and look for a link to the node's entry under eosc.eu/building-the-eosc-federation.
- **5a** review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 20 outbound link(s) on the landing page
  - main text length: 530 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** PASS — The landing page links to what appears to be an Acceptable Use Policy.
  - "Terms of Use" -> https://eosc-dto.d4science.org/terms-of-use
  - *Reviewer action:* Confirm the target really is an Acceptable Use Policy, is in English, and covers all the node's resources.
- **5c** review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 20 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** review — No contact route was found, but the page did not fully render, so absence cannot be concluded: a cookie-consent overlay dominates the captured text (main text only 530 chars; markers: Accept All, Reject All, This website uses cookies); only 20 links captured, low for a landing page; only 530 characters of main text captured
  - 20 link(s) examined
  - *Reviewer action:* Open the page, dismiss any consent banner, and look for a helpdesk or support contact.
- **7** PASS — The main content is English and the page declares English.
  - declared lang attribute: "en-US"
  - detected language: en (confidence 1.0)

### Data Terra
<https://www.data-terra.org/eosc/>

- **1** PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 19620 characters of text rendered
- **1R** review — Not assessable without following every resource link and confirming each login is EOSC AAI. This tool makes one request per node by design, and AAI compliance is verified during EEN enrolment rather than by reading a page.
  - 38 distinct external host(s) linked from the landing page
  - cnes.fr
  - fr.linkedin.com
  - intranet.data-terra.org
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "Accueil The EOSC Node f... The EOSC Node for the Earth system and environmental sciences (under construction) The EOSC node’s digital gateway plays a crucial role in connecting research organizations to the broader European ecosystem. It serves as a single-entry point to the European Open Science Cloud (EOSC), facilitating access to open science resources and services across Europe. The DATA TERRA..."
  - no organisation-like names matched by pattern
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — the tool has no authoritative list of approved names.
  - EOSC-referencing image asset(s): 1
  - img: eosc node data terra environment
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** **FAIL** — No link to eosc.eu was found on the landing page.
  - 93 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-data-terra/ but is not linked from here
- **5a** review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 93 outbound link(s) on the landing page
  - main text length: 5739 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** review — No pointer to an Acceptable Use Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 93 link(s) examined, none matching an Acceptable Use Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for an Acceptable Use Policy.
- **5c** review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 93 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** review — A contact route exists, but nothing identifies it as a helpdesk. The checklist asks specifically for the node helpdesk, and a general enquiries or press address does not obviously satisfy that.
  - "Contact & accès" -> https://www.data-terra.org/contact-acces/
  - "Contact & accès" -> https://www.data-terra.org/contact-acces/
  - *Reviewer action:* Confirm this contact route reaches the node's user support, not a general mailbox.
- **7** PASS — The main content is English. The page declares "fr-FR", which is a metadata inconsistency worth fixing but does not breach point 7.
  - declared lang attribute: "fr-FR"
  - detected language: en (confidence 1.0)
  - *Reviewer action:* Suggest the node correct its lang attribute.

### EOSC Finland
<https://eosc.fi/>

- **1** PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 3329 characters of text rendered
  - redirects followed: 1
- **1R** review — Not assessable without following every resource link and confirming each login is EOSC AAI. This tool makes one request per node by design, and AAI compliance is verified during EEN enrolment rather than by reading a page.
  - 10 distinct external host(s) linked from the landing page
  - csc.fi (Detailed contact information (External link), Directions (External link), Main website – csc.fi (External link))
  - docs.csc.fi (Applications catalogue (External link), Docs CSC - User guides (External link), User guides (External link))
  - etsin.fairdata.fi (Etsin (External link))
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "EOSC Finland Pilot Node Dataset-as-a-Service EOSC Finland - Tools for service providers and data managers EOSC Finland for researchers More about the EOSC Federation and the Finnish Pilot Node MyAccessID - a new way to access CSC services Discover services Browse services in the EOSC federation available for researchers with a Finnish affiliation or project. Service catalogue Start using services ..."
  - organisation-like names found: Browse CSC; CSC; Copyright CSC; Docs CSC; Espoo Life Science Center; IT Center
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — the tool has no authoritative list of approved names.
  - EOSC-referencing image asset(s): 1
  - img: EOSCNode_Finland-1-1-scaled.jpg
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** **FAIL** — No link to eosc.eu was found on the landing page.
  - 85 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-finland/ but is not linked from here
- **5a** review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 85 outbound link(s) on the landing page
  - main text length: 823 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** PASS — The landing page links to what appears to be an Acceptable Use Policy.
  - "Terms of use" -> https://research.csc.fi/terms-of-use/
  - *Reviewer action:* Confirm the target really is an Acceptable Use Policy, is in English, and covers all the node's resources.
- **5c** review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 85 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** PASS — A support or helpdesk contact route is present.
  - "Service Desk" -> https://research.csc.fi/support
  - "Service Desk" -> https://research.csc.fi/support
- **7** PASS — The main content is English and the page declares English.
  - declared lang attribute: "en-US"
  - detected language: en (confidence 1.0)

### PaNOSC
<https://eosc.panosc.eu/>

- **1** PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 7714 characters of text rendered
  - redirects followed: 2
- **1R** review — Not assessable without following every resource link and confirming each login is EOSC AAI. This tool makes one request per node by design, and AAI compliance is verified during EEN enrolment rather than by reading a page.
  - 37 distinct external host(s) linked from the landing page
  - aiidalab-qe.readthedocs.io (AiiDAlab Quantum ESPRESSO (QE) app)
  - api.whatsapp.com
  - archive.materialscloud.org (Materials Cloud Archive)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "Menu About About PaNOSC Node PaNOSC project (2018-2022) European Research Infrastructures FAIR Principles Contact Science Cluster About Members Services Photon and Neutron Competence Centre PaNOSC data policy framework PaN OSCARS funded projects PaNOSC Node About Services Training Project (2018-2022) Services Data E-learning platform Use Cases Video Women in science Materials Branding Material Pub..."
  - organisation-like names found: EOSC Association; Institut; Lund University; Neutron Competence Centre; Paul Scherrer Institute
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — the tool has no authoritative list of approved names.
  - EOSC-referencing image asset(s): 3
  - img: EOSCNodePaNOSC_ColourPos-scaled.png
  - img: EOSC-Federation-logo.png
  - img: European Open Science Cloud
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** **FAIL** — Links only to the building-the-eosc-federation index, which the checklist explicitly excludes. The node's own dedicated entry is required.
  - "Building the EOSC Federation" -> https://eosc.eu/eosc-about/building-the-eosc-federation/
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-panosc/ but is not linked from here
- **5a** review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 118 outbound link(s) on the landing page
  - main text length: 7714 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** review — No pointer to an Acceptable Use Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 118 link(s) examined, none matching an Acceptable Use Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for an Acceptable Use Policy.
- **5c** review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 118 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** review — A contact route exists, but nothing identifies it as a helpdesk. The checklist asks specifically for the node helpdesk, and a general enquiries or press address does not obviously satisfy that.
  - "Contact" -> https://www.panosc.eu/contact/
  - "Contact us" -> https://www.panosc.eu/contact/
  - "Contact" -> https://www.panosc.eu/contact/
  - *Reviewer action:* Confirm this contact route reaches the node's user support, not a general mailbox.
- **7** PASS — The main content is English and the page declares English.
  - declared lang attribute: "en-GB"
  - detected language: en (confidence 1.0)

### EUDAT
<https://portal.eudat.eu/>

- **1** PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 932 characters of text rendered
  - redirects followed: 1
- **1R** review — Not assessable without following every resource link and confirming each login is EOSC AAI. This tool makes one request per node by design, and AAI compliance is verified during EEN enrolment rather than by reading a page.
  - 3 distinct external host(s) linked from the landing page
  - docs.eudat.eu (Set up your workspace Read about the first steps in becoming an EUDAT Node user., User Guides Browse guides on how to best use the EUDAT Node for your research.)
  - eudat.eu (Discover services Browse services offered by EUDAT and the EOSC Federation., Meet the EUDAT Community Learn who the main users of EUDAT Services are and about their experiences.)
  - www.eudat.eu (Accessibility Statement, EUDAT AUP, FAQs)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "EOSC Node Marketplace Welcome to the EUDAT Portal Find information about EUDAT Services and how to best utilise the EUDAT Node workspace, a platform built for better research and limitless science. Uncertain where to start? Discover services Browse services offered by EUDAT and the EOSC Federation. Set up your workspace Read about the first steps in becoming an EUDAT Node user. User Guides Browse ..."
  - organisation-like names found: EUDAT Ltd
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — the tool has no authoritative list of approved names.
  - EOSC-referencing image asset(s): 2
  - img: EOSC Node
  - img: EOSC Node
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** review — No link to eosc.eu was found, but the page did not fully render, so absence cannot be concluded: only 10 links captured, low for a landing page; only 560 characters of main text captured
  - 10 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-eudat/ but is not linked from here
  - *Reviewer action:* Open the page, dismiss any consent banner, and look for a link to the node's entry under eosc.eu/building-the-eosc-federation.
- **5a** review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 10 outbound link(s) on the landing page
  - main text length: 560 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** PASS — The landing page links to what appears to be an Acceptable Use Policy.
  - "EUDAT AUP" -> https://www.eudat.eu/eudat-cdi-aup
  - *Reviewer action:* Confirm the target really is an Acceptable Use Policy, is in English, and covers all the node's resources.
- **5c** review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 10 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** review — A contact route exists, but nothing identifies it as a helpdesk. The checklist asks specifically for the node helpdesk, and a general enquiries or press address does not obviously satisfy that.
  - "info@eudat.eu" -> mailto:info@eudat.eu
  - *Reviewer action:* Confirm this contact route reaches the node's user support, not a general mailbox.
- **7** PASS — The main content is English and the page declares English.
  - declared lang attribute: "en"
  - detected language: en (confidence 1.0)

### EGI
<https://www.egi.eu/egi-node>

- **1** PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 6638 characters of text rendered
- **1R** review — Not assessable without following every resource link and confirming each login is EOSC AAI. This tool makes one request per node by design, and AAI compliance is verified during EEN enrolment rather than by reading a page.
  - 5 distinct external host(s) linked from the landing page
  - bsky.app
  - github.com
  - www.linkedin.com
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - opening main text: "EGI for EOSC EGI Node Operated by the EGI Foundation on behalf of the EGI Federation, the Node provides scalable compute, storage, data management and advanced digital research services for data-intensive science. It delivers EOSC Core and Federating Capabilities including AAI, catalogue, monitoring, accounting, helpdesk and application deployment management, while supporting multi-node use cases ..."
  - organisation-like names found: About About Us EGI Foundation; About EGI Foundation; EGI Digital Innovation Hub Foundation; EGI Foundation; EGI Infrastructure EGI Community Foundation
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** review — No EOSC-referencing image asset was found in the markup. This is NOT proof of absence: a logo shown as a CSS background image, an SVG sprite reference, or a file named without "eosc" would all be missed by this check.
  - 40 image/SVG element(s) examined, none referencing EOSC
  - mentions of EOSC in page text: 23
  - *Reviewer action:* Look at the page (or its screenshot) and confirm whether an EOSC logo is visibly displayed.
- **4** **FAIL** — No link to eosc.eu was found on the landing page.
  - 167 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-egi/ but is not linked from here
- **5a** review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 167 outbound link(s) on the landing page
  - main text length: 4451 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** PASS — The landing page links to what appears to be an Acceptable Use Policy.
  - "terms of use" -> https://www.egi.eu/terms-of-use/
  - *Reviewer action:* Confirm the target really is an Acceptable Use Policy, is in English, and covers all the node's resources.
- **5c** review — A user access policy is mentioned in the page text but not as a followable link.
  - text mentions: Access Polic
  - *Reviewer action:* Find where a User Access Policy is actually published and confirm it is reachable.
- **6** review — A contact route exists, but nothing identifies it as a helpdesk. The checklist asks specifically for the node helpdesk, and a general enquiries or press address does not obviously satisfy that.
  - "Contact Us" -> https://www.egi.eu/contact-us/
  - "Contact Us" -> https://www.egi.eu/contact-us/
  - "Contact us" -> https://www.egi.eu/contact-us/
  - "(no label)" -> mailto:contact@egi.eu
  - *Reviewer action:* Confirm this contact route reaches the node's user support, not a general mailbox.
- **7** PASS — The main content is English and the page declares English.
  - declared lang attribute: "en"
  - detected language: en (confidence 1.0)

### GÉANT
<https://geant.org/geant-eosc-node/>

- **1** PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 9549 characters of text rendered
  - redirects followed: 1
- **1R** review — Not assessable without following every resource link and confirming each login is EOSC AAI. This tool makes one request per node by design, and AAI compliance is verified during EEN enrolment rather than by reading a page.
  - 27 distinct external host(s) linked from the landing page
  - careers.geant.org (Careers)
  - clouds.geant.org (About the GÉANT Cloud Frameworks, Above-the-Net Services Incubator, Clouds)
  - community.geant.org (Community Award, Community Programme, GÉANT Community)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - meta description: "The GÉANT EOSC Node provides trusted digital infrastructure that enables researchers across Europe to discover, access and use research resources seamlessly."
  - opening main text: "Home . Projects . GÉANT EOSC Node GÉANT EOSC Node The GÉANT EOSC Node is GÉANT's contribution to the EOSC Federation, providing trusted digital infrastructure that enables researchers across Europe to discover, access and use research resources seamlessly. GÉANT Service Catalogue The catalogue provides an overview of the GÉANT services onboarded into the EOSC Federation. EOSC Federation An evolvin..."
  - organisation-like names found: Association; Security Operations Centre
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** review — An EOSC-referencing image asset is present, so the logo requirement is likely met. Two things remain human judgements: whether it is "clearly and visibly" shown, and whether the node name on the page is the official Tripartite-approved one — the tool has no authoritative list of approved names.
  - EOSC-referencing image asset(s): 1
  - img: EOSCNode-GEANT-300x59.jpg
  - *Reviewer action:* Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.
- **4** **FAIL** — Links only to the building-the-eosc-federation index, which the checklist explicitly excludes. The node's own dedicated entry is required.
  - "An evolving European federation enabling researchers to discover, access, share and reuse data and resources." -> https://eosc.eu/building-the-eosc-federation
  - "A ‘system of systems’ to find and access data and services for research and innovation in Europe." -> https://eosc.eu/building-the-eosc-federation
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-geant/ but is not linked from here
- **5a** review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 122 outbound link(s) on the landing page
  - main text length: 5841 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** review — No pointer to an Acceptable Use Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 122 link(s) examined, none matching an Acceptable Use Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for an Acceptable Use Policy.
- **5c** review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 122 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** review — A contact route exists, but nothing identifies it as a helpdesk. The checklist asks specifically for the node helpdesk, and a general enquiries or press address does not obviously satisfy that.
  - "Contact" -> https://geant.org/contact
  - "Contact To find out more about the GÉANT EOSC Node get in touch via the contact form." -> https://geant.org/contact/
  - "Contact" -> https://geant.org/contact
  - *Reviewer action:* Confirm this contact route reaches the node's user support, not a general mailbox.
- **7** PASS — The main content is English and the page declares English.
  - declared lang attribute: "en-US"
  - detected language: en (confidence 1.0)

### EBRAINS
<https://ebrains.eu/>

- **1** PASS — Served content to an anonymous request, satisfying branch (a).
  - HTTP 200 anonymously, 6693 characters of text rendered
- **1R** review — Not assessable without following every resource link and confirming each login is EOSC AAI. This tool makes one request per node by design, and AAI compliance is verified during EEN enrolment rather than by reading a page.
  - 5 distinct external host(s) linked from the landing page
  - bsky.app (Bluesky)
  - mastodon.social (Mastodon)
  - www.linkedin.com (LinkedIn)
  - *Reviewer action:* Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.
- **2** review — Requires reading the page: "clearly state" is a judgement about whether the prose conveys scope, intended users, and the responsible organisation to a researcher. Evidence is extracted below so the decision is quick.
  - meta description: "An open research infrastructure that provides data, tools and services for brain-related research – from the molecular and cellular levels to the whole organ."
  - opening main text: "Built for Brain Breakthroughs Europe's Digital Infrastructure for Brain Research Explore data, tools and services EBRAINS RI EBRAINS is an open research infrastructure (RI) that provides data, tools and services for brain-related research – from the molecular and cellular levels to the whole organ. The EBRAINS infrastructure was originally built by the EU-funded Human Brain Project and is now adva..."
  - organisation-like names found: University
  - *Reviewer action:* Read the extracted text and confirm all three elements are present and clear.
- **3** review — No EOSC-referencing image asset was found in the markup. This is NOT proof of absence: a logo shown as a CSS background image, an SVG sprite reference, or a file named without "eosc" would all be missed by this check.
  - 51 image/SVG element(s) examined, none referencing EOSC
  - mentions of EOSC in page text: 0
  - *Reviewer action:* Look at the page (or its screenshot) and confirm whether an EOSC logo is visibly displayed.
- **4** **FAIL** — No link to eosc.eu was found on the landing page.
  - 127 link(s) examined, none pointing to eosc.eu
  - the node's dedicated page exists at https://eosc.eu/building-the-eosc-federation/eosc-node-ebrains-ri/ but is not linked from here
- **5a** review — Quantifies over "all research resources offered by the Node", which cannot be enumerated from the landing page alone. The checklist also allows the description to live in the resource's EOSC Catalogue entry rather than on this page.
  - 127 outbound link(s) on the landing page
  - main text length: 4833 characters
  - *Reviewer action:* List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.
- **5b** review — No pointer to an Acceptable Use Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 127 link(s) examined, none matching an Acceptable Use Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for an Acceptable Use Policy.
- **5c** review — No pointer to a User Access Policy was found on the landing page. This is deliberately not a FAIL: the checklist permits the policy to be reached via each resource's entry in the EOSC Catalogue, which this tool does not follow.
  - 127 link(s) examined, none matching a User Access Policy
  - *Reviewer action:* Check the node's resource entries in the EOSC Catalogue for a User Access Policy.
- **6** PASS — A support or helpdesk contact route is present.
  - "EBRAINS Support for EuroHPC Applications" -> https://ebrains.eu/data-tools-services/computing-infrastructure/ebrains-support-for-eurohpc-applications
- **7** PASS — The main content is English and the page declares English.
  - declared lang attribute: "en"
  - detected language: en (confidence 1.0)
