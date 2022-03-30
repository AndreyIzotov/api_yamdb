import os
import csv

from reviews.models import Comment

cwd = os.getcwd()
files = os.listdir(cwd)
print("Files in %r: %s" % (cwd, files))

# with open('api_yamdb/static/data/comments.csv', newline='') as f:
#    reader = csv.reader(f)
#    for row in reader:
#        print(row)

with open(
        'api_yamdb/static/data/comments.csv',
        'r',
        newline=''
    ) as f:
        reader = csv.reader(f)
        for row in reader:
            _, created = Comment.objects.get_or_create(
                id=row[0],
                review_id=row[1],
                text=row[2],
                author=row[3],
                pub_date=row[4]
                )