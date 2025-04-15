from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LocalCls:
	"""Local commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("local", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:OPTimization:LOCal \n
		Snippet: driver.source.correction.fresponse.rf.optimization.local.set() \n
		For high-quality I/Q modulation optimizations, triggers optimization for the current settings.
		To enable these optimizations, see the following command: [:SOURce<hw>]:CORRection:FRESponse:RF:OPTimization:MODE \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:OPTimization:LOCal')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:CORRection:FRESponse:RF:OPTimization:LOCal \n
		Snippet: driver.source.correction.fresponse.rf.optimization.local.set_with_opc() \n
		For high-quality I/Q modulation optimizations, triggers optimization for the current settings.
		To enable these optimizations, see the following command: [:SOURce<hw>]:CORRection:FRESponse:RF:OPTimization:MODE \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:CORRection:FRESponse:RF:OPTimization:LOCal', opc_timeout_ms)
