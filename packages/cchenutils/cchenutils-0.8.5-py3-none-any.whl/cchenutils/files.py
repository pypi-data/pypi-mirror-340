import csv
import os

from .dictutils import Dict


def csvwrite(fp, headers, d):
    writeheader = False if os.path.exists(fp) else True
    with open(fp, 'a', encoding='utf-8') as o:
        csvwriter = csv.DictWriter(o, fieldnames=headers)
        if writeheader:
            csvwriter.writeheader()
        csvwriter.writerow(dict(zip(headers, Dict(d).gets(headers))))
