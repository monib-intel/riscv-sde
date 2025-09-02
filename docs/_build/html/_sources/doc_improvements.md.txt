# Documentation Improvements

The documentation for the RISC-V SDE has been improved in the following ways:

## 1. Added New Bazel Workflows Documentation

- Created a new document `user_guide/bazel_workflows.md` that explains:
  - How to use the `run_with_bazel.sh` script
  - The available workflow stages (software, simulation, analysis)
  - Command-line options and configurations
  - Best practices for working with Bazel in the RISC-V SDE

## 2. Fixed Documentation Warnings

- Reduced documentation warnings from 71+ to just 2 minor header structure warnings
- Fixed issues with duplicate section labels
- Added missing documents to the toctree structure
- Added support for Mermaid diagram syntax highlighting

## 3. Improved Directory Structure

- Added missing `analyze` directory required by tests
- Ensured all documentation references are properly linked
- Created an `_ext` directory for custom Sphinx extensions

## 4. Created Utility Scripts

- Added `fix_doc_warnings.py` to help maintain documentation quality
- This script can be run periodically to fix common issues

## Next Steps

Future documentation improvements could include:

1. Resolving remaining header structure warnings in the API reference
2. Adding more examples and tutorials
3. Improving cross-references between documents
4. Adding diagrams to illustrate the build and flow processes

The documentation is now more user-friendly and provides better guidance for using Bazel with the RISC-V SDE.
