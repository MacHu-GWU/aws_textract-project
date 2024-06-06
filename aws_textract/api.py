# -*- coding: utf-8 -*-

"""
Public APIs.

Usage example::

    import aws_textract.api as aws_textract

    aws_textract.better

See full list of public APIs at
https://github.com/MacHu-GWU/aws_textract-project/blob/main/tests/test_api.py
"""

from .better_boto import api as better_boto
from .response import api as res
