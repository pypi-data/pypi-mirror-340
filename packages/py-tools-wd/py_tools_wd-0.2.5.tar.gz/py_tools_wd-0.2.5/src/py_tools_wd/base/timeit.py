import time
from functools import wraps

# 全局字典用于存储不同 key 的计时器
_timers = {}

# 默认 key 值
DEFAULT_KEY = "default_timer"


def timer(key=None, logger=None, auto_stop=True):
    """
    装饰器，用于为函数添加计时功能。
    :param key: 计时器的唯一标识符。如果不传，则使用函数名作为 key。
    :param logger: 可选的日志记录器（需要有一个 info 方法）。
    :param auto_stop: 是否在函数执行结束后自动停止计时器。默认为 True。
    """

    def decorator(func):
        nonlocal key
        # 如果没有指定 key，则使用函数名作为 key
        key = key or func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 启动计时器
            start_timer(key, logger)
            try:
                # 执行被装饰的函数
                result = func(*args, **kwargs)
            finally:
                if auto_stop:
                    # 打印总耗时并清理计时器
                    total_elapsed_timer(key, logger)
                    stop_timer(key, logger)
            return result

        return wrapper

    return decorator


def start_timer(key=None, logger=None):
    """
    启动一个计时器。
    :param key: 计时器的唯一标识符。如果不传，则使用默认值。
    :param logger: 可选的日志记录器（需要有一个 info 方法）。
    """
    key = key or DEFAULT_KEY  # 如果没有传 key，则使用默认值
    _timers[key] = {
        "start_time": time.perf_counter(),
        "last_time": time.perf_counter(),
        "checkpoints": []  # 用于记录每个检查点的时间和消息
    }
    log(f"Timer '{key}' started.", key, logger)


def checkpoint_timer(key=None, message="", logger=None):
    """
    打印从上一个检查点到当前的耗时。
    :param key: 计时器的唯一标识符。如果不传，则使用默认值。
    :param message: 可选的消息，用于标识检查点。
    :param logger: 可选的日志记录器（需要有一个 info 方法）。
    """
    key = key or DEFAULT_KEY  # 如果没有传 key，则使用默认值
    if key not in _timers:
        raise Exception(f"Timer '{key}' not started. Call start_timer('{key}') first.")

    current_time = time.perf_counter()
    elapsed_since_last = current_time - _timers[key]["last_time"]
    _timers[key]["last_time"] = current_time

    # 将检查点信息保存到 checkpoints 列表中
    _timers[key]["checkpoints"].append((message, elapsed_since_last))

    log(f"[Checkpoint '{key}'] {message} - Elapsed time since last checkpoint: {elapsed_since_last:.6f} seconds", key,
        logger)


def total_elapsed_timer(key=None, logger=None):
    """
    打印从计时器启动到当前的总耗时。
    :param key: 计时器的唯一标识符。如果不传，则使用默认值。
    :param logger: 可选的日志记录器（需要有一个 info 方法）。
    """
    key = key or DEFAULT_KEY  # 如果没有传 key，则使用默认值
    if key not in _timers:
        raise Exception(f"Timer '{key}' not started. Call start_timer('{key}') first.")

    current_time = time.perf_counter()
    total_elapsed_time = current_time - _timers[key]["start_time"]
    log(f"[Total '{key}'] Elapsed time since timer started: {total_elapsed_time:.6f} seconds", key, logger)


def stop_timer(key=None, logger=None):
    """
    停止并清理计时器。
    :param key: 计时器的唯一标识符。如果不传，则使用默认值。
    :param logger: 可选的日志记录器（需要有一个 info 方法）。
    """
    key = key or DEFAULT_KEY  # 如果没有传 key，则使用默认值
    if key not in _timers:
        raise Exception(f"Timer '{key}' not found.")

    del _timers[key]
    log(f"Timer '{key}' stopped and cleaned up.", key, logger)


def print_all_checkpoints(key=None, logger=None):
    """
    打印所有记录点的用时情况。
    :param key: 计时器的唯一标识符。如果不传，则使用默认值。
    :param logger: 可选的日志记录器（需要有一个 info 方法）。
    """
    key = key or DEFAULT_KEY  # 如果没有传 key，则使用默认值
    if key not in _timers:
        raise Exception(f"Timer '{key}' not found.")

    log(f"--- Checkpoints for Timer '{key}' ---", key, logger)
    for i, (message, elapsed) in enumerate(_timers[key]["checkpoints"], start=1):
        log(f"Checkpoint {i}: {message} - Elapsed: {elapsed:.6f} seconds", key, logger)


def log(message, key, logger=None):
    """
    打印日志，并在日志中附加标志型字符串 [TIMER_KEY:key]。
    :param message: 日志内容。
    :param key: 关联的计时器标识。
    :param logger: 可选的日志记录器（需要有一个 info 方法）。
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 添加标志型字符串 [TIMER_KEY:key] 到日志中
    log_message = f"[{timestamp}] [TIMER_KEY:{key}] {message}"

    if logger is not None:
        # 如果传入了 logger，则使用 logger 的 info 方法
        logger.info(log_message)
    else:
        # 如果没有传入 logger，则使用 print
        print(log_message)


# 示例用法
if __name__ == "__main__":
    # 使用装饰器为函数计时，默认 key 为函数名，自动停止计时器
    @timer()
    def example_function():
        time.sleep(1)
        checkpoint_timer("example_function", "After sleep 1 second")

        time.sleep(2)
        checkpoint_timer("example_function", "After sleep 2 seconds")


    # 调用被装饰的函数
    example_function()


    # 使用装饰器为函数计时，但不自动停止计时器
    @timer(auto_stop=False)
    def long_running_task():
        time.sleep(1)
        checkpoint_timer("long_running_task", "Task in progress...")


    # 调用被装饰的函数
    long_running_task()

    # 手动打印总耗时并停止计时器
    total_elapsed_timer("long_running_task")
    stop_timer("long_running_task")