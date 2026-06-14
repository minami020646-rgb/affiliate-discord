import os
import sys
import requests
import argparse
from pathlib import Path
from datetime import date

def load_slot(content, slot):
    labels = {"1": "【朝】", "2": "【昼】", "3": "【夜】"}
    label = labels.get(slot)
    if not label:
        return None

    lines = content.split("\n")
    result = []
    capturing = False

    for line in lines:
        if line.strip() == label:
            capturing = True
            continue
        if capturing:
            if line.strip() in ["【朝】", "【昼】", "【夜】"]:
                break
            result.append(line)

    return "\n".join(result).strip()

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

    slot_labels = {"1": "朝", "2": "昼", "3": "夜"}
    label = slot_labels.get(args.slot, args.slot)

    message = f"**【{label}の投稿】**\n\n{post}"
    requests.post(webhook_url, json={"content": message}, timeout=10)
    print(f"送信完了：slot {args.slot}")

if __name__ == "__main__":
    main()
