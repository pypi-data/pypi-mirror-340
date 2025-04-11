import threading


class CallbackThread(threading.Thread):
    """A thread class that supports a callback function upon completion.

    Args:
        target (callable): The function to run in the thread.
        args (tuple, optional): Arguments to pass to the target function. Defaults to ().
        kwargs (dict, optional): Keyword arguments to pass to the target function. Defaults to None.
        callback (callable, optional): A function to execute when the thread completes. Defaults to None.
    """

    def __init__(self, target, args=(), kwargs=None, callback=None):
        super().__init__(target=target, args=args, kwargs=kwargs if kwargs is not None else {})
        self.callback = callback
        self._stop_event = threading.Event()

    def run(self):
        """Executes the target function and then invokes the callback if provided.

        The `_stop_event` is passed to the target function to allow for controlled stopping.
        """
        if self._target:
            self._target(self._stop_event, *self._args, **self._kwargs)
        if self.callback:
            self.callback()

    def stop(self):
        """Stops the thread by setting the stop event and waiting for the thread to finish."""
        if self.is_alive():
            self._stop_event.set()
            self.join()
