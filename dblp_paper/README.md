# PaperFilter

## Introduction
This project aims to filter papers that you are interested from DBLP([https://dblp.org][DBLP]) according to keywords.

## Start up
To install requested packages:``pip3 install -r requirements.txt``.

## Guidance
### Step 1
Set names and links in DBLP of journals or conferences in ``PAGES`` of ``constant.py``.
``PAGES`` is a dictionary in Python, and its key is string that is the name of a journal or conference,
its value is a tuple which is (link of the journal or conference, rank of the journal or conference). 
For example:
```
PAGES = {"IEEE Conference on Computer Communications (INFOCOM)":
             ("https://dblp.uni-trier.de/db/conf/infocom/index.html", "A"),
         "Symposium on Networked Systems Design and Implementation (NSDI)":
             ("https://dblp.uni-trier.de/db/conf/nsdi/index.html", "A"),
         "Transactions on Networking (TON)":
             ("https://dblp.uni-trier.de/db/journals/ton/index.html", "A"),
         "Computer Communication Review (ACM SIGCOMM)":
             ("https://dblp.uni-trier.de/db/journals/ccr/index.html", "A"),
         "IEEE Journal of Selected Areas in Communications (JSAC)":
             ("https://dblp.uni-trier.de/db/journals/jsac/index.html", "A")}
```
### Step 2
Set the range of years you want to search in ``YEARS`` of ``constant.py``.
For examples, if want search papers from 2015 to 2020, I need to set ``YEARS`` as follows.
```
YEARS = list(range(2015, 2021))
```
### Step 3
Run ``dblp_spider.py``:
```
python3 dblp_spider.py
```
Then, you can get lists of papers in csv format files named by names of journals or conference.
They includes
**_[paper title, doi, year, rank of the journal or conference, name of the journal or conference]_**
### Step 4
Set keywords in ``keywords_filter.py``.
``keywords_inlcude`` indicates the keywords that the paper title may include.
``keywords_exclude`` indicates the keywords that must be not in the paper title.
``keywords_must_in`` indicates the keywords that must be in the paper title.
For example"
```
keywords_include = ["optimization", "video", "quality"]
keywords_exclude = ["wireless"]
keywords_must_in = ["data center"]
```
The above implies that the filtered paper titles may include "optimization", "video", and "quality"; they must not include
"wireless"; and they must contain "data center".

You can also set the path of output files:
```
output_file = "filter.csv"
count_file = "count.txt"
```
where ``output_file`` is the path of file that contains the filtered information,
``count_file`` is the path of file that contains the statistical information.
### Step 5
Run ``keywords_filter.py``:
```
python3 keywords_filter.py
```
Then, you can get a csv format file that includes the filtered information, a txt format file that includes the statistical
information.



[DBLP]: https://dblp.org