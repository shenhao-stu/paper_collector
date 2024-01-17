# coding=utf-8
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
import os
import random
from BaiduTransAPI import get_translate as trans
import tqdm


def get_one_page(url):
    response = requests.get(url)
    print(response.status_code)
    while response.status_code == 403:
        time.sleep(500 + random.uniform(0, 500))
        response = requests.get(url)
        print(response.status_code)
    print(response.status_code)
    if response.status_code == 200:
        return response.text

    return None


def main():
    url = "https://arxiv.org/list/cs/pastweek?show=2000"
    try:
        html = get_one_page(url)
    except:
        # Computer Science authors_titles recent submissions.html为url对应下载倒本地的html文件
        html = "\n".join(
            open(
                "Computer Science authors_titles recent submissions.html",
                encoding="utf-8",
            ).readlines()
        )
    soup = BeautifulSoup(html, features="html.parser")
    content = soup.dl
    list_ids = content.find_all("a", title="Abstract")
    list_title = content.find_all("div", class_="list-title mathjax")
    list_authors = content.find_all("div", class_="list-authors")
    list_subjects = content.find_all("div", class_="list-subjects")
    list_subject_split = []
    for subjects in list_subjects:
        subjects = subjects.text.split(": ", maxsplit=1)[1]
        subjects = subjects.replace("\n\n", "")
        subjects = subjects.replace("\n", "")
        subject_split = subjects.split("; ")
        list_subject_split.append(subject_split)
    print("Paper Number:", len(list_ids))

    """获取所有paper"""
    items = []
    for i, paper in tqdm.tqdm(
        enumerate(
            zip(list_ids, list_title, list_authors, list_subjects, list_subject_split)
        )
    ):
        try:
            transresult = trans(": ".join(paper[1].text.split(": ")[1:]), "en", "zh")
            chn = transresult["trans_result"][0]["dst"]
            items.append(
                [
                    paper[0].text,
                    ": ".join(paper[1].text.split(": ")[1:]),
                    chn,
                    paper[2].text,
                    "https://arxiv.org/pdf/%s.pdf" % paper[0].text.split(":")[-1],
                    paper[3].text,
                    paper[4],
                ]
            )
        except:
            print("ERROR", transresult)
    name = ["id", "title", "title_zh", "authors", "url", "subjects", "subject_split"]
    paper = pd.DataFrame(columns=name, data=items)
    paper.to_excel(
        "./daily/" + time.strftime("%Y-%m-%d") + "_" + str(len(items)) + ".xls",
        encoding="utf-8",
    )

    """按照subject进行统计"""
    subject_all = []
    for subject_split in list_subject_split:
        for subject in subject_split:
            subject_all.append(subject)
    subject_cnt = Counter(subject_all)
    subject_items = []
    for subject_name, times in subject_cnt.items():
        subject_items.append([subject_name, times])
    subject_items = sorted(
        subject_items, key=lambda subject_items: subject_items[1], reverse=True
    )
    name = ["name", "times"]
    subject_file = pd.DataFrame(columns=name, data=subject_items)
    subject_file.to_excel(
        "./subject_count/" + time.strftime("%Y-%m-%d") + "_" + str(len(items)) + ".xls",
        encoding="utf-8",
    )
    for dirr in os.listdir():
        if dirr in [
            ".ipynb_checkpoints",
            "daily",
            "subject_count",
            "__pycache__",
            ".idea",
        ]:
            continue
        if not os.path.isdir(dirr):
            continue
        print(dirr)
        key_words = [
            i.strip()
            for i in open(os.path.join(dirr, "key_words.txt"), encoding="utf-8")
        ]

        selected_papers = paper[paper["title"].str.contains(key_words[0], case=False)]
        for key_word in key_words[1:]:
            selected_paper1 = paper[paper["title"].str.contains(key_word, case=False)]
            selected_papers = pd.concat([selected_papers, selected_paper1], axis=0)
        selected_papers.to_excel(
            os.path.join(
                dirr,
                time.strftime("%Y-%m-%d") + "_" + str(len(selected_papers)) + ".xls",
            ),
            encoding="utf-8",
        )
    return content


if __name__ == "__main__":
    main()
