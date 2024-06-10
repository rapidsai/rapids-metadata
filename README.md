# RAPIDS Metadata

`rapids-metadata` is a repository where information about the structure of the
RAPIDS project itself is kept. This information is split into RAPIDS versions,
which in turn are split into RAPIDS repositories, which are further split into
RAPIDS packages (both Python packages and Conda packages.)

The information currently provided by this package consists of:

- Which RAPIDS repositories are available
- Which RAPIDS packages are available
- Which RAPIDS packages require a CUDA suffix (`-cu11`, `-cu12`, etc.)
- Which RAPIDS packages require an alpha spec (`>=0.0.0a0`) due to publishing
  nightly binaries

The motivating use case for this project is
[`pre-commit-hooks`](https://github.com/rapidsai/pre-commit-hooks), but other
projects may certainly use it too.

## Justification

`pre-commit-hooks` has to know things about the structure of the RAPIDS project
in order to make the correct recommendations to the developer. However, this
structure changes frequently enough that publishing a new version of
`pre-commit-hooks` for each structural change is not feasible. Therefore, this
package acts as an unpinned dependency of `pre-commit-hooks` (and any other
project that wants to use it) so that the RAPIDS project structure can be
maintained independently of the `pre-commit-hooks` logic.
