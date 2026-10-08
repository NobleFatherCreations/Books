#!/usr/bin/env bash
# Loudness/true-peak/format QC for a folder of audio before DistroKid upload.
# Usage: ./qc.sh <folder> [out.csv]      (needs ffmpeg + ffprobe; free)
# Pass rules used: integrated -16..-9 LUFS, true peak <= -1.0 dBTP,
# sample rate 44.1k/48k, WAV/FLAC preferred over MP3 for delivery.
set -euo pipefail
dir="${1:?folder}"; out="${2:-qc-report.csv}"
echo "file,format,sample_rate,bit_depth,kbps,duration_s,lufs_i,true_peak_dbtp,lra,verdict" > "$out"
shopt -s nullglob nocaseglob
for f in "$dir"/*.{mp3,wav,flac}; do
  fmt="${f##*.}"
  read -r sr bits < <(ffprobe -v error -select_streams a:0 \
      -show_entries stream=sample_rate,bits_per_raw_sample -of csv=p=0 "$f" | tr ',' ' ')
  read -r dur br < <(ffprobe -v error -show_entries format=duration,bit_rate -of csv=p=0 "$f" | tr ',' ' ')
  r=$(ffmpeg -nostats -hide_banner -i "$f" -af ebur128=peak=true -f null - 2>&1 | tail -14)
  I=$(awk '/ I:/{print $2}' <<<"$r"); L=$(awk '/LRA:/{print $2; exit}' <<<"$r"); P=$(awk '/Peak:/{print $2}' <<<"$r")
  v=OK
  awk -v p="$P" 'BEGIN{exit !(p > -1.0)}' && v="TRUE-PEAK-HOT"
  awk -v i="$I" 'BEGIN{exit !(i > -9 || i < -16)}' && v="$v;LOUDNESS-OUT-OF-RANGE"
  [[ "${fmt,,}" == mp3 ]] && v="$v;LOSSY-SOURCE"
  echo "\"$(basename "$f")\",$fmt,$sr,${bits:-},$(( ${br:-0} / 1000 )),${dur%.*},$I,$P,$L,$v" >> "$out"
  printf '%-50.50s %6s LUFS %6s dBTP  %s\n' "$(basename "$f")" "$I" "$P" "$v"
done
echo "-> $out"
