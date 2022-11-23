import pytest
import main


@pytest.mark.parametrize("form", list(main.Form.__subclasses__()))
def test_all_forms(form):
    json_form = form.get_form_request_json()

    form_action_ids = list(main.gen_dict_extract(json_form, "action_id"))
    assert len(form_action_ids) == len(set(form_action_ids))

    # noinspection PyUnresolvedReferences
    assert sorted(form_action_ids) == sorted(list(form.__match_args__))


def test_sample_form_1():
    sample_form_response = {
        "some_thing_1": {
            "some": "asfa",
            "daf": "deafa",
            "some_thing_4": {"value": "woooo"},
        },
        "b": {"some": "asfa", "daf": "deafa", "some_thing_2": {"value": "2"}},
    }

    sample_form: main.SampleForm = main.SampleForm.from_form_response(sample_form_response)
    assert sample_form == main.SampleForm(some_thing_2="2", some_thing_4="woooo")

def test_sample_form_1_with_bad_data():
    sample_form_response = {
        "some_thing_1": {
            "some": "asfa",
            "daf": "deafa",
            "some_thing_5": {"value": "woooo"},
        },
        "b": {"some": "asfa", "daf": "deafa", "some_thing_2": {"value": "2"}},
    }
    with pytest.raises(ValueError):
        main.SampleForm = main.SampleForm.from_form_response(sample_form_response)

