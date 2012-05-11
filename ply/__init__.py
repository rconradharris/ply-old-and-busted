import glob
import os

from ply import exceptions
from ply import git
from ply import utils


def create_patch_branch(patch_repo_path, branch_name):
    git.checkout(branch_name, create_and_reset=True)
    write_patch_head(0)
    apply_patches(patch_repo_path)


def apply_patches(patch_repo_path, start_patch_num=1):
    for patch_path in get_all_patch_paths(patch_repo_path):
        filename = os.path.basename(patch_path)
        patch_num = get_patch_num_from_patch_name(filename)
        if patch_num < start_patch_num:
            continue

        git.am(patch_path, three_way_merge=True)
        write_and_commit_patch_head(patch_num)


def get_patch_repo_path(path):
    """Return location of PR"""
    patch_repo_path = utils.read_nearest_file('.PATCH_REPO', path).strip()
    return patch_repo_path


def get_patch_num_from_patch_name(patch_name):
    patch_prefix = patch_name.split('-', 1)[0]
    patch_num = int(patch_prefix)
    return patch_num


def link(patch_repo_path):
    """Link a working repo to a patch repo.

    Creates a .ply directory to hold ply state.
    """
    patch_repo_path = utils.fixup_path(patch_repo_path)

    if not os.path.exists(patch_repo_path):
        raise exceptions.PathNotFound(patch_repo_path)

    # TODO: verify that this is a git repo
    utils.write_file('.PATCH_REPO', patch_repo_path)


def get_patch_head(path):
    return int(utils.read_nearest_file('.PATCH_HEAD', path).strip())


def get_all_patch_paths(patch_repo_path):
    patches_glob = os.path.join(patch_repo_path, "*.patch")
    for path in glob.iglob(patches_glob):
        yield path


def get_max_patch_num(patch_repo_path):
    patch_paths = list(get_all_patch_paths(patch_repo_path))
    if not patch_paths:
        return 0

    last_patch_path = patch_paths[-1]
    filename = os.path.basename(last_patch_path)
    patch_num = get_patch_num_from_patch_name(filename)
    return patch_num


def resolve(path, patch_repo_path):
    git.am(resolved=True)

    last_patch_num = get_patch_head(path)
    this_patch_num = last_patch_num + 1

    generate_and_commit_to_patch_repo(
            patch_repo_path, start_number=this_patch_num)

    next_patch_num = this_patch_num + 1
    apply_patches(patch_repo_path, start_patch_num=next_patch_num)


def save(patch_repo_path):
    """Writes out last git commit to a patch file in the patch repo.

    """
    # TODO: add guard to ensure that new commit differs from last master
    # commit and last applied patch. Forgetting to commit, will be a common
    # mistake!
    next_patch_num = get_max_patch_num(patch_repo_path) + 1

    # TODO: write these patch files to the ply directory
    # NOTE: for now we're assuming we're dealing with 1 patch (could it be
    # more?)
    generate_and_commit_to_patch_repo(
            patch_repo_path, start_number=next_patch_num)


def generate_and_commit_to_patch_repo(patch_repo_path, start_number=None):
    # NOTE: assume we're dealing with one patch for now
    filenames = git.format_patch(1, start_number=start_number)
    for filename in filenames:
        os.rename(filename, os.path.join(patch_repo_path, filename))

    # TODO: generate a different commit message based on whether this is the
    # original patch commit, or resolving a conflict
    with utils.temporary_chdir(patch_repo_path):
        for filename in filenames:
            git.add(filename)
        git.commit("Adding or updating %d" % start_number)


def write_and_commit_patch_head(patch_num):
    write_patch_head(patch_num)

    git.add('.PATCH_HEAD')

    # Don't create a separate commit just to bump the PATCH_HEAD
    git.commit(None, amend=True, use_commit_object="HEAD")


def write_patch_head(patch_num):
    """Write out a counter which keeps track of the last successfully applied
    patch.
    """
    with open('.PATCH_HEAD', 'w') as f:
        f.write("%d\n" % patch_num)
