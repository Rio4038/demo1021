import re
import os
from collections import defaultdict

# 入力
id_file = "ID"
segment_dir = "./ref_to_kaldi_text"
output_dir = "./merged_trn"
os.makedirs(output_dir, exist_ok=True)

# IDファイルを読み込んで、講演ごとに分ける
id_map = defaultdict(list)
with open(id_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if match := re.match(r"^(A0[1-5]M\d{4})_\d{7}_\d{7}$", line):
            talk_id = match.group(1)
            id_map[talk_id].append(line)

# 各講演ごとに変換ファイルを読み込み、対応する発話をマージ
for talk_id, full_ids in id_map.items():
    # .trn に対応（.txt ではない）
    segment_path = os.path.join(segment_dir, f"{talk_id}_convert.trn")
    if not os.path.exists(segment_path):
        print(f"❌ {segment_path} が見つかりません")
        continue

    # セグメント読み込み
    segments = []
    with open(segment_path, "r", encoding="utf-8") as f:
        for line in f:
            if match := re.match(rf"^({talk_id})_(\d{{7}})_(\d{{7}})\s+(.*)", line.strip()):
                _, start, end, text = match.groups()
                segments.append({
                    "start": int(start),
                    "end": int(end),
                    "text": text
                })

    # マージ処理
    output_lines = []
    for full_id in full_ids:
        match = re.match(rf"^({talk_id})_(\d{{7}})_(\d{{7}})$", full_id)
        if not match:
            continue
        _, target_start, target_end = match.groups()
        target_start, target_end = int(target_start), int(target_end)

        combined_text = ""
        for seg in segments:
            if target_start <= seg["start"] and seg["end"] <= target_end:
                combined_text += seg["text"]
        if combined_text:
            output_lines.append(f"{full_id} {combined_text}")

    # 出力
    output_path = os.path.join(output_dir, f"{talk_id}_merged.trn")
    with open(output_path, "w", encoding="utf-8") as f:
        for line in output_lines:
            f.write(line + "\n")

    print(f"✅ {talk_id}: {len(output_lines)} 件の発話を {output_path} に出力しました。")
