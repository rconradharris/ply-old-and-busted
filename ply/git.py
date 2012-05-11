import subprocess

class GitException(Exception):
    pass


class PatchDidNotApplyCleanly(GitException):
    pass


class MutuallyIncompatibleOptions(GitException):
    pass


def add(filename):
    subprocess.check_call(['git', 'add', filename])


def am(*patch_paths, **kwargs):
    three_way_merge = kwargs.get('three_way_merge', False)
    resolved = kwargs.get('resolved', False)

    args = ['git', 'am']
    args.extend(patch_paths)

    if three_way_merge:
        args.append('--3way')

    if resolved:
        args.append('--resolved')

    try:
        subprocess.check_call(args)
    except subprocess.CalledProcessError:
        raise PatchDidNotApplyCleanly


def checkout(branch_name, create=False, create_and_reset=False):
    args = ['git', 'checkout']

    if create and create_and_reset:
        raise MutuallyIncompatibleOptions("create and create_and_reset")

    if create:
        args.append('-b')

    if create_and_reset:
        args.append('-B')


    args.append(branch_name)

    subprocess.check_call(args)


def commit(msg, all=False, amend=False, use_commit_object=None):
    args = ['git', 'commit']

    if msg is not None:
        args.extend(['-m', '%s' % msg])

    if all:
        args.append('-a')

    if amend:
        args.append('--amend')


    if use_commit_object:
        args.extend(['-C', use_commit_object])

    subprocess.check_call(args)


def format_patch(since, start_number=None):
    """Returns a list of patch files"""
    args = ['git', 'format-patch', '-%d' % since]
    if start_number is not None:
        args.extend(['--start-number', str(start_number)])

    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    filenames = [line.strip() for line in stdout.split('\n') if line]
    return filenames
