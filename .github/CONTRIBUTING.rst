Thank you for your interest in contributing to Junction. We welcome all
contributions and greatly appreciate your effort!

Bugs and Features
-----------------

If you have found any bugs or would like to request a new feature, please do
check in the project's GitHub `issue tracker`_, if there is a similar existing
issue already filed. If not, please file a new issue.

If you want to help out by fixing bugs, choose an issue from the `issue
tracker`_ to work on and claim it by posting a comment saying "I would like to
work on this.". Feel free to ask any doubts in the issue thread.

Once you have implemented the feature to an extent, go ahead and file a pull
request by following the tips below. File a pull request early to get feedback
as early as possible.

Pull Requests
-------------

Pull Requests should be small to facilitate easier review. Keep them
self-contained, and limited in scope. Studies have shown that review quality
falls off as patch size grows. Sometimes this will result in many small PRs to
land a single large feature.
Checklist:

1. Always create a new branch to work on a new issue::

    $ git checkout -b <branch-name>

2. Make sure your branch is up-to-date with upstream master before you file
   a pull request.
3. All pull requests *must* be made against the ``master`` branch.
4. Include tests for any functionality you implement. Contributions that
   improve existing tests are welcome.
5. Update documentation as necessary and provide documentation for any new
   functionality.
6. In case of UI changes, please include screenshots.

If you do make any changes to models (modification or addition), make sure to
run ``python manage.py makemigrations`` to enable the server to migrate existing
data to the new models.

Commit Guidelines
-----------------

It is advised to care of the following while committing any change:

1. Separate subject from body with a blank line
2. Limit the subject line to 50 characters
3. Capitalize the subject line
4. Do not end the subject line with a period
5. Use the imperative mood in the subject line
6. Wrap the body at 72 characters
7. Use the body to explain what and why vs. how

Do note that the above are meant to be guidelines and not lines set in stone.

Source and Credits: `How to Write a Git Commit Message`_ by Chris Beam.

Code Convention
---------------

We follow the `Black Coding Style`_, and sort our imports with `isort`_. This
code style is enforced with automation.

.. _`issue tracker`: https://github.com/pythonindia/junction/issues
.. _`How to Write a Git Commit Message`: https://chris.beams.io/posts/git-commit/
.. _`isort`: https://isort.readthedocs.org/en/latest/
.. _`Black Coding Style`: https://black.readthedocs.io/en/latest/the_black_code_style.html
