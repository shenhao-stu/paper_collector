import pandas as pd
import csv
import os
from constant import PAGES


def main():
    keywords_include = ["reinforcement", "meta", "subgraph", "graph"]
    keywords_exclude = []
    keywords_must_in = ["federated"]

    output_file = "output.csv"
    count_file = "output_count.txt"

    if os.path.exists(output_file):
        os.remove(output_file)
    if os.path.exists(count_file):
        os.remove(count_file)

    pages = list(PAGES.items())
    summary = 0

    for page in pages:
        journal_name = page[0]
        input_file = "total/" + journal_name + ".csv"

        file = pd.read_csv(input_file, header=None)
        count = 0

        with open(output_file, "a+") as csv_file:
            writer = csv.writer(csv_file)
            for index, row in file.iterrows():
                title = row[0].lower()
                stage_1 = True
                for word_exclude in keywords_exclude:
                    if word_exclude in title:
                        stage_1 = False
                        break
                stage_2 = True
                if stage_1:
                    for word_must_in in keywords_must_in:
                        if word_must_in not in title:
                            stage_2 = False
                            break
                stage_3 = False
                if stage_1 and stage_2:
                    if len(keywords_include) == 0:
                        stage_3 = True
                    for word_include in keywords_include:
                        if word_include in title:
                            stage_3 = True
                            break
                if stage_1 and stage_2 and stage_3:
                    writer.writerow(row)
                    count += 1
        summary += count
        file = open(count_file, "a+")
        file.write("{}: {}\n".format(journal_name, count))
        csv_file.close()
        file.close()
    file = open(count_file, "a+")
    file.write("summary: %d\n" % summary)


if __name__ == "__main__":
    main()
