import os
import yaml
import csv

ignore_files = ['MWPageLoader.yaml', 'languages.yaml', 'JsonDict.yaml', 'Dictd.yaml', 'mt-defaults.wikimedia.yaml']

supported_pairs = []

# Loop through all the YAML files in the config directory
for file_name in os.listdir('config'):
    if file_name.endswith('.yaml') and file_name not in ignore_files:
        with open(os.path.join('config', file_name)) as f:
            data = yaml.safe_load(f)
            engine = file_name[:-5]
            preferred_engine = data.get("preferred_engine", False)

            # Check if the YAML file has a "handler" key
            if "handler" in data:
                handler = data["handler"]
                if handler == "transform.js":
                    source_lang = list(data["languages"])
                    target_langs = []
                    for j in source_lang:
                        target_lang = []
                        for k in source_lang:
                            if j != k and not ((j == "simple" and k == "en") or (k == "en" and j == "simple")):
                                target_lang.append(k)
                        target_langs.append(target_lang)
                else:
                    # Ignore other types of handlers
                    continue
            else:
                # Handle standard configuration files
                source_lang = list(data.keys())
                target_langs = []
                for j in source_lang:
                    target_langs.append(data[j])

            # Add the supported pairs to the list
            for i, src_lang in enumerate(source_lang):
                for tgt_lang in target_langs[i]:
                    supported_pairs.append([src_lang, tgt_lang, engine, preferred_engine])

# Write all supported pairs to a CSV file
with open('supported_pairs.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['source language', 'target language', 'translation engine', 'is preferred engine?'])
    writer.writerows(supported_pairs)
