ply
===

Patch Repository Manager


Concepts
========

A 'working repo' (WR) is linked to a 'patch repo' (PR).

The PR stores formatted patches which can be applied to the WR to create a
'patch branch' (PB).


Design
======

In the WR's working directory a file called `PATCH_REPO` is stored which
points to the local PR.


Commands
========

# Link a WR to a PR
$ ply link <path-to-patch-repo>


# Create a new PB
$ ply patch <branch-name>


# Save last commit as a patch in the PR
$ ply save


# Mark conflicts in a PB resolved
$ ply resolve
