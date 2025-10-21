import re
import os
import glob

# 入力ディレクトリ（コピーされた .trn ファイルがある場所）
input_dir = "./copied_trn_files"

# 出力ディレクトリ
output_dir = "./ref_to_kaldi_text"
os.makedirs(output_dir, exist_ok=True)  # 出力先がなければ作成

# .trn ファイルすべてに処理
for input_path in glob.glob(os.path.join(input_dir, "*.trn")):
    base_name = os.path.basename(input_path)
    talk_id = base_name.replace(".trn", "")
    output_path = os.path.join(output_dir, f"{talk_id}_convert.trn")

    with open(input_path, "r", encoding="shift_jis", errors="ignore") as f:
        lines = f.readlines()

    output_lines = []
    current_id = ""
    current_block_lines = []

    for line in lines:
        match = re.match(r"^(\d{4}) (\d{5}\.\d{3})-(\d{5}\.\d{3})", line)
        if match:
            if current_id and current_block_lines:
                merged = " ".join(l.split("&")[0].strip() for l in current_block_lines if l.strip())
                output_lines.append(f"{current_id} {merged}")
            start_ms = str(int(float(match.group(2)) * 1000)).zfill(7)
            end_ms = str(int(float(match.group(3)) * 1000)).zfill(7)
            current_id = f"{talk_id}_{start_ms}_{end_ms}"
            current_block_lines = []
            continue
        if line.strip() and not line.startswith("%"):
            current_block_lines.append(line)

    if current_id and current_block_lines:
        merged = " ".join(l.split("&")[0].strip() for l in current_block_lines if l.strip())
        output_lines.append(f"{current_id} {merged}")

    with open(output_path, "w", encoding="utf-8") as f:
        for line in output_lines:
            f.write(line + "\n")

    print(f"✅ {talk_id}: {len(output_lines)} 発話を {output_path} に出力しました。")
