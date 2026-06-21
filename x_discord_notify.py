import os
import sys
import time
import requests
import argparse
from pathlib import Path
from datetime import date, datetime

def load_slot(content, slot):
    parts = [p.strip() for p in content.split("---")]
    idx = int(slot) - 1
    if idx < 0 or idx >= len(parts):
        return None
    return parts[idx] if parts[idx] else None

def get_header(slot):
    now = datetime.now()
    weekdays = ["月", "火", "水", "木", "金", "土", "日"]
    weekday = weekdays[now.weekday()]
    date_str = now.strftime(f"%Y-%m-%d（{weekday}）")
    slot_info = {"1": ("朝", "07:00"), "2": ("昼", "12:00"), "3": ("夜", "21:00")}
    slot_name, time_str = slot_info.get(str(slot), ("", ""))
    return f"[{date_str}{slot_name} {time_str}]"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slot", default="1")
    args = parser.parse_args()

    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("DISCORD_WEBHOOK_URL が設定されていません")
        sys.exit(1)

    today = str(date.today())
    path = Path("posts") / f"{today}.md"

    if not path.exists():
        print(f"{today}.md が見つかりません")
        sys.exit(0)

    content = path.read_text(encoding="utf-8")
    post = load_slot(content, args.slot)

    if not post:
        print(f"slot {args.slot} の内容が見つかりません")
        sys.exit(0)

    header = get_header(args.slot)

    requests.post(webhook_url, json={"content": header}, timeout=10)
    time.sleep(1)
    requests.post(webhook_url, json={"content": post}, timeout=10)

    print(f"送信完了：slot {args.slot}")

if __name__ == "__main__":
    main()
