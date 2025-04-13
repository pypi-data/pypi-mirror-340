import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tqdm import tqdm

from jsdfile.plot.utility import BasePlotter, PlotType


class FileSizeComparisonPlotter(BasePlotter):
    """
    Creates a bar chart comparing file sizes between JSD and JSON formats.
    """

    def plot(self, *, specific_save_path=None, **kwargs):
        """
        Create and display the file size comparison bar chart.

        Args:
            specific_save_path: Optional path to override the default save path
            **kwargs:
        """
        size_data = self._prepare_size_data()
        fig = self._create_figure()
        bar_width, index = self._setup_bar_positions(size_data)
        self._plot_size_bars(size_data, index, bar_width)
        self._add_reduction_percentages(size_data, index)
        self._configure_chart(size_data, index)
        self._save_and_show(fig, specific_save_path)

    def _prepare_size_data(self):
        """Prepare the size data by converting string sizes to numeric values."""
        size_data = self.df.drop_duplicates(subset=["size"])
        size_data["jsd_size_bytes"] = size_data["jsd_size"].apply(self._parse_size)
        size_data["json_size_bytes"] = size_data["json_size"].apply(self._parse_size)
        return size_data

    @staticmethod
    def _create_figure():
        """Create and return the figure for the plot."""
        return plt.figure(figsize=(10, 6))

    def _setup_bar_positions(self, size_data):
        """Set up the positions for the bars in the chart."""
        bar_width = 0.35
        index = np.arange(len(size_data))
        return bar_width, index

    def _plot_size_bars(self, size_data, index, bar_width):
        """Plot the size comparison bars for JSD and JSON."""
        plt.bar(
            index - bar_width / 2,
            size_data["jsd_size_bytes"] / 1024,
            bar_width,
            label="JSD",
            color=self.colors[0],
        )
        plt.bar(
            index + bar_width / 2,
            size_data["json_size_bytes"] / 1024,
            bar_width,
            label="JSON",
            color=self.colors[1],
        )

    @staticmethod
    def _add_reduction_percentages(size_data, index):
        """Add text annotations showing size reduction percentages."""
        for i, row in size_data.iterrows():
            reduction = (1 - row["jsd_size_bytes"] / row["json_size_bytes"]) * 100
            plt.text(
                i,
                max(row["jsd_size_bytes"], row["json_size_bytes"]) / 1024 * 1.05,
                f"{reduction:.1f}% smaller",
                ha="center",
                va="bottom",
                rotation=0,
                bbox=dict(facecolor="white", alpha=0.8),
            )

    @staticmethod
    def _configure_chart(size_data, index):
        """Configure the chart appearance with labels, title, and grid."""
        plt.xlabel("Number of Records")
        plt.ylabel("File Size (KB)")
        plt.title("File Size Comparison: JSD vs JSON")
        plt.xticks(index, size_data["size"])
        plt.legend()
        plt.grid(axis="y", linestyle="--", alpha=0.7)


class ExecutionTimePlotter(BasePlotter):
    """Class for creating execution time comparison plots."""

    def plot(self, *, specific_save_path=None, **kwargs):
        """
        Create a bar chart comparing execution times for each library across different data sizes.

        Args:
            specific_save_path: Optional path to override the default save path
            **kwargs:
        """
        fig, axes = self._setup_dual_subplot()

        for i, operation in enumerate(self.operations):
            self._plot_operation_execution_time(axes[i], operation)

        plt.tight_layout()
        self._save_and_show(fig, specific_save_path)

    def _plot_operation_execution_time(self, ax, operation):
        """
        Plot execution time for a specific operation.

        Args:
            ax: The matplotlib axis to plot on
            operation: The operation type (Read/Write)
        """
        op_data = self._get_operation_data(operation)
        bar_width, index = self._setup_bar_positions(op_data)

        self._plot_library_time_bars(ax, index, bar_width, op_data)
        self._configure_bar_axis(
            ax, index, op_data, f"{operation} Operation Time", "Time (ms)"
        )

    def _plot_library_time_bars(self, ax, index, bar_width, op_data):
        """
        Plot execution time bars for each library.

        Args:
            ax: The matplotlib axis to plot on
            index: The x-positions for the bars
            bar_width: Width of each bar
            op_data: DataFrame containing the operation data
        """
        ax.bar(
            index - bar_width,
            op_data["jsd_time"],
            bar_width,
            color=self.colors[0],
            label="JSD",
        )
        ax.bar(
            index,
            op_data["orjson_time"],
            bar_width,
            color=self.colors[1],
            label="orjson",
        )
        ax.bar(
            index + bar_width,
            op_data["msgspec_time"],
            bar_width,
            color=self.colors[2],
            label="msgspec",
        )


class MemoryUsagePlotter(BasePlotter):
    """Class for creating memory usage comparison plots."""

    def plot(self, *, specific_save_path=None, **kwargs):
        """
        Create a bar chart comparing memory usage for each library across different data sizes.

        Args:
            specific_save_path: Optional path to override the default save path
            **kwargs:
        """
        fig, axes = self._setup_dual_subplot()

        for i, operation in enumerate(self.operations):
            self._plot_operation_memory_usage(axes[i], operation)

        plt.tight_layout()
        self._save_and_show(fig, specific_save_path)

    def _plot_operation_memory_usage(self, ax, operation):
        """
        Plot memory usage for a specific operation.

        Args:
            ax: The matplotlib axis to plot on
            operation: The operation type (Read/Write)
        """
        op_data = self._get_operation_data(operation)
        bar_width, index = self._setup_bar_positions(op_data)

        self._plot_library_memory_bars(ax, index, bar_width, op_data)
        self._configure_memory_axis(ax, index, op_data, operation)

    def _plot_library_memory_bars(self, ax, index, bar_width, op_data):
        """
        Plot memory usage bars for each library.

        Args:
            ax: The matplotlib axis to plot on
            index: The x-positions for the bars
            bar_width: Width of each bar
            op_data: DataFrame containing the operation data
        """
        ax.bar(
            index - bar_width,
            op_data["jsd_mem"],
            bar_width,
            color=self.colors[0],
            label="JSD",
        )
        ax.bar(
            index,
            op_data["orjson_mem"],
            bar_width,
            color=self.colors[1],
            label="orjson",
        )
        ax.bar(
            index + bar_width,
            op_data["msgspec_mem"],
            bar_width,
            color=self.colors[2],
            label="msgspec",
        )

    def _configure_memory_axis(self, ax, index, op_data, operation):
        """
        Configure the axis for memory usage plot.

        Args:
            ax: The matplotlib axis to configure
            index: The x-positions for the bars
            op_data: DataFrame containing the operation data
            operation: The operation type (Read/Write)
        """
        self._configure_bar_axis(
            ax,
            index,
            op_data,
            f"{operation} Operation Memory Usage",
            "Memory Usage (KB)",
        )


class PerformanceRatioPlotter(BasePlotter):
    """Class for creating line charts showing JSD performance ratios compared to other libraries."""

    def plot(self, *, specific_save_path=None, **kwargs):
        """
        Create a line chart showing JSD performance ratio compared to other libraries.

        Args:
            specific_save_path: Optional path to override the default save path
            **kwargs:
        """
        fig, axes = self._setup_dual_subplot()

        for i, operation in enumerate(self.operations):
            op_data = self._get_operation_data(operation)

            self._plot_ratio_lines(axes[i], op_data)
            self._add_reference_line(axes[i])
            self._configure_axis(axes[i], operation)

            if i == 0:
                self._add_explanation_text(axes[i])

        plt.tight_layout()
        self._save_and_show(fig, specific_save_path)

    @staticmethod
    def _plot_ratio_lines(ax, op_data):
        """Plot the performance ratio lines."""
        ax.plot(op_data["size"])
        ax.plot(op_data["size"])

    @staticmethod
    def _add_reference_line(ax):
        """Add horizontal reference line at 100%."""
        ax.axhline(y=100, color="gray", linestyle="--", alpha=0.7)

    @staticmethod
    def _configure_axis(ax, operation):
        """Configure the axis settings."""
        ax.set_xlabel("Number of Records")
        ax.set_ylabel("Performance Ratio (%)")
        ax.set_title(f"{operation} Performance Ratio (JSD vs Others)")
        ax.set_xscale("log")
        ax.legend()
        ax.grid(True, alpha=0.3)

    @staticmethod
    def _add_explanation_text(ax):
        """Add explanatory text to the plot."""
        ax.text(
            0.05,
            0.05,
            "Values below 100% mean JSD is faster\nValues above 100% mean JSD is slower",
            transform=ax.transAxes,
            bbox=dict(facecolor="white", alpha=0.8),
        )


class HeatmapComparisonPlotter(BasePlotter):
    """
    Creates heatmap visualizations comparing performance metrics across different libraries.
    """

    # noinspection PyIncorrectDocstring
    def plot(self, *, specific_save_path=None, **kwargs):
        """
        Create a heatmap showing relative performance across different sizes and operations.

        Args:
            metric: 'time' or 'memory' to specify which metric to visualize
            specific_save_path: Optional path to override the default save path
        """
        metric = kwargs.get("metric", "time")

        plt.figure(figsize=(15, 10))

        if metric == "time":
            self._create_time_heatmaps()
        elif metric == "memory":
            self._create_memory_heatmaps()

        plt.tight_layout()
        self._save_and_show(plt.gcf(), specific_save_path)

    def _create_time_heatmaps(self):
        """Create time-based performance heatmaps for read and write operations."""
        write_data, read_data = self._split_data_by_operation()
        write_pivot = self._create_time_normalized_pivot(write_data)
        read_pivot = self._create_time_normalized_pivot(read_data)
        self._plot_time_heatmaps(write_pivot, read_pivot)

    @staticmethod
    def _create_time_normalized_pivot(data):
        """Create a normalized pivot table for time metrics.

        Args:
            data: DataFrame containing time data for one operation type

        Returns:
            DataFrame with normalized time values
        """
        pivot = pd.DataFrame()
        for _, row in data.iterrows():
            min_time = min(row["jsd_time"], row["orjson_time"], row["msgspec_time"])
            pivot.at[row["size"], "JSD"] = row["jsd_time"] / min_time
            pivot.at[row["size"], "orjson"] = row["orjson_time"] / min_time
            pivot.at[row["size"], "msgspec"] = row["msgspec_time"] / min_time
        return pivot

    def _plot_time_heatmaps(self, write_pivot, read_pivot):
        """Plot heatmaps for write and read execution times.

        Args:
            write_pivot: DataFrame with normalized write time data
            read_pivot: DataFrame with normalized read time data
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))

        self._create_single_heatmap(
            write_pivot, ax1, "Write Performance (normalized, lower is better)"
        )
        self._create_single_heatmap(
            read_pivot, ax2, "Read Performance (normalized, lower is better)"
        )

    def _create_memory_heatmaps(self):
        """Create memory-based performance heatmaps for read and write operations."""
        write_data, read_data = self._split_data_by_operation()
        write_pivot = self._create_normalized_pivot(write_data)
        read_pivot = self._create_normalized_pivot(read_data)
        self._plot_memory_heatmaps(write_pivot, read_pivot)

    def _split_data_by_operation(self):
        """Split the data into write and read operations."""
        write_data = self.df[self.df["operation"] == "Write"]
        read_data = self.df[self.df["operation"] == "Read"]
        return write_data, read_data

    @staticmethod
    def _create_normalized_pivot(data):
        """Create a normalized pivot table for memory metrics.

        Args:
            data: DataFrame containing memory data for one operation type

        Returns:
            DataFrame with normalized memory values
        """
        pivot = pd.DataFrame()
        for _, row in data.iterrows():
            min_mem = min(row["jsd_mem"], row["orjson_mem"], row["msgspec_mem"])
            pivot.at[row["size"], "JSD"] = row["jsd_mem"] / min_mem
            pivot.at[row["size"], "orjson"] = row["orjson_mem"] / min_mem
            pivot.at[row["size"], "msgspec"] = row["msgspec_mem"] / min_mem
        return pivot

    def _plot_memory_heatmaps(self, write_pivot, read_pivot):
        """Plot heatmaps for write and read memory usage.

        Args:
            write_pivot: DataFrame with normalized write memory data
            read_pivot: DataFrame with normalized read memory data
        """
        _, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))

        self._create_single_heatmap(
            write_pivot, ax1, "Write Memory Usage (normalized, lower is better)"
        )
        self._create_single_heatmap(
            read_pivot, ax2, "Read Memory Usage (normalized, lower is better)"
        )

    @staticmethod
    def _create_single_heatmap(data, ax, title):
        """Create a single heatmap subplot.

        Args:
            data: DataFrame with normalized data
            ax: Matplotlib axis to plot on
            title: Title for the subplot
        """
        sns.heatmap(data, annot=True, fmt=".2f", cmap="YlOrRd", ax=ax, vmin=1, vmax=3)
        ax.set_title(title)


class RadarChartPlotter(BasePlotter):
    """
    Creates radar/spider charts comparing metrics for a specific data size.
    """

    # noinspection PyIncorrectDocstring
    def plot(self, *, specific_save_path=None, **kwargs):
        """
        Create a radar/spider chart comparing all metrics for a specific data size.

        Args:
            size_value: The specific data size to visualize
            specific_save_path: Optional path to override the default save path
        """
        size_value = kwargs.get("size_value", None)
        size_data = self._get_size_data(size_value)

        if len(size_data) < 2:
            print(f"No data available for size {size_value}")
            return

        # Extract data for Write and Read operations
        write_data, read_data = self._extract_operation_data(size_data)

        # Prepare metrics and normalized values
        metrics, angles = self._prepare_metrics()
        jsd_values, orjson_values, msgspec_values = self._calculate_normalized_values(
            write_data, read_data
        )

        # Create and configure the plot
        fig, ax = self._create_radar_plot(
            angles, metrics, jsd_values, orjson_values, msgspec_values, size_value
        )

        self._save_and_show(fig, specific_save_path)

    def _get_size_data(self, size_value):
        """Extract data for the specified size."""
        return self.df[self.df["size"] == size_value]

    @staticmethod
    def _extract_operation_data(size_data):
        """Extract write and read operation data."""
        write_data = size_data[size_data["operation"] == "Write"].iloc[0]
        read_data = size_data[size_data["operation"] == "Read"].iloc[0]
        return write_data, read_data

    @staticmethod
    def _prepare_metrics():
        """Prepare metrics and angles for the radar chart."""
        metrics = ["Write Time", "Read Time", "Write Memory", "Read Memory"]

        angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
        angles.append(angles[0])

        return metrics, angles

    def _calculate_normalized_values(self, write_data, read_data):
        """Calculate normalized values for each library."""
        # Find maximum values for normalization
        max_values = self._find_max_values(write_data, read_data)

        # Calculate normalized values for each library
        jsd_values = self._normalize_library_values(
            "jsdfile", write_data, read_data, max_values
        )
        orjson_values = self._normalize_library_values(
            "orjson", write_data, read_data, max_values
        )
        msgspec_values = self._normalize_library_values(
            "msgspec", write_data, read_data, max_values
        )

        # Close the radar chart loops
        self._close_radar_loops(jsd_values, orjson_values, msgspec_values)

        return jsd_values, orjson_values, msgspec_values

    @staticmethod
    def _find_max_values(write_data, read_data):
        """Find maximum values for each metric for normalization."""
        return {
            "max_write_time": max(
                write_data["jsd_time"],
                write_data["orjson_time"],
                write_data["msgspec_time"],
            ),
            "max_read_time": max(
                read_data["jsd_time"],
                read_data["orjson_time"],
                read_data["msgspec_time"],
            ),
            "max_write_mem": max(
                write_data["jsd_mem"],
                write_data["orjson_mem"],
                write_data["msgspec_mem"],
            ),
            "max_read_mem": max(
                read_data["jsd_mem"], read_data["orjson_mem"], read_data["msgspec_mem"]
            ),
        }

    @staticmethod
    def _normalize_library_values(library, write_data, read_data, max_values):
        """Calculate normalized values for a specific library (1 is worst, 0 is best)."""
        return [
            write_data[f"{library}_time"] / max_values["max_write_time"],
            read_data[f"{library}_time"] / max_values["max_read_time"],
            write_data[f"{library}_mem"] / max_values["max_write_mem"],
            read_data[f"{library}_mem"] / max_values["max_read_mem"],
        ]

    @staticmethod
    def _close_radar_loops(*value_lists):
        """Add the first value to the end of each list to close the radar chart loops."""
        for values in value_lists:
            values.append(values[0])

    def _create_radar_plot(
        self, angles, metrics, jsd_values, orjson_values, msgspec_values, size_value
    ):
        """Create and configure the radar plot."""
        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))

        # Plot each library
        ax.plot(
            angles, jsd_values, "o-", linewidth=2, label="JSD", color=self.colors[0]
        )
        ax.plot(
            angles,
            orjson_values,
            "s-",
            linewidth=2,
            label="orjson",
            color=self.colors[1],
        )
        ax.plot(
            angles,
            msgspec_values,
            "^-",
            linewidth=2,
            label="msgspec",
            color=self.colors[2],
        )

        # Fill areas
        ax.fill(angles, jsd_values, alpha=0.25, color=self.colors[0])
        ax.fill(angles, orjson_values, alpha=0.25, color=self.colors[1])
        ax.fill(angles, msgspec_values, alpha=0.25, color=self.colors[2])

        # Configure the plot
        self._configure_plot_appearance(ax, angles, metrics, size_value)

        return fig, ax

    @staticmethod
    def _configure_plot_appearance(ax, angles, metrics, size_value):
        """Configure the appearance of the radar plot."""
        # Set the labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics[:-1])

        # Remove radial labels and set y-limits
        ax.set_yticklabels([])
        ax.set_ylim(0, 1.05)

        # Add legend and title
        ax.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))
        ax.set_title(
            f"Performance Comparison for {size_value} Records\n(closer to center is better)",
            pad=20,
            fontsize=14,
        )

        # Add explanation text
        plt.figtext(
            0.5,
            0.01,
            "This chart compares normalized metrics where smaller values (closer to center) indicate better performance.",
            ha="center",
            fontsize=10,
            bbox=dict(facecolor="white", alpha=0.8),
        )


class Plotter(BasePlotter):
    """
    Main plotter class that utilizes all specialized plotting components.
    """

    def __init__(self, df, save_path=None):
        """
        Initialize the Plotter with benchmark data and optional save path.

        Args:
            df: DataFrame with benchmark results
            save_path: Optional base path to save figures
        """
        super().__init__(df, save_path)

        # Initialize all specialized plotters
        self._initialize_plotters(df, save_path)

        # Map of plot types to their handler methods
        self._plot_handlers = {
            PlotType.EXECUTION_TIME: self._handle_execution_time,
            PlotType.MEMORY_USAGE: self._handle_memory_usage,
            PlotType.PERFORMANCE_RATIO: self._handle_performance_ratio,
            PlotType.FILE_SIZE: self._handle_file_size,
            PlotType.HEATMAP_TIME: self._handle_heatmap_time,
            PlotType.HEATMAP_MEMORY: self._handle_heatmap_memory,
            PlotType.RADAR: self._handle_radar,
            PlotType.ALL: self._handle_all,
        }

    def _initialize_plotters(self, df, save_path):
        """Initialize all specialized plotters."""
        self.execution_plotter = ExecutionTimePlotter(df, save_path)
        self.memory_plotter = MemoryUsagePlotter(df, save_path)
        self.ratio_plotter = PerformanceRatioPlotter(df, save_path)
        self.file_size_plotter = FileSizeComparisonPlotter(df, save_path)
        self.heatmap_plotter = HeatmapComparisonPlotter(df, save_path)
        self.radar_plotter = RadarChartPlotter(df, save_path)

    # noinspection PyIncorrectDocstring
    def plot(self, specific_save_path=None, **kwargs):
        """
        Unified plot function that handles all plot types.

        Args:
            plot_type: PlotType enum specifying which plot to generate
            specific_save_path: Optional path to override the default save path
            show_progress: Whether to show progress bar
            **kwargs: Additional arguments specific to certain plot types
                      (e.g., size_value for RADAR plots)

        Returns:
            None
        """
        plot_type = kwargs.get("plot_type", None)
        show_progress = kwargs.get("show_progress", False)
        if plot_type not in self._plot_handlers:
            raise ValueError(f"Unknown plot type: {plot_type}")

        # Call the appropriate handler method
        self._plot_handlers[plot_type](
            specific_save_path, show_progress=show_progress, **kwargs
        )

    def _handle_execution_time(self, specific_save_path=None, **_):
        """Handler for execution time plots."""
        save_path = specific_save_path or (
            f"{self.save_path}/execution_times.png" if self.save_path else None
        )
        self.execution_plotter.plot(specific_save_path=save_path)

    def _handle_memory_usage(self, specific_save_path=None, **_):
        """Handler for memory usage plots."""
        save_path = specific_save_path or (
            f"{self.save_path}/memory_usage.png" if self.save_path else None
        )
        self.memory_plotter.plot(specific_save_path=save_path)

    def _handle_performance_ratio(self, specific_save_path=None, **_):
        """Handler for performance ratio plots."""
        save_path = specific_save_path or (
            f"{self.save_path}/performance_ratios.png" if self.save_path else None
        )
        self.ratio_plotter.plot(specific_save_path=save_path)

    def _handle_file_size(self, specific_save_path=None, **_):
        """Handler for file size comparison plots."""
        save_path = specific_save_path or (
            f"{self.save_path}/file_size_comparison.png" if self.save_path else None
        )
        self.file_size_plotter.plot(specific_save_path=save_path)

    def _handle_heatmap_time(self, specific_save_path=None, **_):
        """Handler for time heatmap plots."""
        save_path = specific_save_path or (
            f"{self.save_path}/heatmap_time.png" if self.save_path else None
        )
        self.heatmap_plotter.plot(specific_save_path=save_path, metric="time")

    def _handle_heatmap_memory(self, specific_save_path=None, **_):
        """Handler for memory heatmap plots."""
        save_path = specific_save_path or (
            f"{self.save_path}/heatmap_memory.png" if self.save_path else None
        )
        self.heatmap_plotter.plot(specific_save_path=save_path, metric="memory")

    def _handle_radar(self, specific_save_path=None, **kwargs):
        """
        Handler for radar plots.

        Args:
            specific_save_path: Optional path to override the default save path
            **kwargs: Must contain 'size_value' for radar plots
        """
        size_value = kwargs.get("size_value")
        if size_value is None:
            raise ValueError("size_value is required for radar plots")

        save_path = specific_save_path or (
            f"{self.save_path}/radar_chart_{size_value}.png" if self.save_path else None
        )
        self.radar_plotter.plot(size_value=size_value, specific_save_path=save_path)

    def _handle_all(self, specific_save_path=None, show_progress=True, **kwargs):
        """
        Handler for generating all plots.

        Args:
            specific_save_path: Optional base path to override the default save path
            show_progress: Whether to show progress bar
        """
        # Define the plots to generate
        plots = self._get_plots(specific_save_path, **kwargs)

        # Get unique sizes for radar charts
        sizes = self.df["size"].unique()
        for size in sizes:
            plots.append(
                (
                    f"Radar Chart (size={size})",
                    lambda s=size: self._handle_radar(
                        specific_save_path, size_value=s, **kwargs
                    ),
                )
            )

        # Generate plots with progress bar if requested
        if show_progress:
            self._show_plots_progress(plots)
        else:
            for _, plot_func in plots:
                plot_func()

    @staticmethod
    def _show_plots_progress(plots):
        """Show plots with progress bar."""
        with tqdm(total=len(plots), desc="Generating plots", unit="plot") as pbar:
            for plot_name, plot_func in plots:
                pbar.set_description(f"Generating {plot_name}")
                plot_func()
                pbar.update(1)

    def _get_plots(self, specific_save_path=None, **kwargs):
        """Get all plots to generate."""
        return [
            (
                "Execution Time",
                lambda: self._handle_execution_time(specific_save_path, **kwargs),
            ),
            (
                "Memory Usage",
                lambda: self._handle_memory_usage(specific_save_path, **kwargs),
            ),
            (
                "Performance Ratio",
                lambda: self._handle_performance_ratio(specific_save_path, **kwargs),
            ),
            (
                "File Size Comparison",
                lambda: self._handle_file_size(specific_save_path, **kwargs),
            ),
            (
                "Time Heatmap",
                lambda: self._handle_heatmap_time(specific_save_path, **kwargs),
            ),
            (
                "Memory Heatmap",
                lambda: self._handle_heatmap_memory(specific_save_path, **kwargs),
            ),
        ]


# Update the visualization function to use the updated Plotter class
def create_visualizations(df, output_dir=None):
    """
    Create all visualizations from benchmark data.

    Args:
        df: DataFrame with benchmark results
        output_dir: Optional directory to save the visualizations
    """
    # Create all visualizations using the main Plotter class
    plotter = Plotter(df, output_dir)
    plotter.plot(PlotType.ALL, show_progress=True)
