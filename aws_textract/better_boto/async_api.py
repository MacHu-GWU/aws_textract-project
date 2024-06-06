# -*- coding: utf-8 -*-

"""
Human friendly version of Amazon Textract async operations.
"""

import typing as T
import enum
import dataclasses

from ..vendor.waiter import Waiter
from ..vendor.better_dataclasses import DataClass


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

    Usage example::

        document_location, output_config = preprocess_input_output_config(
            input_bucket="my-input-bucket",
            input_key="my-folder/my-document.pdf",
            input_version=None,
            output_bucket="my-output-bucket",
            output_prefix="my-folder/my-document",
        )
        boto3.client("textract").start_text_detection(
            DocumentLocation=document_location,
            OutputConfig=output_config,
            ...
        )

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
    """
    The Textract async API will return a JobId, then you can use the JobId to get
    the response. Since the response usually are big, you need to use the
    ``get_xyz()`` paginator API to get all the response. This function does the
    pagination automatically for you.

    Note that the ``get_xyz()`` API requires a valid job id, but a job id only valid for 7 days.
    (See, https://docs.aws.amazon.com/textract/latest/dg/API_GetDocumentTextDetection.html)
    After that, you cannot get the response from the Textract API. You should
    consider getting the response from S3 directly.
    """
    final_res = None
    next_token = None
    while True:
        kwargs = dict(JobId=job_id)
        if max_results:
            kwargs["MaxResults"] = max_results
        if next_token:
            kwargs["NextToken"] = next_token
        res = api(**kwargs)

        if final_res is None:
            final_res = res
        else:
            final_res.get(key, []).extend(res.get(key, []))

        if all_pages is False:  # immediately exit
            return final_res

        next_token = res.get("NextToken")
        if next_token:
            pass
        else:
            break

    if "NextToken" in res:
        del final_res["NextToken"]

    return final_res


def get_document_analysis(
    textract_client: "TextractClient",
    job_id: str,
    max_results: T.Optional[int] = 1000,
    all_pages: bool = True,
) -> "GetDocumentAnalysisResponseTypeDef":  # pragma: no cover
    """
    Get all the blocks from the document analysis job. Automatically iterate through
    all the pages if there are more than one.

    :param textract_client: boto3.client("textract") object.
    :param job_id: job id.
    :param max_results: maximum number of results in the paginator to return.
    :param all_pages: whether to get all pages. if False, only get the first page.
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
    max_results: T.Optional[int] = 1000,
    all_pages: bool = True,
) -> "GetDocumentTextDetectionResponseTypeDef":  # pragma: no cover
    """
    Get all the blocks from the document text detection job.
    Automatically iterate through all the pages if there are more than one.

    :param textract_client: boto3.client("textract") object.
    :param job_id: job id.
    :param max_results: maximum number of results in the paginator to return.
    :param all_pages: whether to get all pages. if False, only get the first page.
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
    max_results: T.Optional[int] = 20,
    all_pages: bool = True,
) -> "GetExpenseAnalysisResponseTypeDef":  # pragma: no cover
    """
    Get all the blocks from the expense analysis job.
    Automatically iterate through all the pages if there are more than one.

    :param textract_client: boto3.client("textract") object.
    :param job_id: job id.
    :param max_results: maximum number of results in the paginator to return.
    :param all_pages: whether to get all pages. if False, only get the first page.
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
    max_results: T.Optional[int] = 30,
    all_pages: bool = True,
) -> "GetLendingAnalysisResponseTypeDef":  # pragma: no cover
    """
    Get all the blocks from the lending analysis job.
    Automatically iterate through all the pages if there are more than one.

    :param textract_client: boto3.client("textract") object.
    :param job_id: job id.
    :param max_results: maximum number of results in the paginator to return.
    :param all_pages: whether to get all pages. if False, only get the first page.
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


def wait_lending_analysis_job_to_succeed(
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


wait_for_lending_analysis_job_to_succeed = wait_lending_analysis_job_to_succeed


@dataclasses.dataclass
class TextractDocumentLocation(DataClass):
    S3Bucket: str = dataclasses.field()
    S3ObjectName: str = dataclasses.field()


@dataclasses.dataclass
class TextractEvent(DataClass):
    """
    You can let Amazon Textract to send the status of an analysis request to
    an Amazon Simple Notification Service (Amazon SNS) topic when using
    Asynchronous Operations. This class represents the payload of the SNS message.

    Usage example::

        import json

        def lambda_handler(event, context):
            message = event["Records"][0]["Sns"]["Message"]
            textract_event = TextractEvent.from_dict(json.loads(message))

    See more details about the textract SNS message at
    https://docs.aws.amazon.com/textract/latest/dg/async-notification-payload.html.
    The most important field is the ``JobTag``. You can use ``JobTag`` to pass
    data via the SNS notification. If the data is a short string, you can use
    ``JobTag``. If the data is a large object, you can use an S3 object or DynamoDB
    to store the data and pass the URI via ``JobTag``.

    See more details about the SNS event JSON at
    https://docs.aws.amazon.com/sns/latest/dg/sns-message-and-json-formats.html#http-notification-json
    """

    JobId: str = dataclasses.field()
    Status: str = dataclasses.field()
    API: str = dataclasses.field()
    JobTag: str = dataclasses.field()
    Timestamp: int = dataclasses.field()
    DocumentLocation: TextractDocumentLocation = TextractDocumentLocation.nested_field()
