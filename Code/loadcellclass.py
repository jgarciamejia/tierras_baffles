#!/usr/bin/env python3
"""
Phidget Load Cell Class 
    Import to use a number of load cells originating from one hub
    Use cell path as #-#, hub port-bridge channel

Avaliable functions
    cell = PhidgetLoadCell("#-#", sensor_label="#", sensor_no="#")
    cell.calibrate(n_readings=#, calib_type="compression/tension",
                   mid_weight=#kg, max_weight=#kg)

    or load existing coefficients and 
    cell = PhidgetLoadCell("#-#", sensor_no="#")
    cell.load_calibration("compression")
    cell.read_once()
    or
    cell.read_continuous()
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.VoltageRatioInput import *

# Comment out if you want to connect to something else or through the file rather than through import
Net.addServer("hub5000", "hub5000.local.", 5661, "", 0)

CALIB_FILE_TEMPLATE = "load_sensor_calibration_coeffs_{calib_type}_{sensor_no}.txt"
# ---------------------------------------------------------------------------


class PhidgetLoadCell:
    """
    Represents one load cell wired to a specific port.

    wiring_path : str
        (e.g. "3-0")
    sensor_label : str, optional
        Sharpie label written on the sensor
    sensor_no : str, optional
        Serial/etch number on the sensor body
    """

    def __init__(self, wiring_path: str, sensor_label: str = "", sensor_no: str = ""):
        parts = wiring_path.strip().split("-")
        if len(parts) != 2:
            raise ValueError(
                f"wiring_path must be '#-#', got {wiring_path!r}"
            )
        self.hub_port   = int(parts[0])
        self.channel    = int(parts[1])
        self.wiring_path = wiring_path

        self.sensor_label = sensor_label
        self.sensor_no    = sensor_no

        # Calibration coefficients (set by calibrate() or load_calibration())
        self.slope     = None
        self.intercept = None
        self.calib_type = None

        self._vri: VoltageRatioInput | None = None

    # connection
    def connect(self, timeout_ms: int = 20_000) -> None:
        """Open the VoltageRatioInput channel and wait for attachment."""
        if self._vri is not None:
            return  # already connected

        vri = VoltageRatioInput()
        vri.setHubPort(self.hub_port)
        vri.setChannel(self.channel)
        vri.setIsRemote(True)
        vri.openWaitForAttachment(timeout_ms)
        self._vri = vri
        print(f"[{self.wiring_path}] Phidget attached.")

    def disconnect(self) -> None:
        """Close the channel if it is open."""
        if self._vri is not None:
            self._vri.close()
            self._vri = None
            print(f"[{self.wiring_path}] Phidget disconnected.")

    # readings
    def get_voltage_ratio(self) -> float:
        """Return a single voltage ratio reading (V/V)."""
        if self._vri is None:
            raise RuntimeError("Not connected. Call connect() first.")
        return self._vri.getVoltageRatio()

    def collect_readings(self, n: int, label: str = "", interval_s: float = 1.0) -> float:
        """
        Collect *n* readings spaced by *interval_s* seconds, print each one, and return the average.
        """
        tag = f"[{self.wiring_path}] {label}" if label else f"[{self.wiring_path}]"
        print(f"{tag} — collecting {n} readings...")
        readings = []
        for _ in range(n):
            vr = self.get_voltage_ratio()
            print(f"  VR = {vr:.8f} V/V")
            readings.append(vr)
            time.sleep(interval_s)
        avg = float(np.mean(readings))
        print(f"{tag} average VR = {avg:.8f} V/V")
        return avg

    # Calibration
    def calibrate(self, n_readings: int = 5, calib_type: str   = "", mid_weight: float = 0.0,
                  max_weight: float = 0.0, interval_s: float = 1.0) -> None:
        """
        Run a 3-point calibration and save coefficients.
        Any parameter left at its default will be prompted interactively.
        """
        if not self.sensor_label:
            self.sensor_label = input("Enter Sensor Label (Sharpie on sensor): ")
        if not self.sensor_no:
            self.sensor_no = input("Enter Sensor No (etched on sensor): ")
        if not calib_type:
            calib_type = input("Is this a tension or compression calibration? ")
        if mid_weight == 0.0:
            mid_weight = float(input("Enter the mid-point calibration weight (kg): "))
        if max_weight == 0.0:
            max_weight = float(input("Enter the max-point calibration weight (kg): "))

        self.calib_type = calib_type
        self.connect()

        try:
            # Zero point
            print("\nEnsure the sensor is upright and unloaded.")
            input("Press Enter to begin zero-point collection.")
            zero_vr = self.collect_readings(n_readings, "Zero-pt", interval_s)

            # Mid point
            input(f"\nLoad the sensor with {mid_weight} kg, then press Enter.")
            mid_vr = self.collect_readings(n_readings, "Mid-pt", interval_s)

            # Max point
            input(f"\nLoad the sensor with {max_weight} kg, then press Enter.")
            max_vr = self.collect_readings(n_readings, "Max-pt", interval_s)

        finally:
            self.disconnect()

        vrs     = [zero_vr, mid_vr, max_vr]
        weights = [0.0, mid_weight, max_weight]
        slope, intercept, r, p, se = stats.linregress(vrs, weights)
        self.slope     = slope
        self.intercept = intercept
        print(f"\nSlope: {slope}  Intercept: {intercept}  R²: {r**2:.6f}")

        self._save_calibration(calib_type, self.sensor_no)

        self._plot_calibration(vrs, weights, calib_type)

    def _save_calibration(self, calib_type: str) -> None:
        fname = CALIB_FILE_TEMPLATE.format(calib_type=calib_type, )
        with open(fname, "a+") as f:
            f.write(
                f"\n {self.sensor_label} {self.sensor_no}"
                f" {self.slope} {self.intercept}"
            )
        print(f"Calibration coefficients saved to {fname}.")

    def _plot_calibration(self, vrs, weights, calib_type: str) -> None:
        x = np.linspace(min(vrs), max(vrs), 50)
        y = self.slope * x + self.intercept

        fig, ax = plt.subplots()
        ax.plot(vrs, weights, "o", label="Data")
        ax.plot(x, y, label="Fit")
        ax.set_xlabel("Voltage Ratio (V/V)")
        ax.set_ylabel("Load (kg)")
        ax.set_title(
            f"Slope: {self.slope:.4f}  Intercept: {self.intercept:.4f}"
        )
        ax.invert_xaxis()
        ax.legend()
        plt.tight_layout()

        fname = (
            f"3ptcalib_Sensor{self.sensor_label}"
            f"_No{self.sensor_no}_{calib_type}.pdf"
        )
        fig.savefig(fname)
        print(f"Calibration plot saved to {fname}.")
        plt.show()

    # Load calibration from file
    def load_calibration(self, calib_type: str) -> None:
        """
        Read slope and intercept for *this* sensor from the calibration file.

        Requires sensor_no to be set (pass at construction or set directly).
        """
        if not self.sensor_no:
            self.sensor_no = input("Enter Sensor No (etched on sensor): ")

        fname = CALIB_FILE_TEMPLATE.format(calib_type=calib_type, sensor_no=self.sensor_no)
        with open(fname) as f:
            lines = f.readlines()[1:] 

        sensor_nos = [ln.split()[1] for ln in lines]
        if self.sensor_no not in sensor_nos:
            raise ValueError(
                f"Sensor No {self.sensor_no!r} not found in {fname}."
            )

        idx            = sensor_nos.index(self.sensor_no)
        parts          = lines[idx].split()
        self.sensor_label = parts[0]
        self.slope        = float(parts[2])
        self.intercept    = float(parts[3])
        self.calib_type   = calib_type
        print(
            f"[{self.wiring_path}] Loaded calibration for sensor {self.sensor_no}: "
            f"slope={self.slope}, intercept={self.intercept}"
        )

    # Measurement
    def _require_calibration(self) -> None:
        if self.slope is None or self.intercept is None:
            raise RuntimeError(
                "No calibration loaded. Call calibrate() or load_calibration() first."
            )

    def voltage_to_load(self, vr: float) -> float:
        """Convert a voltage ratio (V/V) to load (kg) using stored coefficients."""
        self._require_calibration()
        return self.slope * vr + self.intercept

    def read_once(self) -> tuple[float, float]:
        """
        Take a single reading, print it, and return (voltage_ratio, load_kg).
        Opens and closes the connection automatically.
        """
        self._require_calibration()
        self.connect()
        try:
            vr   = self.get_voltage_ratio()
            load = self.voltage_to_load(vr)
            print(
                f"[{self.wiring_path}] VR = {vr:.8f} V/V  |  Load = {load:.4f} kg"
            )
            return vr, load
        finally:
            self.disconnect()

    def read_continuous(self, interval_s: float = 1.0) -> None:
        """
        Stream readings until Ctrl-C.  Connection is managed automatically.
        """
        self._require_calibration()
        self.connect()
        print(
            f"[{self.wiring_path}] Reading continuously. Press Ctrl-C to stop.\n"
        )
        try:
            while True:
                vr   = self.get_voltage_ratio()
                load = self.voltage_to_load(vr)
                print(
                    f"[{self.wiring_path}] VR = {vr:.8f} V/V  |  Load = {load:.4f} kg"
                )
                time.sleep(interval_s)
        except KeyboardInterrupt:
            print(f"\n[{self.wiring_path}] Stopped by user.")
        finally:
            self.disconnect()

    def __repr__(self) -> str:
        calib_str = (
            f"slope={self.slope:.4f}, intercept={self.intercept:.4f}"
            if self.slope is not None
            else "uncalibrated"
        )
        return (
            f"PhidgetLoadCell(path={self.wiring_path!r}, "
            f"sensor_no={self.sensor_no!r}, {calib_str})"
        )


##########################################################################
if __name__ == "__main__":
    MODE = input("Mode — [c]alibrate or [r]ead? ").strip().lower()
    calib_type = input("compression or tension? ").strip()

    cell0 = PhidgetLoadCell("3-0")
    cell1 = PhidgetLoadCell("3-1")

    if MODE == "c":
        mid  = float(input("Mid-point weight (kg): "))
        maxi = float(input("Max-point weight (kg): "))
        n    = int(input("Readings per point: "))
        cell0.calibrate(n_readings=n, calib_type=calib_type,
                        mid_weight=mid, max_weight=maxi)
        cell1.calibrate(n_readings=n, calib_type=calib_type,
                        mid_weight=mid, max_weight=maxi)
    else:
        cell0.load_calibration(calib_type)
        cell1.load_calibration(calib_type)

        # Connect both before entering the loop so we don't open/close repeatedly
        cell0.connect()
        cell1.connect()
        print("Reading both cells. Ctrl-C to stop.\n")
        try:
            while True:
                for cell in (cell0, cell1):
                    vr   = cell.get_voltage_ratio()
                    load = cell.voltage_to_load(vr)
                    print(
                        f"[{cell.wiring_path}] VR = {vr:.8f} V/V | Load = {load:.4f} kg"
                    )
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopped by user.")
        finally:
            cell0.disconnect()
            cell1.disconnect()