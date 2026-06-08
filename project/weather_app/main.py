"""
Weather Forecast Application - Main GUI Module.
A modern weather application built with Tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import json
import os
import threading
from typing import Optional, List

import config
from weather_api import WeatherAPI


class SearchHistory:
    """
    Manages the search history for weather queries.
    Persists history to a JSON file.
    """

    def __init__(self, file_path: str, max_items: int = 5):
        """
        Initialize search history manager.

        Args:
            file_path: Path to the JSON file for storing history.
            max_items: Maximum number of items to keep in history.
        """
        self.file_path = file_path
        self.max_items = max_items
        self.history: List[str] = []
        self._load_history()

    def _load_history(self) -> None:
        """Load search history from JSON file."""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    self.history = json.load(f)
        except (json.JSONDecodeError, IOError):
            self.history = []

    def _save_history(self) -> None:
        """Save search history to JSON file."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.history, f, indent=2)
        except IOError as e:
            print(f"Error saving history: {e}")

    def add(self, city: str) -> None:
        """
        Add a city to the search history.

        Args:
            city: City name to add.
        """
        city = city.strip()
        if not city:
            return

        # Remove if already exists (to move to front)
        if city in self.history:
            self.history.remove(city)

        # Add to front
        self.history.insert(0, city)

        # Limit to max items
        if len(self.history) > self.max_items:
            self.history = self.history[:self.max_items]

        self._save_history()

    def get_all(self) -> List[str]:
        """Return list of all history items."""
        return self.history.copy()


class WeatherApp:
    """
    Main Weather Application class.
    Handles GUI creation and user interactions.
    """

    def __init__(self, root: tk.Tk):
        """
        Initialize the Weather Application.

        Args:
            root: Tkinter root window.
        """
        self.root = root
        self.root.title("Weather Forecast App")
        self.root.geometry("450x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f8")

        # Initialize components
        self.weather_api = WeatherAPI()
        self.search_history = SearchHistory(config.HISTORY_FILE, config.MAX_HISTORY_ITEMS)
        self.current_units = tk.StringVar(value="metric")
        self.weather_icon: Optional[ImageTk.PhotoImage] = None

        # Center window on screen
        self._center_window()

        # Build GUI
        self._create_widgets()

        # Update date/time display
        self._update_datetime()

    def _center_window(self) -> None:
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _create_widgets(self) -> None:
        """Create all GUI widgets."""
        # Main container
        self.main_frame = tk.Frame(self.root, bg="#f0f4f8")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header section
        self._create_header()

        # Search section
        self._create_search_section()

        # Weather display section
        self._create_weather_section()

        # Status bar
        self._create_status_bar()

    def _create_header(self) -> None:
        """Create header with datetime display."""
        header_frame = tk.Frame(self.main_frame, bg="#f0f4f8")
        header_frame.pack(fill="x", pady=(0, 15))

        # Title
        title_label = tk.Label(
            header_frame,
            text="☀️ Weather Forecast",
            font=("Segoe UI", 24, "bold"),
            bg="#f0f4f8",
            fg="#1a365d"
        )
        title_label.pack()

        # DateTime label
        self.datetime_label = tk.Label(
            header_frame,
            text="",
            font=("Segoe UI", 10),
            bg="#f0f4f8",
            fg="#4a5568"
        )
        self.datetime_label.pack(pady=(5, 0))

    def _create_search_section(self) -> None:
        """Create search input and controls section."""
        search_frame = tk.Frame(self.main_frame, bg="#ffffff", relief="flat")
        search_frame.pack(fill="x", pady=(0, 15))
        search_frame.configure(highlightbackground="#e2e8f0", highlightthickness=1)

        inner_frame = tk.Frame(search_frame, bg="#ffffff", padx=15, pady=15)
        inner_frame.pack(fill="x")

        # City input with label
        input_label = tk.Label(
            inner_frame,
            text="Enter City Name:",
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#2d3748"
        )
        input_label.pack(anchor="w")

        # City entry with history dropdown
        entry_frame = tk.Frame(inner_frame, bg="#ffffff")
        entry_frame.pack(fill="x", pady=(5, 10))

        self.city_var = tk.StringVar()
        self.city_entry = ttk.Combobox(
            entry_frame,
            textvariable=self.city_var,
            font=("Segoe UI", 11),
            values=self.search_history.get_all(),
            state="normal"
        )
        self.city_entry.pack(fill="x", ipady=5)

        # Units selection
        units_frame = tk.Frame(inner_frame, bg="#ffffff")
        units_frame.pack(fill="x", pady=(0, 10))

        units_label = tk.Label(
            units_frame,
            text="Temperature Unit:",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#4a5568"
        )
        units_label.pack(side="left")

        celsius_rb = tk.Radiobutton(
            units_frame,
            text="Celsius",
            variable=self.current_units,
            value="metric",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#2d3748",
            selectcolor="#ffffff",
            activebackground="#ffffff"
        )
        celsius_rb.pack(side="left", padx=(10, 0))

        fahrenheit_rb = tk.Radiobutton(
            units_frame,
            text="Fahrenheit",
            variable=self.current_units,
            value="imperial",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#2d3748",
            selectcolor="#ffffff",
            activebackground="#ffffff"
        )
        fahrenheit_rb.pack(side="left", padx=(10, 0))

        # Buttons frame
        buttons_frame = tk.Frame(inner_frame, bg="#ffffff")
        buttons_frame.pack(fill="x")

        # Get Weather button
        self.get_weather_btn = tk.Button(
            buttons_frame,
            text="🔍 Get Weather",
            font=("Segoe UI", 11, "bold"),
            bg="#3182ce",
            fg="white",
            activebackground="#2c5282",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self._on_get_weather
        )
        self.get_weather_btn.pack(side="left", fill="x", expand=True, ipady=8)

        # Refresh button
        self.refresh_btn = tk.Button(
            buttons_frame,
            text="🔄",
            font=("Segoe UI", 11),
            bg="#48bb78",
            fg="white",
            activebackground="#38a169",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=3,
            command=self._on_refresh
        )
        self.refresh_btn.pack(side="right", padx=(10, 0), ipady=8)

    def _create_weather_section(self) -> None:
        """Create weather display section."""
        self.weather_frame = tk.Frame(self.main_frame, bg="#ffffff", relief="flat")
        self.weather_frame.pack(fill="both", expand=True)
        self.weather_frame.configure(highlightbackground="#e2e8f0", highlightthickness=1)

        # Initial placeholder
        self._show_placeholder()

    def _show_placeholder(self) -> None:
        """Show placeholder message when no weather data."""
        # Clear existing widgets
        for widget in self.weather_frame.winfo_children():
            widget.destroy()

        placeholder_text = tk.Label(
            self.weather_frame,
            text="🌤️\n\nEnter a city name and click\n'Get Weather' to see the forecast",
            font=("Segoe UI", 12),
            bg="#ffffff",
            fg="#a0aec0",
            justify="center"
        )
        placeholder_text.pack(expand=True)

    def _display_weather(self, weather_data: dict) -> None:
        """
        Display weather information in the GUI.

        Args:
            weather_data: Dictionary containing weather information.
        """
        # Clear existing widgets
        for widget in self.weather_frame.winfo_children():
            widget.destroy()

        # Main content frame
        content_frame = tk.Frame(self.weather_frame, bg="#ffffff", padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)

        # City name
        city_label = tk.Label(
            content_frame,
            text=f"{weather_data['city']}, {weather_data['country']}",
            font=("Segoe UI", 18, "bold"),
            bg="#ffffff",
            fg="#1a365d"
        )
        city_label.pack()

        # Weather icon and temperature frame
        icon_temp_frame = tk.Frame(content_frame, bg="#ffffff")
        icon_temp_frame.pack(pady=15)

        # Weather icon
        if weather_data.get('icon_image'):
            icon_label = tk.Label(
                icon_temp_frame,
                image=weather_data['icon_image'],
                bg="#ffffff"
            )
            icon_label.pack(side="left", padx=(0, 10))

        # Temperature
        temp_label = tk.Label(
            icon_temp_frame,
            text=weather_data['temperature'],
            font=("Segoe UI", 36, "bold"),
            bg="#ffffff",
            fg="#2b6cb0"
        )
        temp_label.pack(side="left")

        # Weather condition
        condition_label = tk.Label(
            content_frame,
            text=weather_data['condition'],
            font=("Segoe UI", 14),
            bg="#ffffff",
            fg="#4a5568"
        )
        condition_label.pack(pady=(0, 15))

        # Separator
        separator = tk.Frame(content_frame, bg="#e2e8f0", height=1)
        separator.pack(fill="x", pady=10)

        # Details frame
        details_frame = tk.Frame(content_frame, bg="#ffffff")
        details_frame.pack(fill="x")

        # Create detail rows
        details = [
            ("🌡️ Feels Like", weather_data['feels_like']),
            ("💧 Humidity", weather_data['humidity']),
            ("💨 Wind Speed", weather_data['wind_speed'])
        ]

        for i, (label, value) in enumerate(details):
            row_frame = tk.Frame(details_frame, bg="#ffffff")
            row_frame.pack(fill="x", pady=5)

            label_widget = tk.Label(
                row_frame,
                text=label,
                font=("Segoe UI", 11),
                bg="#ffffff",
                fg="#718096",
                anchor="w"
            )
            label_widget.pack(side="left")

            value_widget = tk.Label(
                row_frame,
                text=value,
                font=("Segoe UI", 11, "bold"),
                bg="#ffffff",
                fg="#2d3748",
                anchor="e"
            )
            value_widget.pack(side="right")

    def _create_status_bar(self) -> None:
        """Create status bar at the bottom."""
        self.status_var = tk.StringVar(value="Ready. Enter a city to get weather information.")
        status_label = tk.Label(
            self.main_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            bg="#f0f4f8",
            fg="#718096",
            anchor="w"
        )
        status_label.pack(fill="x", pady=(10, 0))

    def _update_datetime(self) -> None:
        """Update the date and time display."""
        now = datetime.now()
        formatted = now.strftime("%A, %B %d, %Y | %I:%M %p")
        self.datetime_label.config(text=formatted)
        # Schedule next update in 1 second
        self.root.after(1000, self._update_datetime)

    def _on_get_weather(self) -> None:
        """Handle Get Weather button click."""
        city = self.city_var.get().strip()

        if not city:
            self.status_var.set("Please enter a city name.")
            self._show_error("Please enter a city name.")
            return

        # Disable buttons during fetch
        self.get_weather_btn.config(state="disabled")
        self.refresh_btn.config(state="disabled")
        self.status_var.set(f"Fetching weather for {city}...")

        # Run API call in separate thread
        threading.Thread(target=self._fetch_weather, args=(city,), daemon=True).start()

    def _on_refresh(self) -> None:
        """Handle Refresh button click - refresh current city."""
        city = self.city_var.get().strip()

        if not city:
            self.status_var.set("No city to refresh. Please enter a city name first.")
            return

        self._on_get_weather()

    def _fetch_weather(self, city: str) -> None:
        """
        Fetch weather data in a background thread.

        Args:
            city: City name to fetch weather for.
        """
        units = self.current_units.get()
        result = self.weather_api.get_weather(city, units)

        # Update GUI from main thread
        self.root.after(0, lambda: self._handle_weather_result(city, result))

    def _handle_weather_result(self, city: str, result: dict) -> None:
        """
        Handle the weather API result.

        Args:
            city: City that was queried.
            result: Result dictionary from WeatherAPI.
        """
        # Re-enable buttons
        self.get_weather_btn.config(state="normal")
        self.refresh_btn.config(state="normal")

        if result['success']:
            # Fetch icon
            icon_image = None
            if result.get('icon_code'):
                icon = self.weather_api.get_weather_icon(result['icon_code'], (100, 100))
                if icon:
                    icon_image = ImageTk.PhotoImage(icon)
                    # Keep reference to prevent garbage collection
                    self.weather_icon = icon_image

            result['icon_image'] = icon_image

            # Add to history
            self.search_history.add(city)

            # Update combobox values
            self.city_entry['values'] = self.search_history.get_all()

            # Display weather
            self._display_weather(result)
            self.status_var.set(f"Weather loaded for {city}")
        else:
            self._show_error(result['error'])
            self.status_var.set(f"Error: {result['error']}")
            self._show_placeholder()

    def _show_error(self, message: str) -> None:
        """
        Display an error message.

        Args:
            message: Error message to display.
        """
        messagebox.showerror("Error", message)


def main():
    """Main entry point for the Weather Application."""
    root = tk.Tk()

    # Set ttk style
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TCombobox', padding=5)

    app = WeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
