ply
===

Patch Repository Manager


Description
===========

`ply` is a utility to manage patches held against another project. These
patches are stored in a separate `git` repository and are applied to generate
a `patch branch` that you can package or deploy from.

`ply` is similar to other tools like `quilt` and `sGit` but differs in some
key ways:

1. Simple, maintains a linear, sequence of patches to applied to `master`
2. Tightly integrated with `git`
3. Doesn't require you to checkpoint files before you edit them (like `quilt`
   does).


Concepts
========

A 'working repo' (WR) is linked to a 'patch repo' (PR).

The PR stores formatted patches which can be applied to the WR to create a
'patch branch' (PB).

New patches are created by adding a commit to a PB and then saving into the
PR.

If the WR changes, conflicts will be created in a PB. These are resolved one
at a time by editing the files and then running `ply resolve`. This process
updates the patches in the PR so that these lines won't conflict in the
future. (One way to think of this is as a cross-repository rebase, we're
rebasing the changes in the PR onto the WR to generate a PB.)


Design
======

In the WR's working directory a file called `PATCH_REPO` is stored which
points to the local PR.


Commands
========

::

    # Link a WR to a PR
    $ ply link <path-to-patch-repo>


    # Create a new PB
    $ ply patch <branch-name>


    # Save last commit as a patch in the PR
    $ ply save


    # Mark conflicts in a PB resolved
    $ ply resolve
