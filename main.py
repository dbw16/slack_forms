from __future__ import annotations
from blockkit import Button, MarkdownText, Message, PlainText, Section
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Tuple
from collections import defaultdict


def gen_dict_extract(var: dict, key: str):
    if isinstance(var, dict):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, (dict, list)):
                yield from gen_dict_extract(v, key)
    elif isinstance(var, list):
        for d in var:
            yield from gen_dict_extract(d, key)


class Form(ABC):
    @classmethod
    def from_form_response(cls, response_json: dict) -> Form:
        action_ids = list(gen_dict_extract(cls.get_form_request_json(), "action_id"))
        if len(set(action_ids)) != len(action_ids):
            raise ValueError("Not all action_id of request form are unique")
        class_dict = {}
        for action_id in action_ids:
            internal_dicts = list(gen_dict_extract(response_json, action_id))
            for internal_dict in internal_dicts:
                if "selected_option" in internal_dict:
                    class_dict[action_id] = internal_dict["selected_option"]["value"]
                    break
                elif "value" in internal_dict:
                    class_dict[action_id] = internal_dict["value"]
                    break
            else:
                raise ValueError(
                    f"could not find all action_ids {action_ids} in response json"
                )

        try:
            # noinspection PyArgumentList
            return cls(**class_dict)
        except TypeError:
            raise ValueError(
                "action_id do not match 1 to 1 with class instance variables"
            )

    @staticmethod
    @abstractmethod
    def get_form_request_json() -> dict:
        pass


@dataclass
class SampleForm(Form):
    # A list of variables we want from the user, note these variable names much match 1 to 1 with the action_id in
    # get_form_request_json
    some_thing_4: str
    some_thing_2: str

    @staticmethod
    def get_form_request_json() -> dict:
        return Message(
            blocks=[
                Section(
                    block_id="test",
                    text=MarkdownText(text="this is a block with a button"),
                    accessory=Button(
                        text=PlainText(text="test", emoji=True),
                        action_id="some_thing_4",
                    ),
                ),
                Section(
                    block_id="test_2",
                    text=MarkdownText(text="this is a block with a button"),
                    accessory=Button(
                        text=PlainText(text="test", emoji=True),
                        action_id="some_thing_2",
                    ),
                ),
            ]
        ).build()


@dataclass
class BadSampleForm(Form):
    # A list of variables we want from the user, note these variable names much match 1 to 1 with the action_id in
    # get_form_request_json
    some_thing_1: str

    @staticmethod
    def get_form_request_json() -> dict:
        return Message(
            blocks=[
                Section(
                    block_id="test",
                    text=MarkdownText(text="this is a block with a button"),
                    accessory=Button(
                        text=PlainText(text="test", emoji=True),
                        action_id="some_thing_4",
                    ),
                ),
                Section(
                    block_id="test_1",
                    text=MarkdownText(text="this is a block with a button"),
                    accessory=Button(
                        text=PlainText(text="test", emoji=True),
                        action_id="some_thing_2",
                    ),
                ),
            ]
        ).build()
