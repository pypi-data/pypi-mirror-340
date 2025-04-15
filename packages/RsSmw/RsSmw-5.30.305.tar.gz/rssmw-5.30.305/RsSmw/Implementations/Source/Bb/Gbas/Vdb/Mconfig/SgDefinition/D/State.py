from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool, vdbTransmitter=repcap.VdbTransmitter.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:SGDefinition:D:STATe \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.sgDefinition.d.state.set(state = False, vdbTransmitter = repcap.VdbTransmitter.Default) \n
		If enabled, the specified slot is assigned for use by the ground station. \n
			:param state: 1| ON| 0| OFF
			:param vdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
		"""
		param = Conversions.bool_to_str(state)
		vdbTransmitter_cmd_val = self._cmd_group.get_repcap_cmd_value(vdbTransmitter, repcap.VdbTransmitter)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{vdbTransmitter_cmd_val}:MCONfig:SGDefinition:D:STATe {param}')

	def get(self, vdbTransmitter=repcap.VdbTransmitter.Default) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:SGDefinition:D:STATe \n
		Snippet: value: bool = driver.source.bb.gbas.vdb.mconfig.sgDefinition.d.state.get(vdbTransmitter = repcap.VdbTransmitter.Default) \n
		If enabled, the specified slot is assigned for use by the ground station. \n
			:param vdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: state: 1| ON| 0| OFF"""
		vdbTransmitter_cmd_val = self._cmd_group.get_repcap_cmd_value(vdbTransmitter, repcap.VdbTransmitter)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{vdbTransmitter_cmd_val}:MCONfig:SGDefinition:D:STATe?')
		return Conversions.str_to_bool(response)
