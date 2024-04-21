# -*- coding: utf-8 -*-

import typing as T
import json
from s3pathlib import S3Path

if T.TYPE_CHECKING:  # pragma: no cover
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_textract.type_defs import GetDocumentAnalysisResponseTypeDef
    from mypy_boto3_textract.type_defs import GetDocumentTextDetectionResponseTypeDef
    from mypy_boto3_textract.type_defs import GetExpenseAnalysisResponseTypeDef
    from mypy_boto3_textract.type_defs import GetLendingAnalysisResponseTypeDef


def _merge_textract_response(
    s3_client: "S3Client",
    s3dir: S3Path,
    key: str,
) -> dict: # pragma: no cover
    """
    The Textract async API stores the response in multiple files in a temp
    S3 directory. This function merges the response from all the files into one dict.
    The paginator version of the ``textract_client.get_xyz()`` can do the same tricks.
    However, that API requires a valid job id but a job id only valid for 7 days.
    After that, you cannot get the response from the Textract API, but this function
    can still get the response from the S3 bucket.

    :param s3_client: the boto3 S3 client.
    :param s3dir: the S3 directory where the Textract response files are stored.
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
) -> "GetDocumentAnalysisResponseTypeDef": # pragma: no cover
    return _merge_textract_response(
        s3_client=s3_client,
        s3dir=s3dir,
        key="Blocks",
    )


def merge_document_text_detection_result(
    s3_client: "S3Client",
    s3dir: S3Path,
) -> "GetDocumentTextDetectionResponseTypeDef": # pragma: no cover
    return _merge_textract_response(
        s3_client=s3_client,
        s3dir=s3dir,
        key="Blocks",
    )


def merge_expense_analysis_result(
    s3_client: "S3Client",
    s3dir: S3Path,
) -> "GetExpenseAnalysisResponseTypeDef": # pragma: no cover
    return _merge_textract_response(
        s3_client=s3_client,
        s3dir=s3dir,
        key="ExpenseDocuments",
    )


def merge_lending_analysis_result(
    s3_client: "S3Client",
    s3dir: S3Path,
) -> "GetLendingAnalysisResponseTypeDef": # pragma: no cover
    return _merge_textract_response(
        s3_client=s3_client,
        s3dir=s3dir,
        key="Results",
    )
