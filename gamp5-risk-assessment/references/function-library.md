# Function Library — Typical Functions and Failure Modes by System Type

Use this reference when the user has not provided specific functions, or to suggest
additions. Always confirm with the user before generating — these are starting points,
not prescriptive lists.

---

## LIMS (Laboratory Information Management System)
**GAMP Category:** 4 (Configured) — typically with Cat 5 interfaces
**Typical Regulatory Scope:** GMP, 21 CFR Part 11, EU Annex 11

| Function | Typical Failure Modes | Potential Harm |
|---|---|---|
| Sample login and registration | Duplicate sample IDs, incorrect sample data entry | Wrong test performed on wrong sample; incorrect results attributed |
| Test assignment and scheduling | Tests not assigned, wrong method selected | Missing tests; incorrect method applied; product release risk |
| Results entry and review | Incorrect data entry, unauthorized modification, system error | Incorrect test results recorded; patient safety risk |
| Specification management | Incorrect limits stored, outdated specs used | Out-of-spec results accepted; non-conforming product released |
| Out-of-specification (OOS) workflow | OOS not triggered, investigation not initiated | Non-conforming results not investigated; product release risk |
| Audit trail | Audit trail disabled, incomplete records | Data integrity failure; regulatory non-compliance (21 CFR Part 11 / Annex 11) |
| Electronic signature | Unauthorized signatures, signature bypass | Unapproved data released; regulatory violation |
| User access control | Unauthorized access, privilege escalation | Data integrity risk; unauthorized result modifications |
| Instrument integration / data import | Data transmission errors, data truncation | Incorrect results imported into LIMS; wrong product disposition |
| Report generation | Incorrect data pulled, formatting errors | Wrong information on certificate of analysis (CoA); release of incorrect data |
| Sample storage and chain of custody | Sample tracking lost, incorrect location | Sample lost; incorrect sample tested; stability study invalidated |
| System backup and recovery | Backup failure, data loss on restore | Loss of GxP records; inability to reconstruct data history |
| Change control integration | Unauthorized system changes, no documentation | System changes without impact assessment; compliance gap |
| Column / stability management | Incorrect tracking, expired items used | Invalid test results from degraded columns/samples |

---

## ERP (Enterprise Resource Planning — e.g., SAP S/4HANA)
**GAMP Category:** 4 (Configured) — with Cat 5 custom developments common
**Typical Regulatory Scope:** GMP, GDP, 21 CFR Part 11, EU Annex 11

| Function | Typical Failure Modes | Potential Harm |
|---|---|---|
| Batch/lot number management | Duplicate batch numbers, incorrect batch assignment | Wrong batch released; traceability failure; recall complications |
| Goods receipt and inspection | Incorrect material codes, skipped QC status | Non-conforming materials released to production |
| Batch record management | Missing data, unauthorized changes | Incomplete batch records; regulatory non-compliance |
| Product release | System bypass, incorrect release status | Non-conforming product released to market |
| Materials management (expiry, quarantine) | Expired materials used, quarantine not enforced | Patient safety risk from use of non-conforming materials |
| Electronic batch disposition | Status not locked, unauthorized disposition | Product released without proper QA approval |
| Change control management | Change not documented, unauthorized changes | Uncontrolled process changes; regulatory risk |
| User authorization and roles | Privilege creep, separation of duties violation | Unauthorized transactions; audit integrity risk |
| Audit trail / system logging | Incomplete logs, log tampering | Data integrity failure; regulatory non-compliance |
| Electronic signatures | Unauthorized approval, signature bypass | Compliance violation (21 CFR Part 11) |
| Data archiving and retrieval | Data not archived, retrieval failure | Inability to reconstruct GxP records |
| Integration with manufacturing systems | Data transfer errors, lost transactions | Incorrect data in batch records; traceability gaps |

---

## SCADA / DCS / MES / Process Control
**GAMP Category:** 4 (Configured) — may include Cat 5 custom logic
**Typical Regulatory Scope:** GMP, EU Annex 11, FDA Process Validation guidance

| Function | Typical Failure Modes | Potential Harm |
|---|---|---|
| Process parameter monitoring | Sensor failure, data dropout, incorrect calibration | CPPs not controlled; process drift; product quality impact |
| Alarm management | Alarm suppression, missed critical alarms | Out-of-range CPPs undetected; product quality failure |
| Setpoint control | Incorrect setpoint, unauthorized modification | Process parameters outside validated range |
| Recipe management | Wrong recipe loaded, unauthorized recipe change | Incorrect product manufactured; batch failure |
| Electronic batch records | Missing entries, data corruption | Incomplete GxP batch records; regulatory non-compliance |
| Audit trail / event log | Log disabled, timestamps incorrect | Data integrity failure; inability to reconstruct process history |
| User access control | Unauthorized setpoint changes, no separation of duties | Unauthorized process modifications |
| System availability / failover | Unplanned downtime, failover failure | Production stoppage; incomplete batch; product loss |
| Data historian | Data gaps, historian corruption | Incomplete process records for batch review |
| Calibration management | Instruments out of calibration, records missing | Invalid process data; product quality risk |
| Sequence interlock logic | Interlock failure, incorrect sequence | Safety risk; process deviation |

---

## Equipment / Laboratory Instruments
**GAMP Category:** 3 (Standard) or 4 (if software-configurable workflows)
**Typical Regulatory Scope:** GMP/GLP, 21 CFR Part 11 (if electronic records generated)

| Function | Typical Failure Modes | Potential Harm |
|---|---|---|
| Measurement / analysis function | Instrument malfunction, drift, out of calibration | Incorrect analytical results; wrong product decision |
| Data acquisition and recording | Data not captured, transmission error | Incomplete records; loss of test data |
| Electronic results output | Incorrect format, truncation, wrong units | Incorrect results imported to LIMS/ERP |
| Calibration tracking | Expired calibration, no alert | Use of non-calibrated instrument; invalid results |
| Method storage and loading | Wrong method loaded, method corruption | Incorrect analysis performed |
| Audit trail | Audit trail disabled or incomplete | Data integrity risk; regulatory non-compliance |
| User access / login | Unauthorized access, shared credentials | Unauthorized modifications; data integrity risk |
| Maintenance and service records | Missing records, incomplete history | Unable to demonstrate instrument fitness for use |
| Environmental monitoring integration | Data gaps, incorrect sensor | Environmental excursions not detected |
| System qualification status | Equipment used outside qualified parameters | Invalid results; compliance gap |

---

## Custom In-House Software / Bespoke Applications
**GAMP Category:** 5 (Custom) — highest inherent risk
**Typical Regulatory Scope:** Depends on use; usually GMP, 21 CFR Part 11, EU Annex 11

| Function | Typical Failure Modes | Potential Harm |
|---|---|---|
| Core calculation / algorithm | Logic error, rounding error, incorrect formula | Incorrect output used for GxP decision |
| Data input validation | No range checks, accepts invalid data | Garbage-in-garbage-out; incorrect GxP records |
| Database write / read operations | Data corruption, incorrect record retrieved | Wrong data used for decision; data integrity failure |
| User authentication | Weak authentication, bypass possible | Unauthorized access to GxP data |
| Audit trail | Not implemented, incomplete, tamper-possible | Data integrity failure; non-compliance |
| Electronic signature | Not implemented correctly, bypass possible | Regulatory violation (21 CFR Part 11) |
| Report generation | Incorrect data pulled, wrong template | Incorrect GxP reports used for decisions |
| Error handling | Errors silently ignored, no user alert | System failures undetected; incorrect processing |
| System integration / interfaces | Data lost in transfer, format mismatch | GxP records incomplete or incorrect |
| Backup and data recovery | Backup failure, data not recoverable | Loss of critical GxP records |
| Access control / roles | Insufficient segregation of duties | Unauthorized data modifications |
| Version / configuration control | Uncontrolled updates, wrong version in production | Unvalidated system version used in GxP context |

---

## Typical Controls by Risk Type (GAMP 5 Second Edition §11.5.5, Table 11.2)

| Risk Type | Control Options |
|---|---|
| Data entry errors | Input validation rules, range checks, mandatory fields, double-entry verification |
| Unauthorized access / modification | Role-based access control, unique user IDs, audit trail, electronic signatures |
| Data integrity / audit trail | System-enforced audit trail (cannot be disabled), timestamping, regular review |
| System availability | Redundant hardware, UPS, disaster recovery plan, backup schedule |
| Calculation errors (Cat 5) | Code review, unit testing, independent verification of algorithm |
| Process parameter excursions | Automated alarms, interlock logic, operator training, manual verification |
| Integration / interface failures | Interface testing, data reconciliation checks, error handling alerts |
| Calibration / instrument drift | Scheduled calibration, system calibration reminders, out-of-calibration lockout |
| Software configuration errors | Configuration review, change control, regression testing |
