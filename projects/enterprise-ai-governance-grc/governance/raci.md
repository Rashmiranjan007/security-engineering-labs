# AI Governance RACI

R = Responsible, A = Accountable, C = Consulted, I = Informed. Assign named roles and deputies in the organization; this example is not a substitute for an approved delegation of authority.

| Activity | Business owner | AI governance | Security | Privacy/legal | Model/service owner | Data owner | Internal audit |
|---|---|---|---|---|---|---|---|
| Use-case intake | A | R | C | C | R | C | I |
| AI impact classification | A | R | C | C | C | C | I |
| Security threat model | C | I | A/R | C | R | C | I |
| Privacy/legal assessment | C | I | C | A/R | C | C | I |
| Data approval and lineage | C | I | C | C | R | A | I |
| Supplier due diligence | A | C | R | C | R | C | I |
| Production approval | A | R | C | C | R | C | I |
| Operational monitoring | I | C | C | I | A/R | C | I |
| Risk exception | A | R | C | C | C | C | I |
| Independent audit | I | C | C | C | C | C | A/R |

## Decision rights

- Business owner accepts business residual risk within delegated appetite.
- Security can block release for unresolved mandatory security requirements according to enterprise policy.
- Privacy/legal determines required specialist review and legal interpretation.
- AI governance maintains the inventory, process and committee record.
- Internal audit remains independent from design and operation of controls.
