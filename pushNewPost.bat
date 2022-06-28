@echo off
python metaScripts/Conv2HTML.py 
git add .
git commit -m "Changed Something Owo"
git push -u origin master