# Updating the PyCAC docs

Updated Feb 02 2020

Copyright (c) 2017-2018 Georgia Institute of Technology. All Rights Reserved.

## Setting up MkDocs

The documentation is deployed using [MkDocs](https://www.mkdocs.org/#mkdocs), and uses the [PyMdown](https://squidfunk.github.io/mkdocs-material/extensions/pymdown/) extenstion to render TeX markup using MathJax. 

Installation instructions can be found on the respective project documentation. Or use pip to install necessary libraries.

```
pip install -r requirements.txt
```


## Directory format
In the root directory, `mkdocs.yml` contains the site layout, under the `nav` tag. The chapters and subpages are organized in the `docs` folder relative to the root directory:
```
    /
    /mkdocs.yml
    /docs/chapter1/README.md
    /docs/chapter1/publications.md
    /docs/chapter2/README.md
    ....
```

## Testing changes
Test changes on the `doc-staging` [GitHub branch](https://github.com/GT-McDowell-Lab/PyCAC/tree/doc-staging) before updating the gh-pages branch. To view changes locally, at http://127.0.0.1:8000 

```
mkdocs serve
``` 

Depending on your installation process, you may need to do:

```
python -m mkdocs serve
```


## Deploying documentation updates
Once satisfied with the changes, MkDocs will automatically update the HTML pages on the gh-pages branch (by default). No need to manually push to gh-pages!

```
mkdocs gh-deploy
```

## Updating the staging branch
Once changes are finalized, commit your changes to the `doc-staging` branch

## Pro tips
When embedding using HTML tags (e.g. for video files), must move up one relative directory. See chapter 7 for examples.