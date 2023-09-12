#!/usr/bin/env python
# @Project: test-hub
# @Author: zero
# @Create time: 2023/8/28 01:26
from typing import List, Any

from ninja import Schema
from ninja.pagination import PaginationBase
from pydantic import Field


class CustomPagination(PaginationBase):
    class Input(Schema):
        page: int = Field(1, ge=1)

    class Output(Schema):
        code: int = 200
        message: str = 'success'
        data: List[Any]
        total: int
        page: int

    items_attribute: str = "data"

    def paginate_queryset(self, queryset, pagination: Input, **params):
        page = pagination.page
        start = (page - 1) * 10
        end = page * 10
        return {
            'data': queryset[start: end],
            'page': page,
            'total': queryset.count(),
        }
