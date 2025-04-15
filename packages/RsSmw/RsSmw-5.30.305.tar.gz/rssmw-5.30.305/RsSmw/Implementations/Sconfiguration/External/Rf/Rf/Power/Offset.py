from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OffsetCls:
	"""Offset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("offset", core, parent)

	def set(self, power_offset: float, path=repcap.Path.Default) -> None:
		"""SCPI: SCONfiguration:EXTernal:RF<CH>:RF:POWer:OFFSet \n
		Snippet: driver.sconfiguration.external.rf.rf.power.offset.set(power_offset = 1.0, path = repcap.Path.Default) \n
		In coupled mode, offsets the RF level of the external instrument with the selected delta value. \n
			:param power_offset: float Range: -100 to 100
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
		"""
		param = Conversions.decimal_value_to_str(power_offset)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		self._core.io.write(f'SCONfiguration:EXTernal:RF{path_cmd_val}:RF:POWer:OFFSet {param}')

	def get(self, path=repcap.Path.Default) -> float:
		"""SCPI: SCONfiguration:EXTernal:RF<CH>:RF:POWer:OFFSet \n
		Snippet: value: float = driver.sconfiguration.external.rf.rf.power.offset.get(path = repcap.Path.Default) \n
		In coupled mode, offsets the RF level of the external instrument with the selected delta value. \n
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: power_offset: float Range: -100 to 100"""
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:RF{path_cmd_val}:RF:POWer:OFFSet?')
		return Conversions.str_to_float(response)
