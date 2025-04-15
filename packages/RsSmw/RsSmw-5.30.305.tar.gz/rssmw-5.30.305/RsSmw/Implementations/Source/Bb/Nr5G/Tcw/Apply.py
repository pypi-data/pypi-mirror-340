from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApplyCls:
	"""Apply commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("apply", core, parent)

	def set(self) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:APPLy \n
		Snippet: driver.source.bb.nr5G.tcw.apply.set() \n
		Activates the current settings of the test case wizard. Note: The settings of the selected test case become active only
		after executing this command. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:APPLy')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:TCW:APPLy \n
		Snippet: driver.source.bb.nr5G.tcw.apply.set_with_opc() \n
		Activates the current settings of the test case wizard. Note: The settings of the selected test case become active only
		after executing this command. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:NR5G:TCW:APPLy', opc_timeout_ms)
