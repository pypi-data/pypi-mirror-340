"""


"""

import os
import pathlib

import pyperclip
import time


def display_copy_execute_rsync(hostname: str,
                               remote_path: pathlib.Path,
                               local_path: pathlib.Path,
                               command_to_clipboard: int = None,
                               command_to_execute: int = None,
                               verbose: bool = True):
    """
    Display, copy to clipboard, or execute rsync commands for syncing files between
    a local and a remote machine over SSH.

    Requirements
    ------------
    - `rsync` must be installed on both the local and remote machines.
    - SSH access should be configured (e.g., via SSH keys and `~/.ssh/config`).

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
        Should match `command_to_clipboard` if both are used.

    verbose : bool, default=True
        If True, prints all available rsync commands and status messages.
        If False, suppresses all printed output.

    Behavior
    --------
    - Prints four rsync command options for file synchronization.
    - If `command_to_clipboard` is provided, the specified command is copied to the clipboard.
    - If `command_to_execute` is provided, the specified command is executed via the system shell.
    - If both are provided, the same command can be copied and executed.

    Examples
    --------
    Example 1: Copy and execute the rsync command from remote to local
    >>> from pathlib import Path
    >>> display_copy_execute_rsync(
    ...     hostname='myserver',
    ...     remote_path=Path('/remote/data'),
    ...     local_path=Path('/local/data'),
    ...     command_to_clipboard=1,
    ...     command_to_execute=1,
    ...     verbose=True
    ... )

    Output:
    1. Sync from remote to local
    rsync -avz myserver:/remote/data/ /local/data

    2. Sync from local to remote
    rsync -avz /local/data/ myserver:/remote/data

    3. Sync from remote to local (with --delete)
    rsync -avz --delete myserver:/remote/data/ /local/data

    4. Sync from local to remote (with --delete)
    rsync -avz --delete /local/data/ myserver:/remote/data

    [Copied to clipboard] 1. Sync from remote to local:
    rsync -avz myserver:/remote/data/ /local/data

    [Executing] 1. Sync from remote to local:
    rsync -avz myserver:/remote/data/ /local/data

    ✅ Command 1 executed successfully.

    Example 2: Show available rsync commands only
    >>> display_copy_execute_rsync(
    ...     hostname='g01',
    ...     remote_path=Path('/remote/data'),
    ...     local_path=Path('/local/data')
    ... )

    Output:
    1. Sync from remote to local
    rsync -avz g01:/remote/data/ /local/data

    2. Sync from local to remote
    rsync -avz /local/data/ g01:/remote/data

    3. Sync from remote to local (with --delete)
    rsync -avz --delete g01:/remote/data/ /local/data

    4. Sync from local to remote (with --delete)
    rsync -avz --delete /local/data/ g01:/remote/data
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
        print(f"[Copied to clipboard] {command_to_clipboard}.{descriptions[command_to_clipboard]}:")
        print(commands[command_to_clipboard] , "\n")

    if command_to_execute is not None :
        if command_to_execute not in commands :
            raise ValueError("Invalid command number for execution.")
        print(f"[Executing] {command_to_execute}.{descriptions[command_to_execute]}:")
        print(commands[command_to_execute] , "\n")
        exit_status = os.system(commands[command_to_execute])
        if exit_status == 0 :
            print(f"✅ Command {command_to_execute} executed successfully.\n")
        else :
            print(f"❌ Command {command_to_execute} failed with exit status: {exit_status}\n")


def run_rsync_loop(hostname: str ,
                   remote_path: pathlib.Path ,
                   local_path: pathlib.Path ,
                   command_to_execute: int = None ,
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
    - Prints available rsync commands.
    - Runs until interrupted by the user (via Ctrl+C).
    - Executes the specified rsync command every `delay_seconds` seconds.
    - Prints the command being executed and a wait message between iterations.

    Example
    -------
    >>> run_rsync_loop(
            hostname="myserver",
            remote_path=pathlib.Path("/remote/path"),
            local_path=pathlib.Path("/local/path"),
            command_to_execute=1,
            delay_seconds=300
        )
    """

    _f = display_copy_execute_rsync

    # print -help
    _f(hostname , remote_path , local_path)

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
