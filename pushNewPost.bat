@echo off
pushd .\metaScripts\
python Conv2HTML.py
popd
git add .
git commit -m "Changed Something Owo"
git push -u origin master