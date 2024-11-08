Junction
---

[![Documentation Status](https://readthedocs.org/projects/in-junction/badge/?version=latest)](https://in-junction.readthedocs.io/en/latest/?badge=latest)

Junction is a software to manage proposals, reviews, schedule, feedback during conference.

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



<p><strong>To setup this on your local system. Follow the steps: </strong></p>
<p>To start with you have to setup docker on your local system. For that you need docker-compose to be installed on your system.</p>
<code>brew install docker-compose</code> for mac<br>
<code>sudo apt install docker-compose</code> for linux<br>

Check the path of the docker-compose using<br><code>echo $PATH</code><br>
If <code>/usr/local/bin</code> is not in your path, you need to add it.<br><pre><code>echo 'export PATH="$PATH:/usr/local/bin"' >> ~/.zshrc
source ~/.zshrc</code></pre>
<p>After accomplishing these steps you need to login into your docker account</p>
<code>docker login</code><br>If you are using the cli version you need to execute <code>docker login username <__username__></code><p>After successfully following these steps you can refer to the docs[getting-started] for further execution of the application</p>
License
-------

This software is licensed under The MIT License(MIT). See the [LICENSE][LICENSE] file in the top distribution directory for the full license text.

[LICENSE]: https://github.com/pythonindia/junction/blob/master/LICENSE






