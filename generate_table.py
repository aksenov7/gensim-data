#!/usr/bin/env python
"""Script for generation table with data/models from list.json in .md format"""
import argparse
import json


DATASETS_SOURCE = "list.json"


def generate_table(fn):
    with open(fn) as infile:
        data = json.loads(infile.read())

    datasets = sorted(data["corpora"].items(), key=lambda kv: kv[0])
    models = sorted(data["models"].items(), key=lambda kv: kv[0])

    print("## Available data")
    print("### Datasets")
    print("| name | file size | read_more | description | license |")
    print("|------|-----------|-----------|-------------|---------|")
    for name, other in datasets:
        if name.startswith("__testing_"):
            continue

        links = "<ul>" + " ".join("<li>{}</li>".format(link) for link in other["read_more"]) + "</ul>"
        print("| {name} | {size} | {links} | {description} | {license} |".format(
            name=name, links=links, description=other["description"],
            size="{} MB".format(other["file_size"] // 2 ** 20), license=other["license"]
        ))

    print("")
    print("### Models")
    print("| name | num vectors | file size | base dataset | read_more  | description | parameters | preprocessing | license |")
    print("|------|-------------|-----------|--------------|------------|-------------|------------|---------------|---------|")
    for name, other in models:
        if name.startswith("__testing_"):
            continue

        links = "<ul>" + " ".join("<li>{}</li>".format(link) for link in other["read_more"]) + "</ul>"
        parameters = "<ul>" + " ".join("<li>{} - {}</li>".format(k, v) for (k, v) in other["parameters"].items()) + "</ul>"
        print("| {name} | {num_vectors} | {size} | {base_dataset} | {links} | {description} | {parameters} | {preprocessing} | {license} |".format(
            name=name, num_vectors=other["num_records"], size="{} MB".format(other["file_size"] // 2 ** 20), 
            base_dataset=other["base_dataset"], links=links, description=other["description"], parameters=parameters,
            preprocessing=other.get("preprocessing", "-"), license=other["license"]
        ))
    print("\n(generated by {} based on {})".format(__file__, fn))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-file", help="Path to {}".format(DATASETS_SOURCE), default=DATASETS_SOURCE)
    args = parser.parse_args()
    generate_table(args.input_file)


if __name__ == "__main__":
    main()
