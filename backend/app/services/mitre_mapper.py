# mitre_mapper.py
# Maps our plain-English risk reasons to real MITRE ATT&CK technique IDs.
# MITRE ATT&CK is a globally-used knowledge base of real attacker
# behaviors -- mapping to it makes our alerts feel "SOC-analyst ready"
# instead of just custom made-up categories.

# Each key is a substring we look for inside a reason string.
# Each value is the MITRE technique this reason maps to.
MITRE_RULES = [
    ("unusual time", "T1078 - Valid Accounts (Unusual Login Time)"),
    ("Unknown or unregistered device", "T1200 - Hardware Additions"),
    ("unusual location", "T1078.004 - Valid Accounts: Cloud Accounts (Unusual Location)"),
    ("failed login attempts", "T1110 - Brute Force"),
    ("high file downloads", "T1030 - Data Transfer Size Limits (Exfiltration)"),
    ("USB storage device", "T1052 - Exfiltration Over Physical Medium (Removable Media)"),
    ("sensitive database", "T1213 - Data from Information Repositories"),
    ("administrator-level access", "T1078.003 - Valid Accounts: Local Accounts (Privilege Escalation)"),
]


def map_reasons_to_mitre(reasons: list[str]) -> list[str]:
    """
    Given a list of plain-English risk reasons, returns the corresponding
    list of MITRE ATT&CK technique labels. Avoids duplicate tags.
    """
    mitre_tags = []
    for reason in reasons:
        for keyword, technique in MITRE_RULES:
            if keyword.lower() in reason.lower():
                if technique not in mitre_tags:
                    mitre_tags.append(technique)
    return mitre_tags