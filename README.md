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
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install libpq-dev python-dev build-essential tcl
pip install -r requirements-dev.txt
cp settings/dev.py.sample settings/dev.py
python manage.py migrate --noinput
python manage.py sample_data
sudo apt-get -y install redis-server
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

### API

- HTTP API documentation is [here](https://github.com/pythonindia/junction/blob/master/docs/api.md).
- Python Client for junction is [here](https://github.com/pythonindia/junction-client).

## Contributors

<table>
  <tr>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/7703416?v=3><br>Aayush (<a href=https://github.com/Aayush-Kasurde>@Aayush-Kasurde</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/633765?v=3><br>Abhijeet (<a href=https://github.com/Akasurde>@Akasurde</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/788023?v=3><br>Akshay Arora (<a href=https://github.com/akshayaurora>@akshayaurora</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/5647941?v=3><br>Amit Kumar (<a href=https://github.com/aktech>@aktech</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/316177?v=3><br>Anand B Pillai (<a href=https://github.com/pythonhacker>@pythonhacker</a>)</td>
  </tr>
  <tr>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/7569?v=3><br>Anand Chitipothu (<a href=https://github.com/anandology>@anandology</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/6907950?v=3><br>Anirudh (<a href=https://github.com/animenon>@animenon</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/2134563?v=3><br>Ankesh Anand (<a href=https://github.com/ankeshanand>@ankeshanand</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/2016794?v=3><br>Anshul Sharma (<a href=https://github.com/raun>@raun</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/499894?v=3><br>Anuvrat Parashar (<a href=https://github.com/bhanuvrat>@bhanuvrat</a>)</td>
  </tr>
  <tr>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/7693265?v=3><br>arjoonn sharma (<a href=https://github.com/theSage21>@theSage21</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/4463796?v=3><br>Chillar Anand (<a href=https://github.com/ChillarAnand>@ChillarAnand</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/3947424?v=3><br>Deep Sukhwani (<a href=https://github.com/ProProgrammer>@ProProgrammer</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/502170?v=3><br>dhilipsiva (<a href=https://github.com/dhilipsiva>@dhilipsiva</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/1227312?v=3><br>Fayaz Yusuf Khan (<a href=https://github.com/fayazkhan>@fayazkhan</a>)</td>
  </tr>
  <tr>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/5219194?v=3><br>Ganeshkumar S (<a href=https://github.com/ganeshks>@ganeshks</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/8327178?v=3><br><a href=https://github.com/gangadharmgithub>@gangadharmgithub</a></td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/1011202?v=3><br>Geetanjali  (<a href=https://github.com/geetanjaligg>@geetanjaligg</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/13134808?v=3><br>Hari (<a href=https://github.com/haridjango123>@haridjango123</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/717628?v=3><br>Haris Ibrahim K. V. (<a href=https://github.com/harisibrahimkv>@harisibrahimkv</a>)</td>
  </tr>
  <tr>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/645284?v=3><br>Imran Ahmed (<a href=https://github.com/rekenerd>@rekenerd</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/2682729?v=3><br>Indradhanush Gupta (<a href=https://github.com/indradhanush>@indradhanush</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/13776892?v=3><br>jaocb  (<a href=https://github.com/jklmn13>@jklmn13</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/822537?v=3><br>Karanveer Singh (<a href=https://github.com/kvsingh>@kvsingh</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/3635354?v=3><br>Kenith Aiyappa (<a href=https://github.com/K-7>@K-7</a>)</td>
  </tr>
  <tr>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/7105012?v=3><br>Kishor Bhat (<a href=https://github.com/therealkbhat>@therealkbhat</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/311929?v=3><br>Kracekumar Ramaraj (<a href=https://github.com/kracekumar>@kracekumar</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/5357586?v=3><br>Kumar Anirudha (<a href=https://github.com/anistark>@anistark</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/1861842?v=3><br>Mudassir (<a href=https://github.com/mudassir0909>@mudassir0909</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/6704555?v=3><br>Nabeel Valapra (<a href=https://github.com/nabeelvalapra>@nabeelvalapra</a>)</td>
  </tr>
  <tr>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/1247749?v=3><br>Navaneethan (<a href=https://github.com/nava45>@nava45</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/69051?v=3><br>Noufal Ibrahim (<a href=https://github.com/nibrahim>@nibrahim</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/4817493?v=3><br>Parbhat Puri (<a href=https://github.com/Parbhat>@Parbhat</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/5495474?v=3><br>Parth Oberoi (<a href=https://github.com/hTrap>@hTrap</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/14878279?v=3><br>Peeyush Aggarwal (<a href=https://github.com/dhuadaar>@dhuadaar</a>)</td>
  </tr>
  <tr>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/315678?v=3><br>Puneeth Chaganti (<a href=https://github.com/punchagan>@punchagan</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/13493137?v=3><br><a href=https://github.com/rahulrb0509>@rahulrb0509</a></td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/5002019?v=3><br>Ramaseshan (<a href=https://github.com/ramaseshan>@ramaseshan</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/2959038?v=3><br>Ravi Shanker B (<a href=https://github.com/ravishanker404>@ravishanker404</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/1109442?v=3><br>Sai Krishna (<a href=https://github.com/psykrsna>@psykrsna</a>)</td>
  </tr>
  <tr>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/3982193?v=3><br>Saurabh (<a href=https://github.com/saurabh-fueled>@saurabh-fueled</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/236356?v=3><br>Saurabh Kumar (<a href=https://github.com/theskumar>@theskumar</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/240368?v=3><br>Shrayas Rajagopal (<a href=https://github.com/shrayasr>@shrayasr</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/2163422?v=3><br>Sivasubramaniam Arunachalam (<a href=https://github.com/sivaa>@sivaa</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/5251453?v=3><br><a href=https://github.com/sjose1x>@sjose1x</a></td>
  </tr>
  <tr>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/6754255?v=3><br>Sumit Chahal (<a href=https://github.com/smtchahal>@smtchahal</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/12380569?v=3><br>Suraj Jayakumar (<a href=https://github.com/sjayakum>@sjayakum</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/5258890?v=3><br>Suresh R. (<a href=https://github.com/umulingu>@umulingu</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/4143778?v=3><br>Tapasweni Pathak (<a href=https://github.com/tapasweni-pathak>@tapasweni-pathak</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/8518239?v=3><br>The Gitter Badger (<a href=https://github.com/gitter-badger>@gitter-badger</a>)</td>
  </tr>
  <tr>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/9103291?v=3><br><a href=https://github.com/vanishan>@vanishan</a></td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/889999?v=3><br>Vignesh Sarma K (<a href=https://github.com/vigneshsarma>@vigneshsarma</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/316253?v=3><br>Vijay (<a href=https://github.com/vnbang2003>@vnbang2003</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/6693374?v=3><br>Vinay Singh (<a href=https://github.com/vinay13>@vinay13</a>)</td>
    <td align=center><img width=100 src=https://avatars.githubusercontent.com/u/7351791?v=3><br>Rahul Arora (<a href=https://github.com/rahulxxarora>@rahulxxarora</a>)</td>
  </tr>
</table>


[![Throughput Graph](https://graphs.waffle.io/pythonindia/junction/throughput.svg)](https://waffle.io/pythonindia/junction/metrics/throughput)

License
-------

This software is licensed under The MIT License(MIT). See the [LICENSE][LICENSE] file in the top distribution directory for the full license text.

[LICENSE]: https://github.com/pythonindia/junction/blob/master/LICENSE
