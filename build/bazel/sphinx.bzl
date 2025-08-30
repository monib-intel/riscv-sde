# Documentation rules

"""
Bazel rules for building and managing documentation.
"""

load("@rules_python//python:defs.bzl", "py_binary")

def sphinx_doc(name, srcs, data = [], deps = [], visibility = None):
    """
    Rule to build Sphinx documentation.
    
    Args:
        name: Target name
        srcs: Source files for documentation
        data: Additional data files
        deps: Dependencies
        visibility: Target visibility
    """
    py_binary(
        name = name + "_builder",
        srcs = ["sphinx_build.py"],
        main = "sphinx_build.py",
        args = [
            "--src-dir=$(location " + srcs[0] + ")",
            "--build-dir=$(GENDIR)/" + name,
            "--format=html",
        ],
        data = srcs + data,
        deps = deps,
        visibility = visibility,
    )
    
    native.genrule(
        name = name,
        srcs = srcs + data,
        outs = [name + ".tar.gz"],
        cmd = "$(location :" + name + "_builder) && " +
              "cd $(GENDIR)/" + name + "/html && " +
              "tar -czf ../../$(RULEDIR)/" + name + ".tar.gz .",
        tools = [":" + name + "_builder"],
        visibility = visibility,
    )
