#!/usr/bin/env python3

# Run from the current directory.

import argparse
import sys

import testconfig
import logging
import subprocess
from pathlib import Path
from typing import List

root_path = Path(__file__).parent.resolve()


def subdirs() -> List[Path]:
    dirs: List[Path] = []
    for r in root_path.iterdir():
        if r.is_dir():
            dirs.extend(Path(r).rglob("**/"))
    return [d for d in dirs if not (any(c.startswith("_") for c in d.parts) or any(c.startswith(".") for c in d.parts))]


def module_dict(module):
    return {k: v for k, v in module.__dict__.items() if not k.startswith("_")}


def dir_config(dir):
    import importlib

    module_name = str(dir.relative_to(root_path)).replace("/", ".") + ".config"
    try:
        return module_dict(importlib.import_module(module_name))
    except ModuleNotFoundError:
        return {}


def read_file(filename):
    with open(filename) as f:
        return f.read()
    return None


# Input file
def workflow_yaml_template_text(os):
    return Path(root_path / f"runner-templates/build-test-{os}").read_text()


# Output files
def workflow_yaml_file(dir, os, test_name):
    return Path(dir / f"build-test-{os}-{test_name}.yml")


# String function from test dir to test name
def test_name(dir):
    return str(dir.relative_to(root_path)).replace("/", "-")


def transform_template(template_text, replacements):
    t = template_text
    for r, v in replacements.items():
        t = t.replace(r, v)
    return t


def test_files_in_dir(dir):
    g = Path(root_path / dir).glob("test_*.py")
    return [] if g is None else [f for f in g]


# Replace with update_config
def generate_replacements(conf, dir, test_files):
    assert len(test_files) > 0
    replacements = {
        "INSTALL_TIMELORD": read_file(Path(root_path / "runner-templates/install-timelord.include.yml")).rstrip(),
        "CHECKOUT_TEST_BLOCKS_AND_PLOTS": read_file(
            Path(root_path / "runner-templates/checkout-test-plots.include.yml")
        ).rstrip(),
        "TEST_DIR": "",
        "TEST_NAME": "",
        "PYTEST_PARALLEL_ARGS": "",
    }

    if not conf["checkout_blocks_and_plots"]:
        replacements[
            "CHECKOUT_TEST_BLOCKS_AND_PLOTS"
        ] = "# Omitted checking out blocks and plots repo Chia-Network/test-cache"
    if not conf["install_timelord"]:
        replacements["INSTALL_TIMELORD"] = "# Omitted installing Timelord"
    if conf["parallel"]:
        replacements["PYTEST_PARALLEL_ARGS"] = " -n auto"
    if conf["job_timeout"]:
        replacements["JOB_TIMEOUT"] = str(conf["job_timeout"])
    test_paths = [str(f.relative_to(root_path.parent)) for f in test_files]
    # We have to list the test files individually until pytest has the
    # option to only collect tests in the named dir, and not those below
    replacements["TEST_DIR"] = " ".join(sorted(test_paths))
    replacements["TEST_NAME"] = test_name(dir)
    if "test_name" in conf:
        replacements["TEST_NAME"] = conf["test_name"]
    for var in conf["custom_vars"]:
        replacements[var] = conf[var] if var in conf else ""
    return replacements


# Overwrite with directory specific values
def update_config(parent, child):
    if child is None:
        return parent
    conf = child
    for k, v in parent.items():
        if k not in child:
            conf[k] = v
    return conf


def dir_path(string):
    p = Path(root_path / string)
    if p.is_dir():
        return p
    else:
        raise NotADirectoryError(string)


# args
arg_parser = argparse.ArgumentParser(description="Build github workflows")
arg_parser.add_argument("--output-dir", "-d", default="../.github/workflows", type=dir_path)
arg_parser.add_argument("--fail-on-update", "-f", action="store_true")
arg_parser.add_argument("--verbose", "-v", action="store_true")
args = arg_parser.parse_args()

if args.verbose:
    logging.basicConfig(format="%(asctime)s:%(message)s", level=logging.DEBUG)

# main
test_dirs = subdirs()

for os in testconfig.oses:
    template_text = workflow_yaml_template_text(os)
    for dir in test_dirs:
        test_files = test_files_in_dir(dir)
        if len(test_files) == 0:
            logging.info(f"Skipping {dir}: no tests collected")
            continue
        conf = update_config(module_dict(testconfig), dir_config(dir))
        replacements = generate_replacements(conf, dir, test_files)
        txt = transform_template(template_text, replacements)
        logging.info(f"Writing {os}-{test_name(dir)}")
        workflow_yaml_file(args.output_dir, os, test_name(dir)).write_text(txt)

if subprocess.run(["git", "--no-pager", "diff", args.output_dir], capture_output=True).stdout:
    print("New workflow updates available.")
    if args.fail_on_update:
        sys.exit(1)
else:
    print("Nothing to do.")
