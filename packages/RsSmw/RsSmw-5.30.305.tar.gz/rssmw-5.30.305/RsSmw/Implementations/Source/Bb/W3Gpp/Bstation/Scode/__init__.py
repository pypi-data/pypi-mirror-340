from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScodeCls:
	"""Scode commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scode", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	def set(self, scode: str, baseStation=repcap.BaseStation.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:SCODe \n
		Snippet: driver.source.bb.w3Gpp.bstation.scode.set(scode = rawAbc, baseStation = repcap.BaseStation.Default) \n
		Sets the identification for the base station. This value is simultaneously the initial value of the scrambling code
		generator. \n
			:param scode: integer Range: #H0 to #H5FFF
			:param baseStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
		"""
		param = Conversions.value_to_str(scode)
		baseStation_cmd_val = self._cmd_group.get_repcap_cmd_value(baseStation, repcap.BaseStation)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{baseStation_cmd_val}:SCODe {param}')

	def get(self, baseStation=repcap.BaseStation.Default) -> str:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:BSTation<ST>:SCODe \n
		Snippet: value: str = driver.source.bb.w3Gpp.bstation.scode.get(baseStation = repcap.BaseStation.Default) \n
		Sets the identification for the base station. This value is simultaneously the initial value of the scrambling code
		generator. \n
			:param baseStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:return: scode: integer Range: #H0 to #H5FFF"""
		baseStation_cmd_val = self._cmd_group.get_repcap_cmd_value(baseStation, repcap.BaseStation)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{baseStation_cmd_val}:SCODe?')
		return trim_str_response(response)

	def clone(self) -> 'ScodeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ScodeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
