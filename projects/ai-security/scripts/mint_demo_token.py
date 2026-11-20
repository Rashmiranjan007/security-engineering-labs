"""Mint a short-lived JWT for local testing only; never use this as an identity provider."""
import argparse
import os
import time

import jwt

ISSUER = "ai-security-lab"
AUDIENCE = "ai-security-api"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tenant", default="tenant-a")
    parser.add_argument("--user", default="analyst-1")
    parser.add_argument("--role", choices=("user", "admin"), default="user")
    args = parser.parse_args()

    secret = os.getenv("JWT_SECRET", "")
    if len(secret.encode("utf-8")) < 32:
        parser.error("Set JWT_SECRET to a random value of at least 32 bytes")

    now = int(time.time())
    claims = {
        "sub": args.user,
        "tenant_id": args.tenant,
        "role": args.role,
        "iat": now,
        "exp": now + 300,
        "iss": ISSUER,
        "aud": AUDIENCE,
    }
    print(jwt.encode(claims, secret, algorithm="HS256"))


if __name__ == "__main__":
    main()
