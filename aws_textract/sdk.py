# -*- coding: utf-8 -*-

import typing as T
from datetime import datetime, timezone

import botocore
from boto_session_manager import BotoSesManager

if T.TYPE_CHECKING:  # pragma: no cover
    import botocore.session


class SDK:
    def __init__(
        self,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        aws_session_token: str = None,
        region_name: str = None,
        botocore_session: 'botocore.session.Session' = None,
        profile_name: str = None,
        default_client_kwargs: dict = None,
        expiration_time: datetime = datetime(2100, 1, 1, tzinfo=timezone.utc),
        bsm: BotoSesManager = None,
    ):
        if bsm is None:
            self.bsm = bsm
        else:
            self.bsm = BotoSesManager(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_token,
                region_name=region_name,
                botocore_session=botocore_session,
                profile_name=profile_name,
                default_client_kwargs=default_client_kwargs,
                expiration_time=expiration_time,
            )

    @property
    def boto_ses(self) -> botocore.session.Session:
        return self.bsm.boto_ses

    @property
    def aws_region(self) -> str:
        return self.bsm.aws_region

    @property
    def aws_account_id(self) -> str:
        return self.bsm.aws_account_id
