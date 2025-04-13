"""Comprehensive benchmark comparing JSD against orjson and msgspec."""

import gc
import io
import shutil
import sys
import time
import tracemalloc
from pathlib import Path

import msgspec.json
import orjson
from tabulate import tabulate
from tqdm.auto import tqdm

from jsdfile.benchmark.config import generate_test_data
from jsdfile.benchmark.utils import get_file_size, BenchmarkResults
from jsdfile.core.main import JSD


class HighBalancedBenchmark:
    """Run benchmark comparing JSD against orjson and msgspec with balanced memory and timing."""

    def __init__(self, iterations=5, capture_results=True):
        """Initialize the benchmark with the specified parameters.

        Args:
            iterations: Number of iterations to run for each test
            capture_results: If True, return a BenchmarkResults object instead of printing to console
        """
        self.iterations = iterations
        self.capture_results = capture_results
        self.test_sizes = [100, 1000, 10000, 100000]
        self.tmp_dir = Path("./benchmark_tmp")
        self.msgspec_encoder = msgspec.json.Encoder()
        self.msgspec_decoder = msgspec.json.Decoder()
        self.benchmark_results = BenchmarkResults() if capture_results else None
        self.original_stdout = None
        self.captured_output = None

    def run(self):
        """Run the complete benchmark suite.

        Returns:
            BenchmarkResults object if capture_results is True, None otherwise
        """
        self._setup_output_capture()
        self._prepare_temp_directory()

        try:
            self._run_benchmarks()
        finally:
            self._cleanup_temp_directory()
            self._restore_output_capture()

        return self.benchmark_results if self.capture_results else None

    def _setup_output_capture(self):
        """Set up output capture if needed."""
        if not self.capture_results:
            self._print_header()
        else:
            self.captured_output = io.StringIO()
            self.original_stdout = sys.stdout
            sys.stdout = self.captured_output

    def _prepare_temp_directory(self):
        """Prepare temporary directory for benchmark files."""
        if self.tmp_dir.exists():
            shutil.rmtree(self.tmp_dir)
        self.tmp_dir.mkdir(exist_ok=True)

    def _run_benchmarks(self):
        """Run benchmarks for all test sizes."""
        for size in tqdm(
            self.test_sizes, desc="Testing with different sizes", unit="size"
        ):
            self._benchmark_size(size)

    def _cleanup_temp_directory(self):
        """Clean up temporary directory after benchmarks."""
        if self.tmp_dir.exists():
            shutil.rmtree(self.tmp_dir)

    def _restore_output_capture(self):
        """Restore stdout and save captured output if needed."""
        if self.capture_results and self.original_stdout:
            sys.stdout = self.original_stdout

            # Save captured output to a log file
            with open("benchmark_results.log", "w") as f:
                f.write(self.captured_output.getvalue())

    def _print_header(self):
        """Print the benchmark header information."""
        print(
            f"Running Storage Format Benchmarks (averaged over {self.iterations} iterations)"
        )
        print("=" * 120)
        print("Write Benchmark Results")
        print("=" * 120)
        print(
            f"{'Records':<10} {'Operation':<10} {'JSD (ms)':<10} {'orjson (ms)':<12} {'msgspec (ms)':<12} "
            f"{'JSD/orjson':<12} {'JSD/msgspec':<12} {'JSD Size':<15} {'JSON Size':<15} {'JSD Mem (KB)':<12} "
            f"{'orjson Mem (KB)':<12} {'msgspec Mem (KB)':<12}"
        )
        print("-" * 150)

    def _benchmark_size(self, size):
        """Run benchmarks for a specific data size.

        Args:
            size: Number of records to test with
        """
        print(f"\nTesting with {size} records:")
        test_data = generate_test_data(size)

        # Setup paths
        jsd_path, json_path, msgspec_path = self._setup_benchmark_paths(size)

        # Run write benchmarks
        write_results = self._run_write_benchmarks(
            test_data, jsd_path, json_path, msgspec_path
        )

        # Run read benchmarks
        read_results = self._run_read_benchmarks(jsd_path, json_path, msgspec_path)

        # Process results
        self._process_write_results(size, jsd_path, json_path, *write_results)
        self._process_read_results(size, jsd_path, json_path, *read_results)

    def _setup_benchmark_paths(self, size):
        """Set up file paths for benchmark files.

        Args:
            size: Number of records to test with

        Returns:
            Tuple of paths for JSD, JSON, and msgspec files
        """
        jsd_path = self.tmp_dir / f"test_{size}.jsdfile"
        json_path = self.tmp_dir / f"test_{size}.json"
        msgspec_path = self.tmp_dir / f"test_{size}.msgspec"
        return jsd_path, json_path, msgspec_path

    def _run_write_benchmarks(self, test_data, jsd_path, json_path, msgspec_path):
        """Run write benchmarks for all formats.

        Args:
            test_data: Data to write
            jsd_path: Path to JSD file
            json_path: Path to JSON file
            msgspec_path: Path to msgspec file

        Returns:
            Tuple of arrays with benchmark results
        """
        # Arrays for write benchmarks
        jsd_write_times, orjson_write_times, msgspec_write_times = [], [], []
        jsd_write_mem_usage, orjson_write_mem_usage, msgspec_write_mem_usage = (
            [],
            [],
            [],
        )

        for _ in tqdm(range(self.iterations), desc="Iterations", leave=False):
            # Clean up between iterations
            gc.collect()

            # JSD Write
            jsd_write_time, jsd_write_mem = self._benchmark_jsd_write(
                test_data, jsd_path
            )
            jsd_write_times.append(jsd_write_time)
            jsd_write_mem_usage.append(jsd_write_mem)

            gc.collect()
            # orjson Write
            orjson_write_time, orjson_write_mem = self._benchmark_orjson_write(
                test_data, json_path
            )
            orjson_write_times.append(orjson_write_time)
            orjson_write_mem_usage.append(orjson_write_mem)

            gc.collect()
            # msgspec Write
            msgspec_write_time, msgspec_write_mem = self._benchmark_msgspec_write(
                test_data, msgspec_path
            )
            msgspec_write_times.append(msgspec_write_time)
            msgspec_write_mem_usage.append(msgspec_write_mem)

        return (
            jsd_write_times,
            orjson_write_times,
            msgspec_write_times,
            jsd_write_mem_usage,
            orjson_write_mem_usage,
            msgspec_write_mem_usage,
        )

    def _run_read_benchmarks(self, jsd_path, json_path, msgspec_path):
        """Run read benchmarks for all formats.

        Args:
            jsd_path: Path to JSD file
            json_path: Path to JSON file
            msgspec_path: Path to msgspec file

        Returns:
            Tuple of arrays with benchmark results
        """
        # Arrays for read benchmarks
        jsd_read_times, orjson_read_times, msgspec_read_times = [], [], []
        jsd_read_mem_usage, orjson_read_mem_usage, msgspec_read_mem_usage = [], [], []

        for _ in tqdm(range(self.iterations), desc="Iterations", leave=False):
            # Clean up between iterations
            gc.collect()

            # JSD Read
            jsd_read_time, jsd_read_mem = self._benchmark_jsd_read(jsd_path)
            jsd_read_times.append(jsd_read_time)
            jsd_read_mem_usage.append(jsd_read_mem)

            gc.collect()
            # orjson Read
            orjson_read_time, orjson_read_mem = self._benchmark_orjson_read(json_path)
            orjson_read_times.append(orjson_read_time)
            orjson_read_mem_usage.append(orjson_read_mem)

            gc.collect()
            # msgspec Read
            msgspec_read_time, msgspec_read_mem = self._benchmark_msgspec_read(
                msgspec_path
            )
            msgspec_read_times.append(msgspec_read_time)
            msgspec_read_mem_usage.append(msgspec_read_mem)

        return (
            jsd_read_times,
            orjson_read_times,
            msgspec_read_times,
            jsd_read_mem_usage,
            orjson_read_mem_usage,
            msgspec_read_mem_usage,
        )

    @staticmethod
    def _benchmark_jsd_write(test_data, jsd_path):
        """Benchmark JSD write operation."""
        gc.disable()
        tracemalloc.start()
        start_time = time.time()
        jsd_file = JSD(jsd_path)
        jsd_file.write(test_data)
        elapsed_time = (time.time() - start_time) * 1000
        _, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        gc.enable()
        return elapsed_time, peak_mem / 1024  # KB

    @staticmethod
    def _benchmark_orjson_write(test_data, json_path):
        """Benchmark orjson write operation."""
        gc.disable()
        tracemalloc.start()
        start_time = time.time()
        with open(json_path, "wb") as f:
            f.write(orjson.dumps(test_data))
        elapsed_time = (time.time() - start_time) * 1000
        _, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        gc.enable()
        return elapsed_time, peak_mem / 1024  # KB

    def _benchmark_msgspec_write(self, test_data, msgspec_path):
        """Benchmark msgspec write operation."""
        gc.disable()
        tracemalloc.start()
        try:
            start_time = time.time()
            encoded_data = self.msgspec_encoder.encode(test_data)
            with open(msgspec_path, "wb") as f:
                f.write(encoded_data)
            elapsed_time = (time.time() - start_time) * 1000
            _, peak_mem = tracemalloc.get_traced_memory()
            mem_usage = peak_mem / 1024  # KB
        except Exception as e:
            print(f"Warning: msgspec encode error: {e}")
            elapsed_time = float("nan")
            mem_usage = float("nan")
        tracemalloc.stop()
        gc.enable()
        return elapsed_time, mem_usage

    @staticmethod
    def _benchmark_jsd_read(jsd_path):
        """Benchmark JSD read operation."""
        gc.disable()
        tracemalloc.start()
        start_time = time.time()
        _ = JSD(jsd_path).read()
        elapsed_time = (time.time() - start_time) * 1000
        _, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        gc.enable()
        return elapsed_time, peak_mem / 1024  # KB

    @staticmethod
    def _benchmark_orjson_read(json_path):
        """Benchmark orjson read operation."""
        gc.disable()
        tracemalloc.start()
        start_time = time.time()
        with open(json_path, "rb") as f:
            file_data = f.read()
            _ = orjson.loads(file_data)
        elapsed_time = (time.time() - start_time) * 1000
        _, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        gc.enable()
        return elapsed_time, peak_mem / 1024  # KB

    def _benchmark_msgspec_read(self, msgspec_path):
        """Benchmark msgspec read operation."""
        gc.disable()
        tracemalloc.start()
        try:
            start_time = time.time()
            with open(msgspec_path, "rb") as f:
                file_data = f.read()
                _ = self.msgspec_decoder.decode(file_data)
            elapsed_time = (time.time() - start_time) * 1000
            _, peak_mem = tracemalloc.get_traced_memory()
            mem_usage = peak_mem / 1024  # KB
        except Exception as e:
            print(f"Warning: msgspec decode error: {e}")
            elapsed_time = float("nan")
            mem_usage = float("nan")
        tracemalloc.stop()
        gc.enable()
        return elapsed_time, mem_usage

    def _process_write_results(
        self,
        size,
        jsd_path,
        json_path,
        jsd_times,
        orjson_times,
        msgspec_times,
        jsd_mem,
        orjson_mem,
        msgspec_mem,
    ):
        """Process and display write benchmark results."""
        avg_times = self._calculate_average_times(
            jsd_times, orjson_times, msgspec_times
        )
        avg_memory = self._calculate_average_memory(jsd_mem, orjson_mem, msgspec_mem)
        file_sizes = self._get_file_sizes(jsd_path, json_path)

        # Store results if capturing
        if self.capture_results:
            self._store_write_results(size, avg_times, avg_memory, file_sizes)

        # Display results
        self._display_write_results(size, avg_times, avg_memory, file_sizes)

    def _store_write_results(self, size, avg_times, avg_memory, file_sizes):
        """Store write benchmark results in the results collection."""
        self.benchmark_results.add_result(
            size=size,
            operation="Write",
            jsd_time=avg_times["jsdfile"],
            orjson_time=avg_times["orjson"],
            msgspec_time=avg_times["msgspec"],
            jsd_mem=avg_memory["jsdfile"],
            orjson_mem=avg_memory["orjson"],
            msgspec_mem=avg_memory["msgspec"],
            jsd_size=file_sizes["jsdfile"],
            json_size=file_sizes["json"],
        )

    @staticmethod
    def _display_write_results(size, avg_times, avg_memory, file_sizes):
        """Display write benchmark results in a formatted table."""
        headers = [
            "Size",
            "Operation",
            "JSD (ms)",
            "orjson (ms)",
            "msgspec (ms)",
            "JSD/orjson (%)",
            "JSD/msgspec (%)",
            "JSD Size",
            "JSON Size",
            "JSD Mem (KB)",
            "orjson Mem (KB)",
            "msgspec Mem (KB)",
        ]

        jsd_vs_orjson = f"{(avg_times['jsdfile'] / avg_times['orjson'] * 100):.1f}%"
        jsd_vs_msgspec = f"{(avg_times['jsdfile'] / avg_times['msgspec'] * 100):.1f}%"

        write_data = [
            [
                size,
                "Write",
                f"{avg_times['jsdfile']:.2f}",
                f"{avg_times['orjson']:.2f}",
                f"{avg_times['msgspec']:.2f}",
                jsd_vs_orjson,
                jsd_vs_msgspec,
                file_sizes["jsdfile"],
                file_sizes["json"],
                f"{avg_memory['jsdfile']:.1f}",
                f"{avg_memory['orjson']:.1f}",
                f"{avg_memory['msgspec']:.1f}",
            ]
        ]
        print(tabulate(write_data, headers=headers, tablefmt="grid"))

    def _process_read_results(
        self,
        size,
        jsd_path,
        json_path,
        jsd_times,
        orjson_times,
        msgspec_times,
        jsd_mem,
        orjson_mem,
        msgspec_mem,
    ):
        """Process and display read benchmark results."""
        # Calculate averages
        avg_times = self._calculate_average_times(
            jsd_times, orjson_times, msgspec_times
        )
        avg_memory = self._calculate_average_memory(jsd_mem, orjson_mem, msgspec_mem)

        # Get file sizes
        file_sizes = self._get_file_sizes(jsd_path, json_path)

        # Store results if capturing
        if self.capture_results:
            self._store_read_results(size, avg_times, avg_memory, file_sizes)

        # Display results
        self._display_read_results(size, avg_times, avg_memory, file_sizes)

    def _calculate_average_times(self, jsd_times, orjson_times, msgspec_times):
        """Calculate average execution times for each library."""
        return {
            "jsdfile": sum(jsd_times) / self.iterations,
            "orjson": sum(orjson_times) / self.iterations,
            "msgspec": sum(msgspec_times) / self.iterations,
        }

    def _calculate_average_memory(self, jsd_mem, orjson_mem, msgspec_mem):
        """Calculate average memory usage for each library."""
        return {
            "jsdfile": sum(jsd_mem) / self.iterations,
            "orjson": sum(orjson_mem) / self.iterations,
            "msgspec": sum(msgspec_mem) / self.iterations,
        }

    @staticmethod
    def _get_file_sizes(jsd_path, json_path):
        """Get file sizes for JSD and JSON formats."""
        return {"jsdfile": get_file_size(jsd_path), "json": get_file_size(json_path)}

    def _store_read_results(self, size, avg_times, avg_memory, file_sizes):
        """Store read benchmark results in the results collection."""
        self.benchmark_results.add_result(
            size=size,
            operation="Read",
            jsd_time=avg_times["jsdfile"],
            orjson_time=avg_times["orjson"],
            msgspec_time=avg_times["msgspec"],
            jsd_mem=avg_memory["jsdfile"],
            orjson_mem=avg_memory["orjson"],
            msgspec_mem=avg_memory["msgspec"],
            jsd_size=file_sizes["jsdfile"],
            json_size=file_sizes["json"],
        )

    @staticmethod
    def _display_read_results(size, avg_times, avg_memory, file_sizes):
        """Display read benchmark results in a formatted table."""
        headers = [
            "Size",
            "Operation",
            "JSD (ms)",
            "orjson (ms)",
            "msgspec (ms)",
            "JSD/orjson (%)",
            "JSD/msgspec (%)",
            "JSD Size",
            "JSON Size",
            "JSD Mem (KB)",
            "orjson Mem (KB)",
            "msgspec Mem (KB)",
        ]

        # Calculate comparison percentages
        jsd_vs_orjson = avg_times["jsdfile"] / avg_times["orjson"] * 100
        jsd_vs_msgspec = avg_times["jsdfile"] / avg_times["msgspec"] * 100

        read_data = [
            [
                size,
                "Read",
                f"{avg_times['jsdfile']:.2f}",
                f"{avg_times['orjson']:.2f}",
                f"{avg_times['msgspec']:.2f}",
                f"{jsd_vs_orjson:.1f}%",
                f"{jsd_vs_msgspec:.1f}%",
                file_sizes["jsdfile"],
                file_sizes["json"],
                f"{avg_memory['jsdfile']:.1f}",
                f"{avg_memory['orjson']:.1f}",
                f"{avg_memory['msgspec']:.1f}",
            ]
        ]
        print(tabulate(read_data, headers=headers, tablefmt="grid"))
