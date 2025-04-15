from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PpowerCls:
	"""Ppower commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ppower", core, parent)

	@property
	def step(self):
		"""step commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_step'):
			from .Step import StepCls
			self._step = StepCls(self._core, self._cmd_group)
		return self._step

	def set(self, ppower: float, mobileStation=repcap.MobileStation.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PRACh:PPOWer \n
		Snippet: driver.source.bb.w3Gpp.mstation.prach.ppower.set(ppower = 1.0, mobileStation = repcap.MobileStation.Default) \n
		The command defines the power of the preamble component of the PRACH. If the preamble is repeated and the power increased
		with each repetition, this setting specifies the power achieved during the last repetition. \n
			:param ppower: float Range: -80 dB to 0 dB
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
		"""
		param = Conversions.decimal_value_to_str(ppower)
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:PRACh:PPOWer {param}')

	def get(self, mobileStation=repcap.MobileStation.Default) -> float:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:PRACh:PPOWer \n
		Snippet: value: float = driver.source.bb.w3Gpp.mstation.prach.ppower.get(mobileStation = repcap.MobileStation.Default) \n
		The command defines the power of the preamble component of the PRACH. If the preamble is repeated and the power increased
		with each repetition, this setting specifies the power achieved during the last repetition. \n
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: ppower: float Range: -80 dB to 0 dB"""
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:PRACh:PPOWer?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'PpowerCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PpowerCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
