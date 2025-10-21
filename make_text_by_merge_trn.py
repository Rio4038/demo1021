import os
import glob

# 入力ディレクトリと出力ファイル
input_dir = "./merged_trn"
output_text = "text"

# 出力ファイル作成
with open(output_text, "w", encoding="utf-8") as fout:
    for filepath in sorted(glob.glob(os.path.join(input_dir, "*_merged.trn"))):
        with open(filepath, "r", encoding="utf-8") as fin:
            for line in fin:
                fout.write(line)

print(f"✅ Kaldi用の text ファイルを {output_text} に作成しました。")
