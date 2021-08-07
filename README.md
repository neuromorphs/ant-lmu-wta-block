Installation Instructions
=========================

This package is set up to be installed with the normal python approach:

```
git clone https://github.com/neuromorphs/ant-lmu-wta-block
pip install -e ant-lmu-wta-block
```

Important: remember to include the `-e` option!  Otherwise every time you make
a change to the code in the repository, you'll have to re-install it!


Developer Guidelines
====================

Since this is a project that multiple people will be contributing to, we're
going to attempt to follow some basic software development guidelines.  In
particular, we will:

 - use git branches to develop new features
 - use pytest to test the features
 - use flake8 to enforce basic coding standards


Branches
--------

If you are adding a new feature to the code, start by creating a new git
branch.  This is sort of a separate version of the code base where you can
make changes without interfering with what other people are doing:

```
git checkout -b my_feature_name
```

Now make your changes and make new files and do whatever development you
are planning on doing.  When you are happy with your changes, you now need
to tell `git` about which files you changed and added by doing a `git add`:

```
git add some_file_I_changed.py
git add directory/some_other_file_in_a_subdirectory.py
git add a_totally_new_file.py
```

Once the various files that make up your changes have been added, you need
to also do a `git commit`, which group the additions together with a comment
that tells other people what you've done.

```
git commit -m "Added a new example feature"
```

Once changes have been added and committed, you can go back to the main version
of your code by using the `git checkout` command.

```
git checkout main
```

And you can return to your branch similarly:

```
git checkout my_feature_name
```

Finally, you can do a `git push` to send your changes off to Github so that
other people can have access to your changes:

```
git push
```

Warning: if you are not used to using `git`, there can be a bit of a learning
curve.  The instructions above should all work, but it is quite easy to do
some of the commands wrong and make things very confusing.  There is a reason
that this XKCD comic exists: https://xkcd.com/1597/ and the advice given in
that comic holds pretty well.  If you do run into problems, ask for help.


Testing with pytest
-------------------

The `pytest` framework gives a quick way of defining a bunch of scripts that
can be automatically run to check that the system is working as expected.
Ideally, each new feature added to the software will have an accompanying set
of tests that make sure the feature works as expected.  Tests can be at a very
small scale (i.e. testing one particular function or class -- a "unit" test)
or at larger scales (i.e. functional / integration / end-to-end tests).
Basically, any time there's something where there's a clear "if I do X then I
should get Y as an output" sort of thing, that's a good indication that a
test should be written for that.

Tests are stored in the `tests` subdirectory of the module that they are for.
The file names should start with `test_`.  Each test is a separate function
whose name starts with `test_`.  If the function exits normally, then the test
passes.  If it does not (i.e. if there's an assert failure or some other
Exception is raised), then the test fails.

To install `pytest`, do `pip install pytest`.  You can run all the tests by
going to the `tests` directory and running

```
pytest
```

To run just the tests in one file, do

```
pytest test_filename.py
```

To run one particular test inside one file, do

```
pytest test_filename.py::test_one_particular_test
```

Whenever you have finished working on a particular feature and want to have
it included in the `main` branch, first make sure that 1) you have new tests
for that feature, 2) the new tests pass, and 3) all the old tests also still
pass.


Coding style and flake8
-----------------------

As one final programming aspect, we'll also try to follow the standard style
guide for Python code: https://www.python.org/dev/peps/pep-0008/

A tool for enforcing this is `flake8`, which can be installed with
`pip install flake8`.  If you run `flake8 filename` it will give you a
list of style-guide violations.  If you get no output at all, then your
code is following the style guide.
