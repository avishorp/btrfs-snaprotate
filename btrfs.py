
import os, re, logging, subprocess

class BTRFSExecutionError(RuntimeError):
    def __init__(self, ec, stdout, stderr):
        super(BTRFSExecutionError, self).__init__("BTRFS Execution failed")
        self.ec = ec
        self.stdout = stdout
        self.stderr = stderr

class BTRFSUtil:
  BTRFS_UTIL_EXE_NAME = "btrfs"

  def __init__(self, btrfs_exe = None):
    if btrfs_exe is not None:
      self.btrfs_exe = btrfs_exe
    else:
      self.btrfs_exe = self.which(self.BTRFS_UTIL_EXE_NAME)

    if self.btrfs_exe is None:
        raise RuntimeError("Could not find btrfs executable")

    # Used to decode "subvolume show" command results
    self.show_regex = re.compile(r"([a-zA-Z ()]+):\s*([^\s].*)")

  def which(self, exename):
    # Find the an executable in the path
    for path in os.environ["PATH"].split(os.pathsep):
      path = path.strip('"')
      exe = os.path.join(path, exename)
      if os.path.isfile(exe) and os.access(exe, os.X_OK):
        return exe

    # Not found
    return None

  def exec_btrfs_util(self, arguments):
    cmd = [self.btrfs_exe] + arguments
    logging.debug('Executing: ' + ' '.join(cmd))
    btrfs_proc = subprocess.Popen([self.btrfs_exe] + arguments,
        stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    (stdout, stderr) = btrfs_proc.communicate()
    logging.debug('btrfs finised with return code %d' % btrfs_proc.returncode)

    return (btrfs_proc.returncode, stdout, stderr)

  def create_snapshot(self, subvol, dest):
      ec, stdout, stderr = self.exec_btrfs_util(['subvolume', 'snapshot', subvol, dest])
      if ec != 0:
          # Problem executing the util
          raise BTRFSExecutionError(ec, stdout, stderr)

  def delete_snapshot(self, snapname):
      ec, stdout, stderr = self.exec_btrfs_util(['subvolume', 'delete', 'snapname'])
      if ec != 0:
          # Problem executing the util
          raise BTRFSExecutionError(ec, stdout, stderr)

  def list_subvolumes(self, pathname):
    ec, stdout, stderr = self.exec_btrfs_util(['subvolume', 'list', pathname])
    if (ec != 0):
          # Problem executing the util
          raise BTRFSExecutionError(ec, stdout, stderr)

    subvols = []
    for l in stdout.split('\n'):
        # The subvolume path is the 9th field
        fss = l.split(' ')
        if ((len(fss) >= 9) and (fss[7] == 'path')):
            subvols.append(fss[8])

    return subvols

  def show_subvolume(self, pathname):
    ec, stdout, stderr = self.exec_btrfs_util(['subvolume', 'show', pathname])
    if (ec != 0):
          # Problem executing the util
          raise BTRFSExecutionError(ec, stdout, stderr)

    # Convert the command output into key-data pairs
    info = {}
    for l in stdout.split('\n'):
        m = self.show_regex.match(l.strip())
        if m is not None:
            key = m.groups()[0]
            value = m.groups()[1]
            info[key] = value

    return info

  def is_btrfs(self, pathname):
    ec, stdout, stderr = self.exec_btrfs_util(['subvolume', 'list', pathname])
    return (ec == 0)

  def btrfs_util_version(self):
      # Exepect a return string looking like this
      ver_string = re.compile(r"btrfs-progs v([0-9]+\.[0-9]+)")

      # Execute btrfs to get the version
      ec, stdout, stderr = self.exec_btrfs_util(['version'])

      # Check the return code and the version string
      if ec != 0:
          # Problem executing the util
          raise BTRFSExecutionError(ec, stdout, stderr)

      v = ver_string.match(stdout)
      if v is None:
          # Malformed version string
          raise BTRFSExecutionError(ec, stdout, stderr)

      # This is the version extracted
      return v.groups()[0]
