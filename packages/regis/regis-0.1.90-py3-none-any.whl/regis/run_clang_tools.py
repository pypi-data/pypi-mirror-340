# ============================================ 
#
# Author: Nick De Breuck
# Twitter: @nick_debreuck
# 
# File: run_clang_tools.py
# Copyright (c) Nick De Breuck 2023
#
# ============================================

import os
import argparse
import regis.diagnostics
import regis.subproc
import regis.util
import regis.required_tools
import regis.rex_json
import shutil

clang_tidy_first_pass_filename = ".clang-tidy_first_pass"
clang_tidy_second_pass_filename = ".clang-tidy_second_pass"
clang_tidy_format_filename = ".clang-format"
root = regis.util.find_root()
settings = regis.rex_json.load_file(os.path.join(root, regis.util.settingsPathFromRoot))
intermediate_folder = settings["intermediate_folder"]
build_folder = settings["build_folder"]
processes_in_flight_filename = os.path.join(root, intermediate_folder, build_folder, "ninja", "post_builds_in_flight.tmp")
project = ""

class NoClangToolsConfig(Exception): pass

def __quoted_path(path):
  quote = "\""
  return f"{quote}{path}{quote}"

def __run_command(command):
  proc = regis.subproc.run(command)
  streamdata = proc.communicate()[0]
  return proc.returncode

def run(compdb : str, srcRoot : str, bRunAllChecks : bool, clangTidyRegex : str, headerFilters : str, bRebuild : bool = False):
  script_path = os.path.dirname(__file__)

  headerFiltersRegex = regis.util.create_header_filter_regex(headerFilters)

  clang_tidy_path = regis.required_tools.tool_paths_dict["clang_tidy_path"]
  clang_format_path = regis.required_tools.tool_paths_dict["clang_format_path"]
  clang_apply_replacements_path = regis.required_tools.tool_paths_dict["clang_apply_replacements_path"]
  clang_config_file = os.path.join(compdb, clang_tidy_first_pass_filename)

  compdb_path = os.path.join(compdb, "compile_commands.json")
  if os.path.exists(compdb_path):
    regis.diagnostics.log_info(f"Compiler db found at {compdb_path}")

    regis.diagnostics.log_info("Running clang-tidy - auto fixes")
    cmd = f"py {__quoted_path(script_path)}/run_clang_tidy.py -clang-tidy-binary={__quoted_path(clang_tidy_path)} -clang-apply-replacements-binary={__quoted_path(clang_apply_replacements_path)} -config-file={__quoted_path(clang_config_file)} -p={__quoted_path(compdb)} -header-filter={headerFiltersRegex} -quiet -fix {clangTidyRegex}"
    
    if not bRebuild:
      cmd += ' -incremental'
    
    proc = regis.util.run_subprocess_from_command(cmd)
    rc = regis.util.wait_for_process(proc)

    if rc != 0:
      raise Exception("clang-tidy auto fixes failed")
  
    if bRunAllChecks:
      clang_config_file = os.path.join(compdb, clang_tidy_second_pass_filename)
      regis.diagnostics.log_info("Running clang-tidy - all checks")  
      cmd = f"py {__quoted_path(script_path)}/run_clang_tidy.py -clang-tidy-binary={__quoted_path(clang_tidy_path)} -clang-apply-replacements-binary={__quoted_path(clang_apply_replacements_path)} -config-file={__quoted_path(clang_config_file)} -p={__quoted_path(compdb)} -header-filter={headerFiltersRegex} -quiet {clangTidyRegex}"
      rc = __run_command(cmd) # force clang compiler, as clang-tools expect it


  else:
    regis.diagnostics.log_warn(f"No compiler db found at {compdb}")

  regis.diagnostics.log_info("Running clang-format")
  rc = __run_command(f"py {__quoted_path(script_path)}/run_clang_format.py --clang-format-executable={__quoted_path(clang_format_path)} -r -i {srcRoot}")

  if rc != 0:
    raise Exception("clang-format failed")

def run_from_config(clangToolsConfigPath : str):
  if not os.path.isfile(clangToolsConfigPath):
    raise NoClangToolsConfig(f'clang-tools-config file does not exist at: {clangToolsConfigPath}')
  
  clang_tools_config = regis.rex_json.load_file(clangToolsConfigPath)

  source_root = clang_tools_config['SrcRoot']
  compdb = clang_tools_config['CompilerDBDirectory']
  run_all_checks = clang_tools_config['PerformAllChecks']
  clang_tidy_regex = clang_tools_config['ClangTidyRegex']
  header_filters = clang_tools_config['HeaderFilters']

  run(compdb, source_root, run_all_checks, clang_tidy_regex, header_filters)

if __name__ == "__main__":
  # arguments setups
  parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

  parser.add_argument("-compdb", help="compiler database folder")
  parser.add_argument("-srcroot", help="src root folder")
  parser.add_argument("-run-all-checks", help="run all clang tooling checks", action='store_true')
  parser.add_argument("-clang-tidy-regex", help="clang-tidy-regex to be applied. only files matching will be processed", default='*')
  parser.add_argument("-header-filters", help="header-filters regex, only matching headers will be processed", default='*')
  parser.add_argument("-rebuild", help="rebuild all", action='store_true')
  
  args, unknown = parser.parse_known_args()

 # useful for debugging
  regis.diagnostics.log_info(f"Executing {__file__}")

 # execute the script
  run(args.compdb, args.srcroot, args.run_all_checks, args.clang_tidy_regex, args.header_filters, args.rebuild)

 # print. We're done.
  regis.diagnostics.log_info("Done.")

  exit(0)