# Smuxent
v0.0.2
**Smuxent** is a lightweight native threading module for Python, backed by C++ and pybind11.  
It allows you to easily launch background threads in Python using true native threads - with cooperative control and ID tracking.

This project was built for fun, learning, and utility. If you're using this, thanks!
Feedback and suggestions are welcome though not sure where that'd be.

> Currently supports: **Python 3.11.x-3.12.x** on **Windows (x64 and x86)**

---

## What It Does

- Run Python functions in detached threads
- Create and run thread pools
- Track threads by ID
- Submit tasks to said thread pools
- Kill individual threads or all running threads
- Track thread IDs and check if they are alive
- Automatically loads the correct native extension based on system architecture

---

## Example

```python
from Smuxent import hello_thread, basic_thread

hello_thread(3)  # prints "Hello, Thread!" three times on another thread

def my_func():
    print("Running on another thread")

thread_id = basic_thread(my_func)  # runs my_func() on another thread, returning the thread ID

```

---

## All Existing Functions

```python

# === v0.0.1 - Basic Threading ===

def basic_thread(func: Callable, *args: Any) -> int: ...
def hello_thread(loop_count: int = 1) -> int: ...

def is_alive(id: int) -> bool: ...
def kill_thread(id: int) -> None: ...
def kill_all_threads() -> None: ...
def get_all_thread_ids() -> List[int]: ...

# === v0.0.2 - Thread Pools ===

def thread_pool(size: int) -> str: ...
def submit(pool_id: str, func: Callable, *args: Any) -> bool: ...
def get_pool_thread_ids(pool_id: str) -> List[int]: ...
def kill_pool(pool_id: str) -> None: ...

# === Deprecated / Legacy Functions ===

def __basic_threadOld(func: Callable, *args: Any) -> None:
    """[Deprecated] Use basic_thread instead. This version does not return a thread ID."""

def __hello_threadOld(loop_count: int = 1) -> None:
    """[Deprecated] Use hello_thread instead. This version does not support thread tracking."""


```