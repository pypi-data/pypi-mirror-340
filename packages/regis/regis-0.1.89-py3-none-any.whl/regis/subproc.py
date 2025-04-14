import re
import subprocess
import regis.diagnostics

def __has_word(line : str, word : str):
  return word.lower() in line.lower()

def __has_error(line : str):
  return __has_word(line, "error") or __has_word(line, "errors") or __has_word(line, "failed")

def __has_warning(line):
  return __has_word(line, "warning") or __has_word(line, "warnings")

def __build_output_callback(output : bytes):
  for line in iter(output.readline, b''):
    new_line : str = line.decode('UTF-8')
    if new_line.endswith('\n'):
      new_line = new_line.removesuffix('\n')

    if __has_error(new_line):
      regis.diagnostics.log_err(new_line)
    elif __has_warning(new_line):
      regis.diagnostics.log_warn(new_line)
    else:
      regis.diagnostics.log_no_color(new_line)

def run(cmd):
  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  __build_output_callback(proc.stdout)
  return proc
