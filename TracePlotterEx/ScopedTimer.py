import time


class ScopedTimer:
    def __init__(self, label="Elapsed time"):
        self.label = label

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.perf_counter()
        elapsed = end - self.start
        print(f"{self.label}: {elapsed:.3f} seconds")
