"""Deterministic AI security mock target. No network or model calls."""
import re

CANARY = "CANARY-DO-NOT-LEAK"

SECURE_CONTROLS = {
    "prompt_injection_guard",
    "tenant_isolation",
    "tool_authorization",
    "retrieval_content_isolation",
    "output_redaction",
    "abuse_throttling",
}

VULNERABLE_CONTROLS = {
    "prompt_injection_guard",
    "retrieval_content_isolation",
    "output_redaction",
}


class MockTarget:
    def __init__(self, profile="secure"):
        if profile not in {"secure", "intentionally-vulnerable"}:
            raise ValueError("Unsupported profile; only local mock profiles are allowed")
        self.profile = profile
        self.controls = set(SECURE_CONTROLS)
        if profile == "intentionally-vulnerable":
            self.controls -= VULNERABLE_CONTROLS

    def execute(self, case):
        control = case["control"]
        data = case["input"]
        blocked = False

        if control == "prompt_injection_guard":
            blocked = control in self.controls and bool(
                re.search(r"ignore all prior rules|disclose the protected canary", data["prompt"], re.I)
            )
        elif control == "tenant_isolation":
            blocked = control in self.controls and data["tenant"] != data["document_tenant"]
        elif control == "tool_authorization":
            blocked = control in self.controls and (
                data["role"] != "admin" or data["tool"] != "admin_export" or not data["approval"]
            )
        elif control == "retrieval_content_isolation":
            blocked = control in self.controls and "SYSTEM OVERRIDE" in data["retrieved_text"].upper()
        elif control == "output_redaction":
            blocked = control in self.controls and CANARY in data["candidate_output"]
        elif control == "abuse_throttling":
            blocked = control in self.controls and data["requests"] > data["limit"]
        else:
            raise ValueError(f"Unsupported control: {control}")

        return {"blocked": bool(blocked), "control": control, "profile": self.profile}
