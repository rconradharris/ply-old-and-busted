ply
===

Patch Repository Manager


Description
===========

`ply` is a utility to manage a series of patches against an upstream project.
These patches are stored as files in a separate git repositiory so that they
can themselves be versioned. The patch series is applied in order to create a
patch-branch which can then be used for packaging and/or deployment.


Concepts
========

The upstream project is housed in the ``working repo`` (WR).

The series of patches are stored in the ``patch repo`` (PR).

The patches in the PR can be applied to the WR to generate a ``patch branch``
(PB).

Patches are added to the PR by committing a new patch to the PB and then
running `ply save`.

If conflicts are encountered while generating the PB, the affected patches in
the PR are updated so that future conflicts won't occur.


Design
======

In the WR's working directory a file called `PATCH_REPO` is stored which
points to the local PR.

Each PB has a file called `PATCH_HEAD` which stores the index of the last
successfully applied patch.


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
