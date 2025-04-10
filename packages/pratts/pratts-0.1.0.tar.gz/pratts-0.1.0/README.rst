======
pratts
======

Pure-Python library that enables generation and verification of `Pratt certificates <https://en.wikipedia.org/wiki/Primality_certificate#Pratt_certificates>`__ for prime numbers.

|pypi| |readthedocs| |actions| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/pratts.svg#
   :target: https://badge.fury.io/py/pratts
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/pratts/badge/?version=latest
   :target: https://pratts.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |actions| image:: https://github.com/reity/pratts/workflows/lint-test-cover-docs/badge.svg#
   :target: https://github.com/reity/pratts/actions/workflows/lint-test-cover-docs.yml
   :alt: GitHub Actions status.

.. |coveralls| image:: https://coveralls.io/repos/github/reity/pratts/badge.svg?branch=main
   :target: https://coveralls.io/github/reity/pratts?branch=main
   :alt: Coveralls test coverage summary.

Installation and Usage
----------------------
This library is available as a `package on PyPI <https://pypi.org/project/pratts>`__:

.. code-block:: bash

    python -m pip install pratts

The library can be imported in the usual manner:

.. code-block:: python

    import pratts
    from pratts import pratts

Examples
^^^^^^^^
To generate a `Pratt certificate <https://en.wikipedia.org/wiki/Primality_certificate#Pratt_certificates>`__ for a prime number, it is sufficient to supply an iterable of appropriately chosen primes that make it possible to recursively construct the certificate:

.. code-block:: python

    >>> pratts(241, [2, 3, 5])
    {2: [], 3: [2], 5: [2], 241: [2, 3, 5]}


.. |primefactors| replace:: ``primefactors``
.. _primefactors: https://docs.sympy.org/latest/modules/ntheory.html#sympy.ntheory.factor_.primefactors

Alternatively, a function that returns prime factors can be supplied (such as the |primefactors|_ function that is available in the `SymPy library <https://www.sympy.org/>`__):

.. code-block:: python

    >>> from sympy import primefactors
    >>> pratts(241, primefactors)
    {2: [], 3: [2], 5: [2], 241: [2, 3, 5]}

A certificate can be verified by supplying its keys (such that the same certificate is generated and returned):

.. code-block:: python

    >>> certificate = pratts(1011235813471123581347, primefactors)
    >>> pratts(1011235813471123581347, certificate.keys()) is not None
    True
    >>> pratts(1011235813471123581347, certificate.keys()) == certificate
    True

Development
-----------
All installation and development dependencies are fully specified in ``pyproject.toml``. The ``project.optional-dependencies`` object is used to `specify optional requirements <https://peps.python.org/pep-0621>`__ for various development tasks. This makes it possible to specify additional options (such as ``docs``, ``lint``, and so on) when performing installation using `pip <https://pypi.org/project/pip>`__:

.. code-block:: bash

    python -m pip install ".[docs,lint]"

Documentation
^^^^^^^^^^^^^
The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org>`__:

.. code-block:: bash

    python -m pip install ".[docs]"
    cd docs
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. && make html

Testing and Conventions
^^^^^^^^^^^^^^^^^^^^^^^
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org>`__ (see the ``pyproject.toml`` file for configuration details):

.. code-block:: bash

    python -m pip install ".[test]"
    python -m pytest

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`__:

.. code-block:: bash

    python src/pratts/pratts.py -v

Style conventions are enforced using `Pylint <https://pylint.readthedocs.io>`__:

.. code-block:: bash

    python -m pip install ".[lint]"
    python -m pylint src/pratts

Contributions
^^^^^^^^^^^^^
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/reity/pratts>`__ for this library.

Versioning
^^^^^^^^^^
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`__.

Publishing
^^^^^^^^^^
This library can be published as a `package on PyPI <https://pypi.org/project/pratts>`__ via the GitHub Actions workflow found in ``.github/workflows/build-publish-sign-release.yml`` that follows the `recommendations found in the Python Packaging User Guide <https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/>`__.

Ensure that the correct version number appears in ``pyproject.toml``, and that any links in this README document to the Read the Docs documentation of this package (or its dependencies) have appropriate version numbers. Also ensure that the Read the Docs project for this library has an `automation rule <https://docs.readthedocs.io/en/stable/automation-rules.html>`__ that activates and sets as the default all tagged versions.

To publish the package, create and push a tag for the version being published (replacing ``?.?.?`` with the version number):

.. code-block:: bash

    git tag ?.?.?
    git push origin ?.?.?
