"""
Pure-Python library that enables generation and verification of
`Pratt certificates \
<https://en.wikipedia.org/wiki/Primality_certificate#Pratt_certificates>`__
for prime numbers.
"""
from __future__ import annotations
from typing import Union, Optional, Dict, Sequence, Iterable, Callable
import doctest
from secrets import randbelow

def _valid(primes: Iterable[int]) -> Iterable[int]:
    """
    Confirm that the result of a callable prime factors parameter to
    :obj:`pratts` is an iterable of valid integers.
    """
    if not isinstance(primes, Iterable):
        raise RuntimeError('primes parameter callable must return an iterable')

    for p in primes:
        if not isinstance(p, int):
            raise RuntimeError('primes parameter callable must return integers')

        if p < 1:
            raise RuntimeError(
                'primes parameter callable must return positive integers'
            )

        yield p

def _lucas(n: int, factors: Iterable[int]) -> bool:
    """
    Confirm that the input ``n`` is prime using Lucas' theorem (assuming
    that the supplied iterable of ``factors`` contains only prime numbers).

    >>> _lucas(2, [])
    True
    >>> _lucas(23, [2, 11])
    True
    >>> _lucas(25, [2, 3])
    False
    """
    if n == 2:
        return True

    for _ in range(100):
        a = 2 + randbelow(n - 2)
        if (
            pow(a, n - 1, n) == 1
            and
            all(pow(a, (n-1) // p, n) != 1 for p in factors)
        ):
            return True

    return False

def pratts(
        argument: int,
        primes: Union[Iterable[int], Callable[[int], Iterable[int]]] = None,
        partial: bool = False
    ) -> Optional[Dict[int, Optional[Sequence[int]]]]:
    # pylint: disable=too-many-branches
    """
    Build a Pratt certificate for the supplied integer argument and the
    accompanying iterable of prime factors.

    :param argument: The prime number for which to generate a certificate.
    :param primes: List of -- or a function that returns -- prime factors.
    :param partial: Flag to allow generation of a best-effort partial certificate.

    This function returns a dictionary in which the keys consist of all primes
    ``p`` for which a certificate was found during the process of generating
    the certificate for the argument (including the argument itself). Each key
    is associated with the list of prime factors of ``p - 1`` (such that every
    prime factor in these lists also appears as a key in the dictionary).

    >>> pratts(2)
    {2: []}
    >>> pratts(3, [2])
    {2: [], 3: [2]}
    >>> pratts(5, [2])
    {2: [], 5: [2]}
    >>> pratts(7, [2, 3])
    {2: [], 3: [2], 7: [2, 3]}
    >>> pratts(11, [2, 5])
    {2: [], 5: [2], 11: [2, 5]}
    >>> pratts(41, [2, 5])
    {2: [], 5: [2], 41: [2, 5]}
    >>> pratts(241, [2, 3, 5])
    {2: [], 3: [2], 5: [2], 241: [2, 3, 5]}
    >>> pratts(257, [2])
    {2: [], 257: [2]}

    It is also possible to supply a function that returns all prime factors
    of its integer input (as an iterable of integers). Note that this function
    must return its input as one of the factors of that input.

    >>> pratts(241, lambda n: [k for k in range(2, n + 1) if n % k == 0])
    {2: [], 3: [2], 5: [2], 241: [2, 3, 5]}

    An exception is raised If the supplied function behaves incorrectly.
    
    >>> pratts(241, lambda n: 1)
    Traceback (most recent call last):
      ...
    RuntimeError: primes parameter callable must return an iterable
    >>> pratts(241, lambda n: ['abc'])
    Traceback (most recent call last):
      ...
    RuntimeError: primes parameter callable must return integers
    >>> pratts(241, lambda n: [-1])
    Traceback (most recent call last):
      ...
    RuntimeError: primes parameter callable must return positive integers

    An example involving a larger prime is presented below.

    >>> certificate = pratts(
    ...     1011235813471123581347,
    ...     [
    ...         2, 3, 5, 7, 11, 17, 19, 31, 97, 229, 251, 463, 5953,
    ...         44449, 177797, 250027, 206955709, 8830800103031
    ...     ]
    ... )
    >>> from pprint import pprint
    >>> pprint(certificate)
    {2: [],
     3: [2],
     5: [2],
     7: [2, 3],
     11: [2, 5],
     17: [2],
     19: [2, 3],
     31: [2, 3, 5],
     97: [2, 3],
     229: [2, 3, 19],
     251: [2, 5],
     463: [2, 3, 7, 11],
     5953: [2, 3, 31],
     44449: [2, 3, 463],
     177797: [2, 44449],
     250027: [2, 3, 7, 5953],
     206955709: [2, 3, 97, 177797],
     8830800103031: [2, 5, 17, 251, 206955709],
     1011235813471123581347: [2, 229, 250027, 8830800103031]}

    A certificate can be verified by supplying its keys to this function.

    >>> pratts(1011235813471123581347, certificate.keys()) is not None
    True

    If the ``partial`` parameter is ``True``, then a partial certificate may
    be returned if a complete certificate could not be generated. In particular,
    any key ``p`` for which a prime factorization of ``p - 1`` could not be
    determined is associated with ``None`` in the certificate.

    >>> pratts(241, [2, 5], True)
    {2: [], 5: [2], 241: None}
    >>> pratts(1011235813471123581347, [], True)
    {1011235813471123581347: None}

    When supplied an input that can be determined to be composite, ``None``
    is returned.

    >>> pratts(4, [2, 3]) is None
    True
    >>> pratts(6, [2, 5]) is None
    True
    >>> pratts(24, [2, 5, 11, 23]) is None
    True

    If the supplied input does not contain sufficiently many primes to
    obtain all the prime factorizations necessary to build a certificate,
    then an exception is raised (which also specifies at least one example
    of a ``p - 1`` term that could not be factored).

    >>> pratts(3, [])
    Traceback (most recent call last):
      ...
    RuntimeError: cannot find all prime factors for 2
    >>> pratts(1011235813471123581347, [8830800103031])
    Traceback (most recent call last):
      ...
    RuntimeError: cannot find all prime factors for 8830800103030
    >>> pratts(1011235813471123581347)
    Traceback (most recent call last):
      ...
    RuntimeError: cannot find all prime factors for 1011235813471123581346
    >>> pratts(24)
    Traceback (most recent call last):
      ...
    RuntimeError: cannot find all prime factors for 23

    An exception is raised if any of the supplied arguments are not valid.

    >>> pratts('abc')
    Traceback (most recent call last):
      ...
    TypeError: argument must be an integer
    >>> pratts(-123)
    Traceback (most recent call last):
      ...
    ValueError: argument must be a positive integer
    >>> pratts(3, primes=2)
    Traceback (most recent call last):
      ...
    TypeError: primes parameter must be an iterable or callable
    >>> pratts(3, ['abc'])
    Traceback (most recent call last):
      ...
    ValueError: every prime factor must be an integer
    >>> pratts(3, [1])
    Traceback (most recent call last):
      ...
    ValueError: every prime factor must be greater than 1
    >>> pratts(25, [6])
    Traceback (most recent call last):
      ...
    RuntimeError: cannot find all prime factors for 5
    """
    if primes is None:
        primes = []

    if not isinstance(argument, int):
        raise TypeError('argument must be an integer')

    if argument < 1:
        raise ValueError('argument must be a positive integer')

    if not isinstance(primes, (Iterable, Callable)):
        raise TypeError('primes parameter must be an iterable or callable')

    # Ensure that the iterable is retained and reusable.
    if isinstance(primes, Iterable):
        primes = list(primes)

        if not all(isinstance(p, int) for p in primes):
            raise ValueError('every prime factor must be an integer')

        if not all(p > 1 for p in primes):
            raise ValueError('every prime factor must be greater than 1')

        # The prime factors must be sorted in ascending order.
        primes = list(sorted(primes))

    # Handle the base cases.
    if argument == 2:
        return {2: []}

    # Build a dictionary representing a certificate for the supplied argument.
    certificate = {}
    for p in (
        (primes if isinstance(primes, list) else list(_valid(primes(argument)))) +
        [argument]
    ):
        # The prime ``2`` is the base case; its entry in a
        # certificate is always an empty list by definition.
        if p == 2:
            certificate.update({2: []})
            continue

        # Find all factors of ``p - 1`` using the supplied
        # list of prime factors.
        n = p - 1
        factors = set()
        for q in primes if isinstance(primes, list) else list(_valid(primes(n))):
            if q < p:
                while n % q == 0:
                    n = n // q
                    factors.add(q)

        # If not all factors of ``p - 1`` are available, then
        # either return a partial certificate (if one has been
        # requested) or indicate that it is not possible to
        # generate a certificate or to confirm that the number
        # is composite.
        if n > 1:
            if partial:
                certificate[p] = None # Partial certificate.
                continue

            # It is not known at this point whether the input
            # is prime, so raise an exception.
            raise RuntimeError(
                'cannot find all prime factors for ' + str(p - 1)
            )

        # At this point, all prime factors of ``p - 1`` are
        # known. If using these prime factors within Lucas'
        # theorem does not prove that the input is prime, it
        # must be composite.
        if not _lucas(p, factors):
            return None # This candidate is definitively composite.

        # Generate an entry for the certificate.
        certificate.update({p: list(sorted(factors))})

        # For each factor, add a certificate of its primality to
        # the joint certificate being built up in this invocation.
        for f in factors:
            certificate_ = pratts(
                f,
                primes=(
                    [p for p in primes if p < f]
                    if isinstance(primes, list)
                    else primes
                )
            )

            # A recursive invocation should never return ``None``,
            # as prime factors should never be composite.
            if certificate_ is None:
                raise RuntimeError( # pragma: no cover
                    'factor ' + str(f) + ' is not prime'
                )

            # Update the certificate with the additional partial
            # certificate returned by the recursive call.
            certificate.update(certificate_)

    # Always sort the entries in the certificate such that
    # the keys are in ascending order.
    return dict(sorted(certificate.items()))

if __name__ == '__main__': # pragma: no cover
    doctest.NORMALIZE_WHITESPACE = True
    doctest.testmod()
