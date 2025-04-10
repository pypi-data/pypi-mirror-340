"""


"""

import os
import pathlib

import pyperclip
import time


def print_rsync_cmds_and_copy_desired_one_to_clipboard_and_execute(hostname: str ,
                                                                   remote_path: pathlib.Path ,
                                                                   local_path: pathlib.Path ,
                                                                   command_to_clipboard: int = None ,
                                                                   command_to_execute: int = None ,
                                                                   verbose: bool = True
                                                                   ) :
    """
    Display and optionally copy or execute rsync commands for syncing files between
    a local and a remote machine over SSH.

    Requirements:
    - `rsync` must be installed on both local and remote machines.
    - SSH access should be configured (e.g., via SSH keys and ~/.ssh/config).

    Parameters
    ----------
    hostname : str
        The remote host alias, e.g., 'myserver', accessible via `ssh hostname`.

    remote_path : pathlib.Path
        Path to the remote directory.

    local_path : pathlib.Path
        Path to the local directory.

    command_to_clipboard : int, optional
        If provided, the corresponding rsync command will be copied to the clipboard:
            1: remote → local
            2: local → remote
            3: remote → local (with --delete)
            4: local → remote (with --delete)

    command_to_execute : int, optional
        If provided, the corresponding rsync command will be executed.
        Should be the same as `command_to_clipboard` for clarity.

    verbose : bool, default=True
        If True, print all available rsync commands and execution status messages.
        If False, suppresses all printed output.
    """

    if not isinstance(remote_path , pathlib.Path) :
        remote_path = pathlib.Path(remote_path)
    if not isinstance(local_path , pathlib.Path) :
        local_path = pathlib.Path(local_path)

    commands = {
            1 : f"rsync -avz {hostname}:{remote_path}/ {local_path}" ,
            2 : f"rsync -avz {local_path}/ {hostname}:{remote_path}" ,
            3 : f"rsync -avz --delete {hostname}:{remote_path}/ {local_path}" ,
            4 : f"rsync -avz --delete {local_path}/ {hostname}:{remote_path}"
            }

    descriptions = {
            1 : "Sync from remote to local" ,
            2 : "Sync from local to remote" ,
            3 : "Sync from remote to local (with --delete)" ,
            4 : "Sync from local to remote (with --delete)"
            }

    if verbose :
        for i in range(1 , 5) :
            print(f"{i}. {descriptions[i]}")
            print(commands[i] , "\n")

    if command_to_clipboard is not None :
        if command_to_clipboard not in commands :
            raise ValueError("Invalid command number for clipboard.")
        pyperclip.copy(commands[command_to_clipboard])
        print(f"[Copied to clipboard] {descriptions[command_to_clipboard]}:")
        print(commands[command_to_clipboard] , "\n")

    if command_to_execute is not None :
        if command_to_execute not in commands :
            raise ValueError("Invalid command number for execution.")
        print(f"[Executing] {descriptions[command_to_execute]}:")
        print(commands[command_to_execute] , "\n")
        exit_status = os.system(commands[command_to_execute])
        if exit_status == 0 :
            print("✅ Command executed successfully.\n")
        else :
            print(f"❌ Command failed with exit status: {exit_status}\n")


def rsync_loop(hostname: str ,
               remote_path: pathlib.Path ,
               local_path: pathlib.Path ,
               command_to_execute = 3 ,
               delay_seconds: int = 60
               ) :
    """
    Continuously run a rsync command in a loop with a specified delay between iterations.

    This function is useful for periodic synchronization of files between a local and remote
    machine over SSH using rsync. The loop continues indefinitely until manually stopped
    (e.g., via Ctrl+C).

    Parameters
    ----------
    hostname : str
        The remote host alias or address accessible via SSH (must be configured via SSH keys and config).

    remote_path : pathlib.Path
        The path to the remote directory to sync to or from.

    local_path : pathlib.Path
        The path to the local directory to sync to or from.

    command_to_execute : int, default=3
        Indicates which rsync command to execute automatically in each loop:
            1: remote → local
            2: local → remote
            3: remote → local (with --delete)
            4: local → remote (with --delete)
        If None, no command will be executed—only the available commands will be printed.

    delay_seconds : int, default=60
        The number of seconds to wait between successive rsync executions.

    Behavior
    --------
    - Runs until interrupted by the user (via Ctrl+C).
    - Executes the specified rsync command every `delay_seconds` seconds.
    - Prints the command being executed and a wait message between iterations.

    Example
    -------
    >>> rsync_loop(
            hostname="myserver",
            remote_path=pathlib.Path("/remote/path"),
            local_path=pathlib.Path("/local/path"),
            command_to_execute=1,
            delay_seconds=300
        )
    """

    _f = print_rsync_cmds_and_copy_desired_one_to_clipboard_and_execute

    try :
        while True :
            _f(hostname = hostname ,
               remote_path = remote_path ,
               local_path = local_path ,
               command_to_clipboard = None ,
               command_to_execute = command_to_execute ,
               verbose = False)

            print(f"\n⏳ Waiting {delay_seconds} seconds before next sync...")

            for seconds_left in range(delay_seconds , 0 , -1) :
                print(f"  Next sync in {seconds_left} seconds..." ,
                      end = '\r' ,
                      flush = True)
                time.sleep(1)

            print(" " * 40 , end = '\r')  # Clear the line

    except KeyboardInterrupt :
        print("\n⏹️  Sync loop stopped by user (Ctrl+C). Goodbye!\n")
