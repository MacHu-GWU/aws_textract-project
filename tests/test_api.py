# -*- coding: utf-8 -*-

from aws_textract import api


def test():
    _ = api
    _ = api.better_boto.preprocess_input_output_config
    _ = api.better_boto.get_document_analysis
    _ = api.better_boto.get_document_text_detection
    _ = api.better_boto.get_expense_analysis
    _ = api.better_boto.get_lending_analysis
    _ = api.better_boto.JobStatusEnum
    _ = api.better_boto.wait_document_analysis_job_to_succeed
    _ = api.better_boto.wait_document_text_detection_job_to_succeed
    _ = api.better_boto.wait_expense_analysis_job_to_succeed
    _ = api.better_boto.wait_lending_analysis_job_to_succeed
    _ = api.better_boto.wait_for_lending_analysis_job_to_succeed
    _ = api.better_boto.TextractDocumentLocation
    _ = api.better_boto.TextractEvent
    _ = api.res.BlockTypeEnum
    _ = api.res.blocks_to_text
    _ = api.res.split_blocks_by_page
    _ = api.res.get_textract_output_s3dir
    _ = api.res.merge_document_analysis_result
    _ = api.res.merge_document_text_detection_result
    _ = api.res.merge_expense_analysis_result
    _ = api.res.merge_lending_analysis_result


if __name__ == "__main__":
    from aws_textract.tests import run_cov_test

    run_cov_test(__file__, "aws_textract.api", preview=False)
