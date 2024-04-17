.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add better integration with `amazon-textract-textractor <https://github.com/aws-samples/amazon-textract-textractor>`_

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.1 (2024-04-17)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
- Add the following public API:
    - ``aws_textract.api.better_boto.preprocess_input_output_config``
    - ``aws_textract.api.better_boto.get_document_analysis``
    - ``aws_textract.api.better_boto.get_document_text_detection``
    - ``aws_textract.api.better_boto.get_expense_analysis``
    - ``aws_textract.api.better_boto.get_lending_analysis``
    - ``aws_textract.api.better_boto.JobStatusEnum``
    - ``aws_textract.api.better_boto.wait_document_analysis_job_to_succeed``
    - ``aws_textract.api.better_boto.wait_document_text_detection_job_to_succeed``
    - ``aws_textract.api.better_boto.wait_expense_analysis_job_to_succeed``
    - ``aws_textract.api.better_boto.wait_for_lending_analysis_job_to_succeed``
    - ``aws_textract.api.res.BlockTypeEnum``
    - ``aws_textract.api.res.blocks_to_text``
