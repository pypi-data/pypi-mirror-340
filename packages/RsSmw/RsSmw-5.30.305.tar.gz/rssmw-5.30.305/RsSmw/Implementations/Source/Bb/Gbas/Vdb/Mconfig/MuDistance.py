from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MuDistanceCls:
	"""MuDistance commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("muDistance", core, parent)

	def set(self, distance: float, vdbTransmitter=repcap.VdbTransmitter.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:MUDistance \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.muDistance.set(distance = 1.0, vdbTransmitter = repcap.VdbTransmitter.Default) \n
		Sets the maximum distance from the reference point for which the integrity is assured. \n
			:param distance: float Range: 0 to 510
			:param vdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
		"""
		param = Conversions.decimal_value_to_str(distance)
		vdbTransmitter_cmd_val = self._cmd_group.get_repcap_cmd_value(vdbTransmitter, repcap.VdbTransmitter)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{vdbTransmitter_cmd_val}:MCONfig:MUDistance {param}')

	def get(self, vdbTransmitter=repcap.VdbTransmitter.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:MUDistance \n
		Snippet: value: float = driver.source.bb.gbas.vdb.mconfig.muDistance.get(vdbTransmitter = repcap.VdbTransmitter.Default) \n
		Sets the maximum distance from the reference point for which the integrity is assured. \n
			:param vdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: distance: float Range: 0 to 510"""
		vdbTransmitter_cmd_val = self._cmd_group.get_repcap_cmd_value(vdbTransmitter, repcap.VdbTransmitter)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{vdbTransmitter_cmd_val}:MCONfig:MUDistance?')
		return Conversions.str_to_float(response)
