from enum import Enum, auto

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class PlotType(Enum):
    """Enum class to specify the type of plot to generate."""

    EXECUTION_TIME = auto()
    MEMORY_USAGE = auto()
    PERFORMANCE_RATIO = auto()
    FILE_SIZE = auto()
    HEATMAP_TIME = auto()
    HEATMAP_MEMORY = auto()
    RADAR = auto()
    ALL = auto()


class BenchmarkParser:
    """
    Parser for benchmark results from log files containing the output of the benchmark script.
    """

    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    def parse(self):
        """
        Parse benchmark results from the log file.

        Returns:
            DataFrame containing the parsed benchmark data
        """
        lines = self._read_log_file()
        results = self._extract_benchmark_data(lines)
        return pd.DataFrame(results)

    def _read_log_file(self):
        """
        Read the log file contents.

        Returns:
            List of lines from the log file
        """
        with open(self.log_file_path, "r") as f:
            return f.readlines()

    def _extract_benchmark_data(self, lines):
        """
        Extract benchmark data from log file lines.

        Args:
            lines: List of lines from the log file

        Returns:
            List of dictionaries containing parsed benchmark data
        """
        results = []
        current_size = None

        for line in lines:
            line = line.strip()

            # Check if this is a new test size
            if line.startswith("Testing with "):
                current_size = self._parse_test_size(line)
                continue

            # Try to extract data from the grid format
            if "|" in line and current_size is not None:
                benchmark_entry = self._parse_benchmark_line(line, current_size)
                if benchmark_entry:
                    results.append(benchmark_entry)

        return results

    @staticmethod
    def _parse_test_size(line):
        """Parse the test size from a line."""
        try:
            return int(line.split()[2])
        except (IndexError, ValueError):
            return None

    def _parse_benchmark_line(self, line, current_size):
        """
        Parse a single benchmark result line.

        Args:
            line: Line containing benchmark data in grid format
            current_size: Current test size

        Returns:
            Dictionary with parsed data or None if parsing failed
        """
        cells = [cell.strip() for cell in line.split("|")]

        if len(cells) < 13:  # We expect 13 cells including empty ones at start/end
            return None

        try:
            operation = cells[2].strip()
            if operation not in ["Write", "Read"]:
                return None

            return self._parse_benchmark_entry(cells, current_size, operation)
        except (ValueError, IndexError):
            return None

    @staticmethod
    def _parse_benchmark_entry(cells, current_size, operation):
        """Parse a single benchmark entry from the log file."""
        return {
            "size": current_size,
            "operation": operation,
            "jsd_time": float(cells[3].replace("ms", "").strip()),
            "orjson_time": float(cells[4].replace("ms", "").strip()),
            "msgspec_time": float(cells[5].replace("ms", "").strip()),
            "jsd_orjson_ratio": float(cells[6].replace("%", "").strip()),
            "jsd_msgspec_ratio": float(cells[7].replace("%", "").strip()),
            "jsd_size": cells[8].strip(),
            "json_size": cells[9].strip(),
            "jsd_mem": float(cells[10].strip()),
            "orjson_mem": float(cells[11].strip()),
            "msgspec_mem": float(cells[12].strip()),
        }


class BasePlotter:
    """
    Base class for all plotting components with shared utilities.
    """

    def __init__(self, df, save_path=None):
        """
        Initialize the base plotter with benchmark data and optional save path.

        Args:
            df: DataFrame with benchmark results
            save_path: Optional base path to save figures
        """
        self.df = df
        self.save_path = save_path
        self.colors = ["#3498db", "#e74c3c", "#2ecc71"]  # Blue, Red, Green
        self.operations = ["Write", "Read"]

    def _get_operation_data(self, operation):
        """Helper method to get data for a specific operation."""
        return self.df[self.df["operation"] == operation]

    @staticmethod
    def _setup_dual_subplot(figsize=(12, 10)):
        """Create a figure with two subplots for Write and Read operations."""
        fig, axes = plt.subplots(2, 1, figsize=figsize)
        return fig, axes

    @staticmethod
    def _setup_bar_positions(op_data):
        """Set up common bar chart positioning."""
        bar_width = 0.25
        index = np.arange(len(op_data["size"].unique()))
        return bar_width, index

    def _save_and_show(self, fig, specific_path=None):
        """Save the figure if a path is provided and display it."""
        if self.save_path:
            save_to = specific_path if specific_path else self.save_path
            plt.savefig(save_to)
        plt.show()

    @staticmethod
    def _configure_bar_axis(ax, index, data, title, ylabel):
        """Configure common bar chart axis settings."""
        ax.set_xlabel("Number of Records")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.set_xticks(index)
        ax.set_xticklabels(data["size"].unique())
        ax.legend()
        ax.grid(axis="y", linestyle="--", alpha=0.7)

    @staticmethod
    def _parse_size(size_str):
        """Convert size string (e.g., '10KB', '2MB') to bytes."""
        if "KB" in size_str:
            return float(size_str.replace("KB", "").strip()) * 1024
        elif "MB" in size_str:
            return float(size_str.replace("MB", "").strip()) * 1024 * 1024
        elif "B" in size_str:
            return float(size_str.replace("B", "").strip())
        else:
            try:
                return float(size_str.strip())
            except ValueError:
                return 0

    def plot(self, *, specific_save_path=None, **kwargs):
        """
        Base plot method to be implemented by subclasses.

        Args:
            specific_save_path: Optional path to override the default save path
        """
        raise NotImplementedError("Subclasses must implement this method")
