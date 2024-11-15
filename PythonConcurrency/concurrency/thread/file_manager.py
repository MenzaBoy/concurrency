import threading
import random
import time
from logging import Logger, basicConfig, getLogger

from concurrency.functions import time_sync

basicConfig(level="INFO")


class FileManager:
    """
    A class to manage file operations in a controlled manner, allowing only
    a specified number of paralel operations.

    Note:
        The current implementation uses locks and relies on the caller to create the threads to
        manage concurrency for demonstration purposes. In a production environment,
        a more efficient approach would involve encapsulating the worker processes into FileManager
        itself and using a task queue with a fixed number of worker threads.
    """

    # Maximum number of concurrent file tasks
    max_file_process: int
    # A list to keep track of saved files
    saved_files: list[str]
    # Number of currently running processes
    current_processes: int
    # A lock for synchronizing access to shared resources (saved_files, file_locks)
    lock: threading.Lock
    # A condition variable for managing state changes
    condition: threading.Condition
    # Dictionary to maintain individual locks for each file
    file_locks: dict[str, threading.Lock]
    # Logger object
    logger: Logger

    def __init__(self, max_file_process: int, logger: Logger) -> None:
        """
        Initialize the FileManager with max_file_process.

        FileManager only allows max_file_process number of parallel tasks, so
        it is vital to set it to a value that works correctly in your system.

        Args:
            max_file_process (int): Maximum number of parralel file tasks.
            logger (Logger): The main logger object
        """
        self.max_file_process = max_file_process
        self.logger = logger
        self.condition.wait()
        self.saved_files = []
        self.current_processes = 0
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.file_locks = {}

    def get_file_lock(self, file_path: str) -> threading.Lock:
        """
        Returns the look of a specified file.

        It safely retrieves the lock for a file. If the file lock doesn't exist,
        the function first creates it.
        """
        with self.lock:
            if file_path not in self.file_locks:
                self.file_locks[file_path] = threading.Lock()
            return self.file_locks[file_path]

    def guard_process(func):
        """
        Decorator function to manage the maximum number of parallel tasks.

        This function ensures that only max_file_process number of threads can
        run at the same time, keeping the application thread-safe.
        """

        def wrapper(self, file_path: str, est: int) -> None:
            with self.condition:
                self.logger.debug(
                    f"Currently running {self.current_processes} processes."
                )
                while self.current_processes >= self.max_file_process:
                    self.logger.info(
                        f"Currently running {self.current_processes} processes, thread {threading.get_ident()} is waiting for a free worker..."
                    )
                    self.condition.wait()

                self.current_processes += 1
            try:
                func(self, file_path, est)
            finally:
                with self.condition:
                    self.current_processes -= 1
                    self.logger.debug(f"Finishing thread {threading.get_ident()}.")
                    self.condition.notify()

        return wrapper

    @guard_process
    def download_file(self, file_path: str, est: int) -> None:
        """
        Simulate file downloading.

        This function starts downloading a file, which is simulated by a certain
        amount of sleep. When the file is downloaded it is saved in self.saved_files
        for further use. The operation locks the resources only for the duration of the save.

        Args:
            file_path (str): Path of the file to be downloaded
            est (int): The number of seconds the simulated download will take
        """
        self.logger.info(
            f"Downloading {file_path}... in thread ID {threading.get_ident()}."
        )

        time.sleep(est)
        file_lock = self.get_file_lock(file_path)
        with file_lock:
            self.logger.info(f"Saving downloaded file {file_path}...")
            with self.lock:
                self.saved_files.append(file_path)
            self.logger.debug("Lock released.")
        self.logger.info(
            f"Downloaded {file_path} in {est} seconds within thread ID: {threading.get_ident()}"
        )

    @guard_process
    def check_saved_file(self, file_path: str, est: int) -> None:
        """
        Simulate file checking.

        This function starts checking a file, which is simulated by a certain
        amount of sleep. It can only carry out the operation if the file exists.
        If it does, the saved file will be checked for est amount of time.
        The operation locks the resources for the whole duration of the check (sleep).

        Args:
            file_path (str): Path of the file to be checked
            est (int): The number of seconds the simulated check will take
        """
        self.logger.info(
            f"Checking {file_path}... in thread ID {threading.get_ident()}."
        )

        file_lock = self.get_file_lock(file_path)
        with file_lock:
            with self.lock:
                if file_path not in self.saved_files:
                    self.logger.error(f"File {file_path} not found.")
                    return
            time.sleep(est)
        self.logger.info(
            f"Checked {file_path} in {est} seconds within thread ID: {threading.get_ident()}"
        )

    @guard_process
    def write_file(self, file_path: str, est: int) -> None:
        """
        Simulate writing / editing the file.

        This function starts "writing" a file, which is simulated by a certain
        amount of sleep. If the file doesn't exist this function creates it first.
        After the file is saved, it will be edited for est amount of time.
        The operation locks the resources for the whole duration of the write (sleep).

        Args:
            file_path (str): Path of the file to be checked
            est (int): The number of seconds the simulated check will take
        """
        self.logger.info(
            f"Checking if {file_path} exists... in thread ID {threading.get_ident()}."
        )

        file_lock = self.get_file_lock(file_path)
        with file_lock:
            with self.lock:
                if file_path not in self.saved_files:
                    self.logger.info(
                        f"File {file_path} not found in saved files.Saving it..."
                    )
                    self.saved_files.append(file_path)
                    self.logger.info(f"Created file {file_path}.")

            time.sleep(est)
        self.logger.info(
            f"Wrote {file_path} in {est} seconds within thread ID: {threading.get_ident()}"
        )


# Some example data for simulating file management tasks.
download_data: list[tuple[str, int]] = [
    ("google.com/testfile", 8),
    ("www.site.com/secret", 5),
    ("local/file/path/notes.txt", 7),
    ("users/passwords.txt", 10),
    ("pypi.org/testpackage/v1.2", 6),
]


@time_sync
def main() -> None:
    """
    The main entrypoint of the application.

    It simulates some file operations by creating new threads for a FileManager
    object to run. It waits for a random amount of seconds after every new thread
    to realistically simulate the incoming operations.
    """
    logger = getLogger("File manager")
    logger.info("Starting main.")

    file_manager = FileManager(3, logger)
    file_operations: list[function] = [
        file_manager.download_file,
        file_manager.check_saved_file,
        file_manager.write_file,
    ]
    threads: list[threading.Thread] = []

    for _ in range(10):
        thread = threading.Thread(
            target=random.choice(file_operations), args=random.choice(download_data)
        )

        threads.append(thread)
        logger.debug(f"Creating a new thread: {thread.name}")
        thread.start()

        # This sleep is here for more closely replicating a real world scenario
        rand_sleep_amount = random.randint(0, 3)
        logger.debug(f"Main sleeping for {rand_sleep_amount} seconds.")
        time.sleep(rand_sleep_amount)

    for thread in threads:
        thread.join()

    logger.info("Main finished")


if __name__ == "__main__":
    main()
