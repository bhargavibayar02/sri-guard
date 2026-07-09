# threat_timeline.py
# Converts a raw log entry's fields into a chronological, human-readable
# TIMELINE of events -- e.g. "09:00 Login", "09:05 Failed Login", etc.
#
# Since our dataset stores one AGGREGATE record per login session
# (not individual timestamped events), we reconstruct a realistic-looking
# timeline by spacing out each notable event a few minutes after login,
# in a logical order that mirrors how an actual insider-threat session
# would unfold.

from datetime import datetime, timedelta


def generate_timeline(log: dict) -> list[str]:
    """
    Builds a list of timeline strings like "09:07 Finance DB accessed"
    based on which fields in this log entry are notable.
    """
    login_dt = datetime.fromisoformat(log["login_time"].replace(" ", "T"))
    timeline = []

    # Event 1: Login (always first)
    timeline.append(f"{login_dt.strftime('%H:%M')} — Login from {log.get('device', 'unknown device')}")

    minute_offset = 2

    # Event 2: Failed logins (if any occurred, they'd show right after)
    failed_logins = int(log.get("failed_logins", 0))
    if failed_logins > 0:
        event_time = login_dt + timedelta(minutes=minute_offset)
        timeline.append(f"{event_time.strftime('%H:%M')} — {failed_logins} failed login attempt(s)")
        minute_offset += 3

    # Event 3: Database access
    db_access = log.get("database_access", "None")
    if db_access and db_access != "None":
        event_time = login_dt + timedelta(minutes=minute_offset)
        timeline.append(f"{event_time.strftime('%H:%M')} — Accessed {db_access}")
        minute_offset += 2

    # Event 4: File downloads
    files_downloaded = int(log.get("files_downloaded", 0))
    if files_downloaded > 0:
        event_time = login_dt + timedelta(minutes=minute_offset)
        timeline.append(f"{event_time.strftime('%H:%M')} — Downloaded {files_downloaded} file(s)")
        minute_offset += 1

    # Event 5: USB connected
    usb = log.get("usb_connected") in [True, "True", "true", 1]
    if usb:
        event_time = login_dt + timedelta(minutes=minute_offset)
        timeline.append(f"{event_time.strftime('%H:%M')} — USB storage device connected")
        minute_offset += 1

    # Event 6: Admin access used
    admin = log.get("admin_access") in [True, "True", "true", 1]
    if admin:
        event_time = login_dt + timedelta(minutes=minute_offset)
        timeline.append(f"{event_time.strftime('%H:%M')} — Administrator-level access used")
        minute_offset += 1

    # Final event: Alert (only if this log ended up flagged as risky)
    risk_score = log.get("risk_score")
    if risk_score is not None and risk_score > 70:
        event_time = login_dt + timedelta(minutes=minute_offset)
        timeline.append(f"{event_time.strftime('%H:%M')} — ⚠️ Risk Alert Generated (Score: {risk_score})")

    return timeline