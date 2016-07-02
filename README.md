junction
========

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

[![Build Status](https://travis-ci.org/pythonindia/junction.svg)](https://travis-ci.org/pythonindia/junction) [![Coverage Status](https://coveralls.io/repos/pythonindia/junction/badge.svg?branch=master)](https://coveralls.io/r/pythonindia/junction?branch=master) [![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/pythonindia/junction?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Requirements Status](https://requires.io/github/pythonindia/junction/requirements.svg?branch=master)](https://requires.io/github/pythonindia/junction/requirements/?branch=master)

**Version**: 0.3.1

Junction is a software to manage proposals, reviews, schedule, feedback during conference.

Setup
=====

It is advised to install all the requirements inside [virtualenv], use [virtualenvwrapper] to manage virtualenvs.

[virtualenv]: https://virtualenv.pypa.io/en/latest/
[virtualenvwrapper]: https://virtualenvwrapper.readthedocs.org/en/latest/

```
sudo apt-get install libpq-dev python-dev
pip install -r requirements-dev.txt
cp settings/dev.py.sample settings/dev.py
python manage.py migrate --noinput
python manage.py sample_data
```

Initial auth data: admin/123123

If docker and docker-compose are not installed already (Not mandatory):
--------------------------------------------
Refer to (http://docs.docker.com/installation/) for detailed installation instructions.

```
curl -sSL https://get.docker.com/ | sudo sh
sudo pip install docker-compose
```

Create aliases for docker and docker-compose to avoid running them with sudo everytime.
Append the following lines to your ~/.bashrc or ~/.zshrc

```
alias docker='sudo docker'
alias docker-compose='sudo docker-compose'
```

Finally, run
```
docker-compose up
```


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
2. Report any bugs/feature request as Github [new issue][new-issue], if it's already not present.
3. If you are starting to work on an issue, please leave a comment saying "I am working on it".
4. Once you are done with feature/bug fix, send a pull request according to the [guidelines].

[issue-list]: https://github.com/pythonindia/junction/issues/
[new-issue]: https://github.com/pythonindia/junction/issues/new
[guidelines]: https://github.com/pythonindia/junction/blob/master/CONTRIBUTING.md

## Contributors

* Aayush ([@Aayush-Kasurde])
* Abhijeet ([@Akasurde])
* Anand B Pillai ([@pythonhacker])
* Anand Chitipothu ([@anandology])
* Anand Pandikunta ([@ChillarAnand])
* Ankesh Anand ([@ankeshanand])
* Anshul Sharma ([@raun])
* Anuvrat Parashar ([@bhanuvrat])
* arjoonn sharma ([@theSage21])
* dhilipsiva ([@dhilipsiva])
* Fayaz Yusuf Khan ([@fayazkhan])
* Ganeshkumar S ([@ganeshks])
* Haris Ibrahim K. V. ([@harisibrahimkv])
* Imran Ahmed ([@rekenerd])
* jaocb  ([@jklmn13])
* Kishor Bhat ([@therealkbhat])
* Kracekumar Ramaraj ([@kracekumar])
* Kumar Anirudha ([@anistark])
* Mudassir ([@mudassir0909])
* Nabeel Valapra ([@nabeelvalapra])
* Parbhat Puri ([@Parbhat])
* Parth Oberoi ([@hTrap])
* Saurabh Kumar ([@theskumar])
* Sivasubramaniam Arunachalam ([@sivaa])
* [@sjose1x]
* Sumit Chahal ([@smtchahal])
* Vignesh Sarma K ([@vigneshsarma])
* Vijay ([@vnbang2003])

[@Aayush-Kasurde]: https://github.com/Aayush-Kasurde
[@Akasurde]: https://github.com/Akasurde
[@anandology]: https://github.com/anandology
[@anistark]: https://github.com/anistark
[@ankeshanand]: https://github.com/ankeshanand
[@bhanuvrat]: https://github.com/bhanuvrat
[@ChillarAnand]: https://github.com/ChillarAnand
[@dhilipsiva]: https://github.com/dhilipsiva
[@fayazkhan]: https://github.com/fayazkhan
[@ganeshks]: https://github.com/ganeshks
[@gitter-badger]: https://github.com/gitter-badger
[@harisibrahimkv]: https://github.com/harisibrahimkv
[@hTrap]: https://github.com/hTrap
[@jklmn13]: https://github.com/jklmn13
[@kracekumar]: https://github.com/kracekumar
[@mudassir0909]: https://github.com/mudassir0909
[@nabeelvalapra]: https://github.com/nabeelvalapra
[@Parbhat]: https://github.com/Parbhat
[@pythonhacker]: https://github.com/pythonhacker
[@raun]: https://github.com/raun
[@rekenerd]: https://github.com/rekenerd
[@sivaa]: https://github.com/sivaa
[@sjose1x]: https://github.com/sjose1x
[@smtchahal]: https://github.com/smtchahal
[@therealkbhat]: https://github.com/therealkbhat
[@theSage21]: https://github.com/theSage21
[@theskumar]: https://github.com/theskumar
[@vigneshsarma]: https://github.com/vigneshsarma
[@vnbang2003]: https://github.com/vnbang2003


License
-------

This software is licensed under The MIT License(MIT). See the [LICENSE][LICENSE] file in the top distribution directory for the full license text.

[LICENSE]: https://github.com/pythonindia/junction/blob/master/LICENSE
