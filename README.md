Junction
---

[![Build Status](https://travis-ci.org/pythonindia/junction.svg)](https://travis-ci.org/pythonindia/junction) [![Coverage Status](https://coveralls.io/repos/pythonindia/junction/badge.svg?branch=master)](https://coveralls.io/r/pythonindia/junction?branch=master) [![Requirements Status](https://requires.io/github/pythonindia/junction/requirements.svg?branch=master)](https://requires.io/github/pythonindia/junction/requirements/?branch=master) [![Documentation Status](https://readthedocs.org/projects/in-junction/badge/?version=latest)](https://in-junction.readthedocs.io/en/latest/?badge=latest)

Junction is a software to manage proposals, reviews, schedule, feedback during conference.

Project Setup using Docker
--------------------------

Prerequisites:
1. Docker: You can download and install Docker from the official website at https://www.docker.com/get-started.

Instructions:
1. Copy the .env.sample file to a new .env file by running the following command: ```cp .env.sample .env```
2. Create a local development settings file by running the following command: ```cp settings/dev.py.sample settings/dev.py```
3. Build the junction_local image using the following command: ```docker build -t junction_local .```
4. Start the project by running the following command: ```docker-compose up```
5. Access the application at https://localhost:8888.

Contributing
------------

1. Choose an [issue][issue-list] and ask any doubts in the issue thread.
2. Report any bugs/feature request as Github [new issue][new-issue], if it's already not present.
3. If you are starting to work on an issue, please leave a comment saying "I am working on it".
4. You can set up the project using the [Getting Started][getting-started] guide.
5. Once you are done with feature/bug fix, send a pull request according to the [guidelines][guidelines].

[issue-list]: https://github.com/pythonindia/junction/issues/
[new-issue]: https://github.com/pythonindia/junction/issues/new
[guidelines]: .github/CONTRIBUTING.rst
[getting-started]: https://in-junction.readthedocs.io/en/latest/development/getting-started.html

License
-------

This software is licensed under The MIT License(MIT). See the [LICENSE][LICENSE] file in the top distribution directory for the full license text.

[LICENSE]: https://github.com/pythonindia/junction/blob/master/LICENSE
