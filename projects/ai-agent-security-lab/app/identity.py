from dataclasses import dataclass
from fastapi import Header, HTTPException


@dataclass(frozen=True)
class Principal:
    subject: str
    tenant_id: str
    roles: frozenset[str]


def get_demo_principal(
    user: str | None = Header(default=None, alias="X-Demo-User"),
    tenant: str | None = Header(default=None, alias="X-Demo-Tenant"),
    roles: str = Header(default="reader", alias="X-Demo-Roles"),
) -> Principal:
    """DEMO ONLY: replace with verified OIDC claims before any real deployment."""
    if not user or not tenant:
        raise HTTPException(status_code=401, detail="Demo identity headers required")
    return Principal(user, tenant, frozenset(x.strip() for x in roles.split(",") if x.strip()))
