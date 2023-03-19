import os
import yaml
import csv

ignore_files = ['MWPageLoader.yaml', 'languages.yaml', 'JsonDict.yaml', 'Dictd.yaml', 'mt-defaults.wikimedia.yaml']

supported_pairs = []
source_to_targets = {}

# Loop through all the YAML files in the config directory
for file_name in os.listdir('config'):
    if file_name.endswith('.yaml') and file_name not in ignore_files:
        with open(os.path.join('config', file_name)) as f:
            data = yaml.safe_load(f)
            f.close()
            engine = file_name[:-5]
            preferred_engine = data.get("preferred_engine", False)

            # Check if the YAML file has a "handler" key
            if "handler" in data and data["handler"] == "transform.js":
                source_lang = data["languages"]
                target_langs = []
                for j in source_lang:
                    target_lang = []
                    for k in source_lang:
                        if j != k and not ((j == "simple" and k == "en") or (k == "en" and j == "simple")):
                            target_lang.append(k)
                    target_langs.append(target_lang)
                # Add the supported pairs to the list
                for i, src_lang in enumerate(source_lang):
                    for tgt_lang in target_langs[i]:
                        supported_pairs.append({
                            "source language": src_lang,
                            "target language": tgt_lang,
                            "translation engine": engine,
                            "is preferred engine?": preferred_engine
                        })
                        # Add the target language to the source's list of targets
                        if src_lang not in source_to_targets:
                            source_to_targets[src_lang] = []
                        source_to_targets[src_lang].append(tgt_lang)
                        
            else:
                # Handle standard configuration files
                source_lang = list(data.keys())
                target_langs = []
                for j in source_lang:
                    target_langs.append(data[j])
                # Add the supported pairs to the list
                for i, src_lang in enumerate(source_lang):
                    for tgt_lang in target_langs[i]:
                        supported_pairs.append({
                            "source language": src_lang,
                            "target language": tgt_lang,
                            "translation engine": engine,
                            "is preferred engine?": preferred_engine
                        })
                        # Add the target language to the source's list of targets
                        if src_lang not in source_to_targets:
                            source_to_targets[src_lang] = []
                        source_to_targets[src_lang].append(tgt_lang)

# Write all supported pairs to a CSV file
with open('supported_pairs.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['source language', 'target language', 'translation engine', 'is preferred engine?'])
    writer.writerows(supported_pairs)

