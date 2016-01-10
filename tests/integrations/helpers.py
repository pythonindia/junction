# -*- coding: utf-8 -*-


def assert_template_used(response, template_name):
    res = False
    for template in response.templates:
        if template.name == template_name:
            res = True
            break

    assert res is True
