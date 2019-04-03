Thank you for your interest in contributing to Junction. We welcome all
contributions and greatly appreciate your effort!

Bugs and Features
-----------------

If you have found any bugs or would like to request a new feature, please do
check if there is an existing issue already filed for the same, in the
project's GitHub `issue tracker`_. If not, please file a new issue.

If you want to help out by fixing bugs, choose an issue from the `issue
tracker`_ to work on and claim it by posting a comment saying "I would like to
work on this.". Feel free to ask any doubts in the issue thread.

Once you have implemented the feature to an extent, go ahead and file a pull
request, following the tips below. File a pull request early to get feedback as
early as possible.

Pull Requests
-------------

Pull Requests should be small to facilitate easier review. Keep them
self-contained, and limited in scope. Studies have shown that review quality
falls off as patch size grows. Sometimes this will result in many small PRs to
land a single large feature.

Checklist:

1. All pull requests *must* be made against the ``master`` branch.
2. Include tests for any functionality you implement. Any contributions helping
   improve existing tests is welcome.
3. Update documentation as necessary and provide documentation for any new
   functionality.
4. In case of UI changes, please include screenshots.
5. Add yourself to ``CONTRIBUTORS.txt`` if you're not there already. :)

If you do make any changes to models (modification or addition), make sure to
run ``python manage.py makemigrations`` to enable the server to migrate existing
data to the new models.

Code Convention
---------------

We follow the `Django Coding Style`_ and enforce it using `flake8`_.

In general, if flake8 is happy with your code, you should be fine. To use
``flake8`` to check your code, you can use the following command::

   $ flake8 --max-complexity=24 --statistics --benchmark --ignore=E5,F4 <project_dir>/

.. _`issue tracker`: https://github.com/pythonindia/junction/issues
.. _`flake8`: https://flake8.readthedocs.org/en/latest/
.. _`Django Coding Style`: https://docs.djangoproject.com/en/2.2/internals/contributing/writing-code/coding-style/
