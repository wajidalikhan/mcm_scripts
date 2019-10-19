#!/bin/bash
git remote -v
git remote add upstream git@github.com:wajidalikhan/mcm_scripts.git
git remote -v
git fetch upstream
git checkout master
git merge upstream/master
git status
git push
git push
