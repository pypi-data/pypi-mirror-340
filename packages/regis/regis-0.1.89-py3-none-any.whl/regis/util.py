import os
import subprocess
import shutil
import sys
import time
import itertools
import threading
import re
from pathlib import Path
import regis.diagnostics
import regis.rex_json

settingsPathFromRoot = os.path.join("_build", "config", "settings.json")

def create_version_file(directory : str, tag : str):
    version = {
        "tag": tag
    }

    if not os.path.exists(directory):
      os.mkdir(directory)
      
    path = os.path.join(directory, "version.json")
    regis.rex_json.save_file(path, version)

def load_version_file(directory):
  version_file = os.path.join(directory, "version.json")
  if os.path.exists(version_file):
    version_data = regis.rex_json.load_file(version_file)           
    if version_data != None:
      return version_data["tag"]

  return None

def env_paths():
  envPath = os.environ["PATH"]
  paths = envPath.split(os.pathsep)
  return paths

def create_header_filter_regex(headerFilters : list[str]):
  res = ""

  for filter in headerFilters:
    res += "("
    res += filter
    res += ")|"

  res = res.removesuffix("|")
  return res

def find_file_in_folder(file, path : str):
  fileToFind = file.lower()
  subFilesOrFolders = os.listdir(path)
  for fileOrFolder in subFilesOrFolders:
    absPath = os.path.join(path, fileOrFolder)
    if os.path.isfile(absPath):
      file_name = Path(absPath).name.lower()
      if file_name == fileToFind:
        return absPath
  
  return ''

def find_file_in_paths(file, directories : list[str]):
  for path in directories:
    if not os.path.exists(path):
      continue

    result = find_file_in_folder(file, path)
    if result != '':
      return result

  return ''

def find_directory_in_paths(dir : str, directories : list[str]):
  dir = dir.replace('\\', '/')
  folders = dir.split('/')  
  num_folders = len(folders)

  for path in directories:
    path = path.replace('\\', '/')
    path_folders = path.split('/')

    dir_idx = -1

    if os.path.exists(os.path.join(path, dir)):
      return os.path.join(path, dir)

    dir_idx = num_folders - 1
    path_idx = len(path_folders) - 1
    if (len(path_folders) < num_folders):
      continue

    while dir_idx >= 0:
      dir_folder = folders[dir_idx]
      path_folder = path_folders[path_idx]
      
      if dir_folder != path_folder:
        break

      dir_idx -= 1
      path_idx -= 1

    if dir_idx == -1:
      if os.path.exists(path):
        return path
      else:
        regis.diagnostics.log_err(f"matching directory found, but doesn't exist: {path}")

  return None

def find_in_parent(path, toFind):
  curr_path = path

  while toFind not in os.listdir(curr_path):
    if Path(curr_path).parent == curr_path:
      regis.diagnostics.log_err(f"{toFind} not found in parents of {path}")
      return ''

    curr_path = Path(curr_path).parent

  return curr_path.__str__()

def find_root(startPath = os.getcwd()):
  res = find_in_parent(startPath, "source")
  if (res == ''):
    regis.diagnostics.log_err(f"root not found")

  return res

def find_files_with_extension(path : str, extension : str):
  files = os.listdir(path)
  files_with_extension = []
  for file in files:
    if Path(file).suffix == extension:
      files_with_extension.append(file)

  return files_with_extension

def is_windows():
  return os.name == 'nt'

def run_subprocess_from_command(command : str):
  proc = subprocess.Popen(command)
  return proc

def run_subprocess(command : str, args = []):
  proc = subprocess.Popen(executable=command, args=args)
  return proc

def run_and_get_output(command):
  proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  output, errc = proc.communicate()

  return output.decode('utf-8'), proc.returncode

def run_subprocess_with_working_dir(command, workingDir):
  proc = subprocess.Popen(command, cwd=workingDir)
  return proc

def run_subprocess_with_callback(command, callback, filterLines):
  proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  callback(proc.pid, proc.stdout, False, filterLines)
  callback(proc.pid, proc.stderr, True, filterLines)
  return proc

def wait_for_process(process):
  process.wait()
  return process.returncode

def is_executable(path):
  if is_windows():
    if Path(path).suffix == ".exe":
      return True
  else:
    return os.access(path, os.X_OK)

def find_all_files_in_folder(dir, toFindRegex):
  return list(Path(dir).rglob(toFindRegex))

def remove_folders_recursive(dir : str):
  if os.path.exists(dir):
    shutil.rmtree(dir)

def temp_cwd(newdir : str):
	"""Create a scoped working directory. 
		
		Example usage:

		with R.temp_cwd('c:\\p4') as d:
			# cwd is now set to c:\\p4
			t = os.path.join('data.txt')
			with open(t, 'wb') as f:
				f.write(data)
			shutil.move(t, somewhere)
		--> cwd is reset to what it was before it entered scope
	"""
	class temp_cwd_(object):
		def __init__(self, newdir):
					self.ndir = newdir
					self.odir = os.getcwd()

		def __enter__(self):
			os.chdir(self.ndir)
			return self.ndir
		
		def __exit__(self, extype, exvalue, tb):
			os.chdir(self.odir)

	return temp_cwd_(newdir)

class LoadingAnimation():
    def __init__(self, msg = 'loading'):
      self.done = False
      self.msg = msg


    def __enter__(self):
      self.thread = threading.Thread(target=self.start)
      self.thread.start()
      return self

    def __exit__(self, exc_type, exc_value, traceback):
      self.stop()

    def start(self):
      for c in itertools.cycle(['|', '/', '-', '\\']):
        if self.done:
            break
        sys.stdout.write(f'\r{self.msg} ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
      num_spaces = len(self.msg)
      sys.stdout.write('\rDone!'.rjust(num_spaces, ' '))
      sys.stdout.write('\n')
      sys.stdout.flush()

    def stop(self):
       self.done = True
       self.thread.join()

def to_camelcase(input : str):
    # We capitalize the first letter of each component except the first one
    # with the 'capitalize' method and join them together.
    return "".join(x.capitalize() for x in input.lower().split("_"))

def to_snakecase(input : str):
  return re.sub(r'(?<!^)(?=[A-Z])', '_', input).lower()

def ask_yesno(question : str):
   answer = input(f'{question}\n')
   if answer.lower() == 'y' or answer.lower() == 'yes':
      return True
   
   return False
   