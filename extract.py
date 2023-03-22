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

            # Check if the YAML file has a "handler" key
            if "handler" in config:
                handler = config["handler"]
                if handler == "transform.js":
                    lst = config["languages"]
                    target_langs = []
                    source_lang = []
                    # Handle transform.js based configuration files
                    for j in lst:
                        source_lang.append(j)
                        target_lang = []
                        for k in lst:
                            if(j != k and not ((j == "simple" and k == "en") or (k == "simple" and j == "en"))):
                                target_lang.append(k)
                        target_langs.append(target_lang)
                    engine = filename[:-5]
                    preferred_engine = config.get("preferred_engine", False)
            else:
                #  Handle standard configuration files
                source_lang = list(config.keys())
                target_langs = []
                for j in source_lang:
                    target_langs.append(config[j])
                    engine = filename[:-5]
                    preferred_engine = config.get("preferred_engine", False)

            # Add the supported pairs to the list
            for k in range(len(source_lang)):
                for i in target_langs[k]:
                   source = source_lang[k] if source_lang[k] is not False else "no"
                    target = i if i is not False else "no" 
                    supported_pairs.append({
                        "source language": source_lang[k],
                        "target language": i,
                        "source language": source,
                        "target language": target,
                        "translation engine": engine,
                        "is preferred engine?": preferred_engine
                    })
 # Read the mt-defaults.csv file and create a dictionary
with open("mt-defaults.csv", "r") as f:
    reader = csv.DictReader(f)
    mt_defaults = {}
    for row in reader:
        key = (row["source language"], row["target language"], row["translation engine"])
        mt_defaults[key] = row   

 # Loop over each pair in the supported_pairs list
for pair in supported_pairs:
# Check the mt_defaults dictionary for the preferred translation settings for the current language pair and engine.
    key = (pair["source language"], pair["target language"], pair["translation engine"])
    match = mt_defaults.get(key)
    # Set the "is preferred engine?" field to True if a match is found.
    if match:
        pair["is preferred engine?"] = "True"                       

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
    writer.writerows(supported_pairs)
