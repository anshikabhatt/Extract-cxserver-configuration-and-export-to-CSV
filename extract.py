import os
import yaml
import csv

supported_pairs = []

# Loop through all the YAML files in the config directory
ignore_files = ['MWPageLoader.yaml', 'languages.yaml', 'JsonDict.yaml', 'Dictd.yaml', 'mt-defaults.wikimedia.yaml']
for filename in os.listdir("config"):
    if filename.endswith('.yaml') and filename not in ignore_files:
        with open(os.path.join("config", filename), "r") as f:
            config = yaml.safe_load(f)
            f.close

            # Check if the YAML file has a "handler" key
            if "handler" in config:
                handler = config["handler"]
                if handler == "transform.js":
                    lst = config["languages"]
                    source_lang = filename[:-5]
                    for target_lang in lst:
                        supported_pairs.append({
                            "source language": source_lang,
                            "target language": target_lang,
                            "translation engine": source_lang,
                            "is preferred engine?": config.get("preferred_engine", False)
                        })
            else:
                # Handle standard configuration files
                for source_lang, target_langs in config.items():
                    for target_lang in target_langs:
                        supported_pairs.append({
                            "source language": source_lang,
                            "target language": target_lang,
                            "translation engine": filename[:-5],
                            "is preferred engine?": config.get("preferred_engine", False)
                        })

# Group the supported pairs by source language
source_to_targets = {}
for pair in supported_pairs:
    source = pair["source language"]
    target = pair["target language"]
    if source not in source_to_targets:
        source_to_targets[source] = []
    source_to_targets[source].append(target)

# Export the list as a CSV file
with open("supported_pairs.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["source language", "target language", "translation engine", "is preferred engine?"])
    writer.writeheader()
    for source, targets in source_to_targets.items():
        for target in targets:
            writer.writerow({
                "source language": source,
                "target language": target,
                "translation engine": source,
                "is preferred engine?": any(pair["is preferred engine?"] for pair in supported_pairs if pair["source language"] == source and pair["target language"] == target)
            })
