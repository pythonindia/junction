Junction | [![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/pythonindia/junction?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Build Status](https://travis-ci.org/pythonindia/junction.svg)](https://travis-ci.org/pythonindia/junction) [![Coverage Status](https://coveralls.io/repos/pythonindia/junction/badge.svg?branch=master)](https://coveralls.io/r/pythonindia/junction?branch=master) [![Requirements Status](https://requires.io/github/pythonindia/junction/requirements.svg?branch=master)](https://requires.io/github/pythonindia/junction/requirements/?branch=master)
========


**Version**: 0.3.2

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

0. Aayush ([@Aayush-Kasurde](https://github.com/Aayush-Kasurde))
0. Abhijeet ([@Akasurde](https://github.com/Akasurde))
0. AMiT Kumar ([@aktech](https://github.com/aktech))
0. Anand B Pillai ([@pythonhacker](https://github.com/pythonhacker))
0. Anand Chitipothu ([@anandology](https://github.com/anandology))
0. Anand Pandikunta ([@ChillarAnand](https://github.com/ChillarAnand))
0. Anirudh ([@animenon](https://github.com/animenon))
0. Ankesh Anand ([@ankeshanand](https://github.com/ankeshanand))
0. Anshul Sharma ([@raun](https://github.com/raun))
0. Anuvrat Parashar ([@bhanuvrat](https://github.com/bhanuvrat))
0. arjoonn sharma ([@theSage21](https://github.com/theSage21))
0. Deep Sukhwani ([@ProProgrammer](https://github.com/ProProgrammer))
0. dhilipsiva ([@dhilipsiva](https://github.com/dhilipsiva))
0. Fayaz Yusuf Khan ([@fayazkhan](https://github.com/fayazkhan))
0. Ganeshkumar S ([@ganeshks](https://github.com/ganeshks))
0. [@gangadharmgithub](https://github.com/gangadharmgithub)
0. Geetanjali  ([@geetanjaligg](https://github.com/geetanjaligg))
0. Hari ([@haridjango123](https://github.com/haridjango123))
0. Haris Ibrahim K. V. ([@harisibrahimkv](https://github.com/harisibrahimkv))
0. Imran Ahmed ([@rekenerd](https://github.com/rekenerd))
0. Indradhanush Gupta ([@indradhanush](https://github.com/indradhanush))
0. jaocb  ([@jklmn13](https://github.com/jklmn13))
0. Karanveer Singh ([@kvsingh](https://github.com/kvsingh))
0. Kenith Aiyappa ([@K-7](https://github.com/K-7))
0. Kishor Bhat ([@therealkbhat](https://github.com/therealkbhat))
0. Kracekumar Ramaraj ([@kracekumar](https://github.com/kracekumar))
0. Kumar Anirudha ([@anistark](https://github.com/anistark))
0. Mudassir ([@mudassir0909](https://github.com/mudassir0909))
0. Nabeel Valapra ([@nabeelvalapra](https://github.com/nabeelvalapra))
0. Navaneethan ([@nava45](https://github.com/nava45))
0. Noufal Ibrahim ([@nibrahim](https://github.com/nibrahim))
0. Parbhat Puri ([@Parbhat](https://github.com/Parbhat))
0. Parth Oberoi ([@hTrap](https://github.com/hTrap))
0. Peeyush Aggarwal ([@PeeyushAgg](https://github.com/PeeyushAgg))
0. Puneeth Chaganti ([@punchagan](https://github.com/punchagan))
0. [@rahulrb0509](https://github.com/rahulrb0509)
0. Sai Krishna ([@psykrsna](https://github.com/psykrsna))
0. Saurabh ([@saurabh-fueled](https://github.com/saurabh-fueled))
0. Saurabh Kumar ([@theskumar](https://github.com/theskumar))
0. Shrayas Rajagopal ([@shrayasr](https://github.com/shrayasr))
0. Sivasubramaniam Arunachalam ([@sivaa](https://github.com/sivaa))
0. [@sjose1x](https://github.com/sjose1x)
0. Sumit Chahal ([@smtchahal](https://github.com/smtchahal))
0. Suraj Jayakumar ([@sjayakum](https://github.com/sjayakum))
0. Suresh R. ([@umulingu](https://github.com/umulingu))
0. Tapasweni Pathak ([@tapasweni-pathak](https://github.com/tapasweni-pathak))
0. The Gitter Badger ([@gitter-badger](https://github.com/gitter-badger))
0. [@vanishan](https://github.com/vanishan)
0. Vignesh Sarma K ([@vigneshsarma](https://github.com/vigneshsarma))
0. Vijay ([@vnbang2003](https://github.com/vnbang2003))
0. vinay singh ([@vinay13](https://github.com/vinay13))
0. VoidspaceXYZ ([@ramaseshan](https://github.com/ramaseshan))

[![Throughput Graph](https://graphs.waffle.io/pythonindia/junction/throughput.svg)](https://waffle.io/pythonindia/junction/metrics/throughput)

License
-------

This software is licensed under The MIT License(MIT). See the [LICENSE][LICENSE] file in the top distribution directory for the full license text.

[LICENSE]: https://github.com/pythonindia/junction/blob/master/LICENSE
