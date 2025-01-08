import importlib.util
import json
import sys

from versioalueet.cli import parse_request
import versioalueet.env as env
from versioalueet import ENCODING, ENCODING_ERRORS_POLICY, VERSION


LIBRARY_ENV_DICT = {
    'debug-mode': False,
    'quiet-mode': False,
    'verbose-mode': True,
    'version': VERSION,
    'encoding': ENCODING,
    'encoding-errors-policy': ENCODING_ERRORS_POLICY,
}

LIBRARY_ENV_TEXT = (
    f'library-env: debug-mode={False}, quiet-mode={False}, verbose-mode={True}, version={VERSION}, encoding={ENCODING},'
    f' encoding-errors-policy={ENCODING_ERRORS_POLICY}'
)


def test_assess():
    options = parse_request(['-v'])
    data = env.assess(options)
    assert data
    assert data.get('library-env', {}) == LIBRARY_ENV_DICT


def test_report_default_without_resource():
    if 'resource' in sys.modules:
        del sys.modules['resource']
        print('removed imported resource module')
    else:
        print('no imported resource module to be removed')
    options = parse_request(['-v'])
    text = env.report(options)
    assert LIBRARY_ENV_TEXT in text
    if importlib.util.find_spec('resource'):
        import resource  # noqa

        print('imported resource again')
    else:
        print('import of resource failed (may be OK)')


def test_report_as_dict():
    options = parse_request(['-v'])
    assessed = env.assess(options)
    del assessed['os-resource-usage']
    reported = env.report(options, format='dict')
    del reported['os-resource-usage']
    assert assessed == reported


def test_report_as_json():
    options = parse_request(['-v'])
    assessed = env.assess(options)
    del assessed['os-resource-usage']
    reported = json.loads(env.report(options, format='json'))  # noqa
    del reported['os-resource-usage']
    assert assessed == reported
