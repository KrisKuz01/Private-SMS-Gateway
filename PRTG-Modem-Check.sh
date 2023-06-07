#!/bin/bash

directory="/var/spool/sms/gsm1"
timeout=300  # Timeout in seconds

files=$(ls "$directory")
now=$(date +%s)
old_files=()

for f in $files; do
    if [[ -f "$directory/$f" && $(expr $now - $(date +%s -r "$directory/$f")) -gt $timeout ]]; then
        old_files+=("$f")
    fi
done

if [ ${#old_files[@]} -gt 0 ]; then
    returncode=2
    value=${#old_files[@]}
    message="Text Messages are queued in GSM1."
else
    returncode=0
    value=0
    message="No files older than 5 minutes found"
fi

echo "$returncode:$value:$message"
