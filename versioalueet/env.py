"""Report facts from the environment."""

import os
import platform

try:
    import resource
except ImportError:
    pass
import sys
import uuid

from versioalueet import DEBUG, ENCODING, ENCODING_ERRORS_POLICY, VERSION


def report() -> tuple[str, ...]:
    node_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, platform.node()))
    machine_type = platform.machine()
    platform_code = platform.platform(aliased=True, terse=True)
    platform_release = platform.release()
    uname = os.uname()
    os_sysname = uname.sysname
    os_nodename = uname.nodename
    os_version = uname.version
    os_cpu_present = os.cpu_count()
    os_cpu_available = len(os.sched_getaffinity(0)) if 'sched_getaffinity' in dir(os) else -1  # type: ignore
    if 'resource' in sys.modules:
        res_self = resource.getrusage(resource.RUSAGE_SELF)
        ru_utime_msec = res_self.ru_utime  # time spent executing in user mode in seconds (usec resolution)
        ru_utime_msec *= 1e3
        ru_utime_msec_usec_precision = round(ru_utime_msec, 3)
        ru_stime_msec = res_self.ru_stime  # time spent executing in kernel mode in seconds (usec resolution)
        ru_stime_msec *= 1e3
        ru_stime_msec_usec_precision = round(ru_stime_msec, 3)
        ru_maxrss = float(res_self.ru_maxrss)  # maximum resident set size used (linux in kilobytes)
        if platform_code.lower().startswith('macos'):
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
        ru_utime_msec = -1
        ru_stime_msec = -1
        ru_maxrss = -1
        ru_minflt = -1
        ru_majflt = -1
        ru_inblock = -1
        ru_oublock = -1
        ru_nvcsw = -1
        ru_nivcsw = -1
    exec_prefix = sys.exec_prefix
    exec_path = sys.executable
    implementation = sys.implementation
    impl_name = implementation.name
    impl_version = implementation.version
    major = impl_version.major
    minor = impl_version.minor
    micro = impl_version.micro
    releaselevel = impl_version.releaselevel
    serial = impl_version.serial
    names = sorted(
        name
        for name in dir(sys.flags)
        if not name.startswith('_') and not name.startswith('n_') and name not in ('count', 'index')
    )
    flags = [f'{name}={getattr(sys.flags, name)}' for name in names if getattr(sys.flags, name)]

    return (
        'environment: [',
        f'- library-env: {DEBUG=}, {VERSION=}, {ENCODING=}, {ENCODING_ERRORS_POLICY=}',
        f'- interpreter-env: {exec_prefix=}, {exec_path=}',
        f'- interpreter-impl: {impl_name=}, version({major=}, {minor=}, {micro=}, {releaselevel=}, {serial=})',
        f'- interpreter-flags: {flags=}',
        f'- os-env: {node_id=}, {machine_type=}, {platform_code=}, {platform_release=}',
        f'- os-uname: {os_sysname=}, {os_nodename=}, {os_version=}',
        (
            f'- os-resource-usage: {ru_maxrss_mbytes_kbytes_precision=}, {ru_utime_msec_usec_precision=},'
            f' {ru_stime_msec_usec_precision=}, {ru_minflt=}, {ru_majflt=}, {ru_inblock=}, {ru_oublock=},'
            f' {ru_nvcsw=}, {ru_nivcsw=}'
        ),
        f'- os-cpu-resources: {os_cpu_present=}, {os_cpu_available=}',
        ']',
    )
