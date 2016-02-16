#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import time
from os.path import join
import subprocess
from subprocess import run
import argparse
import shutil

################################################################################
# This toolchain compiles all variants of a program and compares them with
# generated input.
# - It uses `tests.json` to define the input generation.
# - By default it will run all programs in a folder (use -p to select)
# - By default it will run all tests (select by putting in nargs)
# - By default it will run the large test (-s/--small for small sets)
#
# Example:
#  ./run.py readln_ints -p read_mmfile.d,splittermap_array.d
################################################################################

parser = argparse.ArgumentParser(description="Plot coverage")
parser.add_argument('tests', nargs='*', default=[], help='Tests to run (default all)')
parser.add_argument('-s', '--small', action='store_true',
                    default=False, help='Use smaller test set')
parser.add_argument('-n', '--noclean', action='store_true',
                    default=False, help='Don\'t clean the builddir')
parser.add_argument('-p', '--programs', default=None, help='Use smaller test set')
args = parser.parse_args()


if args.programs:
    args.programs = args.programs.split(",")

compile_exts = ["d", "cpp"]
excludedFiles = ["foo", "gen_test.d"]


def main():
    root_dir = os.path.dirname(os.path.realpath(__file__))
    with open("tests.json", 'r') as fileIn:
        tests = json.load(fileIn)
    buildDir = join(root_dir, tests['buildDir'])
    os.makedirs(buildDir, exist_ok=True)
    if not args.noclean:
        shutil.rmtree(buildDir)
        os.makedirs(buildDir)
    for test_name, test_obj in tests['tests'].items():
        if len(args.tests) > 0 and test_name not in args.tests:
            continue

        print("Testing %s" % test_name)
        test_dummy_data = join(root_dir, buildDir, test_name + "_test")
        if not os.path.exists(test_dummy_data):
            print("..generating test file")
            test_method = 'gen_test_big'
            if args.small:
                test_method = 'gen_test_small'
            test_command = "rdmd " + test_obj[test_method].replace("$file", test_dummy_data)
            test_command = test_command.replace("$folder", join(root_dir, test_name)).split(" ")
            p = run(test_command, stdout=subprocess.PIPE)

        files_to_test = []
        if args.programs:
            programs = args.programs
        else:
            programs = os.listdir(join(root_dir, test_name))

        # build all d files
        for test_file_full in programs:
            if test_file_full in excludedFiles:
                continue
            print(".", end='')
            if "." not in test_file_full:
                print("invalid: %s", test_file_full)
                continue

            test_file, file_ext = test_file_full.split(".")
            build_file = join(buildDir, test_name + "_" + test_file)
            src_file = join(root_dir, test_name, test_file_full)

            if file_ext in compile_exts:
                if file_ext == "d":
                    compile_command = ("ldc -O3 -release %s" % (src_file)).split(" ")
                    # hack ldc doesn't allow one to specify output files
                    build_file = join(buildDir, test_file)
                elif file_ext == "cpp":
                    compile_command = ("g++ -O3 --std=c++11 %s -o %s" % (src_file, build_file)).split(" ")

                p = subprocess.Popen(compile_command, cwd=buildDir, stdout=subprocess.PIPE)
                p.wait()
                if p.returncode != 0:
                    print("COMPILE ERROR")
                    print(p.stdout)
                run_command = ("%s %s" % (build_file, test_dummy_data)).split(" ")
            elif file_ext == "py":
                src_file = join(root_dir, test_name, test_file_full)
                run_command = ("%s %s" % (src_file, test_dummy_data)).split(" ")
            else:
                print("Unknown extension")
                continue

            files_to_test.append((test_file, run_command))

        stats = {}
        check_stdout = None
        for test_file, run_command in files_to_test:
            start_time = time.time()
            p = run(run_command, stdout=subprocess.PIPE)
            if check_stdout is not None:
                if check_stdout != p.stdout.strip():
                    print("OUTPUT DIFFERENT %s", test_file)
            else:
                check_stdout = p.stdout.strip()
            run_time = time.time() - start_time
            stats[test_file] = run_time

        min_runtime = min(stats.items(), key=lambda x: x[1])
        run_times = sorted(stats.items(), key=lambda x: x[1])
        for run_time in run_times:
            print("\r.%s %.1f%% (%.4f s)" % (run_time[0], run_time[1] / min_runtime[1] * 100, run_time[1]))

    # our testing files are quite large - remove them
    if not args.noclean:
        shutil.rmtree(buildDir)


if __name__ == "__main__":
    main()
