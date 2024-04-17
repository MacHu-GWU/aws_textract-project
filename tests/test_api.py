# -*- coding: utf-8 -*-

from aws_textract import api


def test():
    _ = api


if __name__ == "__main__":
    from aws_textract.tests import run_cov_test

    run_cov_test(__file__, "aws_textract.api", preview=False)
