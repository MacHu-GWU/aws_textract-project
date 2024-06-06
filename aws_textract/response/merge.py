# -*- coding: utf-8 -*-

"""
The ``get_xyz()`` API requires a valid job id, but a job id only valid for 7 days.
(See, https://docs.aws.amazon.com/textract/latest/dg/API_GetDocumentTextDetection.html)
After that, you cannot get the response from the Textract API. This module provides
a way to get the response from the S3 bucket where the Textract async API stores the response.
"""

import typing as T
import json
from s3pathlib import S3Path

if T.TYPE_CHECKING:  # pragma: no cover
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_textract.type_defs import GetDocumentAnalysisResponseTypeDef
    from mypy_boto3_textract.type_defs import GetDocumentTextDetectionResponseTypeDef
    from mypy_boto3_textract.type_defs import GetExpenseAnalysisResponseTypeDef
    from mypy_boto3_textract.type_defs import GetLendingAnalysisResponseTypeDef


def get_textract_output_s3dir(
    s3bucket: str,
    s3prefix: str,
    job_id: str,
) -> S3Path:
    """
    Figure out the S3 directory where the Textract async API stores the response files.
    You should see a ``.s3_access_check`` and a bunch of JSON files name as .
    "1", "2", "3", ... in the S3 directory.

    :param s3bucket: the OutputConfig["S3Bucket"] in ``start_xyz()`` async API.
    :param s3prefix: the OutputConfig["S3Prefix"] in ``start_xyz()`` async API.
    :param job_id: the JobId in the response of ``start_xyz()`` async API.
    """
    return S3Path(f"s3://{s3bucket}/").joinpath(s3prefix).joinpath(job_id).to_dir()


def _merge_textract_response(
    s3_client: "S3Client",
    s3dir: S3Path,
    key: str,
) -> dict:  # pragma: no cover
    """
    The Textract async API stores the response in multiple files in a temp
    S3 directory. This function merges the response from all the files into one dict.
    The paginator version of the ``textract_client.get_xyz()`` can do the same tricks.
    However, that API requires a valid job id, but a job id only valid for 7 days.
    (See, https://docs.aws.amazon.com/textract/latest/dg/API_GetDocumentTextDetection.html)
    After that, you cannot get the response from the Textract API, but this function
    can still get the response from the S3 bucket.

    :param s3_client: the boto3 S3 client.
    :param s3dir: the S3 directory where the Textract response files are stored.
        The directory should contain a ``.s3_access_check`` file and a bunch of JSON files.
        The directory looks like "s3://{bucket}/{prefix}/{job_id}/", where the bucket
        and prefix are the OutputConfig["S3Bucket"] and OutputConfig["S3Prefix"] in the
        ``start_xyz()`` async API.
    :param key: "Blocks" | "ExpenseDocuments" | "Results".
    """
    res = s3dir.iter_objects(bsm=s3_client).filter(
        lambda x: x.basename != ".s3_access_check"
    )
    # sort by 1, 2, 3 ...
    res = sorted(res, key=lambda x: int(x.basename), reverse=False)
    data = None
    for s3path in res:
        dct = json.loads(s3path.read_text(bsm=s3_client))
        if data is None:
            data = dct
        else:
            data[key].extend(dct.get(key, []))
    return data


def merge_document_analysis_result(
    s3_client: "S3Client",
    s3dir: S3Path,
) -> "GetDocumentAnalysisResponseTypeDef":  # pragma: no cover
    """
    The Textract async API stores the response in multiple files in a temp
    S3 directory. This function merges the response from all the files into one dict.
    The paginator version of the ``textract_client.get_xyz()`` can do the same tricks.
    However, that API requires a valid job id, but a job id only valid for 7 days.
    (See, https://docs.aws.amazon.com/textract/latest/dg/API_GetDocumentTextDetection.html)
    After that, you cannot get the response from the Textract API, but this function
    can still get the response from the S3 bucket.

    :param s3_client: the boto3 S3 client.
    :param s3dir: the S3 directory where the Textract response files are stored.
        The directory should contain a ``.s3_access_check`` file and a bunch of JSON files.
        The directory looks like "s3://{bucket}/{prefix}/{job_id}/", where the bucket
        and prefix are the OutputConfig["S3Bucket"] and OutputConfig["S3Prefix"] in the
        ``start_xyz()`` async API.
    """
    return _merge_textract_response(
        s3_client=s3_client,
        s3dir=s3dir,
        key="Blocks",
    )


def merge_document_text_detection_result(
    s3_client: "S3Client",
    s3dir: S3Path,
) -> "GetDocumentTextDetectionResponseTypeDef":  # pragma: no cover
    """
    The Textract async API stores the response in multiple files in a temp
    S3 directory. This function merges the response from all the files into one dict.
    The paginator version of the ``textract_client.get_xyz()`` can do the same tricks.
    However, that API requires a valid job id, but a job id only valid for 7 days.
    (See, https://docs.aws.amazon.com/textract/latest/dg/API_GetDocumentTextDetection.html)
    After that, you cannot get the response from the Textract API, but this function
    can still get the response from the S3 bucket.

    :param s3_client: the boto3 S3 client.
    :param s3dir: the S3 directory where the Textract response files are stored.
        The directory should contain a ``.s3_access_check`` file and a bunch of JSON files.
        The directory looks like "s3://{bucket}/{prefix}/{job_id}/", where the bucket
        and prefix are the OutputConfig["S3Bucket"] and OutputConfig["S3Prefix"] in the
        ``start_xyz()`` async API.
    """
    return _merge_textract_response(
        s3_client=s3_client,
        s3dir=s3dir,
        key="Blocks",
    )


def merge_expense_analysis_result(
    s3_client: "S3Client",
    s3dir: S3Path,
) -> "GetExpenseAnalysisResponseTypeDef":  # pragma: no cover
    """
    The Textract async API stores the response in multiple files in a temp
    S3 directory. This function merges the response from all the files into one dict.
    The paginator version of the ``textract_client.get_xyz()`` can do the same tricks.
    However, that API requires a valid job id, but a job id only valid for 7 days.
    (See, https://docs.aws.amazon.com/textract/latest/dg/API_GetDocumentTextDetection.html)
    After that, you cannot get the response from the Textract API, but this function
    can still get the response from the S3 bucket.

    :param s3_client: the boto3 S3 client.
    :param s3dir: the S3 directory where the Textract response files are stored.
        The directory should contain a ``.s3_access_check`` file and a bunch of JSON files.
        The directory looks like "s3://{bucket}/{prefix}/{job_id}/", where the bucket
        and prefix are the OutputConfig["S3Bucket"] and OutputConfig["S3Prefix"] in the
        ``start_xyz()`` async API.
    """
    return _merge_textract_response(
        s3_client=s3_client,
        s3dir=s3dir,
        key="ExpenseDocuments",
    )


def merge_lending_analysis_result(
    s3_client: "S3Client",
    s3dir: S3Path,
) -> "GetLendingAnalysisResponseTypeDef":  # pragma: no cover
    """
    The Textract async API stores the response in multiple files in a temp
    S3 directory. This function merges the response from all the files into one dict.
    The paginator version of the ``textract_client.get_xyz()`` can do the same tricks.
    However, that API requires a valid job id, but a job id only valid for 7 days.
    (See, https://docs.aws.amazon.com/textract/latest/dg/API_GetDocumentTextDetection.html)
    After that, you cannot get the response from the Textract API, but this function
    can still get the response from the S3 bucket.

    :param s3_client: the boto3 S3 client.
    :param s3dir: the S3 directory where the Textract response files are stored.
        The directory should contain a ``.s3_access_check`` file and a bunch of JSON files.
        The directory looks like "s3://{bucket}/{prefix}/{job_id}/", where the bucket
        and prefix are the OutputConfig["S3Bucket"] and OutputConfig["S3Prefix"] in the
        ``start_xyz()`` async API.
    """
    return _merge_textract_response(
        s3_client=s3_client,
        s3dir=s3dir,
        key="Results",
    )
