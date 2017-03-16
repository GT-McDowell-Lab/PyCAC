# cp all files into the github directory
cp -r * /Users/shuozhixu/Public/github/PyCAC/docs/

# cd into the github directory
cd /Users/shuozhixu/Public/github/PyCAC/docs/

# install the plugins and build the static site
gitbook build

# copy the static site files into the current directory.
cp -R _book/* .

# remove 'node_modules' and '_book' directory
#git clean -fx node_modules
#git clean -fx _book

rm -r _book

# add all files
git add .

# commit
git commit -a -m "Update docs"

git push origin master

#git checkout gh-pages

#rm -fr ../.git/rebase-apply

#git rebase master

#git push origin gh-pages

#git checkout master
