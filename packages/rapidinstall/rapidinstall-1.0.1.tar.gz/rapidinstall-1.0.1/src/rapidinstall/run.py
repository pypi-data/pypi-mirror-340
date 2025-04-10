# rapidinstall/src/rapidinstall/run.py

import subprocess
import time
import threading
import queue
import os
import sys
import logging
from typing import List, Dict, Any, Optional
import re
import weakref
import shutil  # Keep for moving files

# --- Optional Import Placeholder ---

try:
    from rapidinstall import pip_concurrent
except ImportError:
    pip_concurrent = None

pySmartDL = None

# --- Configuration ---
DEFAULT_STATUS_UPDATE_INTERVAL = 30
SEPARATOR = "*" * 60
ANSI_ESCAPE_REGEX = re.compile(r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
TASK_STATUS_SENTINEL = "_task_status"

# --- Helper Function for Late Import ---


def _import_pysmartdl():
    global pySmartDL
    if pySmartDL is None:
        try:
            import pySmartDL as pysmartdl_module

            pySmartDL = pysmartdl_module
        except ImportError:
            raise ImportError(
                "The 'pySmartDL' package is required for download tasks. "
                "Please install it using: pip install rapidinstall[download]"
            )
    return pySmartDL


class RapidInstaller:

    """
    Manages parallel command and download tasks. Downloads can be moved
    to a final destination after all tasks complete using the 'move_to' parameter.
    """

    def __init__(
        self,
        update_interval: Optional[int] = DEFAULT_STATUS_UPDATE_INTERVAL,
        verbose: bool = True,
    ):
        self._update_interval = (
            update_interval
            if update_interval is not None and update_interval > 0
            else 0
        )
        self._verbose = verbose

        self._logger = logging.getLogger(f"RapidInstaller-{id(self)}")
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.propagate = False
        if verbose:
            self._logger.setLevel(logging.INFO)
        else:
            self._logger.setLevel(logging.WARNING)
        self._print_lock = threading.Lock()
        self._state_lock = threading.Lock()
        self._active_tasks: Dict[str, Dict[str, Any]] = {}
        self._final_results: Dict[str, Dict[str, Any]] = {}
        self._monitor_thread: Optional[threading.Thread] = None
        self._monitor_thread_started = threading.Event()
        self._stop_monitor_event = threading.Event()
        self._instance_active = True
        self._pip_tasks = []
        self._deferred_moves = []
        self._on_task_start = None
        self._on_task_complete = None

    def add_pip(self, packages: str):
        """
        Schedule concurrent installation of pip packages.
        Accepts a space-separated string of package names.
        """
        pkgs = packages.strip().split()
        if pkgs:
            self._pip_tasks.append(pkgs)
        # Store {'task_name': str, 'src': str, 'dest_dir': str}
        self._deferred_moves: List[Dict[str, str]] = []

        # Callbacks
        self._on_task_start = None
        self._on_task_complete = None

    def add_tasks(self, tasks: List[Dict[str, Any]]):
        """
        Add multiple command tasks at once.
        """
        for task in tasks:
            self.add_task(**task)

    def on_task_start(self, callback):
        """
        Register a callback function to be called when a task starts.
        """
        self._on_task_start = callback

    def on_task_complete(self, callback):
        """
        Register a callback function to be called when a task completes.
        """
        self._on_task_complete = callback

    # --- Helper Methods ---
    def _print_locked(self, *args, level=logging.INFO, **kwargs):
        with self._print_lock:
            if level == logging.ERROR:
                self._logger.error(*args, **kwargs)
            elif level == logging.WARNING:
                self._logger.warning(*args, **kwargs)
            else:
                if self._verbose:
                    self._logger.info(*args, **kwargs)

    @staticmethod
    def _strip_ansi(text: str) -> str:
        return ANSI_ESCAPE_REGEX.sub("", text)

    @staticmethod
    def _format_output_block(title: str, content: str) -> str:
        if not content.strip():
            return ""
        return f"{SEPARATOR}\n{title}\n{SEPARATOR}\n{content.strip()}\n{SEPARATOR}\n"

    @staticmethod
    def _process_status_lines(lines: List[str]) -> str:
        processed_output, current_line = "", ""
        for raw_line in lines:
            stripped_line = RapidInstaller._strip_ansi(raw_line)
            parts = stripped_line.split("\r")
            if len(parts) > 1:
                current_line = parts[-1]
            else:
                current_line += parts[0]
            if raw_line.endswith("\n"):
                processed_output += current_line
                current_line = ""
        if current_line:
            processed_output += current_line
        if lines and lines[-1].endswith("\n") and not processed_output.endswith("\n"):
            processed_output += "\n"
        return processed_output.strip()

    @staticmethod
    def _stream_reader(
        stream,
        output_queue: queue.Queue,
        stream_name: str,
        process_ref: weakref.ReferenceType,
    ):
        # ... (unchanged)
        try:
            for line in iter(stream.readline, ""):
                if process_ref() is None:
                    break
                if line:
                    output_queue.put((stream_name, line))
                else:
                    break
        except ValueError:
            pass
        except Exception as e:
            # Attempt to report the error, but don't crash the reader thread if the queue fails
            error_line = (
                f"[{stream_name}] Error reading stream: {type(e).__name__}: {e}\n"
            )
            try:
                output_queue.put(("stderr", error_line))
            except Exception:
                pass  # Ignore queue errors during error reporting
        finally:
            # Signal that this reader is done (important for knowing when to join)
            try:
                output_queue.put((stream_name, None))  # Sentinel value
            except Exception:
                pass  # Ignore queue errors during final signal
            # Don't close the stream here, the Popen object owns it.

    # --- Download Execution Function (using pySmartDL) ---
    @staticmethod
    def _execute_download_pysmartdl(
        url: str,
        initial_dest_path: str,  # Path where download initially happens
        output_queue: queue.Queue,
        task_name: str,
        verbose: bool,
    ):
        """Performs the download using pySmartDL, reports basic status via queue."""
        try:
            _pysdl = _import_pysmartdl()
        except ImportError as e:
            try:
                output_queue.put(("stderr", f"[{task_name}:stderr] {e}\n"))
                output_queue.put(
                    (TASK_STATUS_SENTINEL, (1, None))
                )  # RC=1, final_path=None
            except Exception:
                pass
                return

        return_code = 1  # Default failure
        final_filepath = None  # Track the actual final path pySmartDL used

        def _put_q(stream, msg):
            try:
                output_queue.put((stream, f"[{task_name}:{stream}] {msg.strip()}\n"))
            except Exception:
                pass  # Ignore queue errors here

        try:
            target_dir = os.path.dirname(initial_dest_path)
            if target_dir:
                os.makedirs(target_dir, exist_ok=True)

            _put_q("stdout", f"Starting download from {url} (Task: {task_name})")

            # Let pySmartDL determine the final filename if possible, by passing dir as dest
            # If initial_dest_path included a filename, pySmartDL *should* respect it.
            # We use 'dest=target_dir' if initial_dest_path was just a dir,
            # or 'dest=initial_dest_path' if it included a filename.
            dest_param = (
                target_dir
                if os.path.basename(initial_dest_path) == ""
                else initial_dest_path
            )

            downloader = _pysdl.SmartDL(
                url, dest=dest_param, progress_bar=False, timeout=120
            )
            downloader.start()  # Blocking

            final_filepath = (
                downloader.get_dest()
            )  # Get the actual path used by pySmartDL

            if downloader.isSuccessful():
                duration = downloader.get_dl_time()
                final_size = downloader.get_final_filesize()
                size_mb = final_size / (1024 * 1024) if final_size else 0
                size_str = f"{size_mb:.2f} MB" if size_mb else f"{final_size} bytes"
                _put_q(
                    "stdout",
                    f"Download completed: '{os.path.basename(final_filepath)}' ({size_str} in {duration:.2f}s)",
                )
                return_code = 0
            else:
                errors = downloader.get_errors()
                error_str = ", ".join(map(str, errors)) if errors else "Unknown error"
                _put_q("stderr", f"Download failed: {error_str}")
                if final_filepath and os.path.exists(final_filepath):
                    try:
                        os.remove(final_filepath)
                        _put_q("stderr", "Removed partial file.")
                    except OSError:
                        pass  # Ignore cleanup errors

        except OSError as e:
            _put_q("stderr", f"Download failed: OS error preparing - {e}")
        except Exception as e:
            _put_q(
                "stderr", f"Download failed: Unexpected error - {type(e).__name__}: {e}"
            )
            # Use initial_dest_path for cleanup attempt if downloader object failed early
            cleanup_path = final_filepath or initial_dest_path
            if os.path.exists(cleanup_path):
                try:
                    os.remove(cleanup_path)
                    _put_q("stderr", f"Removed partial/target file: {cleanup_path}")
                except OSError as remove_err:
                    _put_q(
                        "stderr",
                        f"Error removing partial/target file {cleanup_path}: {remove_err}",
                    )
        finally:
            # Signal completion: (return_code, actual_final_path)
            try:
                output_queue.put((TASK_STATUS_SENTINEL, (return_code, final_filepath)))
            except Exception as q_err:
                # Non-critical, but log it. Failing to put status might cause issues.
                print(
                    f"[{task_name}:ERROR] Failed to put final status on queue: {q_err}",
                    file=sys.stderr,
                )

    # --- Monitor Thread Management ---
    def _ensure_monitor_running(self):
        # ... (unchanged)
        if not self._instance_active:
            raise RuntimeError("Cannot add tasks after wait() or shutdown().")
        with self._state_lock:
            if self._monitor_thread is None or not self._monitor_thread.is_alive():
                self._print_locked("Starting monitor thread...")
                self._stop_monitor_event.clear()
                self._monitor_thread_started.clear()
                self._monitor_thread = threading.Thread(
                    target=self._monitor_loop, daemon=True
                )
                self._monitor_thread.start()
                # Wait briefly for the monitor thread to signal it has started
                if not self._monitor_thread_started.wait(timeout=5):
                    self._print_locked(
                        "Warning: Monitor thread did not signal start within timeout.",
                        file=sys.stderr,
                    )

    # --- Public Task Management Methods ---

    def add_task(self, name: str, commands: str):
        # ... (unchanged)
        if not name:
            raise ValueError("Task 'name' cannot be empty.")
        if not commands:
            raise ValueError("Task 'commands' cannot be empty.")
        self._ensure_monitor_running()
        with self._state_lock:
            if name in self._active_tasks or name in self._final_results:
                self._print_locked(
                    f"Warning: Task '{name}' already exists. Skipping.", file=sys.stderr
                )
                return

            self._final_results[name] = {
                "type": "command",
                "stdout": "",
                "stderr": "Command submitted...",
                "returncode": None,
                "pid": None,
                "start_time": None,
                "duration_sec": None,
            }

            try:
                start_time = time.time()
                output_q = queue.Queue()

                # Ensure unbuffered output from Python subprocesses if possible
                env = os.environ.copy()
                env["PYTHONUNBUFFERED"] = "1"

                # Use shell=True for simplicity with complex commands, but be mindful of security.
                # Consider shell=False and splitting commands if security is paramount.
                process = subprocess.Popen(
                    commands,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    bufsize=1,
                    env=env,
                )
                process_ref = weakref.ref(process)  # Use weakref for reader threads

                stdout_reader = threading.Thread(
                    target=RapidInstaller._stream_reader,
                    args=(process.stdout, output_q, "stdout", process_ref),
                    daemon=True,
                )
                stderr_reader = threading.Thread(
                    target=RapidInstaller._stream_reader,
                    args=(process.stderr, output_q, "stderr", process_ref),
                    daemon=True,
                )
                stdout_reader.start()
                stderr_reader.start()

                self._print_locked(f"*** Started Task '{name}' (PID: {process.pid})")
                if self._on_task_start:
                    self._on_task_start(name, "command")

                self._active_tasks[name] = {
                    "type": "command",
                    "name": name,
                    "process": process,
                    "thread": None,  # No primary thread for commands
                    "pid": process.pid,
                    "output_queue": output_q,
                    "stream_reader_threads": [stdout_reader, stderr_reader],
                    "start_time": start_time,
                    "final_output": {"stdout": [], "stderr": []},
                    "task_status_code": None,
                    "final_filepath": None,  # Not applicable to commands
                }
                self._final_results[name].update(
                    {"start_time": start_time, "pid": process.pid, "stderr": ""}
                )

            except Exception as e:
                err_msg = f"ERROR starting command '{name}': {e}"
                self._print_locked(f"  {err_msg}")
                # Update final result immediately on startup error
                self._final_results[name].update(
                    {"stderr": err_msg, "returncode": -1, "start_time": None}
                )
                # Remove from active tasks if startup failed completely
                if name in self._active_tasks:
                    del self._active_tasks[name]

    def add_download(
        self,
        url: str,
        name: str,
        directory: Optional[str] = None,
        move_to: Optional[str] = None,
    ):
        """
        Adds and starts a download task.

        Args:
            url (str): The URL to download.
            name (str): A unique name for the task.
            directory (Optional[str]): The directory to download the file into initially.
                                       Defaults to the current working directory.
                                       pySmartDL might adjust the filename based on headers.
            move_to (Optional[str]): If provided, the successfully downloaded file will be
                                     moved to this directory *after* all tasks complete.
        """
        try:
            _import_pysmartdl()
        except ImportError as e:
            self._print_locked(f"ERROR: {e}")
            raise e

        if not name:
            raise ValueError("Download 'name' required.")
        if not url:
            raise ValueError("Download 'url' required.")
        self._ensure_monitor_running()

        with self._state_lock:
            if name in self._active_tasks or name in self._final_results:
                self._print_locked(
                    f"Warning: Task '{name}' exists. Skipping.", file=sys.stderr
                )
                return

            # Determine initial download path (might be just a dir, or include filename guess)
            target_dir = directory or os.getcwd()
            # Let pySmartDL determine filename, so pass directory to it if no filename hint needed
            initial_dest_path = target_dir  # Simplification: let pySmartDL handle naming in the target dir

            self._final_results[name] = {
                "type": "download",
                "stdout": "",
                "stderr": "Download submitted...",
                "returncode": None,
                "pid": None,
                "start_time": None,
                "duration_sec": None,
                "url": url,
                "filepath": None,  # Will be set on completion
                "move_to": move_to,  # Store the move request
            }

            try:
                start_time = time.time()
                output_q = queue.Queue()
                dl_thread = threading.Thread(
                    target=RapidInstaller._execute_download_pysmartdl,
                    args=(url, initial_dest_path, output_q, name, self._verbose),
                    daemon=True,
                )
                dl_thread.start()
                self._print_locked(
                    f"*** Started Download '{name}' (Initial Target Dir: {target_dir})"
                )
                if self._on_task_start:
                    self._on_task_start(name, "download")

                self._active_tasks[name] = {
                    "type": "download",
                    "name": name,
                    "process": None,
                    "thread": dl_thread,
                    "pid": None,
                    "output_queue": output_q,
                    "stream_reader_threads": [],
                    "start_time": start_time,
                    "final_output": {"stdout": [], "stderr": []},
                    "task_status_code": None,
                    "final_filepath": None,  # Add placeholder for actual path
                    "move_to_request": move_to,  # Keep track of move request here too
                }
                self._final_results[name].update(
                    {"start_time": start_time, "stderr": ""}
                )

            except Exception as e:
                err_msg = f"ERROR starting download '{name}': {e}"
                self._print_locked(f"  {err_msg}")
                self._final_results[name].update(
                    {"stderr": err_msg, "returncode": -1, "start_time": None}
                )

    # --- Core Monitoring Logic ---
    def _monitor_loop(self):
        self._monitor_thread_started.set()
        # ... (logging, loop setup unchanged) ...

        try:
            output_collected_this_cycle = {}
            finished_tasks_in_cycle = []
            # should_stop_when_idle = False  # unused
            while True:
                # ... (snapshotting, idle check unchanged) ...
                with self._state_lock:
                    # ...
                    active_tasks_snapshot = list(self._active_tasks.items())
                    # ...
                    if not active_tasks_snapshot:
                        # task_status_rc = None  # unused
                        # task_status_path = None  # unused
                        try:  # Drain queue
                            while not q.empty():
                                # all_queues_empty_this_cycle = False  # unused
                                stream_name, content = q.get_nowait()
                                if stream_name == TASK_STATUS_SENTINEL:
                                    # Content is now a tuple: (return_code, final_filepath)
                                    rc, path = (
                                        content
                                        if isinstance(content, tuple)
                                        else (content, None)
                                    )
                                    # task_status_rc = rc  # unused
                                    # task_status_path = path  # unused
                                    continue
                                # ... (handle stream reader sentinel, regular output unchanged) ...
                                if content is None:
                                    continue  # Sentinel from stream reader
                        except queue.Empty:
                            pass
                        except Exception:
                            pass
                    else:
                        for task_name, task_data in active_tasks_snapshot:
                            try:  # Drain queue
                                while not q.empty():
                                    # all_queues_empty_this_cycle = False  # unused
                                    stream_name, content = q.get_nowait()
                                    if stream_name == TASK_STATUS_SENTINEL:
                                        # Content is now a tuple: (return_code, final_filepath)
                                        rc, path = (
                                            content
                                            if isinstance(content, tuple)
                                            else (content, None)
                                        )
                                        # task_status_rc = rc  # unused
                                        # task_status_path = path  # unused
                                        task_data["task_status_code"] = rc  # Store RC
                                        task_data["final_filepath"] = path  # Store actual path
                                        continue
                                    # ... (handle stream reader sentinel, regular output unchanged) ...
                                    if content is None:
                                        continue  # Sentinel from stream reader
                                    task_data["final_output"][stream_name].append(content)
                                    output_collected_this_cycle[task_name][stream_name].append(content)
                            except queue.Empty:
                                pass
                            except Exception:
                                pass

                            is_finished = False
                            final_rc = None
                            if task_data["type"] == "command":
                                process = task_data["process"]
                                rc = process.poll()
                                if rc is not None:
                                    is_finished = True
                                    final_rc = rc
                            elif task_data["type"] == "download":
                                thread = task_data["thread"]
                                if not thread.is_alive():
                                    is_finished = True
                                    final_rc = task_data.get("task_status_code", 1)

                            if is_finished:
                                end_time = time.time()
                                start_time = task_data.get("start_time")
                                duration = (end_time - start_time) if start_time else None
                                final_filepath_dl = task_data.get("final_filepath")

                                # Final drain (important if sentinel arrived before last output)
                                try:
                                    while not q.empty():
                                        stream_name, content = q.get_nowait()
                                        if stream_name == TASK_STATUS_SENTINEL:
                                            rc, path = (
                                                content
                                                if isinstance(content, tuple)
                                                else (content, None)
                                            )
                                            final_rc = rc if rc is not None else final_rc
                                            final_filepath_dl = path if path else final_filepath_dl
                                        elif content is not None:
                                            task_data["final_output"][stream_name].append(content)
                                except Exception:
                                    pass

                                final_stdout = self._strip_ansi(
                                    "".join(task_data["final_output"]["stdout"])
                                )
                                final_stderr = self._strip_ansi(
                                    "".join(task_data["final_output"]["stderr"])
                                )

                                # Update final results, including the actual filepath
                                if task_name in self._final_results:
                                    self._final_results[task_name].update(
                                        {
                                            "stdout": final_stdout,
                                            "stderr": final_stderr,
                                            "returncode": final_rc,
                                            "duration_sec": duration,
                                            "filepath": final_filepath_dl,  # Store the actual final path
                                        }
                                    )
                                    # --- Check if move is needed for successful download ---
                                    move_request = task_data.get("move_to_request")
                                    if (
                                        final_rc == 0
                                        and move_request
                                        and final_filepath_dl
                                    ):
                                        self._deferred_moves.append(
                                            {
                                                "task_name": task_name,
                                                "src": final_filepath_dl,
                                                "dest_dir": move_request,
                                            }
                                        )
                                else:
                                    self._print_locked(
                                        f"Warn: Task '{task_name}' finished but not in results",
                                        file=sys.stderr,
                                    )

                                # Call completion callback
                                if self._on_task_complete:
                                    self._on_task_complete(
                                        task_name,
                                        self._final_results.get(task_name, {}),
                                    )

                                finished_tasks_in_cycle.append(
                                    {...}
                                )  # (unchanged structure)
                                del self._active_tasks[
                                    task_name
                                ]  # Remove finished task

                # Exit monitor loop if no active tasks remain
                if not self._active_tasks:
                    break
                
                # --- End Locked Section ---
                # --- Print Summaries & Status Updates (Unchanged conceptually) ---
                # ...
        # ... (Exception handling and finally block unchanged) ...
        finally:
            ...

    # --- Deferred Move Logic ---
    def _perform_deferred_moves(self):
        """Moves downloaded files requested via 'move_to' after all tasks finish."""
        if not self._deferred_moves:
            return  # Nothing to move

        self._print_locked(f"\n{SEPARATOR}\n--- Performing Deferred File Moves ---")
        # Process moves outside the main state lock for potentially long I/O
        moves_to_process = self._deferred_moves[:]  # Work on a copy
        self._deferred_moves = []  # Clear the original list

        for move_info in moves_to_process:
            task_name = move_info["task_name"]
            src_path = move_info["src"]
            dest_dir = move_info["dest_dir"]
            final_dest_path = None  # Track the final path after move

            try:
                if not os.path.exists(src_path):
                    self._print_locked(
                        f"[{task_name}] ERROR: Source file '{src_path}' not found for move."
                    )
                    # Update result to indicate move failure
                    with self._state_lock:
                        if task_name in self._final_results:
                            self._final_results[task_name][
                                "move_status"
                            ] = "Error: Source not found"
                    continue

                # Ensure destination directory exists
                os.makedirs(dest_dir, exist_ok=True)

                # Construct final destination path
                dest_filename = os.path.basename(src_path)
                final_dest_path = os.path.join(dest_dir, dest_filename)

                self._print_locked(
                    f"[{task_name}] Moving '{src_path}' to '{final_dest_path}'..."
                )

                # Perform the move
                shutil.move(src_path, final_dest_path)

                self._print_locked(f"[{task_name}] Move successful.")

                # Update the final results filepath and add move status (inside lock)
                with self._state_lock:
                    if task_name in self._final_results:
                        self._final_results[task_name][
                            "filepath"
                        ] = final_dest_path  # Update path
                        self._final_results[task_name][
                            "move_status"
                        ] = "Moved successfully"

            except OSError as e:
                self._print_locked(
                    f"[{task_name}] ERROR moving file to '{dest_dir}': {e}"
                )
                with self._state_lock:
                    if task_name in self._final_results:
                        self._final_results[task_name]["move_status"] = f"Error: {e}"
            except Exception as e:
                self._print_locked(f"[{task_name}] UNEXPECTED ERROR during move: {e}")
                with self._state_lock:
                    if task_name in self._final_results:
                        self._final_results[task_name][
                            "move_status"
                        ] = f"Unexpected Error: {e}"

        self._print_locked(f"--- Finished Deferred File Moves ---\n{SEPARATOR}\n")

    # --- Public Control Methods ---
    def wait(self) -> Dict[str, Dict[str, Any]]:
        """Waits for all tasks to complete, performs deferred moves, and returns results."""

        # Run all pip installs first
        if pip_concurrent and getattr(self, "_pip_tasks", []):
            for pkgs in self._pip_tasks:
                print(f"Concurrent pip install: {pkgs}")
                pip_concurrent.concurrent_install(pkgs)

        if hasattr(self, "_monitor_thread"):
            self._monitor_thread.join()
        self._perform_deferred_moves()
        return getattr(self, "_final_results", {})

    def shutdown(self, terminate_processes: bool = False):
        """
        Gracefully stop monitoring and optionally terminate running subprocesses.

        Args:
            terminate_processes (bool): If True, attempt to terminate all running subprocesses.
        """
        self._instance_active = False
        self._stop_monitor_event.set()
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=5)

        if terminate_processes:
            with self._state_lock:
                for task_data in self._active_tasks.values():
                    if task_data["type"] == "command" and task_data.get("process"):
                        try:
                            task_data["process"].terminate()
                        except Exception:
                            pass
        self._print_locked("Waiting for all active tasks to complete...")
        self._stop_monitor_event.set()
        monitor = self._monitor_thread
        if monitor and monitor.is_alive():
            monitor.join()  # Wait for monitor

        self._instance_active = False  # Mark instance inactive AFTER monitor joins

        # --- Perform moves AFTER monitor thread finishes ---
        self._perform_deferred_moves()

        self._print_locked(
            f"{SEPARATOR}\n*** RapidInstall run complete.\n{SEPARATOR}\n\n"
        )
        return self.get_results()  # Return final results (potentially updated by moves)

    # ... (shutdown, get_results unchanged) ...

    # Clarify 'run' method's scope
    def run(self, todos: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        DEPRECATED/LIMITED: Use install() function or class methods (add_task/add_download) directly.

        Processes tasks from a 'todos' list (supports 'commands' or 'download' keys)
        and waits for completion. Less explicit than using dedicated methods.
        """
        self._print_locked(
            "Warning: The run() method is less explicit than install() or add_task/add_download. Consider refactoring.",
            file=sys.stderr,
        )
        try:
            # Logic to handle mixed types from list (similar to standalone run_tasks)
            has_download = any("download" in todo for todo in todos)
            if has_download:
                _import_pysmartdl()  # Check dependency if needed

            tasks_added = set()
            for todo in todos:
                name = todo.get("name")
                if not name:
                    continue  # Skip unnamed
                if name in tasks_added:
                    continue  # Skip duplicate names in list

                if "commands" in todo and todo.get("commands"):
                    self.add_task(name=name, commands=todo["commands"])
                    tasks_added.add(name)
                elif "download" in todo and todo.get("download"):
                    # Extract move_to if present in the todo dict
                    self.add_download(
                        name=name,
                        url=todo["download"],
                        directory=todo.get("directory"),
                        move_to=todo.get("move_to"),
                    )
                    tasks_added.add(name)
        except ImportError as e:
            self._print_locked(f"ERROR: {e}", file=sys.stderr)
            raise e
        except (ValueError, RuntimeError) as e:
            self._print_locked(f"ERROR adding tasks in run(): {e}", file=sys.stderr)
        except Exception as e:
            self._print_locked(
                f"UNEXPECTED ERROR adding tasks in run(): {e}", file=sys.stderr
            )

        return self.wait()  # Waits for *all* tasks added to this instance


# --- Standalone Function (Updated to include move_to) ---
def run_tasks(
    todos: List[Dict[str, Any]],
    update_interval: int = DEFAULT_STATUS_UPDATE_INTERVAL,
    verbose: bool = True,
) -> Dict[str, Dict[str, Any]]:
    """
    Runs tasks defined in the 'todos' list. Supports commands and downloads.

    Each dictionary in 'todos' should have:
    - 'name': str
    And EITHER:
    - 'commands': str
    OR:
    - 'download': str (URL)
    - 'directory': Optional[str] (Initial download directory)
    - 'move_to': Optional[str] (Directory to move file to *after* all tasks finish)
    """
    installer = RapidInstaller(update_interval=update_interval, verbose=verbose)
    final_results = {}
    tasks_added = set()

    try:
        has_download = any("download" in todo for todo in todos)
        if has_download:
            _import_pysmartdl()  # Check dependency

        for todo in todos:
            name = todo.get("name")
            if not name:
                print("Warning: Skipping task with no name.", file=sys.stderr)
                continue
            if name in tasks_added:
                print(
                    f"Warning: Duplicate task name '{name}' in list. Skipping.",
                    file=sys.stderr,
                )
                continue

            if "commands" in todo:
                commands = todo.get("commands")
                if commands:
                    installer.add_task(name=name, commands=commands)
                    tasks_added.add(name)
                else:
                    print(
                        f"Skipping command task '{name}' empty 'commands'.",
                        file=sys.stderr,
                    )
            elif "download" in todo:
                url = todo.get("download")
                if url:
                    installer.add_download(
                        name=name,
                        url=url,
                        directory=todo.get("directory"),
                        move_to=todo.get("move_to"),
                    )  # Pass move_to
                    tasks_added.add(name)
                else:
                    print(
                        f"Skipping download task '{name}' empty 'download' URL.",
                        file=sys.stderr,
                    )
            else:
                print(
                    f"Skipping task '{name}': No 'commands' or 'download'.",
                    file=sys.stderr,
                )

        final_results = installer.wait()  # Wait includes performing moves

    # ... (Exception handling remains similar, ensuring results dict has entries) ...
    except ImportError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        # Potentially raise e here if it's critical, or just return partial results
    except (ValueError, RuntimeError) as e:
        print(f"ERROR during task setup in run_tasks: {e}", file=sys.stderr)
    except Exception as e:
        print(
            f"UNEXPECTED ERROR in run_tasks: {type(e).__name__}: {e}", file=sys.stderr
        )

    return final_results
