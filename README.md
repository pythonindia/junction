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


<h5>To setup this on your local system follow the steps: </h5>
<p>Run the following commands on your shell to setup this project on your mac</p>
<p>To start with you need to setup docker for this.</p>
<p><code>brew install docker-compose</code></p>
<p>Ensure that docker is installed on your environment. You can check it using command<code>which docker</code>. </p><p>If docker is not installed on your system you can install it using <code>brew install docker</code></p>
<p>Now check the path <code>$PATH</code>. If <code>/usr/local/bin</code> is not included in the output you may need to add it. You can add it to your <code>~/.zshrc</code> file like this</p>
<pre><code>echo 'export PATH="$PATH:/usr/local/bin"' >> ~/.zshrc</code></pre>
<p>If you are using the docker desktop then login like this: </p>
<code>docker login</code>
<p>IF your not using the docker desktop then login like this: </p>
<code>docker login --username <your-username></code>
<p>Moving further follow the docs </p>
[docs]: https://in-junction.readthedocs.io/en/latest/development/getting-started.html
<h1>License</h1>
-------

This software is licensed under The MIT License(MIT). See the [LICENSE][LICENSE] file in the top distribution directory for the full license text.

[LICENSE]: https://github.com/pythonindia/junction/blob/master/LICENSE
