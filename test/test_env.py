import importlib.util
import json
import sys

import versioalueet.env as env
from versioalueet import DEBUG, ENCODING, ENCODING_ERRORS_POLICY, VERSION


LIBRARY_ENV_DICT = {
    'debug-mode': DEBUG,
    'version': VERSION,
    'encoding': ENCODING,
    'encoding-errors-policy': ENCODING_ERRORS_POLICY,
}

LIBRARY_ENV_TEXT = (
    f'library-env: debug-mode={DEBUG}, version={VERSION}, encoding={ENCODING},'
    f' encoding-errors-policy={ENCODING_ERRORS_POLICY}'
)


def test_assess():
    data = env.assess()
    assert data
    assert data.get('library-env', {}) == LIBRARY_ENV_DICT


def test_report_default_without_resource():
    if 'resource' in sys.modules:
        del sys.modules['resource']
        print('removed imported resource module')
    else:
        print('no imported resource module to be removed')
    text = env.report()
    assert LIBRARY_ENV_TEXT in text
    if importlib.util.find_spec('resource'):
        import resource  # noqa

        print('imported resource again')
    else:
        print('import of resource failed (may be OK)')


def test_report_as_dict():
    assessed = env.assess()
    del assessed['os-resource-usage']
    reported = env.report(format='dict')
    del reported['os-resource-usage']
    assert assessed == reported


def test_report_as_json():
    assessed = env.assess()
    del assessed['os-resource-usage']
    reported = json.loads(env.report(format='json'))  # noqa
    del reported['os-resource-usage']
    assert assessed == reported
