##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Batching Support """

import zope.schema
from zope.interface.common import sequence


__docformat__ = 'restructuredtext'


class IBatch(sequence.IFiniteSequence):
    """A Batch represents a sub-list of the full sequence.

    The Batch constructor takes a list (or any list-like object) of elements,
    a starting index and the size of the batch. From this information all
    other values are calculated.
    """

    sequence = zope.interface.Attribute('Sequence')

    batches = zope.interface.Attribute('Batches')

    start = zope.schema.Int(
        title='Start Index',
        description=('The index of the sequence at which the batch starts. '
                     'If the full sequence is empty, the value is -1.'),
        min=-1,
        default=0,
        required=True)

    size = zope.schema.Int(
        title='Batch Size',
        description='The maximum size of the batch.',
        min=1,
        default=20,
        required=True)

    end = zope.schema.Int(
        title='End Index',
        description='The index of the sequence at which the batch ends.',
        min=-1,
        default=0,
        readonly=True,
        required=True)

    index = zope.schema.Int(
        title='Current Batch Index',
        description='The index of the batch in relation to all batches.',
        min=0,
        readonly=True,
        required=True)

    number = zope.schema.Int(
        title='Current Batch Number',
        description='The number of the batch in relation to all batches.',
        min=1,
        readonly=True,
        required=True)

    total = zope.schema.Int(
        title='Total Number of Batches',
        description='The total number of batches available.',
        min=1,
        readonly=True,
        required=True)

    next = zope.schema.Field(
        title='Next Batch',
        description='The next batch of the sequence; ``None`` if last.',
        readonly=True,
        required=True)

    previous = zope.schema.Field(
        title='Previous Batch',
        description='The previous batch of the sequence; ``None`` if first.',
        readonly=True,
        required=True)

    firstElement = zope.schema.Field(
        title='First Element',
        description='The first element of the batch.',
        readonly=True,
        required=True)

    totalElements = zope.schema.Int(
        title='Total Number of Elements',
        description='Return the length of the full sequence.',
        min=1,
        readonly=True,
        required=True)

    def __iter__():
        """Creates an iterator for the contents of the batch."""

    def __contains__(item):
        """ `x.__contains__(item)` <==> `item in x` """

    def __eq__(other):
        """`x.__eq__(other)` <==> `x == other`"""

    def __ne__(other):
        """`x.__ne__(other)` <==> `x != other`"""
