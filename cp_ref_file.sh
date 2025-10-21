#!/bin/bash

# ベースディレクトリ
BASE_DIR="/CDshare/Speech/CSJ-SSC.pub2004/TestSet1"

# コピー先ディレクトリ（必要に応じて変更）
DEST_DIR="./copied_trn_files"

# コピー先ディレクトリを作成（存在しなければ）
mkdir -p "$DEST_DIR"

# 対象ディレクトリ名リスト
dirs=(
  "A01M0097"
  "A01M0110"
  "A01M0137"
  "A03M0106"
  "A03M0112"
  "A03M0156"
  "A04M0051"
  "A04M0121"
  "A04M0123"
  "A05M0011"
)

# 各ディレクトリから対応する .trn ファイルをコピー
for dir in "${dirs[@]}"; do
  src_path="$BASE_DIR/$dir/${dir}.trn"
  if [ -f "$src_path" ]; then
    cp "$src_path" "$DEST_DIR"
    echo "Copied: $src_path"
  else
    echo "Not found: $src_path"
  fi
done
