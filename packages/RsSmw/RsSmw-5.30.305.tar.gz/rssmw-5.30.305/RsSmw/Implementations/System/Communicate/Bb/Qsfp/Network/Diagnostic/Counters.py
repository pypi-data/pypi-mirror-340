from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CountersCls:
	"""Counters commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("counters", core, parent)

	def reset(self) -> None:
		"""SCPI: SYSTem:COMMunicate:BB<HW>:QSFP:NETWork:DIAGnostic:COUNters:RESet \n
		Snippet: driver.system.communicate.bb.qsfp.network.diagnostic.counters.reset() \n
		No command help available \n
		"""
		self._core.io.write(f'SYSTem:COMMunicate:BB<HwInstance>:QSFP:NETWork:DIAGnostic:COUNters:RESet')

	def reset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SYSTem:COMMunicate:BB<HW>:QSFP:NETWork:DIAGnostic:COUNters:RESet \n
		Snippet: driver.system.communicate.bb.qsfp.network.diagnostic.counters.reset_with_opc() \n
		No command help available \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsSmw.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SYSTem:COMMunicate:BB<HwInstance>:QSFP:NETWork:DIAGnostic:COUNters:RESet', opc_timeout_ms)

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Rx_Udp_Frames: float: No parameter help available
			- Tx_Udp_Frames: float: No parameter help available
			- Rx_Corrupt_Udp_Fra: float: No parameter help available
			- Rx_Payload_Bytes: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_float('Rx_Udp_Frames'),
			ArgStruct.scalar_float('Tx_Udp_Frames'),
			ArgStruct.scalar_float('Rx_Corrupt_Udp_Fra'),
			ArgStruct.scalar_float('Rx_Payload_Bytes')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rx_Udp_Frames: float = None
			self.Tx_Udp_Frames: float = None
			self.Rx_Corrupt_Udp_Fra: float = None
			self.Rx_Payload_Bytes: float = None

	def get_value(self) -> ValueStruct:
		"""SCPI: SYSTem:COMMunicate:BB<HW>:QSFP:NETWork:DIAGnostic:COUNters \n
		Snippet: value: ValueStruct = driver.system.communicate.bb.qsfp.network.diagnostic.counters.get_value() \n
		No command help available \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('SYSTem:COMMunicate:BB<HwInstance>:QSFP:NETWork:DIAGnostic:COUNters?', self.__class__.ValueStruct())
