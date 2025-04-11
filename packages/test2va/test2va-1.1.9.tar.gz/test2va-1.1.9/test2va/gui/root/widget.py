import os
import threading

import customtkinter as ctk

from test2va.bridge import get_capability_options, get_cap_type, format_caps, check_file_exists
from test2va.execute import ToolExec
from test2va.gui.root.tabs import TabFrameWidget
from importlib.metadata import version

from test2va.gui.shared import def_udid_entry, def_jsrc_entry, def_api_entry, def_data_entry
from test2va.util.write_json import read_json

size_x = 900
size_y = 480

resize_x = False
resize_y = False

title = f"Test2VA {version('test2va')}"
icon = os.path.join(os.path.dirname(__file__), "./assets", "openmoji-android.ico")

columns = 1
c_weight = 1

tab_col = 0
page_col = 1

rows = 0
r_weight = 1

frame_grid = "nsew"


class RootWidget(ctk.CTk):
    """Main GUI application for Test2VA.

        This class initializes the GUI, manages user interactions, and executes Test2VA functions.

        Attributes:
            java_window_content (str): Content of the Java source window.
            current_running_txt (str): Status message for ongoing operations.
            cap_window_open (bool): Whether the capability window is open.
            sav_prof_open (bool): Whether the save profile window is open.
            selected_profile (str): Currently selected profile.
            loaded_profile (str): Currently loaded profile.
            cur_tab (str): Current tab identifier.
            cur_page (str): Current page identifier.
            cap_cache (dict): Cached capabilities.
            page_cache (dict): Cached page references.
            Exe (ToolExec): Tool execution instance.
        """
    def __init__(self):
        """Initializes the Test2VA GUI application."""
        super().__init__()

        self.java_window_content = ""
        self.current_running_txt = None

        self.cap_window_open = False
        self.sav_prof_open = False

        # Main Refs
        self.java_path_ref = None
        self.java_src_ref = None
        self.cap_frame_ref = None
        self.i_frame_ref = None
        self.prof_list_ref = None
        self.prof_butt_ref = None
        self.stat_prev_ref = None
        self.stat_guide_ref = None
        self.stat_list_ref = None
        self.run_out_ref = None
        self.run_butt_ref = None

        # Cap Add Refs
        self.cap_desc_ref = None
        self.cap_val_ref = None
        self.cap_ref = None

        self.selected_profile = None
        self.loaded_profile = None

        self.cur_tab = None
        self.cur_page = None

        self.cap_cache = {}
        self.page_cache = {}

        self.Exe = None

        self.caps = get_capability_options()

        self.geometry(f"{size_x}x{size_y}")
        self.resizable(resize_x, resize_y)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.title(title)
        self.iconbitmap(icon)

        self.grid_columnconfigure(columns, weight=c_weight)
        self.grid_rowconfigure(rows, weight=r_weight)

        self.tab_frame = TabFrameWidget(self)
        self.tab_frame.grid(row=0, column=tab_col, sticky=frame_grid)

        # Note: Home page does not need to be initialized here,
        # it is set as the default tab in the TabFrameWidget class

    def get_cap_type(self, cap):
        """Retrieves the capability type.

        Args:
            cap (str): Capability name.

        Returns:
            str: The type of the capability.
        """
        return get_cap_type(self.caps, cap)

    def format_caps(self):
        """Formats and returns the capability cache.

        Returns:
            dict: Formatted capabilities.
        """
        return format_caps(self.cap_cache, self.caps)

    def on_closing(self):
        """Handles window close event by quitting and destroying the GUI."""
        self.quit()
        self.destroy()

    def stop(self):
        """Stops the execution of Test2VA tool."""
        if self.Exe is None or self.Exe.stopped:
            return

        self.Exe.stop()
        self.run_butt_ref.configure(text="Stopping...", state="disabled")

    def run(self, parse_only=False, m_prediction=False, mutate=False, gen=False):
        """Executes Test2VA operations based on user input.

        Args:
            parse_only (bool): If True, runs only the parsing function.
            m_prediction (bool): If True, runs the AI mutation prediction.
            mutate (bool): If True, runs the mutation process.
            gen (bool): If True, runs the task generation process.

        Returns:
            bool: True if execution started successfully, otherwise None.
        """
        if self.current_running_txt is not None:
            return self._on_log(self.current_running_txt)

        self._on_start()

        apk = self.i_frame_ref.apk_entry.input.get()
        udid = self.i_frame_ref.udid_entry.input.get()
        api = self.i_frame_ref.api_entry.input.get()
        data = self.i_frame_ref.data_entry.input.get()

        if self.i_frame_ref.java_entry.input.get() and self.i_frame_ref.java_entry.input.get() != "Path to Java file":
            if not check_file_exists(self.i_frame_ref.java_entry.input.get(), print):
                self._on_error("Please enter a valid Java file path")
                return
            j_path = self.i_frame_ref.java_entry.input.get()
            j_code = None
        elif self.java_window_content != def_jsrc_entry:
            j_path = None
            j_code = self.java_window_content
        else:
            self._on_error("Please enter a Java file path or paste Java source code", "")
            return

        if parse_only:
            self.current_running_txt = "Currently parsing..."
            try:
                ToolExec.parse_only(self.run_out_ref, apk, j_code, j_path)
            except Exception as e:
                pass

            self.current_running_txt = None
            return

        if gen:
            if not data or data == def_data_entry:
                self._on_error("Please enter a valid data folder path", "")
                return

            self.current_running_txt = "Generating Task Methods..."
            try:
                ToolExec.generate_only(self.run_out_ref, data)
            except Exception as e:
                pass
            self.current_running_txt = None
            return

        if not check_file_exists(apk, print):
            self._on_error("Please enter a valid APK file path", "")
            return

        if not udid or udid == def_udid_entry:
            self._on_error("Please enter a valid device UDID", "")
            return

        if (not api or api == def_api_entry) and not mutate:
            self._on_error("Please enter a valid OpenAI API Key", "")
            return

        if m_prediction:
            if not data or data == def_data_entry:
                self._on_error("Please enter a valid data folder path", "")
                return

            p_data = self.search_folder(data, "_parsed.json")
            if not p_data:
                self._on_error(f"Could not find parsed data in {data} (file that ends with _parsed.json). Did you run "
                               f"the parser?", "")
                return

            p_data_content = read_json(p_data)

        if mutate:
            if not data or data == def_data_entry:
                self._on_error("Please enter a valid data folder path", "")
                return

            ai_data = self.search_folder(data, ".java.json")
            if not ai_data:
                self._on_error(f"Could not find ai_data in {data} (file that ends with .java.json). Did you run the "
                               f"prediction?", "")
                return

            p_data = self.search_folder(data, "_parsed.json")
            if not p_data:
                self._on_error(f"Could not find parsed data in {data} (file that ends with _parsed.json). Did you run "
                               f"the parser?", "")
                return

            ai_data_content = read_json(ai_data)
            p_data_content = read_json(p_data)

            # ai_data has keys "0": {...}, "1": {...}, etc.
            # change them to numbers instead of strings
            ai_data_content = {int(k): v for k, v in ai_data_content.items()}

        Exe = ToolExec(api=api, udid=udid, apk=apk, added_caps=self.cap_cache, cap_data=self.caps, j_path=j_path,
                       j_code=j_code)
        Exe.events.on_start.connect(self._on_start)
        Exe.events.on_error.connect(self._on_error)
        Exe.events.on_log.connect(self._on_log)
        Exe.events.on_progress.connect(self._on_progress)
        Exe.events.on_success.connect(self._on_success)
        Exe.events.on_finish.connect(self._on_finish)

        if m_prediction:
            self._on_progress("Executing base test & Starting AI analysis")
            # Exe.ai_only(p_data_content[0], data, True)
            # Do this with threading instead
            threading.Thread(target=Exe.ai_predictor_only, args=(p_data_content[0], data)).start()
            return

        if mutate:
            self._on_progress("Executing base test & Starting AI analysis")
            # P_data isn't indexed here i didn't make this very consistent
            threading.Thread(target=Exe.mutate_only, args=(p_data_content, ai_data_content, data)).start()
            return

        self.Exe = Exe

        threading.Thread(target=Exe.execute).start()

        return True

    def _on_start(self):
        """Handles execution start event."""
        self.run_out_ref.delete("0.0", "end")

    def _on_error(self, msg, _err):
        """Handles error events.

        Args:
            msg (str): Error message.
            _err (Exception): Exception instance.
        """
        self.run_out_ref.insert("end", f"❌ {msg}\n")

    def _on_log(self, msg):
        """Handles log events.

        Args:
            msg (str): Log message.
        """
        self.run_out_ref.insert("end", f"ℹ️ {msg}\n")
        print(f"ℹ️{msg}")

    def _on_progress(self, msg):
        """Handles progress events.

        Args:
            msg (str): Progress message.
        """
        self.title(f"Test2VA {version('test2va')} - {msg}...")
        self.run_out_ref.insert("end", f"ℹ️ {msg}\n")

    def _on_success(self, msg):
        """Handles success events.

        Args:
            msg (str): Success message.
        """
        self.title(f"Test2VA {version('test2va')}")
        self.run_out_ref.insert("end", f"✅ {msg}\n")

    def _on_finish(self):
        """Handles execution finish event."""
        self.title(f"Test2VA {version('test2va')}")
        self.run_out_ref.insert("end", "🛑 Execution Stopped\n")

        if self.stat_list_ref is not None:
            self.stat_list_ref.redraw_stats()

        self.run_butt_ref.reset()

    # This method will search a folder for a file that ends with a given argument
    def search_folder(self, folder, ext):
        """Searches for a file with a specific extension in a folder.

        Args:
            folder (str): Folder path.
            ext (str): File extension to search for.

        Returns:
            str or None: File path if found, otherwise None.
        """
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(ext):
                    return os.path.join(root, file)
            for dir in dirs:
                if dir.endswith(ext):
                    return os.path.join(root, dir)
        return None
