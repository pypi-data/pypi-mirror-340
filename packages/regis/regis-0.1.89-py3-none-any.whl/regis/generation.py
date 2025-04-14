import os
import copy
import argparse
import shlex
import regis.diagnostics
import regis.rex_json
import regis.util
import regis.required_tools
import regis.subproc
import regis.diagnostics

from pathlib import Path

root = regis.util.find_root()
settings = regis.rex_json.load_file(os.path.join(root, regis.util.settingsPathFromRoot))
temp_dir = os.path.join(root, settings["intermediate_folder"])
tools_install_dir = os.path.join(temp_dir, settings["tools_folder"])
tool_paths_filepath = os.path.join(tools_install_dir, "tool_paths.json")
tool_paths_dict = regis.rex_json.load_file(tool_paths_filepath)

def _find_sharpmake_files(directory):
  sharpmakes_files = []
  for root, dirs, files in os.walk(directory):      
    cs_files = []
    sharpmake_file_found = False
    for file in files:
      extensions = Path(file).suffixes
      path = os.path.join(root, file)
      if len(extensions) == 2:
        if extensions[0] == ".sharpmake" and extensions[1] == ".cs":
          sharpmakes_files.append(path)
          sharpmake_file_found = True
      if len(extensions) == 1:
        if extensions[0] == ".cs":
          cs_files.append(path)

    if 'include' in dirs and 'src' in dirs:
      if len(cs_files) and sharpmake_file_found == False:
        regis.diagnostics.log_warn(f'Expected sharpmake files at "{root}" but none were found')
        regis.diagnostics.log_warn(f'Possible sharpmake files..')
        for cs_file in cs_files:
          regis.diagnostics.log_warn(f'- {cs_file}')
        
        regis.diagnostics.log_warn(f'A sharpmake file should end with ".sharpmake.cs", please rename the extension of your sharpmake files.')
  
  return sharpmakes_files

def _find_sharpmake_root_files(directory):
  sharpmakes_files = []
  for root, dirs, files in os.walk(directory):
    for file in files:
      extensions = Path(file).suffixes
      if len(extensions) == 1:
        if extensions[0] == ".cs":
          path = os.path.join(root, file)
          sharpmakes_files.append(path)

  return sharpmakes_files

def _scan_for_sharpmake_files(settings : dict):
  """
  scans for sharpmake files in the current directory using the settings.
  it searches for all the sharpmake files in the sharpmake root, source folder and test folder.
  all searches are done recursively.
  """
  sharpmake_root = os.path.join(root, "_build", "sharpmake", "src")
  source_root = os.path.join(root, settings["source_folder"])
  tests_root = os.path.join(root, settings["tests_folder"])
  
  sharpmakes_files = []
  sharpmakes_files.extend(_find_sharpmake_root_files(sharpmake_root))
  sharpmakes_files.extend(_find_sharpmake_files(source_root))
  sharpmakes_files.extend(_find_sharpmake_files(tests_root))

  return sharpmakes_files

def _config_path():
  config_dir = os.path.join(os.path.join(root, settings['intermediate_folder'], settings['build_folder']))
  config_path = os.path.join(config_dir, 'generation_config.json')
  return config_path

def _save_config_file(config : dict):
  """Create a new config file. This file will be passed over to sharpmake"""

  config_path = _config_path()
  config_dir = os.path.dirname(config_path)
  if not os.path.exists(os.path.dirname(config_dir)):
    os.mkdir(config_dir)

  config_dir_path = os.path.dirname(config_path)
  if not os.path.isdir(config_dir_path):
    os.makedirs(config_dir_path)

  if config:
    regis.rex_json.save_file(config_path, config)

  return config_path.replace('\\', '/')

def _load_config_file():
  config_dir = os.path.join(os.path.join(root, settings['intermediate_folder'], settings['build_folder']))
  config_path = os.path.join(config_dir, 'generation_config.json')
  return regis.rex_json.load_file(config_path)

def _make_optional_arg(arg : str):
  return f'-{arg}'

def _add_config_arguments(parser : argparse.ArgumentParser, defaultConfig : dict):
  """Load the sharpmake config file from disk and add the options as arguments to this script."""
  settings = defaultConfig["settings"]
  for setting in settings:
    arg = _make_optional_arg(setting)
    val = settings[setting]['Value']
    desc = settings[setting]['Description']
    if 'Options' in settings[setting]:
      desc += f' Options: {settings[setting]["Options"]}'
    
    if type(val) == bool:
      parser.add_argument(arg, help=desc, action='store_true', default=val)
    else:
      parser.add_argument(arg, help=desc, default=val)

def _load_default_config():
  return regis.rex_json.load_file(os.path.join(root, "_build", "sharpmake", "data", "default_config.json"))

def _load_correct_config(useDefaultConfig : bool):
  default_config = _load_default_config()
  if useDefaultConfig:
    return default_config

  if not os.path.exists(_config_path()):
    return default_config

  cached_config = _load_config_file()
  default_version = default_config['version']
  cached_version = cached_config.get('version')
  if default_version != cached_version:
    regis.diagnostics.log_info('generation config version mismatch. Using default config')
    return default_config

  return cached_config

def add_config_arguments_to_parser(parser, useDefaultConfig : bool):
  _add_config_arguments(parser, _load_correct_config(useDefaultConfig))  

def create_config(args, useDefault = True):
  """Create a config dictionary based on the arguments passed in."""

  regis.diagnostics.log_info(f'Creating config using: {args}')

  if type(args) == str:
    parser = argparse.ArgumentParser()
    add_config_arguments_to_parser(parser, useDefault)
    args = parser.parse_args(shlex.split(args))

  config_input = _load_correct_config(useDefault)
  config : dict = copy.deepcopy(config_input)
  for arg in vars(args):
    arg_name = arg
    arg_name = arg_name.replace('_', '-') # python converts all hyphens into underscores so we need to convert them back
    arg_val = getattr(args, arg)

    if arg_name in config['settings']:
      config['settings'][arg_name]['Value'] = arg_val

  return config

def new_generation(settings : dict, config : dict, sharpmakeArgs : list[str] = []):
  """
  performs a new generation using the sharpmake files found by searching the current directory recursively.\n
  '/diagnostics' is always added as a sharpmake arguments.\n
  If config is None the previous used config will be used for generation
  """

  # save the config file to disk
  config_path = _save_config_file(config)
  regis.diagnostics.log_info(f'Saved generation config file to {config_path}')

  # scan recursively to find all the sharpmake files
  sharpmake_files = _scan_for_sharpmake_files(settings)
  
  # load the path where the sharpmake executable is located
  sharpmake_path = tool_paths_dict["sharpmake_path"]
  if len(sharpmake_path) == 0:
    regis.diagnostics.log_err("Failed to find sharpmake path")
    return

  # make sure the sharpmake files are quoted, that's expected by sharpmake
  sharpmake_sources = ""
  for sharpmake_file in sharpmake_files:
    sharpmake_sources += "\""
    sharpmake_sources += sharpmake_file
    sharpmake_sources += "\", "

  # replace all backwards slashes by forward slashes
  sharpmake_sources = sharpmake_sources[0:len(sharpmake_sources) - 2]
  sharpmake_sources = sharpmake_sources.replace('\\', '/')

  # run the actual executable
  proc = regis.util.run_subprocess_from_command(f"{sharpmake_path} /sources({sharpmake_sources}) /diagnostics /configFile(\"{config_path}\") {' '.join(sharpmakeArgs)}")
  regis.util.wait_for_process(proc)
  return proc.returncode