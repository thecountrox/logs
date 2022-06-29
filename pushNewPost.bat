@echo off
pushd .\metaScripts\
python Conv2HTML.py
popd
git add .
git commit -m "Posted Something New!"
git push -u origin master