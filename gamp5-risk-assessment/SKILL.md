---
name: gamp5-risk-assessment
description: >
  Generates a professional, GMP-compliant FMEA-based Quality Risk Assessment document
  as a formatted Word (.docx) file, fully aligned with ISPE GAMP 5 Second Edition (2022),
  ICH Q9, and EU Annex 11. Covers all GAMP software categories (Cat 1, 3, 4, 5) and
  hardware types including LIMS, ERP, SCADA, MES, equipment/instruments, and custom
  in-house software. Use this skill whenever the user asks for a risk assessment, QRM,
  FMEA, functional risk assessment, GxP risk document, GAMP risk form, preliminary risk
  assessment, or system impact assessment — even if phrased casually like "do a risk
  assessment for my LIMS" or "help me assess risk for this system". Always trigger for
  any pharma or GxP context involving computerized system risk, compliance, or validation.
---

# GAMP 5 Second Edition — Quality Risk Assessment Skill

Generates a professional Word (.docx) FMEA-based risk assessment document aligned to
ISPE GAMP 5 Second Edition (2022), ICH Q9, and EU Annex 11.

---

## What This Skill Produces

A structured `.docx` risk assessment document containing:
- Document header (title, system name, version, date, author, approver fields)
- System overview section
- GxP determination and system impact rating
- GAMP software category classification
- Functional FMEA risk table (the core deliverable)
- Risk summary and residual risk statement
- Signature / approval block

---

## Step 1 — Gather Information from the User

Before generating anything, collect the following. Ask in a single, conversational message
— do not pepper the user with multiple rounds of questions.

**Required inputs:**
1. **System name** — e.g., "OasisLIMS 4.5", "SAP S/4HANA", "Empower CDS"
2. **System type** — LIMS / ERP / SCADA / MES / Equipment+Instrument / Custom app / Other
3. **Intended use** — brief description of what the system does in the GxP environment
4. **Business process supported** — e.g., "QC sample testing and results management"
5. **Applicable regulations** — e.g., 21 CFR Part 11, EU Annex 11, GMP, GLP, GCP
6. **GAMP software category** — ask if unsure; see Category Guide below
7. **Key functions to assess** — list of system functions the user wants risk-assessed
   (if not provided, Claude should suggest typical functions based on system type — see
   references/function-library.md for suggestions by system type)
8. **Author name / department / date**

**Optional but useful:**
- Known interfaces with other systems
- Previous risk assessments to build on
- Any known critical quality attributes (CQAs) or critical process parameters (CPPs) involved

If the user provides partial information (e.g., "do a risk assessment for my LIMS"), use
the function library in references/function-library.md to propose standard functions and
ask the user to confirm or modify before generating.

---

## Step 2 — Determine GAMP Category and System Impact

### GAMP Software Categories (GAMP 5 Second Edition, Appendix M4)

| Category | Description | Typical Examples |
|---|---|---|
| **Cat 1** | Infrastructure software, OS, tools | Windows Server, Oracle DB, network tools |
| **Cat 3** | Standard components — cannot be configured to business processes | COTS instruments, firmware-only devices |
| **Cat 4** | Configured components — configurable to business workflows | LIMS, ERP, SCADA, CDS, MES, DCS, EDMS |
| **Cat 5** | Custom applications — bespoke code for specific business needs | Custom interfaces, in-house apps, macros |

> Note per GAMP 5 2nd Ed: Most real-world systems are **multi-category** — e.g., a LIMS
> (Cat 4 core) with custom interfaces (Cat 5) running on Windows Server (Cat 1).
> Assign the **dominant** category and note mixed components.

### System Impact Rating

Based on GAMP 5 Section 5.3 / Appendix M3 — Step 1 (Initial Risk Assessment):

| Rating | Criteria |
|---|---|
| **High** | Directly supports patient safety, product release, regulatory submissions, pharmacovigilance, adverse event reporting, or critical process parameters |
| **Medium** | Supports GxP processes indirectly; failures could affect data integrity or product quality but are detectable |
| **Low** | Supports business processes with minimal direct GxP impact; failures unlikely to affect patient safety or product quality |

---

## Step 3 — Build the FMEA Risk Table

This is the core deliverable. Each row represents one **system function**.

### FMEA Column Definitions

| Column | Definition | Source |
|---|---|---|
| **#** | Sequential entry number | — |
| **System Function** | The specific function being assessed | From user input or function library |
| **Potential Failure Mode** | How this function could fail | SME judgment |
| **Potential Hazard / Effect** | What harm could result from the failure | GAMP 5 §11.5.2 — "What is the harm?" |
| **Impact on** | Patient Safety (PS) / Product Quality (PQ) / Data Integrity (DI) | GAMP 5 §5.2 |
| **Severity (S)** | H / M / L — consequence if failure occurs | GAMP 5 §11.5.4 |
| **Probability (P)** | H / M / L — likelihood of failure occurring | GAMP 5 §11.5.2; increases with category (Cat 5 > Cat 4 > Cat 3) |
| **Detectability (D)** | H / M / L — likelihood failure is detected before harm | GAMP 5 §11.5.2 (Detect = H means easy to detect = lower risk) |
| **Risk Class** | Derived from S × P matrix (see matrix below) | GAMP 5 Fig 11.5 |
| **Risk Priority** | Derived from Risk Class + D (see matrix below) | GAMP 5 Fig 11.5 |
| **Proposed Controls** | Mitigation measures | GAMP 5 §11.5.5 — Table 11.2 |
| **Residual Risk** | Risk level after controls applied | GAMP 5 §11.5.6 |
| **Verification Reference** | Test / document that verifies the control | GAMP 5 §5.3 Step 4 |

### Risk Class Matrix (GAMP 5 Figure 11.5, Step 1)

|  | Severity: High | Severity: Medium | Severity: Low |
|---|---|---|---|
| **Probability: High** | High | High | Medium |
| **Probability: Medium** | High | Medium | Low |
| **Probability: Low** | Medium | Low | Low |

### Risk Priority Matrix (GAMP 5 Figure 11.5, Step 2)

|  | Detectability: Low (hard to detect) | Detectability: Medium | Detectability: High (easy to detect) |
|---|---|---|---|
| **Risk Class: High** | Critical | High | Medium |
| **Risk Class: Medium** | High | Medium | Low |
| **Risk Class: Low** | Medium | Low | Low |

> **Critical** = immediate action required; consider redesign or process change
> **High** = significant controls required; must be verified
> **Medium** = controls recommended; risk-based testing required
> **Low** = acceptable; apply good practice

---

## Step 4 — Generate the Word Document

Read the docx skill at `/mnt/skills/public/docx/SKILL.md` before writing any code.

### Document Structure

```
1. Cover Page
   - Document title: "Quality Risk Assessment"
   - System name, Version, Document number
   - Prepared by / Reviewed by / Approved by (with date fields)
   - Company name (if provided)
   - Regulatory references

2. Table of Contents

3. Section 1 — Purpose and Scope
   - Purpose of this assessment
   - Scope of the assessment (system, modules, functions covered)
   - Regulatory basis (ICH Q9, GAMP 5 2nd Ed, EU Annex 11, 21 CFR Part 11 as applicable)

4. Section 2 — System Overview
   - System name and version
   - System type and GAMP category
   - Intended use and business process supported
   - System interfaces (if known)
   - GxP determination (Yes/No + which regulations)

5. Section 3 — Risk Assessment Methodology
   - Brief description of GAMP 5 5-step QRM process (Steps 1–5)
   - Severity / Probability / Detectability rating scale definitions (H/M/L)
   - Risk Class and Risk Priority derivation matrices
   - Reference to GAMP 5 2nd Ed Appendix M3 and ICH Q9

6. Section 4 — Initial Risk Assessment (Step 1)
   - System impact determination (High / Medium / Low)
   - GxP scope determination
   - Decision on need for functional risk assessment

7. Section 5 — Functional Risk Assessment (Steps 2 & 3)
   - The FMEA table
   - Each function × failure mode as a row

8. Section 6 — Controls and Verification (Step 4)
   - Summary of control measures identified
   - Verification approach for each critical/high risk item

9. Section 7 — Residual Risk and Risk Acceptance (Step 5)
   - Summary of residual risk after controls
   - Statement of risk acceptability
   - Review frequency recommendation

10. Section 8 — Conclusions
    - Overall risk assessment conclusion
    - Fitness for GxP use determination

11. Appendix A — Risk Rating Definitions
    - H/M/L definitions for this specific system context

12. Signature Block
    - Prepared by / Date
    - Reviewed by / Date
    - Approved by / Date
```

### Styling Requirements

- **Page size:** A4 (standard for pharma GMP documents internationally)
- **Font:** Arial 11pt body, 12pt headings
- **Color scheme:** Professional/regulatory — navy headers (`1F3864`), white body, light blue table headers (`BDD7EE`), alternating row shading (`EBF3FB`)
- **Header:** Document title + document number on every page
- **Footer:** "CONFIDENTIAL — For Internal Use Only" + page number
- **FMEA table:** Landscape orientation section for readability
- **Risk Priority color coding in table:**
  - Critical: red fill (`FF0000`) white text
  - High: orange fill (`FF6600`) white text
  - Medium: yellow fill (`FFCC00`) black text
  - Low: green fill (`70AD47`) white text

### Code approach

Use `docx` npm library. Install if needed: `npm install docx`
Work in `/home/claude/` and copy final output to `/mnt/user-data/outputs/`

For the FMEA table, use landscape page section. Generate programmatically — do not
attempt to inline a massive table as a static object.

---

## Step 5 — Quality Check Before Delivery

Before presenting the file, verify:

- [ ] All user-provided system functions are covered in the FMEA table
- [ ] Every High/Critical risk has at least one control measure
- [ ] Every control has a verification reference
- [ ] Risk matrices are applied correctly (cross-check a few entries)
- [ ] GxP determination is stated clearly
- [ ] GAMP category is stated and justified
- [ ] Regulatory references are correct for the applicable framework
- [ ] Document number, version, date, author fields are filled or clearly marked [TBC]
- [ ] Signature block is present

---

## Key GAMP 5 Second Edition Principles to Embed in Every Document

These are non-negotiable — they must be reflected in the language of the document:

1. **Risk is proportionate** — effort/formality scales with risk, complexity, and novelty
2. **Science-based** — assessment based on process understanding, not just checklists
3. **Patient safety, product quality, data integrity** — these are the three pillars; every
   risk must link back to at least one of them
4. **Residual risk** — always addressed after controls; zero risk is not the goal
5. **Five-step process** — Step 1 (initial), Step 2 (identify functions), Step 3 (assess),
   Step 4 (implement controls), Step 5 (review and monitor)
6. **Categories are a continuum** — not hard boxes; most systems are multi-category
7. **Controls preference order:** Eliminate by design > Reduce probability > Increase
   detectability > Downstream traps (per GAMP 5 §11.5.5)

---

## Reference Files

- **`references/function-library.md`** — Pre-built lists of typical functions and failure modes
  by system type (LIMS, ERP, SCADA, MES, Equipment, Custom). Read this when the user
  hasn't provided specific functions, or to supplement their list.
- **`references/regulatory-refs.md`** — Key regulatory citations for different frameworks
  (21 CFR Part 11, EU Annex 11, ICH Q9, etc.) to include in the document.
