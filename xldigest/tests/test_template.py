from xldigest.process.template import FormTemplate


def test_base_form_template():
    template = FormTemplate('/tmp/test_formtemplate.xlsx', blank=True)
    assert template
