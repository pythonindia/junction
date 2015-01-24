# Contributing

All contributions are much welcome and greatly appreciated! Expect to be credited for you effort.


## General

Generally try to limit the scope of any Pull Request to an atomic update if possible. This way, it's much easier to assess and review your changes.

You should expect a considerably faster turn around if you submit two or more PRs instead of baking them all into one major PR.


## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. All the pull requests are made against `master` branch.

2. The pull request should include tests.

3. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in README.md.

4. The pull request containing UI changes should have screen shots.

5. If you are already not added to `CONTRIBUTORS.txt`, please add yourself in :)

## Conventions

- Read and pay attention to current code in the repository
- For the Python part, we follow pep8 in most cases. We use [`flake8`](http://flake8.readthedocs.org/en/latest/) to check for linting errors. Once you're ready to commit changes, check your code with `flake8` with this command -

        flake8 --max-complexity=24 --statistics --benchmark --ignore=E5,F4 <project_dir>/

If there is any error, fix it and then commit.

- For the Django part, we follow standard [Django coding style](https://docs.djangoproject.com/en/1.7/internals/contributing/writing-code/coding-style/).

- If you are changing/creating any model, use `./manage.py makemigrations <appname>` to generate the migrations. Send PR. Let other's review the models.

- And always remember the Zen.
