from datetime import date
from typing import List

from attr import attrs

from base.utils import get_days_for_month


@attrs(auto_attribs=True)
class SkyPickerResponseObject:
    price: int
    booking_token: str
    date: date
    fly_to: str
    fly_from: str


@attrs(auto_attribs=True)
class CheckObject:
    booking_token: str
    valid: bool


class PickerResponse:
    picker_response: List[SkyPickerResponseObject]

    def __init__(self, picker_response):
        self.picker_response = picker_response

    def as_dict(self) -> dict:
        answer, dict_by_city, detail_dict = {}, {}, {}
        days = get_days_for_month()
        for day in days:
            for resp in self.picker_response:
                if resp.date == day:
                    detail_dict[f'{resp.fly_from}-{resp.fly_to}'] = {
                        'price': resp.price,
                        'booking_token': resp.booking_token
                    }
                answer[f"{day.strftime('%d/%m/%Y')}"] = detail_dict
        return answer
