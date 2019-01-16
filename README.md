# Web Scrapers for Dragonfable accessories and weapons

###Scrapes the DF forums to get all the useful data for accessories and weapons using python 2.

Both scrapers takes in 3 arguments, which page to start, how many rows to initially skip, and how many pages to go over
For example, to get all accessories, run:
```commandline
python AccessoryScraperBy.py 1 3 80
```
Starts on page 1, skips first 3 rows (which are pinned), finish on page 81 (80+1)



####To get all the items faster, you can run simultaneous processes.
For example, you can run these commands all at the same time
```commandline
python AccessoryScraperBy.py 1 3 9
python AccessoryScraperBy.py 11 0 9
.
.
.
python AccessoryScraperBy.py 81 0 0
```
WeaponsBy.py and AccessoryBy.py contain helper functions.
####After getting multiple json files from running simultaneous processes, use JSONjoin.py to merge them all into 1 file
The argument it takes in is the directory that all the JSON files are stored.
```commandline
python JSONjoin.py Weapons
```

####What I did with the data
Use power query in Excel to convert the json to sheets which are uploaded to google sheets
