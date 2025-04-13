#!/usr/bin/env python

"""
This module contains the wrapper classes for used equipments in
measure_manager.py. The purpose of this module is to unify the interface
of different equipments, so that they can be combined freely

! not all equipments are included in this module, only those needed wrapping
! for some equipments already wrapped(probe_rotator), the wrapper is not necessary

each wrapper provides the following methods(some only for source meters):
- setup: initialize the equipment, usually just basic settings not including output
- output_switch: switch the output on or off
- uni_output: set the output to a certain value
    all output methods have two implementations, one is from off to on, including
    setting up parameters like range and compliance, the other is just setting the
    output value when already on
- get_output_status: get the current output value
- sense: set the meter to sense current or voltage
- shutdown: shutdown the equipment
- ramp_output: ramp the output to the target value
* the member "meter" is provided for directly accessing the equipment driver
* the member "info_dict" is provided for storing the information of the equipment

Flow:
    Wrapperxxxx(GPIB)
    setup("ac/dc")
    uni_output(value, (freq), compliance, type_str)
    (change value without disabling the output)
    shutdown()

Actions that can be optimized for quicker operation:
- switch operation
- range and compliance setting
"""

import time
from typing import Literal, Optional
from typing_extensions import override

from abc import ABC, abstractmethod

import numpy as np
from pymeasure.instruments.srs import SR830
from pymeasure.instruments.oxfordinstruments import ITC503
from pymeasure.instruments.keithley import KeithleyDMM6500
from pymeasure.instruments.keithley import Keithley2182
from qcodes.instrument_drivers.Keithley import Keithley2400, Keithley2450
from qcodes.instrument_drivers.Lakeshore import LakeshoreModel336
from qcodes.instrument import find_or_create_instrument
from pyomnix.omnix_logger import get_logger
from pyomnix.utils import convert_unit, print_progress_bar, SWITCH_DICT, CacheArray

from .drivers.MercuryiPS_VISA import OxfordMercuryiPS
from .drivers.mercuryITC import MercuryITC
from .drivers.Keithley_6430 import Keithley_6430
from .drivers.keithley6221 import Keithley6221
from .drivers.keysight_b2902b import Keysight_B2902B, KeysightB2902BChannel
from .drivers.SR860 import SR860

logger = get_logger(__name__)


class Meter(ABC):
    """
    The usage should be following the steps:
    1. instantiate
    2. setup method
    3. output_switch method (embedded in output method for the first time)
    4. uni/rms/dc_output method or ramp_output method
    5(if needed). sense method
    LAST. shutdown method
    """

    @abstractmethod
    def __init__(self):
        self.info_dict = {}
        self.meter = None

    @abstractmethod
    def setup(self, function: Literal["sense", "source"], *vargs, **kwargs):
        pass

    def info(self, *, sync=True):
        if sync:
            self.info_sync()
        return self.info_dict

    @abstractmethod
    def info_sync(self):
        self.info_dict.update({})

    def sense_delay(self, type_str: Literal["curr", "volt"], *, delay: float = 0.01):
        time.sleep(delay)
        return self.sense(type_str=type_str)

    @abstractmethod
    def sense(self, type_str: Literal["curr", "volt"]) -> float | list:
        pass

    def __del__(self):
        try:
            self.meter.__del__()
        except AttributeError:
            del self.meter


class SourceMeter(Meter):
    @abstractmethod
    def __init__(self):
        super().__init__()
        self.info_dict.update({"output_type": "curr"})
        self.output_target = 0
        self.safe_step = 1e-6  # step threshold, used for a default ramp

    @abstractmethod
    def output_switch(self, switch: bool | Literal["on", "off", "ON", "OFF"]):
        """the meter must be returned to 0"""
        self.info_dict["output_status"] = (
            switch if isinstance(switch, bool) else switch.lower() in ["on", "ON"]
        )

    @abstractmethod
    def uni_output(
        self,
        value: float | str,
        *,
        freq: Optional[float | str] = None,
        compliance: Optional[float | str] = None,
        fix_range: Optional[float | str] = None,
        type_str: Literal["curr", "volt"],
    ) -> float:
        """
        judge the output type based on if freq is none
        judge if the range and compliance need to be set or modified
        (only modify if needed)
        return the real output value to avoid range issue etc.
        """
        self.info_dict["output_type"] = type_str
        self.output_target = value

        return self.get_output_status()[0]

    @abstractmethod
    def get_output_status(self) -> tuple[float, float, float] | tuple[float, float]:
        """
        return the output value from device and also the target value set by output methods

        Returns:
            tuple[float, float, float]: the actual output value and the target value and current range
            or tuple[float, float]: the actual output value and the target value (no range, e.g. for sr830)
        """
        pass

    @abstractmethod
    def shutdown(self):
        pass

    def ramp_output(
        self,
        type_str: Literal["curr", "volt", "V", "I"],
        value: float | str,
        *,
        freq: Optional[float | str] = None,
        compliance: Optional[float | str] = None,
        interval: Optional[float | str] = None,
        sleep=0.2,
        from_curr=True,
        no_progress=False,
    ) -> None:
        """
        ramp the output to the target value

        Args:
            type_str: "curr" or "volt"
            value: the target value
            freq: the frequency of the output (if ac)
            interval: the step interval between each step
            sleep: the time interval(s) between each step
            value: the target value
            compliance: the compliance value
            from_curr: whether to ramp from the current value(default) or from 0
            no_progress: whether to suppress the progress bar
        """
        type_str: Literal["curr", "volt"] = type_str.replace("V", "volt").replace(
            "I", "curr"
        )
        value = convert_unit(value, "")[0]
        if not from_curr:
            # reset the output to 0 (ensure it in output_switch method)
            self.output_switch("off")
            self.output_switch("on")

        curr_val = self.get_output_status()[0]
        if curr_val == value:
            self.uni_output(value, freq=freq, type_str=type_str, compliance=compliance)
            return
        if interval is None:
            if abs(curr_val - value) > 20:
                arr = np.arange(curr_val, value, 0.2 * np.sign(value - curr_val))
            else:
                arr = np.linspace(curr_val, value, 70)
        elif isinstance(interval, (float, str)):
            interval = convert_unit(interval, "")[0]
            interval = abs(interval) * np.sign(value - curr_val)
            arr = np.arange(curr_val, value, interval)
            arr = np.concatenate((arr, [value]))
        else:
            raise ValueError(
                "interval should be a float or str or just left as default"
            )

        for idx, i in enumerate(arr):
            self.uni_output(i, freq=freq, type_str=type_str, compliance=compliance)
            if not no_progress:
                print_progress_bar(
                    (idx + 1) / len(arr) * 100, 100, prefix="Ramping Meter:"
                )
            time.sleep(sleep)


class ACSourceMeter(SourceMeter):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def rms_output(
        self,
        value: float | str,
        *,
        freq: float | str,
        compliance: float | str,
        type_str: Literal["curr", "volt"],
    ):
        pass


class DCSourceMeter(SourceMeter):
    @abstractmethod
    def __init__(self):
        super().__init__()

    @abstractmethod
    def dc_output(
        self,
        value: float | str,
        *,
        compliance: float | str,
        type_str: Literal["curr", "volt"],
        fix_range: Optional[float | str] = None,
    ):
        pass


class Wrapper6221(ACSourceMeter, DCSourceMeter):
    """
    Flow:
    Wrapper6221(GPIB)
    setup("ac/dc")
    uni_output(value, (freq), compliance, type_str)
    (change value without disabling the output)
    shutdown()
    """

    def __init__(self, GPIB: str = "GPIB0::12::INSTR"):
        super().__init__()
        self.meter = Keithley6221(GPIB)
        self.output_target = 0
        self.safe_step = 1e-6
        self.info_dict = {
            "GPIB": GPIB,
            "output_type": "curr",
            "ac_dc": "ac",
            "output_status": False,
            "output_value": 0,
        }
        self.info_sync()
        self.mea_mode: Literal["normal", "delta", "pulse-delta", "differential"] = (
            "normal"
        )
        logger.info("note the grounding:")  # TODO: add grounding instruction#

    def info_sync(self):
        self.info_dict.update(
            {
                "source_range": self.meter.source_range,
                "output_value": max(
                    self.meter.source_current, self.meter.waveform_amplitude
                ),
                "frequency": self.meter.waveform_frequency,
                "compliance": self.meter.source_compliance,
                "wave_function": self.meter.waveform_function,
                "wave_offset": self.meter.waveform_offset,
                "wave_phasemarker": self.meter.waveform_phasemarker_phase,
                "low_grounded": self.meter.output_low_grounded,
            }
        )

    def setup(
        self,
        function: Literal["source", "sense"] = "source",
        mode: Literal["ac", "dc"] = "ac",
        *,
        offset: float | None = None,
        source_auto_range: bool | None = None,
        low_grounded: bool | None = None,
        wave_function: Literal[
            "sine",
            "ramp",
            "square",
            "arbitrary1",
            "arbitrary2",
            "arbitrary3",
            "arbitrary4",
        ] | None = None,
        mea_mode: Literal["normal", "delta", "pulse-delta", "differential"] = "normal",
        reset: bool = False,
    ) -> None:
        """
        set up the Keithley 6221 instruments, overwrite the specific settings here, other settings will all be
        reserved. Note that the waveform will not begin here
        """
        if reset:
            offset = 0
            source_auto_range = True
            low_grounded = True
            wave_function = "sine"

        source_6221 = self.meter
        # first must close the output to do setup
        self.output_switch("off")
        source_6221.clear()
        if reset:
            source_6221.write("*RST")
        if mea_mode == "normal":
            assert function == "source", (
                "6221 is a source meter, so the function should be source"
            )
        if mea_mode == "delta":
            logger.info(
                "delta mode is selected, please set the specific parameters using delta_setup method"
            )
            self.delta_setup()
            mode = "dc"
        self.mea_mode = mea_mode
        if mode == "ac":
            self.info_dict["ac_dc"] = "ac"
            if wave_function is not None:
                source_6221.waveform_function = wave_function
                self.info_dict.update({"wave_function": wave_function})
            source_6221.waveform_amplitude = 0
            if offset is not None:
                source_6221.waveform_offset = offset
                self.info_dict.update({"wave_offset": offset})
            source_6221.waveform_ranging = "best"
            source_6221.waveform_use_phasemarker = True
            source_6221.waveform_phasemarker_line = 3
            source_6221.waveform_duration_set_infinity()
            source_6221.waveform_phasemarker_phase = 0
            self.info_dict.update(
                {
                    "wave_phasemarker": 0,
                }
            )
        elif mode == "dc":
            self.info_dict["ac_dc"] = "dc"
        if source_auto_range is not None:
            source_6221.source_auto_range = source_auto_range
        if low_grounded is not None:
            source_6221.output_low_grounded = low_grounded
            self.info_dict.update({"low_grounded": low_grounded})

    def delta_setup(
        self,
        *,
        delta_unit: Literal["V", "Ohms", "W", "Siemens"] = "V",
        delta_delay=0.02,
        delta_cycles: int | Literal["INF"] = "INF",
        delta_mea_sets: int | Literal["INF"] = 1,
        delta_compliance_abort: bool = True,
        delta_cold_switch: bool = False,
        trace_pts: int = 10,
    ):
        """
        set the specific parameters for delta mode
        """
        self.mea_mode = "delta"
        self.meter.delta_unit = delta_unit
        self.meter.delta_buffer_points = trace_pts

        self.meter.delta_delay = delta_delay
        self.meter.delta_cycles = delta_cycles
        self.meter.delta_measurement_sets = delta_mea_sets
        self.meter.delta_compliance_abort = delta_compliance_abort
        self.meter.delta_cold_switch = delta_cold_switch

    def output_switch(self, switch: bool | Literal["on", "off", "ON", "OFF"]):
        """
        switch the output on or off (not suitable for special modes)
        """
        switch = SWITCH_DICT.get(switch, False) if isinstance(switch, str) else switch

        if self.info_dict["output_status"] == switch:
            return

        if switch:
            if self.info_dict["ac_dc"] == "ac":
                self.meter.waveform_arm()
                self.meter.waveform_start()
                self.info_dict["output_status"] = True
            elif self.info_dict["ac_dc"] == "dc":
                self.meter.enable_source()
                self.info_dict["output_status"] = True
        else:
            if self.info_dict["ac_dc"] == "ac":
                self.meter.waveform_abort()
            elif self.info_dict["ac_dc"] == "dc":
                self.meter.disable_source()

            self.meter.waveform_amplitude = 0
            self.meter.source_current = 0
            self.info_dict["output_status"] = False

    def get_output_status(self) -> tuple[float, float, float]:
        """
        return the output value from device and also the target value set by output methods (not suitable for special modes)

        Returns:
            tuple[float, float, float]: the output value (rms for ac) and the target value
        """
        if self.info_dict["ac_dc"] == "ac":
            # amplitude for 6221 is peak to peak
            return (
                self.meter.waveform_amplitude / np.sqrt(2),
                self.output_target,
                self.meter.source_range,
            )
        elif self.info_dict["ac_dc"] == "dc":
            return (
                self.meter.source_current,
                self.output_target,
                self.meter.source_range,
            )
        else:
            raise ValueError("ac_dc term in info_dict should be either ac or dc")

    def uni_output(
        self,
        value: float | str,
        *,
        freq: Optional[float | str] = None,
        compliance: Optional[float | str] = None,
        type_str: Literal["curr", "volt"] = "curr",
    ) -> float:
        # judge if the output exceeds the range first
        # since 6221 use the same source_range for both ac and dc
        # so the range could be treated in this unified method
        if self.mea_mode == "normal":
            value = convert_unit(value, "")[0]
            if abs(value) > 0.105:
                raise ValueError("6221 output should be less than 0.105A")
            range_curr = self.meter.source_range
            if (
                abs(range_curr) * 1.05 <= abs(value)
                or abs(value) <= abs(range_curr) / 100
            ) and value != 0:
                if freq is not None:
                    self.output_switch(
                        "off"
                    )  # turn off the output before changing the range for ac mode
                self.meter.source_range = value
            # directly call corresponding output method if desired output type is matched
            # call setup first if desired output type is not matched
            if self.info_dict["ac_dc"] == "ac":
                if freq is not None:
                    self.rms_output(
                        value, freq=freq, compliance=compliance, type_str=type_str
                    )
                else:
                    self.setup("source", "dc")
                    self.dc_output(value, compliance=compliance, type_str=type_str)
            elif self.info_dict["ac_dc"] == "dc":
                if freq is None:
                    self.dc_output(value, compliance=compliance, type_str=type_str)
                elif freq is not None:
                    self.setup("source", "ac")
                    self.rms_output(
                        value, freq=freq, compliance=compliance, type_str=type_str
                    )

            self.output_target = convert_unit(value, "A")[0]
            return self.get_output_status()[0]
        elif self.mea_mode == "delta":
            self.meter.delta_high_source = value
            if compliance is not None:
                compliance = convert_unit(compliance, "")[0]
                self.meter.source_compliance = compliance
            self.meter.delta_arm()
            time.sleep(2)  # wait for the delta mode to be armed
            self.meter.delta_start()
            return self.meter.delta_high_source

    def rms_output(
        self,
        value: float | str,
        *,
        freq: Optional[float | str] = None,
        compliance: Optional[float | str] = None,
        type_str: Literal["curr"] = "curr",
    ):
        """
        6221 is a current source, so the output is always current
        set the output to a certain value
        if current config is dc, then call setup to reset to ac default settings
        set config manually before calling this method if special params are needed
        """
        assert type_str == "curr", (
            "6221 is a current source, so the output is always current"
        )

        if self.info_dict["ac_dc"] == "dc":
            self.setup("source", "ac")

        value = convert_unit(value, "")[0]
        # create a shortcut for turning output to 0
        if value == 0:
            self.meter.waveform_amplitude = 0
            if not self.info_dict["output_status"]:
                self.output_switch("on")
            return
        value_p2p = value * np.sqrt(2)
        if freq is not None:
            self.meter.waveform_frequency = convert_unit(freq, "Hz")[0]
            self.info_dict["frequency"] = freq

        if not self.info_dict["output_status"]:
            if compliance is not None:
                compliance = convert_unit(compliance, "")[0]
            else:
                compliance = value_p2p * 100000
            self.meter.source_compliance = compliance
            self.meter.waveform_amplitude = value_p2p
            self.output_switch("on")

        else:
            self.meter.waveform_amplitude = value_p2p

    def dc_output(
        self,
        value: float | str,
        *,
        compliance: Optional[float | str] = None,
        type_str: Literal["curr"] = "curr",
        fix_range: Optional[float | str] = None,
    ):
        """
        6221 is a current source, so the output is always current
        set the output to a certain value
        """
        assert type_str == "curr", (
            "6221 is a current source, so the output is always current"
        )

        value = convert_unit(value, "")[0]
        # create a shortcut for turning output to 0
        if value == 0:
            self.meter.source_current = 0
            self.output_switch("on")
            return

        if compliance is not None:
            compliance = convert_unit(compliance, "")[0]
        else:
            compliance = abs(
                value * 100000
            )  # 6221 will automatically switch to lowest compliance if too low

        if fix_range is not None:
            self.meter.source_range = fix_range
        self.meter.source_compliance = compliance
        self.meter.source_current = value
        self.output_switch("on")

    def sense(self, type_str: Literal["volt"] = "volt"):
        if self.mea_mode == "normal":
            logger.info("6221 is a source meter, no sense function")
        elif self.mea_mode == "delta":
            return self.meter.delta_sense

    def shutdown(self):
        if self.info_dict["output_status"]:
            self.output_switch("off")
        self.meter.shutdown()


class Wrapper2182(Meter):
    """
    Flow:
    Wrapper2182(GPIB)
    setup(channel)
    sense()
    """

    def __init__(self, GPIB: str = "GPIB0::7::INSTR"):
        super().__init__()
        self.meter = Keithley2182(GPIB, read_termination="\n")
        self.setup()
        self.info_dict = {"GPIB": GPIB, "channel": 1, "sense_type": "volt"}

    def setup(
        self,
        function: Literal["sense"] = "sense",
        *,
        channel: Literal[0, 1, 2] = 1,
        reset: bool = False,
    ) -> None:
        if reset:
            self.meter.reset()
        self.meter.active_channel = channel
        self.meter.channel_function = "voltage"
        self.meter.voltage_nplc = 5
        # source_2182.sample_continuously()
        # source_2182.ch_1.voltage_offset_enabled = True
        # source_2182.ch_1.acquire_voltage_reference()
        self.meter.ch_1.setup_voltage()

    def info_sync(self):
        """
        no parameters to sync for 2182
        """
        pass

    def sense(self, type_str: Literal["volt"] = "volt") -> float:
        return self.meter.voltage


class Wrapper6500(Meter):
    """
    Waiting for refinement, not tested due to the limited usage of 6500
    Flow:
    Wrapper6500(GPIB)
    setup(channel)
    sense()
    """

    def __init__(self, GPIB: str = "GPIB0::16::INSTR"):
        super().__init__()
        self.meter = KeithleyDMM6500(GPIB)
        self.setup("sense")
        self.info_dict = {
            "GPIB": GPIB,
            "channel": 1,
            "sense_type": "volt",
            "auto_range": True,
            "auto_zero": True,
            "terminal": "front",
        }

    def setup(self, function: Literal["source", "sense"], reset: bool = False) -> None:
        """default to measuring voltage"""
        if reset:
            self.meter.write("*RST")
        self.meter.auto_range()
        if function == "sense":
            self.meter.write(":SENS:VOLT:INP AUTO")  # auto impedance
            self.meter.enable_filter("volt", "repeat", 10)
        elif function == "source":
            self.meter.autozero_enabled = True
        else:
            raise ValueError("function should be either source or sense")

    def info_sync(self):
        """
        no parameters to sync for 2182
        """
        self.info_dict.update(
            {
                "auto_range": self.meter.auto_range_status(),
                "sense_type": self.meter.mode,
                "auto_zero": self.meter.autozero_enabled,
                "terminal": self.meter.terminals_used,
            }
        )

    def sense(
        self,
        type_str: Literal["volt", "curr", "freq"] = "volt",
        max_val: Optional[float | str] = None,
        ac_dc: Literal["ac", "dc"] = "dc",
    ) -> float:
        """
        sense the voltage or current or frequency

        Args:
            type_str: "volt" or "curr" or "freq"
            max_val: the manual range for the measurement (anticipated maximum)
            ac_dc: "ac" or "dc"
        """
        if max_val is not None:
            max_val = convert_unit(max_val, "")[0]
        match type_str:
            case "volt":
                self.meter.measure_voltage(
                    max_voltage=(max_val if max_val is not None else 1),
                    ac=(ac_dc == "ac"),
                )
                self.meter.auto_range()
                return self.meter.voltage
            case "curr":
                self.meter.measure_current(
                    max_current=(max_val if max_val is not None else 1e-2),
                    ac=(ac_dc == "ac"),
                )
                self.meter.auto_range()
                return self.meter.current
            case "freq":
                self.meter.measure_frequency()
                self.meter.auto_range()
                return self.meter.frequency


class WrapperSR830(ACSourceMeter):
    def __init__(self, GPIB: str = "GPIB0::8::INSTR", reset=True):
        super().__init__()
        self.meter = SR830(GPIB)
        self.output_target = 0
        self.info_dict = {"GPIB": GPIB}
        self.safe_step = 2e-3
        self.if_source = False  # if the meter has been declared as source (as source initialization is earlier)
        if reset:
            self.setup(reset=True)
        self.info_sync()

    def info_sync(self):
        self.info_dict.update(
            {
                "sensitivity": self.meter.sensitivity,
                "ref_source_trigger": self.meter.reference_source_trigger,
                "reference_source": self.meter.reference_source,
                "harmonic": self.meter.harmonic,
                "output_value": self.meter.sine_voltage,
                "output_status": self.meter.sine_voltage > 0.004,
                "frequency": self.meter.frequency,
                "filter_slope": self.meter.filter_slope,
                "time_constant": self.meter.time_constant,
                "input_config": self.meter.input_config,
                "input_coupling": self.meter.input_coupling,
                "input_grounding": self.meter.input_grounding,
                "input_notch_config": self.meter.input_notch_config,
                "reserve": self.meter.reserve,
                "filter_synchronous": self.meter.filter_synchronous,
            }
        )

    def setup(
        self,
        function: Literal["source", "sense"] = "sense",
        *,
        filter_slope=None,
        time_constant=None,
        input_config=None,
        input_coupling=None,
        input_grounding=None,
        sine_voltage=None,
        input_notch_config=None,
        reserve=None,
        filter_synchronous=None,
        reset: bool = False,
    ) -> None:
        """
        setup the SR830 instruments using pre-stored setups here, this function will not fully reset the instruments,
        only overwrite the specific settings here, other settings will all be reserved
        """
        if reset:
            self.meter.filter_slope = (24,)
            self.meter.time_constant = (0.3,)
            self.meter.input_config = ("A - B",)
            self.meter.input_coupling = ("AC",)
            self.meter.input_grounding = ("Float",)
            self.meter.sine_voltage = (0,)
            self.meter.input_notch_config = ("None",)
            self.meter.reserve = ("Normal",)
            self.meter.filter_synchronous = (False,)
            return
        if function == "sense":
            if filter_slope is not None:
                self.meter.filter_slope = filter_slope
            if time_constant is not None:
                self.meter.time_constant = time_constant
            if input_config is not None:
                self.meter.input_config = input_config
            if input_coupling is not None:
                self.meter.input_coupling = input_coupling
            if input_grounding is not None:
                self.meter.input_grounding = input_grounding
            if input_notch_config is not None:
                self.meter.input_notch_config = input_notch_config
            if reserve is not None:
                self.meter.reserve = reserve
            if filter_synchronous is not None:
                self.meter.filter_synchronous = filter_synchronous

            if not self.if_source:
                self.meter.reference_source = "External"
            else:
                self.if_source = False  # restore the if_source to False for the next initialization, would cause unexpected behavior if called twice in one measurement
            self.info_sync()

        elif function == "source":
            if sine_voltage is not None:
                self.meter.sine_voltage = sine_voltage
            self.meter.reference_source = "Internal"
            self.if_source = True
            self.info_sync()
        else:
            raise ValueError("function should be either source or sense")

    def reference_set(
        self,
        *,
        freq: Optional[float | str] = None,
        source: Optional[Literal["Internal", "External"]] = None,
        trigger: Optional[Literal["SINE", "POS EDGE", "NEG EDGE"]] = None,
        harmonic: Optional[int] = None,
    ):
        """
        set the reference frequency and source
        """
        if freq is not None:
            self.meter.frequency = convert_unit(freq, "Hz")[0]
        if source is not None:
            self.meter.reference_source = source
        if trigger is not None:
            self.meter.reference_source_trigger = trigger
        if harmonic is not None:
            self.meter.harmonic = harmonic
        self.info_sync()

    def sense(self, type_str: Literal["volt", "curr"] = "volt") -> list:
        return self.meter.snap("X", "Y", "R", "THETA")

    def get_output_status(self) -> tuple[float, float]:
        """
        return the output value from device and also the target value set by output methods

        Returns:
            tuple[float, float]: the output value and the target value
        """
        return self.meter.sine_voltage, self.output_target

    def output_switch(self, switch: bool | Literal["on", "off", "ON", "OFF"]):
        switch = SWITCH_DICT.get(switch, False) if isinstance(switch, str) else switch
        if switch:
            # no actual switch of SR830
            self.info_dict["output_status"] = True
        else:
            self.meter.sine_voltage = 0
            self.info_dict["output_status"] = False

    def uni_output(
        self,
        value: float | str,
        *,
        freq: Optional[float | str] = None,
        compliance: Optional[float | str] = None,
        type_str: Literal["volt"] = "volt",
        fix_range: Optional[float | str] = None,
    ) -> float:
        """fix_range is not used for sr830"""
        if value > 5:
            logger.warning("exceed SR830 max output")
        self.rms_output(value, freq=freq, compliance=compliance, type_str=type_str)
        self.output_target = convert_unit(value, "V")[0]
        return self.get_output_status()[0]

    def rms_output(
        self,
        value: float | str,
        *,
        freq: Optional[float | str] = None,
        compliance: Optional[float | str] = None,
        type_str: Literal["volt"] = "volt",
    ):
        assert type_str == "volt", (
            "SR830 is a voltage source, so the output is always voltage"
        )
        value = convert_unit(value, "V")[0]
        self.meter.sine_voltage = value
        self.info_dict["output_value"] = value
        self.info_dict["output_status"] = True
        if freq is not None and freq != self.info_dict["frequency"]:
            self.meter.frequency = convert_unit(freq, "Hz")[0]
            self.info_dict["frequency"] = freq

    def shutdown(self):
        if self.info_dict["output_status"]:
            self.output_switch("off")


class WrapperSR860(ACSourceMeter):
    def __init__(self, GPIB: str = "GPIB0::8::INSTR", reset=True):
        super().__init__()
        self.meter = SR860(GPIB)
        self.output_target = 0
        self.info_dict = {"GPIB": GPIB}
        self.safe_step = 2e-3
        self.if_source = False  # if the meter has been declared as source (as source initialization is earlier)
        if reset:
            self.setup(reset=True)
        self.info_sync()

    def info_sync(self):
        self.info_dict.update(
            {
                "sensitivity": self.meter.sensitivity,
                "ref_source_trigger": self.meter.reference_source_trigger,
                "reference_source": self.meter.reference_source,
                "harmonic": self.meter.harmonic,
                "output_value": self.meter.sine_voltage,
                "output_status": self.meter.sine_voltage > 0.004,
                "frequency": self.meter.frequency,
                "filter_slope": self.meter.filter_slope,
                "time_constant": self.meter.time_constant,
                "input_config": self.meter.input_config,
                "input_coupling": self.meter.input_coupling,
                "input_grounding": self.meter.input_shields,
                "filter_synchronous": self.meter.filter_synchronous,
            }
        )

    def setup(
        self,
        function: Literal["source", "sense"] = "sense",
        *,
        filter_slope=None,
        time_constant=None,
        input_config=None,
        input_coupling=None,
        input_grounding=None,
        sine_voltage=None,
        filter_synchronous=None,
        reset: bool = False,
    ) -> None:
        """
        setup the SR830 instruments using pre-stored setups here, this function will not fully reset the instruments,
        only overwrite the specific settings here, other settings will all be reserved
        """
        if reset:
            self.meter.filter_slope = 3
            self.meter.time_constant = 0.3
            self.meter.input_config = "A-B"
            self.meter.input_coupling = "AC"
            self.meter.input_grounding = "Float"
            self.meter.sine_voltage = 0
            self.meter.filter_synchronous = False
            return
        if function == "sense":
            if filter_slope is not None:
                self.meter.filter_slope = filter_slope
            if time_constant is not None:
                self.meter.time_constant = time_constant
            if input_config is not None:
                self.meter.input_config = input_config
            if input_coupling is not None:
                self.meter.input_coupling = input_coupling
            if input_grounding is not None:
                self.meter.input_shields = input_grounding
            if filter_synchronous is not None:
                self.meter.filter_synchronous = filter_synchronous
            if not self.if_source:
                self.meter.reference_source = "EXT"
            else:
                self.if_source = False  # restore the if_source to False for the next initialization, would cause unexpected behavior if called twice in one measurement
            self.info_sync()
        elif function == "source":
            if sine_voltage is not None:
                self.meter.sine_voltage = sine_voltage
            self.meter.reference_source = "INT"
            self.if_source = True
            self.info_sync()
        else:
            raise ValueError("function should be either source or sense")

    def reference_set(
        self,
        *,
        freq: Optional[float | str] = None,
        source: Optional[Literal["Internal", "External"]] = None,
        trigger: Optional[Literal["SINE", "POS EDGE", "NEG EDGE"]] = None,
        harmonic: Optional[int] = None,
    ):
        """
        set the reference frequency and source
        """
        if freq is not None:
            self.meter.frequency = convert_unit(freq, "Hz")[0]
        if source is not None:
            self.meter.reference_source = source
        if trigger is not None:
            self.meter.reference_source_trigger = trigger
        if harmonic is not None:
            self.meter.harmonic = harmonic
        self.info_sync()

    def sense(
        self, type_str: Literal["volt", "curr"] = "volt"
    ) -> tuple[float, float, float, float]:
        """snap X Y and THETA from the meter and calculate the R, for compatibility with the SR830"""
        x, y, r, theta = self.meter.snap_all()
        return x, y, r, theta

    def get_output_status(self) -> tuple[float, float]:
        """
        return the output value from device and also the target value set by output methods

        Returns:
            tuple[float, float]: the output value and the target value
        """
        return self.meter.sine_voltage, self.output_target

    def output_switch(self, switch: bool | Literal["on", "off", "ON", "OFF"]):
        switch = SWITCH_DICT.get(switch, False) if isinstance(switch, str) else switch
        if switch:
            # no actual switch of SR830
            self.info_dict["output_status"] = True
        else:
            self.meter.sine_voltage = 0
            self.info_dict["output_status"] = False

    def uni_output(
        self,
        value: float | str,
        *,
        freq: Optional[float | str] = None,
        compliance: Optional[float | str] = None,
        type_str: Literal["volt"] = "volt",
        fix_range: Optional[float | str] = None,
    ) -> float:
        """fix_range is not used for sr830"""
        if value > 2:
            logger.warning("exceed SR860 max output")
        self.rms_output(value, freq=freq, compliance=compliance, type_str=type_str)
        self.output_target = convert_unit(value, "V")[0]
        return self.get_output_status()[0]

    def rms_output(
        self,
        value: float | str,
        *,
        freq: Optional[float | str] = None,
        compliance: Optional[float | str] = None,
        type_str: Literal["volt"] = "volt",
    ):
        assert type_str == "volt", (
            "SR830 is a voltage source, so the output is always voltage"
        )
        value = convert_unit(value, "V")[0]
        self.meter.sine_voltage = value
        self.info_dict["output_value"] = value
        self.info_dict["output_status"] = True
        if freq is not None and freq != self.info_dict["frequency"]:
            self.meter.frequency = convert_unit(freq, "Hz")[0]
            self.info_dict["frequency"] = freq

    def shutdown(self):
        if self.info_dict["output_status"]:
            self.output_switch("off")


class Wrapper6430(DCSourceMeter):
    def __init__(self, GPIB: str = "GPIB0::26::INSTR"):
        super().__init__()
        self.meter: Keithley_6430
        self.meter = Keithley_6430("Keithley6430", GPIB)
        self.info_dict = {}
        self.output_target = 0
        self.safe_step = {"volt": 2e-1, "curr": 5e-6}
        self.info_sync()

    def info_sync(self):
        self.info_dict.update(
            {
                "output_status": self.meter.output_enabled(),
                "output_type": self.meter.source_mode()
                .lower()
                .replace("current", "curr")
                .replace("voltage", "volt"),
                "curr_compliance": self.meter.source_current_compliance(),
                "volt_compliance": self.meter.source_voltage_compliance(),
                "source_curr_range": self.meter.source_current_range(),
                "source_volt_range": self.meter.source_voltage_range(),
                "source_delay": self.meter.source_delay(),
                "sense_type": self.meter.sense_mode().lower(),
                "sense_auto_range": self.meter.sense_autorange(),
                "sense_curr_range": self.meter.sense_current_range(),
                "sense_volt_range": self.meter.sense_voltage_range(),
                "sense_resist_range": self.meter.sense_resistance_range(),
                "sense_resist_offset_comp": self.meter.sense_resistance_offset_comp_enabled(),
                "autozero": self.meter.autozero(),
            }
        )

    def setup(
        self,
        function: Literal["sense", "source"] = "sense",
        *,
        auto_zero: str = "on",
        reset: bool = False,
    ):
        if function == "source":
            if reset:
                self.meter.reset()
                self.meter.output_enabled(False)
            self.meter.autozero(auto_zero)
        elif function == "sense":
            if reset:
                self.meter.reset()
                self.meter.sense_autorange(True)
            self.meter.autozero(auto_zero)
        else:
            raise ValueError("function should be either source or sense")
        self.info_sync()

    def sense(self, type_str: Literal["curr", "volt", "resist"]) -> float:
        if self.info_dict["output_status"] == False:
            self.output_switch("on")

        if type_str == "curr":
            self.meter.sense_mode("CURR:DC")
            return self.meter.sense_current()
        elif type_str == "volt":
            self.meter.sense_mode("VOLT:DC")
            return self.meter.sense_voltage()
        elif type_str == "resist":
            self.meter.sense_mode("RES")
            return self.meter.sense_resistance()

    def output_switch(self, switch: bool | Literal["on", "off", "ON", "OFF"]):
        switch = SWITCH_DICT.get(switch, False) if isinstance(switch, str) else switch
        if not switch:
            self.uni_output(0, type_str=self.info_dict["output_type"])
        self.meter.output_enabled(switch)
        self.info_dict["output_status"] = switch

    def get_output_status(self) -> tuple[float, float, float]:
        """
        return the output value from device and also the target value set by output methods

        Returns:
            tuple[float, float]: the output value and the target value
        """
        if self.meter.source_mode().lower() == "curr":
            return (
                self.meter.source_current(),
                self.output_target,
                self.meter.source_current_range(),
            )
        elif self.meter.source_mode().lower() == "volt":
            return (
                self.meter.source_voltage(),
                self.output_target,
                self.meter.source_voltage_range(),
            )

    def uni_output(
        self,
        value: float | str,
        *,
        freq=None,
        fix_range: Optional[float | str] = None,
        compliance: Optional[float | str] = None,
        type_str: Literal["curr", "volt"],
    ) -> float:
        self.dc_output(
            value, compliance=compliance, type_str=type_str, fix_range=fix_range
        )
        self.output_target = convert_unit(value, "")[0]
        return self.get_output_status()[0]

    def dc_output(
        self,
        value: float | str,
        *,
        compliance: Optional[float | str] = None,
        fix_range: Optional[float | str] = None,
        type_str: Literal["curr", "volt"],
    ):
        value = convert_unit(value, "")[0]
        # add shortcut for zero output (no need to care about output type, just set current output to 0)
        if value == 0:
            if self.info_dict["output_type"] == "curr":
                self.meter.source_current(0)
            elif self.info_dict["output_type"] == "volt":
                self.meter.source_voltage(0)
            self.output_switch("on")
            return
        # close and reopen the source meter to avoid error when switching source type
        if self.info_dict["output_type"] != type_str:
            self.output_switch("off")
            self.meter.source_mode(type_str.upper())

        if type_str == "curr":
            if fix_range is not None:
                self.meter.source_current_range(convert_unit(fix_range, "A")[0])
            else:
                if (
                    abs(value) <= self.meter.source_current_range() / 100
                    or abs(value) >= self.meter.source_current_range()
                ):
                    new_range = abs(value) if abs(value) > 1e-12 else 1e-12
                    self.meter.source_current_range(new_range)
            if compliance is None:
                if (
                    abs(value * 100000) < 1e-3
                ):  # this limit is only for 2400 (compliancev > 1E-3)
                    compliance = 1e-3
                else:
                    compliance = abs(value * 100000)
            if compliance != self.meter.source_voltage_compliance():
                self.meter.sense_voltage_range(convert_unit(compliance, "V")[0])
                self.meter.sense_autorange(True)
                self.meter.source_voltage_compliance(convert_unit(compliance, "V")[0])
            self.meter.source_current(value)

        elif type_str == "volt":
            if fix_range is not None:
                self.meter.source_voltage_range(convert_unit(fix_range, "V")[0])
            else:
                if (
                    abs(value) <= self.meter.source_voltage_range() / 100
                    or abs(value) >= self.meter.source_voltage_range()
                ):
                    new_range = abs(value) if abs(value) > 0.2 else 0.2
                    self.meter.source_voltage_range(new_range)
            if compliance is None:
                if abs(value / 1000) < 1e-6:
                    compliance = 1e-6
                else:
                    compliance = abs(value / 1000)
            if compliance != self.meter.source_current_compliance():
                self.meter.sense_current_range(convert_unit(compliance, "A")[0])
                self.meter.sense_autorange(True)
                self.meter.source_current_compliance(convert_unit(compliance, "A")[0])
            self.meter.source_voltage(value)

        self.info_dict["output_type"] = type_str
        self.output_switch("on")

    def shutdown(self):
        self.output_switch("off")


class WrapperB2902Bchannel(DCSourceMeter):
    def __init__(self, GPIB: str = "GPIB0::25::INSTR", channel: int | str = 1):
        super().__init__()
        self.meter_all = find_or_create_instrument(
            Keysight_B2902B, "KeysightB2902B", address=GPIB
        )
        self.meter: KeysightB2902BChannel
        self.meter = self.meter_all.ch1 if int(channel) == 1 else self.meter_all.ch2
        self.info_dict = {}
        self.output_target = 0
        self.safe_step = {"volt": 1e-2, "curr": 2e-6}
        self.info_sync()

    def info_sync(self):
        self.info_dict.update(
            {
                "output_status": self.meter.output(),
                "output_type": self.meter.source_mode()
                .lower()
                .replace("current", "curr")
                .replace("voltage", "volt"),
                "curr_compliance": self.meter.source_current_compliance(),
                "volt_compliance": self.meter.source_voltage_compliance(),
                "source_curr_range": self.meter.source_current_range(),
                "source_volt_range": self.meter.source_voltage_range(),
                "sense_curr_autorange": self.meter.sense_current_autorange(),
                "sense_volt_autorange": self.meter.sense_voltage_autorange(),
                "sense_resist_autorange": self.meter.sense_resistance_autorange(),
                "sense_curr_range": self.meter.sense_current_range(),
                "sense_volt_range": self.meter.sense_voltage_range(),
                "sense_resist_range": self.meter.sense_resistance_range(),
            }
        )

    def setup(
        self, function: Literal["sense", "source"] = "sense", reset: bool = False
    ):
        if reset:
            self.meter_all.reset()
        if function == "sense":
            if reset:
                self.meter.sense_current_autorange(True)
                self.meter.sense_voltage_autorange(True)
                self.meter.sense_resistance_autorange(True)
        elif function == "source":
            if reset:
                self.meter.output(False)
                self.meter.source_current_autorange(True)
                self.meter.source_voltage_autorange(True)
        self.info_sync()

    def sense(self, type_str: Literal["curr", "volt", "resist"]) -> float:
        # if self.info_dict["output_status"] is False:
        #    self.output_switch("on")

        if type_str == "curr":
            return self.meter.sense_current()
        elif type_str == "volt":
            return self.meter.sense_voltage()
        elif type_str == "resist":
            return self.meter.sense_resistance()

    def output_switch(self, switch: bool | Literal["on", "off", "ON", "OFF"]):
        switch = SWITCH_DICT.get(switch, False) if isinstance(switch, str) else switch
        if not switch:
            self.uni_output(0, type_str=self.info_dict["output_type"])
        self.meter.output(switch)
        self.info_dict["output_status"] = switch

    def get_output_status(self) -> tuple[float, float, float]:
        """
        return the output value from device and also the target value set by output methods

        Returns:
            tuple[float, float]: the output value and the target value
        """
        if self.meter.source_mode().lower() == "curr":
            return (
                self.meter.source_current(),
                self.output_target,
                self.meter.source_current_range(),
            )
        elif self.meter.source_mode().lower() == "volt":
            return (
                self.meter.source_voltage(),
                self.output_target,
                self.meter.source_voltage_range(),
            )

    def uni_output(
        self,
        value: float | str,
        *,
        freq=None,
        fix_range: Optional[float | str] = None,
        compliance: Optional[float | str] = None,
        type_str: Literal["curr", "volt"],
    ) -> float:
        self.dc_output(
            value, compliance=compliance, type_str=type_str, fix_range=fix_range
        )
        self.output_target = convert_unit(value, "")[0]
        return self.get_output_status()[0]

    def dc_output(
        self,
        value: float | str,
        *,
        compliance: Optional[float | str] = None,
        fix_range: Optional[float | str] = None,
        type_str: Literal["curr", "volt"],
    ):
        value = convert_unit(value, "")[0]
        # add shortcut for zero output (no need to care about output type, just set current output to 0)
        if value == 0:
            if self.info_dict["output_type"] == "curr":
                self.meter.source_current(0)
            elif self.info_dict["output_type"] == "volt":
                self.meter.source_voltage(0)
            self.output_switch("on")
            return
        # close and reopen the source meter to avoid error when switching source type
        if self.info_dict["output_type"] != type_str:
            self.output_switch("off")
            self.meter.source_mode(type_str.upper())

        if type_str == "curr":
            if fix_range is not None:
                self.meter.source_current_range(convert_unit(fix_range, "A")[0])
            else:
                if (
                    abs(value) <= self.meter.source_current_range() / 100
                    or abs(value) >= self.meter.source_current_range()
                ):
                    new_range = abs(value) if abs(value) > 1e-12 else 1e-12
                    self.meter.source_current_range(new_range)
            if compliance is None:
                if (
                    abs(value * 100000) < 1e-3
                ):  # this limit is only for 2400 (compliancev > 1E-3)
                    compliance = 1e-3
                else:
                    compliance = abs(value * 100000)
            if compliance != self.meter.source_voltage_compliance():
                self.meter.sense_voltage_range(convert_unit(compliance, "V")[0])
                self.meter.sense_voltage_autorange(True)
                self.meter.source_voltage_compliance(convert_unit(compliance, "V")[0])
            self.meter.source_current(value)

        elif type_str == "volt":
            if fix_range is not None:
                self.meter.source_voltage_range(convert_unit(fix_range, "V")[0])
            else:
                if (
                    abs(value) <= self.meter.source_voltage_range() / 100
                    or abs(value) >= self.meter.source_voltage_range()
                ):
                    new_range = abs(value) if abs(value) > 0.2 else 0.2
                    self.meter.source_voltage_range(new_range)
            if compliance is None:
                if abs(value / 1000) < 1e-6:
                    compliance = 1e-6
                else:
                    compliance = abs(value / 1000)
            if compliance != self.meter.source_current_compliance():
                self.meter.sense_current_range(convert_unit(compliance, "A")[0])
                self.meter.sense_current_autorange(True)
                self.meter.source_current_compliance(convert_unit(compliance, "A")[0])
            self.meter.source_voltage(value)

        self.info_dict["output_type"] = type_str
        self.output_switch("on")

    def shutdown(self):
        self.output_switch("off")


class Wrapper2400(DCSourceMeter):
    def __init__(self, GPIB: str = "GPIB0::24::INSTR"):
        super().__init__()
        self.meter = Keithley2400("Keithley2401", GPIB)
        self.info_dict = {}
        self.output_target = 0
        self.safe_step = {"volt": 1e-2, "curr": 2e-6}
        self.info_sync()

    def info_sync(self):
        self.info_dict.update(
            {
                "output_status": self.meter.output(),
                "output_type": self.meter.mode()
                .lower()
                .replace("current", "curr")
                .replace("voltage", "volt"),
                "curr_compliance": self.meter.compliancei(),
                "volt_compliance": self.meter.compliancev(),
                "source_curr_range": self.meter.rangei(),
                "source_volt_range": self.meter.rangev(),
                "sense_curr_range": self.meter.rangei(),
                "sense_volt_range": self.meter.rangev(),
                "sense_type": self.meter.sense().lower(),
            }
        )

    def setup(
        self, function: Literal["sense", "source"] = "sense", reset: bool = False
    ):
        self.meter.write("*CLS")
        self.meter.write(":TRAC:FEED:CONT NEV")  # disables data buffer
        self.meter.write(":RES:MODE MAN")  # disables auto resistance
        if reset:  # reset will also reset the GPIB
            self.meter.write("*RST")
        self.info_sync()

    def sense(self, type_str: Literal["curr", "volt", "resist"]) -> float:
        if type_str == "curr":
            if self.info_dict["output_type"] == "curr":
                logger.info("in curr mode, print the set point")
            return self.meter.curr()
        elif type_str == "volt":
            if self.info_dict["output_type"] == "volt":
                logger.info("in curr mode, print the set point")
            return self.meter.volt()
        elif type_str == "resist":
            return self.meter.resistance()

    def get_output_status(self) -> tuple[float, float, float]:
        """
        return the output value from device and also the target value set by output methods

        Returns:
            tuple[float, float, float]: the output value, target value and range
        """
        if self.meter.mode().lower() == "curr":
            if self.info_dict["output_status"] == False:
                return 0, self.output_target, self.meter.rangei()
            return self.meter.curr(), self.output_target, self.meter.rangei()
        elif self.meter.mode().lower() == "volt":
            if self.info_dict["output_status"] == False:
                return 0, self.output_target, self.meter.rangev()
            return self.meter.volt(), self.output_target, self.meter.rangev()

    def output_switch(self, switch: bool | Literal["on", "off", "ON", "OFF"]):
        switch = SWITCH_DICT.get(switch, False) if isinstance(switch, str) else switch
        if not switch:
            self.uni_output(0, type_str=self.info_dict["output_type"])
        self.meter.output(switch)
        self.info_dict["output_status"] = switch

    def uni_output(
        self,
        value: float | str,
        *,
        freq=None,
        fix_range: Optional[float | str] = None,
        compliance: Optional[float | str] = None,
        type_str: Literal["curr", "volt"],
    ) -> float:
        self.dc_output(
            value, compliance=compliance, type_str=type_str, fix_range=fix_range
        )
        self.output_target = convert_unit(value, "")[0]
        return self.get_output_status()[0]

    def dc_output(
        self,
        value: float | str,
        *,
        fix_range: Optional[float | str] = None,
        compliance: Optional[float | str] = None,
        type_str: Literal["curr", "volt"],
    ):
        value = convert_unit(value, "")[0]
        # add shortcut for zero output (no need to care about output type, just set current output to 0)
        if value == 0:
            if self.info_dict["output_type"] == "curr":
                self.meter.curr(0)
            elif self.info_dict["output_type"] == "volt":
                self.meter.volt(0)
            self.output_switch("on")
            return
        # close and reopen the source meter to avoid error when switching source type
        if self.info_dict["output_type"] != type_str:
            self.output_switch("off")
            self.meter.mode(type_str.upper())

        if type_str == "curr":
            if fix_range is not None:
                self.meter.rangei(convert_unit(fix_range, "A")[0])
            else:
                if (
                    abs(value) <= self.meter.rangei() / 100
                    or abs(value) >= self.meter.rangei()
                ):
                    new_range = value if abs(value) > 1e-6 else 1e-6
                    self.meter.rangei(new_range)
            if compliance is None:
                if (
                    abs(value * 1000) < 1e-3
                ):  # this limit is only for 2400 (compliancev > 1E-3)
                    compliance = 1e-3
                else:
                    compliance = abs(value * 100000)
            if compliance != self.meter.compliancev():
                self.meter.compliancev(convert_unit(compliance, "V")[0])
            self.meter.curr(value)

        elif type_str == "volt":
            if fix_range is not None:
                self.meter.rangev(convert_unit(fix_range, "V")[0])
            else:
                if (
                    abs(value) <= self.meter.rangev() / 100
                    or abs(value) >= self.meter.rangev()
                ):
                    new_range = value if abs(value) > 0.2 else 0.2
                    self.meter.rangev(new_range)
            if compliance is None:
                if abs(value / 1000) < 1e-6:
                    compliance = 1e-6
                else:
                    compliance = abs(value / 1000)
            self.meter.compliancei(convert_unit(compliance, "A")[0])
            self.meter.volt(value)

        self.info_dict["output_type"] = type_str
        self.output_switch("on")

    def shutdown(self):
        self.meter.curr(0)
        self.meter.volt(0)
        self.output_switch("off")


class Wrapper2450(DCSourceMeter):
    ##TODO: not tested yet
    def __init__(self, GPIB: str = "GPIB0::18::INSTR"):
        super().__init__()
        try:
            self.meter = Keithley2450("Keithley2450", GPIB)
        except:
            self.meter = Keithley2450("Keithley2450_2", GPIB)
        self.info_dict = {}
        self.output_target = 0
        self.safe_step = {"volt": 1e-2, "curr": 2e-6}
        self.info_sync()

    def info_sync(self):
        self.info_dict.update(
            {
                "output_status": self.meter.output_enabled(),
                "output_type": self.meter.source_function()
                .lower()
                .replace("current", "curr")
                .replace("voltage", "volt"),
                "compliance": self.meter.source.limit(),
                "source_range": self.meter.source.range(),
                "sense_range": self.meter.sense.range(),
                "sense_type": self.meter.sense_function()
                .lower()
                .replace("current", "curr")
                .replace("voltage", "volt")
                .replace("resistance", "resist"),
                "sense_autozero": self.meter.sense.auto_zero_enabled(),
            }
        )

    def setup(
        self, function: Literal["sense", "source"] = "sense", *, reset: bool = False
    ):
        if reset:
            self.meter.reset()
            self.meter.sense.auto_range(True)
            self.meter.terminals("front")
        if function == "source":
            if reset:
                self.meter.source.auto_range(True)
        self.info_sync()

    def sense(self, type_str: Literal["curr", "volt", "resist"]) -> float:
        if self.info_dict["sense_type"] == type_str:
            pass
        else:
            self.meter.sense.function(
                type_str.replace("curr", "current")
                .replace("volt", "voltage")
                .replace("resist", "resistance")
            )
            self.info_dict["sense_type"] = type_str
        return self.meter.sense._measure()

    def get_output_status(self) -> tuple[float, float, float]:
        """
        return the output value from device and also the target value set by output methods

        Returns:
            tuple[float, float, float]: the real output value, target value and range
        """
        if not self.info_dict["output_status"]:
            return 0, self.output_target, self.meter.source.range()
        if self.meter.source.function() == "current":
            return self.sense("curr"), self.output_target, self.meter.source.range()
        elif self.meter.source.function() == "voltage":
            return self.sense("volt"), self.output_target, self.meter.source.range()

    def output_switch(self, switch: bool | Literal["on", "off", "ON", "OFF"]):
        switch = SWITCH_DICT.get(switch, False) if isinstance(switch, str) else switch
        if self.info_dict["output_status"] == switch:
            return
        if not switch:
            self.uni_output(0, type_str=self.info_dict["output_type"])
        self.meter.output_enabled(switch)
        self.info_dict["output_status"] = switch

    def uni_output(
        self,
        value: float | str,
        *,
        freq=None,
        fix_range: Optional[float | str] = None,
        compliance: float | str = None,
        type_str: Literal["curr", "volt"],
    ) -> float:
        self.dc_output(
            value, compliance=compliance, type_str=type_str, fix_range=fix_range
        )
        self.output_target = convert_unit(value, "")[0]
        return self.get_output_status()[0]

    def dc_output(
        self,
        value: float | str,
        *,
        fix_range: Optional[float | str] = None,
        compliance: Optional[float | str] = None,
        type_str: Literal["curr", "volt"],
    ):
        value = convert_unit(value, "")[0]
        # add shortcut for zero output (no need to care about output type, just set current output to 0)
        if value == 0:
            if self.info_dict["output_type"] == "curr":
                self.meter.source.current(0)
            elif self.info_dict["output_type"] == "volt":
                self.meter.source.voltage(0)
            # open the output to avoid error when sensing
            self.output_switch("on")  # careful about inf loop
            return
        # close and reopen the source meter to avoid error when switching source type
        if self.info_dict["output_type"] != type_str:
            self.output_switch("off")
            self.meter.source.function(
                type_str.replace("curr", "current").replace("volt", "voltage")
            )

        range_limit_dict = {"curr": 1e-8, "volt": 0.02}
        if fix_range is not None:
            self.meter.source.range(convert_unit(fix_range, "")[0])
        else:
            if (
                abs(value) <= self.meter.source.range() / 100
                or abs(value) >= self.meter.source.range()
            ):
                new_range = (
                    value
                    if abs(value) > range_limit_dict[type_str]
                    else range_limit_dict[type_str]
                )
                self.meter.source.range(new_range)

        if type_str == "curr":
            if compliance is None:
                compliance = (
                    abs(value * 100000) if abs(value * 100000) >= 0.02 else 0.02
                )
            if compliance != self.meter.source.limit():
                self.meter.source.limit(convert_unit(compliance, "V")[0])
            self.meter.source.current(value)

        elif type_str == "volt":
            if compliance is None:
                compliance = abs(value / 1000) if abs(value / 1000) >= 1e-8 else 1e-8
            if compliance != self.meter.source.limit():
                self.meter.source.limit(convert_unit(compliance, "A")[0])
            self.meter.source.voltage(value)

        self.info_dict["output_type"] = type_str
        self.output_switch("on")

    def shutdown(self):
        if self.info_dict["output_type"] == "curr":
            self.meter.source.current(0)
        elif self.info_dict["output_type"] == "volt":
            self.meter.source.voltage(0)
        self.output_switch("off")


"""
Wrappers for magnets are following
"""


class Magnet(ABC):
    @abstractmethod
    def __init__(self, address: str):
        pass

    @property
    @abstractmethod
    def field(self) -> float | tuple[float]:
        pass

    @property
    @abstractmethod
    def field_set(self):
        pass

    @field_set.setter
    @abstractmethod
    def field_set(self, field: float | tuple[float]):
        pass

    @abstractmethod
    def ramp_to_field(
        self, field: float, *, rate: float, stability: float, check_interval: float
    ):
        pass

    def if_reach_target(self, tolerance: float = 3e-3):
        """
        check if the magnet has reached the target field

        Args:
            tolerance (float): the tolerance of the field (T)
        """
        return abs(self.field - self.field_set) < tolerance


class WrapperIPS(Magnet):
    """
    Wrapper for MercuryIPS (only z axis magnetic field is considered)
    """

    def __init__(
        self,
        address: str = "TCPIP0::10.97.24.237::7020::SOCKET",
        if_print: bool = False,
        limit_sphere: float = 11,
    ) -> None:
        """
        load Mercury iPS instrument according to the address, store it in self.instrs["ips"]

        Args:
            address (str): the address of the instrument
            if_print (bool): whether to print the snapshot of the instrument
            limit_sphere (float): the limit of the field
        """
        self.ips = OxfordMercuryiPS("mips", address)
        if if_print:
            self.ips.print_readable_snapshot(update=True)

        def spherical_limit(x, y, z) -> bool:
            return np.sqrt(x**2 + y**2 + z**2) <= limit_sphere

        self.ips.set_new_field_limits(spherical_limit)

    @property
    def field(self) -> float | tuple[float]:
        """
        return the current field of the magnet (only z direction considered)
        """
        return self.ips.z_measured()

    @property
    def field_set(self) -> float | tuple[float]:
        """
        set the target field (only z direction considered)
        """
        return self.ips.z_target()

    @field_set.setter
    def field_set(self, field: float | tuple[float]) -> None:
        """
        set the target field (only z direction considered)
        """
        assert isinstance(field, (float, int, tuple, list)), (
            "The field should be a float or a tuple of 3 floats"
        )
        fieldz_target = field if isinstance(field, (float, int)) else field[2]
        self.ips.z_target(fieldz_target)

    def sw_heater(
        self, switch: Optional[bool | Literal["on", "off", "ON", "OFF"]] = None
    ) -> Optional[bool]:
        """
        switch the heater of the magnet
        """
        if switch is not None:
            switch = (
                SWITCH_DICT.get(switch, False) if isinstance(switch, str) else switch
            )
            if switch:
                self.ips.GRPZ.sw_heater("ON")
            else:
                self.ips.GRPZ.sw_heater("OFF")
            logger.info("Heater switched %s", "on" if switch else "off")
        else:
            match self.ips.GRPZ.sw_heater():
                case "ON" | "on" | True:
                    return True
                case "OFF" | "off" | False:
                    return False
                case _:
                    raise ValueError("The heater status is not recognized")

    # =======suitable for Z-axis only ips========
    @property
    def status(self) -> Literal["HOLD", "TO SET", "CLAMP", "TO ZERO"]:
        """
        return the status of the magnet
        """
        return self.ips.GRPZ.ramp_status()

    @status.setter
    def status(self, status: Literal["HOLD", "TO SET", "CLAMP", "TO ZERO"]) -> None:
        """
        set the status of the magnet
        """
        assert status in ["HOLD", "TO SET", "CLAMP", "TO ZERO"], (
            "The status is not recognized"
        )
        self.ips.GRPZ.ramp_status(status)

    def ramp_to_field(
        self,
        field: float | int | tuple[float] | list[float],
        *,
        rate: float | tuple[float] = (0.2,) * 3,
        wait: bool = True,
        tolerance: float = 1e-3,
    ) -> None:
        """
        ramp the magnetic field to the target value with the rate, current the field is only in Z direction limited by the actual instrument setting
        (currently only B_z can be ramped)

        Args:
            field (tuple[float]): the target field coor
            rate (float): the rate of the field change (T/min)
            wait (bool): whether to wait for the ramping to finish
            tolerance (float): the tolerance of the field (T)
        """
        if not self.sw_heater() and field != 0:
            self.sw_heater("on")
            for i in range(310):
                print_progress_bar(i, 310, prefix="waiting for heater")
                time.sleep(1)
        else:
            pass

        if abs(self.field - field) < tolerance:
            return
        if isinstance(rate, (float, int)):
            assert rate <= 0.2, "The rate is too high, the maximum rate is 0.2 T/min"
            self.ips.GRPZ.field_ramp_rate(rate / 60)
        else:
            assert max(rate) <= 0.2, (
                "The rate is too high, the maximum rate is 0.2 T/min"
            )
            self.ips.GRPZ.field_ramp_rate(rate[2] / 60)
        # self.ips.GRPX.field_ramp_rate(rate[0]/60)
        # self.ips.GRPY.field_ramp_rate(rate[1]/60)
        # no x and y field for now (see the setter method for details)
        ini_field = self.field
        self.field_set = field

        self.ips.ramp(mode="simul")
        if wait:
            # the is_ramping() method is not working properly, so we use the following method to wait for the ramping
            # to finish
            while (
                self.status == "TO SET" or abs(self.field - self.field_set) > tolerance
            ):
                print_progress_bar(
                    self.field - ini_field,
                    field - ini_field,
                    prefix="Stablizing",
                    suffix=f"B: {self.field} T",
                )
                time.sleep(1)
            logger.info("ramping finished")


"""
Wrappers for ITC are following
"""


class ITC(ABC):
    # parent class to incorporate both two ITCs
    @abstractmethod
    def __init__(
        self,
        address: str,
        cache_length: int = 60,
        var_crit: float = 1e-4,
        least_length: int = 13,
    ):
        self.cache = CacheArray(
            cache_length=cache_length, var_crit=var_crit, least_length=least_length
        )

    def set_cache(self, *, cache_length: int, var_crit: Optional[float] = None):
        """
        set the cache for the ITC
        """
        if var_crit is None:
            self.cache = CacheArray(cache_length=cache_length)
        else:
            self.cache = CacheArray(cache_length=cache_length, var_crit=var_crit)

    @property
    def temperature(self) -> float:
        """return the precise temperature of the sample"""
        temp: float = self.get_temperature()
        self.cache.update_cache(temp)
        return temp

    def add_cache(self) -> None:
        """add the temperature to the cache without returning"""
        temp: float = self.get_temperature()
        self.cache.update_cache(temp)

    @abstractmethod
    def get_temperature(self) -> float:
        """get the temperature from the instrument without caching"""

    def load_cache(self, load_length: int = 30) -> None:
        """load the cache from the instrument"""
        for i in range(load_length):
            self.add_cache()
            print_progress_bar(i + 1, load_length, prefix="loading cache")
            time.sleep(1)

    @property
    def status(self) -> Literal["VARYING", "HOLD"]:
        """return the varying status of the ITC"""
        status_return = self.cache.get_status()
        return "HOLD" if status_return["if_stable"] else "VARYING"

    @property
    @abstractmethod
    def temperature_set(self):
        """return the setpoint temperature"""
        pass

    @temperature_set.setter
    @abstractmethod
    def temperature_set(self, temp):
        """
        set the target temperature for sample, as for other parts' temperature, use the methods for each ITC
        """
        pass

    @property
    @abstractmethod
    def pid(self):
        """
        return the PID parameters
        """
        pass

    @abstractmethod
    def set_pid(self, pid_dict):
        """
        set the PID parameters

        Args:
            pid_dict (Dict): a dictionary as {"P": float, "I": float, "D": float}
        """
        pass

    @abstractmethod
    def correction_ramping(
        self, temp: float, trend: Literal["up", "down", "up-huge", "down-huge"]
    ):
        """
        Correct the sensor choosing or pressure when ramping through the temperature threshold

        Args:
            temp (float): the current temperature
            trend (Literal["up","down"]): the trend of the temperature
        """
        pass

    def wait_for_temperature(
        self,
        temp,
        *,
        check_interval=1,
        stability_counter=1,
        thermalize_counter=7,
        correction_needed=False,
    ):
        """
        wait for the temperature to stablize for a certain time length

        Args:
            temp (float): the target temperature
            check_interval (int,[s]): the interval to check the temperature
            stability_counter (int): the number of times the temperature is within the delta range
                to consider the temperature stablized
            thermalize_counter (int): the number of times to thermalize the sample
        """

        def tolerance_T(T: float):
            """
            set the tolerance to judge if ramping is needed
            """
            if T > 10:
                return T / 1000
            else:
                return 0.007

        trend: Literal["up", "down", "up-huge", "down-huge"]
        initial_temp = self.temperature
        if abs(initial_temp - temp) < tolerance_T(temp):
            return
        elif initial_temp < temp - 100:
            trend = "up-huge"
        elif initial_temp > temp + 100:
            trend = "down-huge"
        elif initial_temp < temp:
            trend = "up"
        else:
            trend = "down"

        i = 0
        while i < stability_counter:
            # self.add_cache()
            if correction_needed:
                self.correction_ramping(self.temperature, trend)
            if (
                abs(self.cache.get_status()["mean"] - temp) < ITC.dynamic_delta(temp)
                and self.cache.get_status()["if_stable"]
            ):
                i += 1
            else:
                i = 0
            print_progress_bar(
                self.temperature - initial_temp,
                temp - initial_temp,
                prefix="Stablizing",
                suffix=f"Temperature: {self.temperature:.3f} K",
            )
            time.sleep(check_interval)
        logger.info("Temperature stablized")
        for i in range(thermalize_counter):
            print_progress_bar(
                i + 1,
                thermalize_counter,
                prefix="Thermalizing",
                suffix=f"Temperature: {self.temperature:.3f} K",
            )
            time.sleep(check_interval)
        logger.info("Thermalizing finished")

    def ramp_to_temperature(
        self,
        temp,
        *,
        delta=0.02,
        check_interval=1,
        stability_counter=1,
        thermalize_counter=7,
        pid: Optional[dict] = None,
        ramp_rate=None,
        wait=True,
    ):
        """ramp temperature to the target value (not necessary sample temperature)"""
        self.temperature_set = temp
        if pid is not None:
            self.set_pid(pid)
        if wait:
            self.wait_for_temperature(
                temp,
                check_interval=check_interval,
                stability_counter=stability_counter,
                thermalize_counter=thermalize_counter,
            )

    @staticmethod
    def dynamic_delta(temp) -> float:
        """
        calculate a dynamic delta to help high temperature to stabilize (reach 0.1K tolerance when 300K and {delta_lowt} when 10K)
        """
        # linear interpolation
        delta_hight = 0.3
        t_high = 300
        delta_lowt = 0.02
        t_low = 1.5
        return (delta_hight - delta_lowt) * (temp - t_low) / (
            t_high - t_low
        ) + delta_lowt


class ITCLakeshore(ITC):
    def __init__(
        self,
        address: str = "GPIB0::12::INSTR",
        cache_length: int = 60,
        var_crit: float = 5e-4,
        least_length: int = 13,
    ):
        self.ls = LakeshoreModel336("Lakeshore336", address)
        self.cache = CacheArray(
            cache_length=cache_length, var_crit=var_crit, least_length=least_length
        )
        self.channels_no = len(self.ls.channels)
        self.second_stage = self.ls.C
        self.sample_mount = self.ls.B
        self.sample = self.ls.A
        self.heater_intrinsic = [self.ls.output_1, self.ls.output_2]
        self.binding = {"heater_1": "sample", "heater_2": "second_stage"}
        self.binding_inv = {v: k for k, v in self.binding.items()}
        if "sample" not in self.binding_inv and "sample_mount" not in self.binding_inv:
            logger.raise_error(
                "sample related sensor is not in the binding", ValueError
            )
        heater_sample_str = (
            self.binding_inv["sample"]
            if "sample" in self.binding_inv
            else self.binding_inv["sample_mount"]
        )
        self.heater_sample = (
            self.ls.output_1 if heater_sample_str == "sample" else self.ls.output_2
        )

    def get_binding(self):
        print(f"Heater 1 is bound to {self.binding['heater_1']}")
        print(f"Heater 2 is bound to {self.binding['heater_2']}")

    def change_binding(self, *, heater_1: str, heater_2: str):
        logger.warning("usually not needed, be aware of what you are doing")
        self.binding["heater_1"] = heater_1
        self.binding["heater_2"] = heater_2
        self._bind_heater()

    def _bind_heater(self):
        if self.binding["heater_1"] == self.binding["heater_2"]:
            logger.raise_error("Heater 1 and Heater 2 cannot be the same", ValueError)
        match self.binding["heater_1"]:
            case "sample":
                self.ls.output_1.input_channel("A")
            case "second_stage":
                self.ls.output_1.input_channel("C")
            case "sample_mount":
                self.ls.output_1.input_channel("B")
            case _:
                logger.raise_error(
                    f"Invalid heater binding: {self.binding['heater_1']}", ValueError
                )
        match self.binding["heater_2"]:
            case "sample":
                self.ls.output_2.input_channel("A")
            case "second_stage":
                self.ls.output_2.input_channel("C")
            case "sample_mount":
                self.ls.output_2.input_channel("B")
            case _:
                logger.raise_error(
                    f"Invalid heater binding: {self.binding['heater_2']}", ValueError
                )

    def get_temperature(self) -> float:
        return self.sample.temperature()

    @property
    def temperature_set(self) -> float:
        return self.heater_sample.setpoint()

    @temperature_set.setter
    def temperature_set(self, temp: float) -> None:
        self.heater_sample.setpoint(temp)

    @property
    def pid(self) -> dict:
        return {
            "P": self.heater_sample.P(),
            "I": self.heater_sample.I(),
            "D": self.heater_sample.D(),
        }

    def set_pid(self, pid_dict: dict) -> None:
        self.heater_sample.P(pid_dict["P"])
        self.heater_sample.I(pid_dict["I"])
        self.heater_sample.D(pid_dict["D"])

    def correction_ramping(
        self,
        temp: float | str,
        trend: Literal["up"]
        | Literal["down"]
        | Literal["up-huge"]
        | Literal["down-huge"],
    ):
        pass

    def ramp_to_temperature(
        self,
        temp: float | str,
        *,
        delta=0.02,
        check_interval=1,
        stability_counter=1,
        thermalize_counter=7,
        pid: dict | None = None,
        ramp_rate=None,
        wait=True,
    ):
        temp = convert_unit(temp, "K")[0]
        self.temperature_set = temp
        if pid is not None:
            self.set_pid(pid)
        if ramp_rate is not None:
            self.heater_sample.setpoint_ramp_rate(ramp_rate)

        self.heater_sample.output_range("low")
        if wait:
            self.wait_for_temperature(
                temp,
                check_interval=check_interval,
                stability_counter=stability_counter,
                thermalize_counter=thermalize_counter,
            )

    @override
    @property
    def status(self) -> Literal["VARYING", "HOLD"]:
        """return the varying status of the ITC"""
        status_return = self.cache.get_status()
        if status_return["if_stable"] and not self.heater_sample.setpoint_ramp_status():
            return "HOLD"
        else:
            return "VARYING"


class ITCMercury(ITC):
    """
    Variable Params:
    self.correction_ramping: modify pressure according to the temperature and trend
    self.calculate_vti_temp (in driver): automatically calculate the set VTI temperature
    """

    def __init__(
        self,
        address="TCPIP0::10.97.27.13::7020::SOCKET",
        cache_length: int = 60,
        var_crit: float = 5e-4,
        least_length: int = 13,
    ):
        self.mercury = MercuryITC("mercury_itc", address)
        self.cache = CacheArray(
            cache_length=cache_length, var_crit=var_crit, least_length=least_length
        )

    @property
    def pres(self):
        return self.mercury.pressure()

    def set_pres(self, pres: float):
        self.mercury.pressure_setpoint(pres)

    @property
    def flow(self):
        return self.mercury.gas_flow()

    def set_flow(self, flow: float):
        """
        set the gas flow, note the input value is percentage, from 0 to 99.9 (%)
        """
        if not 0.0 < flow < 100.0:
            raise ValueError("Flow must be between 0.0 and 100.0 (%)")
        self.mercury.gas_flow(flow)

    @property
    def pid(self):
        return {
            "P": self.mercury.temp_loop_P(),
            "I": self.mercury.temp_loop_I(),
            "D": self.mercury.temp_loop_D(),
        }

    def set_pid(self, pid_dict: dict):
        """
        set the pid of probe temp loop
        """
        self.mercury.temp_PID = (pid_dict["P"], pid_dict["I"], pid_dict["D"])
        self.pid_control("ON")

    def pid_control(self, control: Literal["ON", "OFF"]):
        self.mercury.temp_PID_control(control)

    def get_temperature(self) -> float:
        return self.mercury.probe_temp()

    def set_temperature(self, temp, vti_diff=None):
        """set the target temperature for sample"""
        self.mercury.temp_setpoint(temp)
        if vti_diff is not None:
            self.mercury.vti_temp_setpoint(temp - vti_diff)
        else:
            self.mercury.vti_temp_setpoint(self.mercury.calculate_vti_temp(temp))

    @property
    def temperature_set(self):
        return self.mercury.temp_setpoint()

    @temperature_set.setter
    def temperature_set(self, temp):
        self.set_temperature(temp)

    @property
    def vti_temperature(self):
        return self.mercury.vti_temp()

    def set_vti_temperature(self, temp):
        self.mercury.vti_temp_setpoint(temp)

    def ramp_to_temperature(
        self,
        temp,
        *,
        check_interval=1,
        stability_counter=10,
        thermalize_counter=7,
        pid=None,
        ramp_rate=None,
        wait=True,
        vti_diff: Optional[float] = 5,
    ):
        """ramp temperature to the target value (not necessary sample temperature)

        Args:
            temp (float): the target temperature
            delta (float): the temperature difference to consider the temperature stablized
            check_interval (int,[s]): the interval to check the temperature
            stability_counter (int): the number of times the temperature is within the delta range to consider the temperature stablized
            thermalize_counter (int): the number of times to thermalize the sample
            pid (Dict): a dictionary as {"P": float, "I": float, "D": float}
            ramp_rate (float, [K/min]): the rate to ramp the temperature
            wait (bool): whether to wait for the ramping to finish
            vti_diff (float, None to ignore VTI): the difference between the sample temperature and the VTI temperature
        """
        temp = convert_unit(temp, "K")[0]
        self.temperature_set = temp
        if pid is not None:
            self.set_pid(pid)

        if ramp_rate is not None:
            self.mercury.probe_ramp_rate(ramp_rate)
            # self.mercury.vti_heater_rate(ramp_rate)
            self.mercury.probe_temp_ramp_mode(
                "ON"
            )  # ramp_mode means limited ramping rate mode
        else:
            self.mercury.probe_temp_ramp_mode("OFF")
        if wait:
            self.wait_for_temperature(
                temp,
                check_interval=check_interval,
                stability_counter=stability_counter,
                thermalize_counter=thermalize_counter,
            )

    def correction_ramping(
        self, temp: float, trend: Literal["up", "down", "up-huge", "down-huge"]
    ):
        """
        Correct the sensor choosing or pressure when ramping through the temperature threshold

        Args:
            temp (float): the current temperature
            trend (Literal["up","down","up-huge","down-huge"]): the trend of the temperature
        """
        if trend == "up-huge":
            self.set_flow(2)
        elif trend == "down-huge":
            if temp >= 5:
                self.set_flow(15)
            elif temp > 2:
                self.set_flow(8)
            else:
                self.set_flow(3)
        else:
            if temp <= 2.3:
                self.set_flow(2)
            if trend == "up":
                self.set_flow(3)
            else:
                self.set_flow(4)


class ITCs(ITC):
    """Represents the ITC503 Temperature Controllers and provides a high-level interface for interacting with the instruments.

    There are two ITC503 incorporated in the setup, named up and down. The up one measures the temperature of the heat switch(up R1), PT2(up R2), leaving R3 no specific meaning. The down one measures the temperature of the sorb(down R1), POT LOW(down R2), POT HIGH(down R3).
    """

    def __init__(
        self,
        address_up: str = "GPIB0::23::INSTR",
        address_down: str = "GPIB0::24::INSTR",
        clear_buffer=True,
        cache_length: int = 60,
        var_crit: float = 3e-4,
        least_length: int = 13,
    ):
        self.itc_up = ITC503(address_up, clear_buffer=clear_buffer)
        self.itc_down = ITC503(address_down, clear_buffer=clear_buffer)
        self.itc_up.control_mode = "RU"
        self.itc_down.control_mode = "RU"
        self.cache = CacheArray(
            cache_length=cache_length, var_crit=var_crit, least_length=least_length
        )

    def chg_display(self, itc_name, target):
        """
        This function is used to change the front display of the ITC503

        Parameters: itc_name (str): The name of the ITC503, "up" or "down" or "all" target (str):  'temperature
        setpoint', 'temperature 1', 'temperature 2', 'temperature 3', 'temperature error', 'heater',
        'heater voltage', 'gasflow', 'proportional band', 'integral action time', 'derivative action time',
        'channel 1 freq/4', 'channel 2 freq/4', 'channel 3 freq/4'.

        Returns:
        None
        """
        if itc_name == "all":
            self.itc_up.front_panel_display = target
            self.itc_down.front_panel_display = target
        elif itc_name == "up":
            self.itc_up.front_panel_display = target
        elif itc_name == "down":
            self.itc_down.front_panel_display = target

    @property
    def temperature_set(self):
        return self.itc_down.temperature_setpoint

    @temperature_set.setter
    def temperature_set(self, temp):
        """
        set the target temperature for sample, as for other parts' temperature, use the methods for each ITC

        Args:
            temp (float): the target temperature
            itc_name (Literal["up","down","all"]): the ITC503 to set the temperature
        """
        self.itc_down.temperature_setpoint = temp

    def ramp_to_temperature_selective(
        self, temp, itc_name: Literal["up", "down"], P=None, I=None, D=None
    ):
        """
        used to ramp the temperature of the ITCs, this method will wait for the temperature to stablize and thermalize for a certain time length
        """
        self.control_mode = ("RU", itc_name)
        if itc_name == "up":
            itc_here = self.itc_up
        elif itc_name == "down":
            itc_here = self.itc_down
        else:
            logger.error("Please specify the ITC to set")
            return
        itc_here.temperature_setpoint = temp
        if P is not None and I is not None and D is not None:
            itc_here.auto_pid = False
            itc_here.proportional_band = P
            itc_here.integral_action_time = I
            itc_here.derivative_action_time = D
        else:
            itc_here.auto_pid = True
        itc_here.heater_gas_mode = "AM"
        logger.info(f"temperature setted to {temp}")

    @property
    def version(self):
        """Returns the version of the ITC503."""
        return [self.itc_up.version, self.itc_down.version]

    @property
    def control_mode(self):
        """Returns the control mode of the ITC503."""
        return [self.itc_up.control_mode, self.itc_down.control_mode]

    @control_mode.setter
    def control_mode(
        self, mode: tuple[Literal["LU", "RU", "LL", "RL"], Literal["all", "up", "down"]]
    ):
        """Sets the control mode of the ITC503. A two-element list is required. The second elecment is "all" or "up"
        or "down" to specify which ITC503 to set."""
        if mode[1] == "all":
            self.itc_up.control_mode = mode[0]
            self.itc_down.control_mode = mode[0]
        elif mode[1] == "up":
            self.itc_up.control_mode = mode[0]
        elif mode[1] == "down":
            self.itc_down.control_mode = mode[0]

    @property
    def heater_gas_mode(self):
        """Returns the heater gas mode of the ITC503."""
        return [self.itc_up.heater_gas_mode, self.itc_down.heater_gas_mode]

    @heater_gas_mode.setter
    def heater_gas_mode(
        self,
        mode: tuple[
            Literal["MANUAL", "AM", "MA", "AUTO"], Literal["all", "up", "down"]
        ],
    ):
        """Sets the heater gas mode of the ITC503. A two-element list is required. The second elecment is "all" or
        "up" or "down" to specify which ITC503 to set."""
        if mode[1] == "all":
            self.itc_up.heater_gas_mode = mode[0]
            self.itc_down.heater_gas_mode = mode[0]
        elif mode[1] == "up":
            self.itc_up.heater_gas_mode = mode[0]
        elif mode[1] == "down":
            self.itc_down.heater_gas_mode = mode[0]

    @property
    def heater_power(self):
        """Returns the heater power of the ITC503."""
        return [self.itc_up.heater, self.itc_down.heater]

    @property
    def heater_voltage(self):
        """Returns the heater voltage of the ITC503."""
        return [self.itc_up.heater_voltage, self.itc_down.heater_voltage]

    @property
    def gas_flow(self):
        """Returns the gasflow of the ITC503."""
        return [self.itc_up.gasflow, self.itc_down.gasflow]

    @property
    def proportional_band(self):
        """Returns the proportional band of the ITC503."""
        return [self.itc_up.proportional_band, self.itc_down.proportional_band]

    @property
    def integral_action_time(self):
        """Returns the integral action time of the ITC503."""
        return [self.itc_up.integral_action_time, self.itc_down.integral_action_time]

    @property
    def derivative_action_time(self):
        """Returns the derivative action time of the ITC503."""
        return [
            self.itc_up.derivative_action_time,
            self.itc_down.derivative_action_time,
        ]

    @property
    def pid(self):
        """Returns the PID of the ITC503."""
        return tuple(
            zip(
                self.proportional_band,
                self.integral_action_time,
                self.derivative_action_time,
            )
        )

    def set_pid(self, pid: dict, mode: Literal["all", "up", "down"] = "down"):
        """Sets the PID of the ITC503. A three-element list is required. The second elecment is "all" or "up" or "down" to specify which ITC503 to set.
        The P,I,D here are the proportional band (K), integral action time (min), and derivative action time(min), respectively.
        """
        self.control_mode = ("RU", mode)
        if mode == "all":
            self.itc_up.proportional_band = pid["P"]
            self.itc_down.proportional_band = pid["P"]
            self.itc_up.integral_action_time = pid["I"]
            self.itc_down.integral_action_time = pid["I"]
            self.itc_up.derivative_action_time = pid["D"]
            self.itc_down.derivative_action_time = pid["D"]
        if mode == "up":
            self.itc_up.proportional_band = pid["P"]
            self.itc_up.integral_action_time = pid["I"]
            self.itc_up.derivative_action_time = pid["D"]
        if mode == "down":
            self.itc_down.proportional_band = pid["P"]
            self.itc_down.integral_action_time = pid["I"]
            self.itc_down.derivative_action_time = pid["D"]

        if self.itc_up.proportional_band == 0:
            return ""
        return f"{mode} PID(power percentage): 100*(E/{pid['P']}+E/{pid['P']}*t/60{pid['I']}-dE*60{pid['D']}/{pid['P']}), [K,min,min]"

    @property
    def auto_pid(self):
        """Returns the auto pid of the ITC503."""
        return [self.itc_up.auto_pid, self.itc_down.auto_pid]

    @auto_pid.setter
    def auto_pid(self, mode):
        """Sets the auto pid of the ITC503. A two-element list is required. The second elecment is "all" or "up" or
        "down" to specify which ITC503 to set."""
        if mode[1] == "all":
            self.itc_up.auto_pid = mode[0]
            self.itc_down.auto_pid = mode[0]
        elif mode[1] == "up":
            self.itc_up.auto_pid = mode[0]
        elif mode[1] == "down":
            self.itc_down.auto_pid = mode[0]

    @property
    def temperature_setpoint(self):
        """Returns the temperature setpoint of the ITC503."""
        return [self.itc_up.temperature_setpoint, self.itc_down.temperature_setpoint]

    @temperature_setpoint.setter
    def temperature_setpoint(self, temperature):
        """Sets the temperature setpoint of the ITC503. A two-element list is required. The second elecment is "all"
        or "up" or "down" to specify which ITC503 to set."""
        if temperature[1] == "all":
            self.itc_up.temperature_setpoint = temperature[0]
            self.itc_down.temperature_setpoint = temperature[0]
        elif temperature[1] == "up":
            self.itc_up.temperature_setpoint = temperature[0]
        elif temperature[1] == "down":
            self.itc_down.temperature_setpoint = temperature[0]

    @property
    def temperatures(self):
        """Returns the temperatures of the whole device as a dict."""
        return {
            "sw": self.itc_up.temperature_1,
            "pt2": self.itc_up.temperature_2,
            "sorb": self.itc_down.temperature_1,
            "pot_low": self.itc_down.temperature_2,
            "pot_high": self.itc_down.temperature_3,
        }

    def get_temperature(self):
        """Returns the precise temperature of the sample"""
        if self.temperatures["pot_high"] < 1.9:
            return self.temperatures["pot_low"]
        elif self.temperatures["pot_high"] >= 1.9:
            return self.temperatures["pot_high"]

    def correction_ramping(
        self, temp: float, trend: Literal["up", "down", "up-huge", "down-huge"]
    ):
        pass
