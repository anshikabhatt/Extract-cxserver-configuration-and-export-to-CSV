import os
import yaml
import csv

def test_supported_pairs_csv():
    # Run the code to generate the CSV file
    supported_pairs = []
    ignore_files = ['MWPageLoader.yaml', 'languages.yaml', 'JsonDict.yaml', 'Dictd.yaml', 'mt-defaults.wikimedia.yaml']
    for filename in os.listdir("config"):
        if filename.endswith('.yaml') and filename not in ignore_files:
            with open(os.path.join("config", filename), "r") as f:
                config = yaml.safe_load(f)

                if "handler" in config:
                    handler = config["handler"]
                    if handler == "transform.js":
                        lst = config["languages"]
                        target_langs = []
                        source_lang = []
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
                    source_lang = list(config.keys())
                    target_langs = []
                    for j in source_lang:
                        target_langs.append(config[j])
                        engine = filename[:-5]
                        preferred_engine = config.get("preferred_engine", False)

                for k in range(len(source_lang)):
                    for i in target_langs[k]:
                        supported_pairs.append({
                            "source language": source_lang[k],
                            "target language": i,
                            "translation engine": engine,
                            "is preferred engine?": preferred_engine
                        })

    with open("mt-defaults.csv", "r") as f:
        reader = csv.DictReader(f)
        mt_defaults = {}
        for row in reader:
            key = (row["source language"], row["target language"], row["translation engine"])
            mt_defaults[key] = row

    for pair in supported_pairs:
        key = (pair["source language"], pair["target language"], pair["translation engine"])
        match = mt_defaults.get(key)
        if match:
            pair["is preferred engine?"] = "True"

    source_to_targets = {}
    for pair in supported_pairs:
        source = pair["source language"]
        target = pair["target language"]
        if source not in source_to_targets:
            source_to_targets[source] = []
        source_to_targets[source].append(target)

    with open("supported_pairs.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["source language", "target language", "translation engine", "is preferred engine?"])
        writer.writeheader()
        writer.writerows(supported_pairs)

    # Check that the CSV file was created and contains expected data
    assert os.path.isfile("supported_pairs.csv"), "CSV file was not created"
    with open("supported_pairs.csv", "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            assert row["source language"] in source_to_targets, f"Unsupported source language {row['source language']} found in CSV file"
            assert row["target language"] in source_to_targets[row["source language"]], f"Unsupported target language {row['target language']} found in CSV file for source language {row['source language']}"

