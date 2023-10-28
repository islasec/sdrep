#!/usr/bin/env python3

import re
import glob

def extract_loras_from_file(file_contents):
    """Extract Lora hashes from file content and return a list."""
    return re.findall(r"<(lora:[\w:._-]+)>", file_contents)

def extract_model_and_cfg_from_file(file_contents):
    """Extract Model and CFG scale from file content and return them."""
    model_match = re.search(r"Model: ([\w\s]+),", file_contents)
    cfg_match = re.search(r"CFG scale: ([\d\.]+),", file_contents)
    return model_match.group(1) if model_match else None, cfg_match.group(1) if cfg_match else None

# Get a list of all .txt files in the current directory
txt_files = glob.glob("*.txt")

# Dictionaries to store the occurrences of Lora hashes, Models, and CFG scales
lora_counts = {}
model_counts = {}
cfg_counts = {}

# Extracting details from each file
for filename in txt_files:
    with open(filename, "r") as file:
        file_contents = file.read()
    
    # Updating the count of each Lora hash
    for lora in extract_loras_from_file(file_contents):
        lora_counts[lora] = lora_counts.get(lora, 0) + 1

    # Extracting and updating the count of Model and CFG scale
    model, cfg = extract_model_and_cfg_from_file(file_contents)
    if model:
        model_counts[model] = model_counts.get(model, 0) + 1
    if cfg:
        cfg_counts[cfg] = cfg_counts.get(cfg, 0) + 1

# Sorting the Lora hashes, Models, and CFG scales by occurrence counts in descending order
sorted_loras = sorted(lora_counts.items(), key=lambda x: x[1], reverse=True)
sorted_models = sorted(model_counts.items(), key=lambda x: x[1], reverse=True)
sorted_cfgs = sorted(cfg_counts.items(), key=lambda x: x[1], reverse=True)

# Preparing the re-ordered consolidated report
report = "Consolidated Model Occurrences:\n"
for model, count in sorted_models:
    report += f"{count} - {model} occurrences\n"

report += "\nConsolidated CFG Scale Occurrences:\n"
for cfg, count in sorted_cfgs:
    report += f"{count} - CFG scale: {cfg} occurrences\n"

report += "\nConsolidated Lora Hash Occurrences:\n"
for lora, count in sorted_loras:
    report += f"{count} - {lora} occurrences\n"

print(report)
