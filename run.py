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


parser = argparse.ArgumentParser(description="Plot coverage")
parser.add_argument('tests', nargs='*', default=[], help='Tests to run (default all)')
parser.add_argument('-s', '--small', action='store_true',
                    default=False, help='Use smaller test set')
parser.add_argument('-n', '--noclean', action='store_true',
                    default=False, help='Don\'t clean the builddir')
args = parser.parse_args()


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

        stats = {}
        check_stdout = None
        for test_file in test_obj['files']:
            print(".", end='')
            src_file = join(root_dir, test_name, "%s.d" % test_file)
            build_file = join(buildDir, test_file)
            compile_command = ("gdc -O3 %s -o %s" % (src_file, build_file)).split(" ")
            p = run(compile_command, stdout=subprocess.PIPE)
            if p.returncode != 0:
                print("COMPILE ERROR")
                print(p.stdout)
            start_time = time.time()
            run_command = ("%s %s" % (build_file, test_dummy_data)).split(" ")
            p = run(run_command, stdout=subprocess.PIPE)
            if check_stdout is not None:
                if check_stdout != p.stdout.strip():
                    print("OUTPUT DIFFERENT")
            else:
                check_stdout = p.stdout.strip()
            run_time = time.time() - start_time
            stats[test_file] = run_time

        min_runtime = min(stats.items(), key=lambda x: x[1])
        run_times = sorted(stats.items(), key=lambda x: x[1])
        for run_time in run_times:
            print("\r.%s %.0f%% (%.4f s)" % (run_time[0], run_time[1] / min_runtime[1] * 100, run_time[1]))


if __name__ == "__main__":
    main()
