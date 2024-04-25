#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2024 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_discrete_set


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Keithley705(Instrument):
    """Instrument class for the Keithley 705 scanner.

    .. code-block:: python

        scanner = Keithley705("GPIB::1")

    """

    def __init__(self, adapter, name="Keithley 705 Scanner", read_termination='\r',
                 **kwargs) -> None:
        self.channels = tuple(range(1, 21))
        super().__init__(adapter, name, read_termination=read_termination,
                         includeSCPI=False, **kwargs)
        self.reset()

    number_of_poles = Instrument.setting(
        "A%dX",
        """Set the number of poles.
        Valid options are 0 (matrix mode), 1, 2, or 4.
        Upon changing, First Channel = 1, Last Channel = last (20 to 200), and Channel
        1 is displayed.""",
        validator=strict_discrete_set,
        values=(0, 1, 2, 4)
    )

    display_channel = Instrument.setting(
        "B%dX",
        """Set which channel to display.""",
        )

    display_mode = Instrument.setting(
        "D%dX",
        """Set display mode.
        Valid options are `channel`, `interval`, `time`, `date`, `message""",
        validator=strict_discrete_set,
        values={"channel": 0, "interval": 1, "time": 2, "date": 3, "message": 4},
        map_values=True
    )

    date_format = Instrument.setting(
        "E%dX",
        """Set date format to `American` or `International`.""",
        validator=strict_discrete_set,
        values={"American": 0, "International": 1},
        map_values=True
    )

    first_channel = Instrument.setting(
        "F%dX",
        """Set first channel.""",
    )

    settle_time = Instrument.setting(
        "H%fX",
        """Set the settle time.""",
    )

    last_channel = Instrument.setting(
        "L%dX",
        """Set last channel.""",
    )

    def reset(self) -> None:
        """Open all channels and display FIRST channel."""
        self.write("RX")

    def open_channel(self, channel: int) -> None:
        """Open selected channel."""
        self.write(f"N{channel}X")

    def close_channel(self, channel: int) -> None:
        """Close selected channel."""
        self.write(f"C{channel}X")

    def exclusive_close(self, channel: int) -> None:
        """Close selected channel and open all others."""
        for c in self.channels:
            if c != channel:
                self.open_channel(c)
        self.close_channel(channel)
