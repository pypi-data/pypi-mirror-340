import os
import pathlib
import time
from threading import Thread, Event

from appium.options.android import UiAutomator2Options

from test2va.mutation_predictor.util.util import save_json_to_file
from test2va.mutation_validator.util.grant_permissions import grant_permissions

from test2va.mutation_validator.util.setup_test import setup_test

from test2va.mutation_predictor.main import analysis_start
from test2va.mutation_validator.util.base_test_executor import base_test_executor

from test2va.bridge import format_caps, check_node_installed, check_npm_appium_install, install_appium, \
    check_uia2_driver_install, install_uia2_driver, new_start_server, parse, wait_app_load, validate_mutation, \
    generate_va_methods
from test2va.exceptions import NoJavaData, CapTypeMismatch, NodeNotInstalled, ExecutionStopped, \
    AppiumInstallationError
from test2va.mutation_predictor.config import gpt_config


class T2VAEvent:
    def __init__(self):
        self.handlers = []

    def connect(self, func):
        self.handlers.append(func)

    def fire(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)


class ExecEvents:
    def __init__(self):
        self.on_start = T2VAEvent()
        self.on_finish = T2VAEvent()
        self.on_error = T2VAEvent()
        self.on_progress = T2VAEvent()
        self.on_log = T2VAEvent()
        self.on_success = T2VAEvent()


class ToolExec:
    def __init__(self, api: str, udid: str, apk: str, added_caps: dict[str, str], cap_data, j_path: str = None,
                 j_code: str = None):
        self.events = ExecEvents()
        self._connect_default()

        self.apk = apk
        self.api = api
        self.udid = udid
        self.j_code = j_code
        self.j_path = j_path
        self.caps = added_caps
        self.cap_data = cap_data
        self.temp_java = None
        self.options = UiAutomator2Options()
        self.driver = None
        self.app_service = None
        self.start = None

        self.stopped = False

    def execute(self, setup_only=False):
        self.events.on_start.fire()

        # Get the absolute path of gp_config.py
        config_path = pathlib.Path(gpt_config.__file__).resolve().parent / "gpt_config.py"
        content = f'GPT_API_KEY = "{self.api}"'
        config_path.write_text(content)

        if self.j_code is None and self.j_path is None:
            raise NoJavaData("No Java source code or path provided. See console for details.", self.events)

        if self.j_code is not None:
            self.temp_java = os.path.join(os.path.dirname(__file__), "../output/temp_java.java")
            with open(self.temp_java, "w") as f:
                f.write(self.j_code)

            self.j_path = self.temp_java

        self.caps = format_caps(self.caps, self.cap_data)
        self.options.udid = self.udid
        self.options.app = self.apk
        self.options.automation_name = "UiAutomator2"

        for cap, val in self.caps.items():
            try:
                setattr(self.options, cap, val)
            except Exception:
                raise CapTypeMismatch(f"Capability type mismatch for {cap}. See console for details.", self.events)

        self.events.on_progress.fire("Checking Node installation")

        if not check_node_installed():
            raise NodeNotInstalled("Node installation not found. Install it here: "
                                   "https://nodejs.org/en/download/package-manager. Make sure it is added to PATH.",
                                   self.events)

        self.events.on_success.fire("Node installation found")
        self.events.on_progress.fire("Checking Appium installation")

        if not check_npm_appium_install():
            self.events.on_progress.fire("Appium installation not found. Attempting installation")
            install_success = install_appium()

            if not install_success:
                raise AppiumInstallationError("Appium installation failed. Use 'npm install -g appium' to install "
                                              "manually. See console for details.", self.events)

            self.events.on_success.fire("Appium installation successful")
        else:
            self.events.on_success.fire("Appium installation found")

        self.events.on_progress.fire("Checking UiAutomator2 driver installation")

        if not check_uia2_driver_install():
            self.events.on_progress.fire("UiAutomator2 driver installation not found. Attempting installation")

            install_success = install_uia2_driver()

            if not install_success:
                raise AppiumInstallationError("UiAutomator2 driver installation failed. Use 'appium driver install "
                                              "uiautomator2' to install manually. See console for details.",
                                              self.events)

            self.events.on_success.fire("UiAutomator2 driver installation successful")
        else:
            self.events.on_success.fire("UiAutomator2 driver installation found")

        self.events.on_progress.fire("Starting Appium server")

        self.driver, self.app_service = new_start_server(self.options, self.events)

        self.events.on_success.fire("Appium server started")

        self.start = time.time()

        if setup_only:
            return

        parse_start_time = time.time()

        self.events.on_progress.fire("Parsing java source code")

        data, output_path = parse(self.apk, self.j_path, self.driver, self.events)

        self.events.on_success.fire(f"Parsing complete - output saved to {os.path.abspath(output_path)}")

        parse_end_time = time.time()

        self.events.on_progress.fire("Waiting for app to load")

        wait_app_load()

        app_wait_end_time = time.time()

        ai_data = self.ai_only(data[0], output_path)

        ai_end_time = time.time()

        self.events.on_progress.fire("Attempting possible mutable paths")
        m_out_path, new_ai_data = validate_mutation(self.driver, data, self.start, ai_data, output_path, self.events,
                                                    lambda: self.ai_only(data[0], output_path), True)

        self.events.on_success.fire(f"Mutation complete - output saved to {os.path.abspath(m_out_path)}")

        mutator_end_time = time.time()

        parse_time = parse_end_time - parse_start_time
        app_wait_time = app_wait_end_time - parse_end_time
        ai_time = ai_end_time - app_wait_end_time
        mutator_time = mutator_end_time - ai_end_time
        total_time = mutator_end_time - parse_start_time

        new_ai_data["times"] = {
            "parse_time": parse_time,
            "app_wait_time": app_wait_time,
            "ai_time": ai_time,
            "mutator_time": mutator_time,
            "total_time": total_time
        }

        # Write the new AI data to the output path
        save_json_to_file(ai_data, f"{output_path}/mutant_data.json")

        self.events.on_progress.fire("Generating results and task methods")

        method_path = generate_va_methods(self.j_path, f"{output_path}/mutant_data.json", output_path, self.events)

        self.events.on_success.fire(f"Generation complete - output saved to {os.path.abspath(method_path)}")

        self.driver.quit()

        self.events.on_log.fire("Appium server stopped")

        self.events.on_finish.fire()

    @staticmethod
    def parse_only(out, apk: str, j_code: str = None, j_path: str = None):
        if j_code is None and j_path is None:
            raise NoJavaData("No Java source code or path provided. See console for details.", ExecEvents())

        if j_code is not None:
            temp_java = os.path.join(os.path.dirname(__file__), "../output/temp_java.java")
            with open(temp_java, "w") as f:
                f.write(j_code)

            j_path = temp_java

        out.insert("end", f"Parsing java source code\n")

        data, output_path = parse(apk, j_path, None, ExecEvents())

        out.insert("end", f"Parsing complete - output saved to {os.path.abspath(output_path)}\n")

        # If temp java was created, remove it
        if j_code is not None:
            os.remove(temp_java)

    def ai_only(self, data, output_path, setup_driver=False):
        if setup_driver:
            self.execute(setup_only=True)

        self.events.on_progress.fire("Executing base test & Starting AI analysis")

        grant_permissions(self.driver, self.driver.current_package)

        # First, we will set up the test if it had a setup function
        if data["Before"] is not None:
            setup_test(self.driver, data)

        # Then, we will execute the base test to make sure that it works properly as given.
        # At the same time, at each step, we will populate relevant potential mutators.
        # First arg (mutators) isn't needed anymore
        pg_src_path = base_test_executor([], self.driver, data, [], [], output_path)

        if pg_src_path is None:
            raise Exception("Error during base test execution. The base test did not return a page source path, "
                            "indicating that the final step was not reached or another error has occurred.")

        def keep_session_alive(_, s_e, interval=30):
            while not s_e.is_set():  # Check if stop event is triggered
                time.sleep(interval)
                self.driver.current_activity  # No-op to keep session active

        # Initialize the stop event
        stop_event = Event()

        # Start the thread
        keep_alive_thread = Thread(target=keep_session_alive, args=(self.driver, stop_event))
        keep_alive_thread.start()

        # AI Stuff
        ai_data = analysis_start(pg_src_path, self.j_path, output_path)

        stop_event.set()
        keep_alive_thread.join()

        self.events.on_success.fire("AI analysis complete")

        return ai_data

    def mutate_only(self, data, ai_data, output_path):
        self.execute(setup_only=True)

        self.events.on_progress.fire("Attempting possible mutable paths")

        m_out_path, ai_only = validate_mutation(self.driver, data, self.start, ai_data, output_path, self.events, True)

        self.events.on_success.fire(f"Mutation complete - output saved to {os.path.abspath(m_out_path)}")

    @staticmethod
    def generate_only(out, output_path):
        out.insert("end", "Generating results and task methods...\n")

        # The ai data will be a file in the output folder ending in .java.json, find it:
        ai_data_file = None
        for file in os.listdir(output_path):
            if file.endswith(".java.json"):
                ai_data_file = os.path.join(output_path, file)
                break

        if ai_data_file is None:
            out.insert("end", "No AI data file found.\n")
            raise NoJavaData("No AI data file found.", ExecEvents())

        # Check for a file called "java.xml" in the output folder
        xml_path = None
        for file in os.listdir(output_path):
            if file.endswith(".xml"):
                xml_path = os.path.join(output_path, file)
                break

        if xml_path is None:
            out.insert("end", "No XML file found.\n")
            raise NoJavaData("No XML file found.", ExecEvents())

        # find mutant_data.json in output_path
        ai_data_file = os.path.join(output_path, "mutant_data.json")
        if not os.path.exists(ai_data_file):
            out.insert("end", "No AI data file found.\n")
            raise NoJavaData("No AI data file found.", ExecEvents())

        method_path = generate_va_methods(xml_path, ai_data_file, output_path, ExecEvents())

        out.insert("end", f"Generation complete - output saved to {os.path.abspath(method_path)}\n")

    def stop(self):
        self.events.on_log.fire("Stop request received. Stopping execution when possible...")
        self.stopped = True

    def _connect_default(self):
        # Remove temp java
        self.events.on_error.connect(self._remove_temp_java)
        self.events.on_finish.connect(self._remove_temp_java)
        self.events.on_finish.connect(self._on_stop)
        self.events.on_progress.connect(self._on_prog_stop_check)

    def _remove_temp_java(self, _=None, __=None):
        if self.temp_java is not None and os.path.exists(self.temp_java):
            os.remove(self.temp_java)

    def _on_prog_stop_check(self, _):
        if self.stopped:
            raise ExecutionStopped("Execution stopped by user", self.events)

    def _on_stop(self):
        if self.app_service is not None:
            try:
                self.app_service.stop()
            except Exception:
                pass

        if self.driver is not None:
            try:
                self.driver.quit()
            except Exception:
                pass

        self.app_service = None
        self.driver = None
