# External Dependencies

This directory is for managing git submodules and external dependencies that are not handled by Bazel or package managers.

## Adding Dependencies

To add a new external dependency as a git submodule:

```bash
git submodule add https://github.com/username/repo.git dependencies/repo-name
git submodule update --init --recursive
```

## Current Dependencies

Below is a list of the current external dependencies:

| Dependency | Description | Version | URL |
|------------|-------------|---------|-----|
| (none yet) | | | |

## Updating Dependencies

To update all dependencies:

```bash
git submodule update --remote
```

To update a specific dependency:

```bash
cd dependencies/repo-name
git fetch
git checkout <tag-or-commit>
cd ../..
git add dependencies/repo-name
git commit -m "Update repo-name to <tag-or-commit>"
```
