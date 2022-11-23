import pytest
import main


@pytest.mark.parametrize("form", list(main.Form.__subclasses__()))
def test_all_forms(form):
    json_form = form.get_form_request_json()

    form_action_ids = list(main.gen_dict_extract(json_form, "action_id"))
    assert len(form_action_ids) == len(set(form_action_ids))

    # noinspection PyUnresolvedReferences
    assert sorted(form_action_ids) == sorted(list(form.__match_args__))
