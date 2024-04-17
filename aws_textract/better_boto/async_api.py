# -*- coding: utf-8 -*-

import typing as T
import enum

from ..vendor.waiter import Waiter

if T.TYPE_CHECKING:  # pragma: no cover
    from mypy_boto3_textract import TextractClient
    from mypy_boto3_textract.type_defs import GetDocumentAnalysisResponseTypeDef
    from mypy_boto3_textract.type_defs import GetDocumentTextDetectionResponseTypeDef
    from mypy_boto3_textract.type_defs import GetExpenseAnalysisResponseTypeDef
    from mypy_boto3_textract.type_defs import GetLendingAnalysisResponseTypeDef


def preprocess_input_output_config(
    input_bucket: str,
    input_key: str,
    input_version: T.Optional[str],
    output_bucket: str,
    output_prefix: str,
) -> T.Tuple[dict, dict]:  # pragma: no cover
    """
    Preprocess DocumentLocation and OutputConfig parameters for the following
    Textract API:

    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/start_document_analysis.html
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/start_document_text_detection.html
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/start_expense_analysis.html
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/start_lending_analysis.html

    :param input_bucket: input document bucket
    :param input_key: input document key
    :param input_version: if S3 bucket has versioning, specify the version id
    :param output_bucket: output bucket
    :param output_prefix: output prefix, it should not have '/' at the end
    """
    if input_key.endswith("/"):
        raise ValueError("input_key should not end with '/'")
    if output_prefix.endswith("/"):
        output_prefix = output_prefix[:-1]
    if input_version:
        document_location = dict(
            S3Object=dict(
                Bucket=input_bucket,
                Name=input_key,
                Version=input_version,
            ),
        )
    else:
        document_location = dict(
            S3Object=dict(
                Bucket=input_bucket,
                Name=input_key,
            ),
        )
    output_config = dict(
        S3Bucket=output_bucket,
        S3Prefix=output_prefix,
    )
    return document_location, output_config


def _get_result(
    api: T.Callable,
    job_id: str,
    key: str,
    max_results: T.Optional[int] = None,
    all_pages: bool = True,
):  # pragma: no cover
    res = None
    while True:
        kwargs = dict(JobId=job_id)
        if max_results:
            kwargs["MaxResults"] = max_results
        r = api(
            JobId=job_id,
        )

        if res is None:
            res = r
        else:
            res.get(key, []).extend(r.get(key, []))

        if all_pages is False:  # immediately exit
            return res

        if r.get("NextToken"):
            pass
        else:
            break

    if "NextToken" in res:
        del res["NextToken"]

    return res


def get_document_analysis(
    textract_client: "TextractClient",
    job_id: str,
    max_results: T.Optional[int] = None,
    all_pages: bool = True,
) -> "GetDocumentAnalysisResponseTypeDef":  # pragma: no cover
    """
    Get all the blocks from the document analysis job. Automatically iterate through
    all the pages if there are more than one.
    """
    return _get_result(
        api=textract_client.get_document_analysis,
        job_id=job_id,
        key="Blocks",
        max_results=max_results,
        all_pages=all_pages,
    )


def get_document_text_detection(
    textract_client: "TextractClient",
    job_id: str,
    max_results: T.Optional[int] = None,
    all_pages: bool = True,
) -> "GetDocumentTextDetectionResponseTypeDef":  # pragma: no cover
    """
    Get all the blocks from the document text detection job.
    Automatically iterate through all the pages if there are more than one.
    """
    return _get_result(
        api=textract_client.get_document_text_detection,
        job_id=job_id,
        key="Blocks",
        max_results=max_results,
        all_pages=all_pages,
    )


def get_expense_analysis(
    textract_client: "TextractClient",
    job_id: str,
    max_results: T.Optional[int] = None,
    all_pages: bool = True,
) -> "GetExpenseAnalysisResponseTypeDef":  # pragma: no cover
    """
    Get all the blocks from the expense analysis job.
    Automatically iterate through all the pages if there are more than one.
    """
    return _get_result(
        api=textract_client.get_expense_analysis,
        job_id=job_id,
        key="ExpenseDocuments",
        max_results=max_results,
        all_pages=all_pages,
    )


def get_lending_analysis(
    textract_client: "TextractClient",
    job_id: str,
    max_results: T.Optional[int] = None,
    all_pages: bool = True,
) -> "GetLendingAnalysisResponseTypeDef":  # pragma: no cover
    """
    Get all the blocks from the lending analysis job.
    Automatically iterate through all the pages if there are more than one.
    """
    return _get_result(
        api=textract_client.get_lending_analysis,
        job_id=job_id,
        key="Results",
        max_results=max_results,
        all_pages=all_pages,
    )


class JobStatusEnum(str, enum.Enum):
    IN_PROGRESS = "IN_PROGRESS"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"


def _wait_job_to_succeed(
    api: T.Callable,
    job_id: str,
    delays: int = 5,
    timeout: int = 60,
    verbose: bool = True,
):  # pragma: no cover
    """
    Wait for the async job to succeed.
    """
    for _ in Waiter(delays=delays, timeout=timeout, verbose=verbose):
        res = api(JobId=job_id)
        job_status = res["JobStatus"]
        if job_status in [JobStatusEnum.SUCCEEDED]:
            return res
        elif job_status in [JobStatusEnum.FAILED]:
            raise Exception(f"Job failed: {res}")
        else:
            pass


def wait_document_analysis_job_to_succeed(
    textract_client: "TextractClient",
    job_id: str,
    delays: int = 5,
    timeout: int = 60,
    verbose: bool = True,
) -> "GetDocumentAnalysisResponseTypeDef":  # pragma: no cover
    """
    Wait for the document analysis job to succeed.
    """
    return _wait_job_to_succeed(
        api=textract_client.get_document_analysis,
        job_id=job_id,
        delays=delays,
        timeout=timeout,
        verbose=verbose,
    )


def wait_document_text_detection_job_to_succeed(
    textract_client: "TextractClient",
    job_id: str,
    delays: int = 5,
    timeout: int = 60,
    verbose: bool = True,
) -> "GetDocumentTextDetectionResponseTypeDef":  # pragma: no cover
    """
    Wait for the document text detection job to succeed.
    """
    return _wait_job_to_succeed(
        api=textract_client.get_document_text_detection,
        job_id=job_id,
        delays=delays,
        timeout=timeout,
        verbose=verbose,
    )


def wait_expense_analysis_job_to_succeed(
    textract_client: "TextractClient",
    job_id: str,
    delays: int = 5,
    timeout: int = 60,
    verbose: bool = True,
) -> "GetExpenseAnalysisResponseTypeDef":  # pragma: no cover
    """
    Wait for the expense analysis job to succeed.
    """
    return _wait_job_to_succeed(
        api=textract_client.get_expense_analysis,
        job_id=job_id,
        delays=delays,
        timeout=timeout,
        verbose=verbose,
    )


def wait_for_lending_analysis_job_to_succeed(
    textract_client: "TextractClient",
    job_id: str,
    delays: int = 5,
    timeout: int = 60,
    verbose: bool = True,
) -> "GetLendingAnalysisResponseTypeDef":  # pragma: no cover
    """
    Wait for the lending analysis job to succeed.
    """
    return _wait_job_to_succeed(
        api=textract_client.get_lending_analysis,
        job_id=job_id,
        delays=delays,
        timeout=timeout,
        verbose=verbose,
    )
