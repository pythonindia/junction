junction
========

[![Build Status](https://travis-ci.org/pythonindia/junction.svg)](https://travis-ci.org/pythonindia/junction) [![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/pythonindia/junction?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
<!-- fix to mkdocs display these badges correctly -->
<style>
div.col-md-9 img {display: inline-block; padding: 0; border: none; border-radius: 0; margin: 0;}
</style>

Junction is a software to manage proposals, reviews, schedule, feedback during conference.

Setup
=====

It is advised to install all the requirements inside [virtualenv], use [virtualenvwrapper] to manage virtualenvs.

[virtualenv]: https://virtualenv.pypa.io/en/latest/
[virtualenvwrapper]: https://virtualenvwrapper.readthedocs.org/en/latest/

```
pip install -r requirements-dev.txt
cp settings/dev.py.sample settings/dev.py
python manage.py migrate --noinput
python manage.py sample_data
```

Initial auth data: admin/123123

Configuring Django-allauth
---------------------------

 - Go to `http://localhost:8000/nimda/sites/site/` 
 - Change the default site's(the one with ID = 1) name and display to `localhost:8000`
 - Go to `Social Applications` in admin panel and add [Github](http://django-allauth.readthedocs.org/en/latest/providers.html#github) and [Google](http://django-allauth.readthedocs.org/en/latest/providers.html#google)'s auth details

Making Frontend Changes
---------------------------
Make sure you have nodejs, npm, bower, grunt-cli & grunt installed

```
$ cd junction/static
$ npm install
$ bower install
$ grunt // This starts a watcher to watch for file changes
```


Contributing
------------

1. Choose an [issue][issue-list] and ask any doubts in the issue thread.
2. Report any bugs/feature request as github [new issue][new-issue], if it's already not present.
3. If you are starting to work on an issue, please leave a comment saying "I am working on it".
4. Once you are done with feature/bug fix, send a pull request according to the [guidelines]. 

[issue-list]: https://github.com/pythonindia/junction/issues/
[new-issue]: https://github.com/pythonindia/junction/issues/new
[guidelines]: https://github.com/pythonindia/junction/blob/master/CONTRIBUTING.md
