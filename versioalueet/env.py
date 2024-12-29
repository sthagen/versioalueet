"""Report facts from the environment."""

import importlib.util
import json
import os
import platform

if importlib.util.find_spec('resource'):
    import resource
else:  # pragma: no cover
    pass
import sys
import uuid
from typing import Union
from versioalueet import DEBUG, ENCODING, ENCODING_ERRORS_POLICY, VERSION

VolatileDictType = dict[str, Union[str, bool, float, int]]
EnvType = dict[str, dict[str, VolatileDictType]]
FormatType = str
FORMATS = ('text', 'dict', 'json')


def assess() -> EnvType:
    """Assess process environment with standard library functions."""
    uname = os.uname()
    os_sysname = uname.sysname
    os_nodename = uname.nodename
    os_version = uname.version
    os_cpu_present = os.cpu_count()
    os_cpu_available = len(os.sched_getaffinity(0)) if 'sched_getaffinity' in dir(os) else -1  # type: ignore

    names = sorted(
        name
        for name in dir(sys.flags)
        if not name.startswith('_') and not name.startswith('n_') and name not in ('count', 'index')
    )
    flags = {name: getattr(sys.flags, name) for name in names if getattr(sys.flags, name)}

    if 'resource' in sys.modules:
        res_self = resource.getrusage(resource.RUSAGE_SELF)
        ru_utime_msec = res_self.ru_utime  # time spent executing in user mode in seconds (usec resolution)
        ru_utime_msec *= 1e3
        ru_utime_msec_usec_precision = round(ru_utime_msec, 3)
        ru_stime_msec = res_self.ru_stime  # time spent executing in kernel mode in seconds (usec resolution)
        ru_stime_msec *= 1e3
        ru_stime_msec_usec_precision = round(ru_stime_msec, 3)
        ru_maxrss = float(res_self.ru_maxrss)  # maximum resident set size used (linux in kilobytes)
        if platform.platform(aliased=True, terse=True).lower().startswith('macos'):  # pragma: no cover
            ru_maxrss /= 1024  # "man 2 getrusage" on MacOS indicates unit is bytes
        ru_maxrss_mbytes_kbytes_precision = round(ru_maxrss / 1024, 3)
        ru_minflt = res_self.ru_minflt  # number of page faults serviced without any I/O activity
        ru_majflt = res_self.ru_majflt  # number of page faults serviced that required I/O activity
        ru_inblock = res_self.ru_inblock  # number of times the filesystem had to perform input
        ru_oublock = res_self.ru_oublock  # number of times the filesystem had to perform output
        ru_nvcsw = res_self.ru_nvcsw  # number of times a context switch resulted due to a process
        # voluntarily giving up the processor before its time slice
        # was completed
        ru_nivcsw = res_self.ru_nivcsw  # number of times a context switch resulted due to a higher
        # priority process becoming runnable or because the current
        # process exceeded its time slice
    else:
        ru_utime_msec_usec_precision = -1
        ru_stime_msec_usec_precision = -1
        ru_maxrss_mbytes_kbytes_precision = -1
        ru_minflt = -1
        ru_majflt = -1
        ru_inblock = -1
        ru_oublock = -1
        ru_nvcsw = -1
        ru_nivcsw = -1

    data = {
        'library-env': {
            'debug-mode': DEBUG,
            'version': VERSION,
            'encoding': ENCODING,
            'encoding-errors-policy': ENCODING_ERRORS_POLICY,
        },
        'interpreter-env': {
            'exec-prefix': sys.exec_prefix,
            'exec-path': sys.executable,
        },
        'interpreter-impl': {
            'impl-name': sys.implementation.name,
            'version': {
                'major': sys.implementation.version.major,
                'minor': sys.implementation.version.minor,
                'micro': sys.implementation.version.micro,
                'releaselevel': sys.implementation.version.releaselevel,
                'serial': sys.implementation.version.serial,
            },
        },
        'interpreter-flags': {
            **flags,
        },
        'os-env': {
            'node-id': str(uuid.uuid3(uuid.NAMESPACE_DNS, platform.node())),
            'machine-type': platform.machine(),
            'platform-code': platform.platform(aliased=True, terse=True),
            'platform_release': platform.release(),
        },
        'os-uname': {
            'os-sysname': os_sysname,
            'os-nodename': os_nodename,
            'os-version': os_version,
        },
        'os-resource-usage': {
            'ru-maxrss-mbytes-kbytes-precision': ru_maxrss_mbytes_kbytes_precision,
            'ru-utime-msec-usec-precision': ru_utime_msec_usec_precision,
            'ru-stime-msec-usec-precision': ru_stime_msec_usec_precision,
            'ru-minflt': ru_minflt,
            'ru-majflt': ru_majflt,
            'ru-inblock': ru_inblock,
            'ru-outblock': ru_oublock,
            'ru_nvcsw': ru_nvcsw,
            'ru_nivcsw': ru_nivcsw,
        },
        'os-cpu-resources': {
            'os-cpu-present': os_cpu_present,
            'os-cpu-available': os_cpu_available,
        },
    }

    return data  # type: ignore


def report(format: FormatType = 'text') -> Union[str, EnvType]:
    """Assess process environment and provide report in JSON or text format."""
    data = assess()

    if format == 'dict':
        return data

    if format == 'json':
        return json.dumps(data, indent=2)

    # Format is text
    text = []
    for pk, pv in data.items():
        line = f'{pk}: '
        values = []
        for sk, sv in pv.items():
            if not isinstance(sv, dict):
                values.append(f'{sk}={sv}')
            else:
                tvs = ', '.join([f'{tk}={tv}' for tk, tv in sv.items()])
                values.append(f'{sk}({tvs})')
        text.append(line + ', '.join(values))

    return '\n'.join(text)
