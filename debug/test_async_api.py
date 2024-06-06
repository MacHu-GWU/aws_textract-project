# -*- coding: utf-8 -*-

"""
It's very hard to do unit test for this library. This script is for manual integration test.
"""

import json
from pathlib_mate import Path
from boto_session_manager import BotoSesManager
from s3pathlib import S3Path, context
from rich import print as rprint

import aws_textract.api as aws_textract

bsm = BotoSesManager(profile_name="bmt_app_dev_us_east_1")
context.attach_boto_session(bsm.boto_ses)

dir_here = Path.dir_here(__file__)
path_doc = dir_here / "fw2.png"
path_json1 = path_doc.change(new_fname=path_doc.fname + "-1", new_ext=".json")
path_txt1 = path_doc.change(new_fname=path_doc.fname + "-1", new_ext=".txt")
path_json2 = path_doc.change(new_fname=path_doc.fname + "-2", new_ext=".json")
path_txt2 = path_doc.change(new_fname=path_doc.fname + "-2", new_ext=".txt")

s3dir = S3Path(
    f"s3://{bsm.aws_account_alias}-{bsm.aws_region}-data/projects/aws_textract/"
)
print(f"{s3dir.console_url = }")
s3dir_input = s3dir.joinpath("input").to_dir()
s3dir_output = s3dir.joinpath("output").to_dir()
s3path = s3dir_input / path_doc.fname

s3path.upload_file(path_doc, extra_args={"ContentType": "image/png"}, overwrite=True)


def s1_start_document_analysis():
    document_location, output_config = (
        aws_textract.better_boto.preprocess_input_output_config(
            input_bucket=s3path.bucket,
            input_key=s3path.key,
            input_version=None,
            output_bucket=s3dir_output.bucket,
            output_prefix=s3dir_output.to_file().key,
        )
    )
    res = bsm.textract_client.start_document_analysis(
        DocumentLocation=document_location,
        FeatureTypes=["TABLES", "FORMS", "LAYOUT"],
        OutputConfig=output_config,
    )
    res.pop("ResponseMetadata")
    rprint(res)
    return res["JobId"]


def s2_wait_document_analysis_job_to_succeed(job_id: str):
    aws_textract.better_boto.wait_document_analysis_job_to_succeed(
        textract_client=bsm.textract_client,
        job_id=job_id,
    )


def s3_get_document_analysis_output(job_id: str) -> dict:
    res = aws_textract.better_boto.get_document_analysis(bsm.textract_client, job_id)
    text = aws_textract.res.blocks_to_text(res["Blocks"])
    path_json1.write_text(json.dumps(res, indent=4))
    path_txt1.write_text(text)
    return res


def s4_get_document_analysis_output_from_s3(job_id: str) -> dict:
    s3dir = aws_textract.res.get_textract_output_s3dir(
        s3dir_output.bucket, s3dir_output.key, job_id
    )
    res = aws_textract.res.merge_document_analysis_result(bsm.s3_client, s3dir)
    text = aws_textract.res.blocks_to_text(res["Blocks"])
    path_json2.write_text(json.dumps(res, indent=4))
    path_txt2.write_text(text)
    return res


def s1_start_document_text_detection():
    document_location, output_config = (
        aws_textract.better_boto.preprocess_input_output_config(
            input_bucket=s3path.bucket,
            input_key=s3path.key,
            input_version=None,
            output_bucket=s3dir_output.bucket,
            output_prefix=s3dir_output.to_file().key,
        )
    )
    res = bsm.textract_client.start_document_text_detection(
        DocumentLocation=document_location,
        OutputConfig=output_config,
    )
    res.pop("ResponseMetadata")
    rprint(res)
    return res["JobId"]


def s2_wait_document_text_detection_job_to_succeed(job_id: str):
    aws_textract.better_boto.wait_document_text_detection_job_to_succeed(
        textract_client=bsm.textract_client,
        job_id=job_id,
    )


def s3_get_document_text_detection_output(job_id: str) -> dict:
    res = aws_textract.better_boto.get_document_text_detection(
        bsm.textract_client, job_id
    )
    text = aws_textract.res.blocks_to_text(res["Blocks"])
    path_json1.write_text(json.dumps(res, indent=4))
    path_txt1.write_text(text)
    return res


def s4_get_document_text_detection_output_from_s3(job_id: str) -> dict:
    s3dir = aws_textract.res.get_textract_output_s3dir(
        s3dir_output.bucket, s3dir_output.key, job_id
    )
    res = aws_textract.res.merge_document_text_detection_result(bsm.s3_client, s3dir)
    text = aws_textract.res.blocks_to_text(res["Blocks"])
    path_json2.write_text(json.dumps(res, indent=4))
    path_txt2.write_text(text)
    return res


if __name__ == "__main__":
    job_id = "3b2be6c6b743ced81f6a1239d9d5ae5cb6aac0d2eb33546aa3cf6d6a71159b94"

    # s1_start_document_analysis()
    # s2_wait_document_analysis_job_to_succeed(job_id)
    # s3_get_document_analysis_output(job_id)
    # s4_get_document_analysis_output_from_s3(job_id)

    # s1_start_document_text_detection()
    # s2_wait_document_text_detection_job_to_succeed(job_id)
    # s3_get_document_text_detection_output(job_id)
    # s4_get_document_text_detection_output_from_s3(job_id)

    pass
