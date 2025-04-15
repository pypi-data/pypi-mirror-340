from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExecuteCls:
	"""Execute commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("execute", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:ALEVel:EXECute \n
		Snippet: driver.source.bbin.alevel.execute.set() \n
		For [:SOURce<hw>]:BBIN:DIGital:SOURce CODER1|CODER2 Starts measuring the input signal. The measurement estimates the
		crest factor, peak and RMS level. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BBIN:ALEVel:EXECute')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:BBIN:ALEVel:EXECute \n
		Snippet: driver.source.bbin.alevel.execute.set_with_opc() \n
		For [:SOURce<hw>]:BBIN:DIGital:SOURce CODER1|CODER2 Starts measuring the input signal. The measurement estimates the
		crest factor, peak and RMS level. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BBIN:ALEVel:EXECute', opc_timeout_ms)
