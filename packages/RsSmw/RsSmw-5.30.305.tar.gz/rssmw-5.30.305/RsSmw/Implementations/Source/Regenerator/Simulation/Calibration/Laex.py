from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LaexCls:
	"""Laex commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("laex", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:REGenerator:SIMulation:CALibration:LAEX \n
		Snippet: driver.source.regenerator.simulation.calibration.laex.set() \n
		Triggers system latency calibration. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:REGenerator:SIMulation:CALibration:LAEX')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:REGenerator:SIMulation:CALibration:LAEX \n
		Snippet: driver.source.regenerator.simulation.calibration.laex.set_with_opc() \n
		Triggers system latency calibration. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:REGenerator:SIMulation:CALibration:LAEX', opc_timeout_ms)
