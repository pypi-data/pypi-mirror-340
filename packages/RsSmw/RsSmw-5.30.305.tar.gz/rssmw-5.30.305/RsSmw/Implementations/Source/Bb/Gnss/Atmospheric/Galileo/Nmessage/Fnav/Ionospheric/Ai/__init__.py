from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ...........Internal.RepeatedCapability import RepeatedCapability
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AiCls:
	"""Ai commands group definition. 2 total commands, 1 Subgroups, 1 group commands
	Repeated Capability: AiOrder, default value after init: AiOrder.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ai", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_aiOrder_get', 'repcap_aiOrder_set', repcap.AiOrder.Nr1)

	def repcap_aiOrder_set(self, aiOrder: repcap.AiOrder) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AiOrder.Default.
		Default value after init: AiOrder.Nr1"""
		self._cmd_group.set_repcap_enum_value(aiOrder)

	def repcap_aiOrder_get(self) -> repcap.AiOrder:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def unscaled(self):
		"""unscaled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unscaled'):
			from .Unscaled import UnscaledCls
			self._unscaled = UnscaledCls(self._core, self._cmd_group)
		return self._unscaled

	def set(self, ai: int, aiOrder=repcap.AiOrder.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ATMospheric:GALileo:NMESsage:FNAV:IONospheric:AI<CH0> \n
		Snippet: driver.source.bb.gnss.atmospheric.galileo.nmessage.fnav.ionospheric.ai.set(ai = 1, aiOrder = repcap.AiOrder.Default) \n
		Sets the parameters effective ionization level 1st to 3rd order of the satellite's navigation message. \n
			:param ai: integer Range: a_i0 (0 to 2047) , a_i1 (-1024 to 1023) , a_i2 (-8192 to 8191)
			:param aiOrder: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ai')
		"""
		param = Conversions.decimal_value_to_str(ai)
		aiOrder_cmd_val = self._cmd_group.get_repcap_cmd_value(aiOrder, repcap.AiOrder)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:GALileo:NMESsage:FNAV:IONospheric:AI{aiOrder_cmd_val} {param}')

	def get(self, aiOrder=repcap.AiOrder.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:GNSS:ATMospheric:GALileo:NMESsage:FNAV:IONospheric:AI<CH0> \n
		Snippet: value: int = driver.source.bb.gnss.atmospheric.galileo.nmessage.fnav.ionospheric.ai.get(aiOrder = repcap.AiOrder.Default) \n
		Sets the parameters effective ionization level 1st to 3rd order of the satellite's navigation message. \n
			:param aiOrder: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ai')
			:return: ai: integer Range: a_i0 (0 to 2047) , a_i1 (-1024 to 1023) , a_i2 (-8192 to 8191)"""
		aiOrder_cmd_val = self._cmd_group.get_repcap_cmd_value(aiOrder, repcap.AiOrder)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:GALileo:NMESsage:FNAV:IONospheric:AI{aiOrder_cmd_val}?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'AiCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AiCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
