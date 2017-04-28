import os

from xldigest.process.template import FormTemplate
from xldigest.tests.fixtures import TMP_DIR


def test_base_form_template():
    template = FormTemplate(os.path.join(TMP_DIR, 'test_formtemplate.xlsx'), blank=True)
    assert template
