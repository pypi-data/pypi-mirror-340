from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExternalCls:
	"""External commands group definition. 3 total commands, 1 Subgroups, 2 group commands
	Repeated Capability: External, default value after init: External.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("external", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_external_get', 'repcap_external_set', repcap.External.Nr1)

	def repcap_external_set(self, external: repcap.External) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to External.Default.
		Default value after init: External.Nr1"""
		self._cmd_group.set_repcap_enum_value(external)

	def repcap_external_get(self) -> repcap.External:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def synchronize(self):
		"""synchronize commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_synchronize'):
			from .Synchronize import SynchronizeCls
			self._synchronize = SynchronizeCls(self._core, self._cmd_group)
		return self._synchronize

	def get_delay(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:TETRa:TRIGger:[EXTernal]:DELay \n
		Snippet: value: float = driver.source.bb.tetra.trigger.external.get_delay() \n
		Sets the trigger delay. \n
			:return: delay: float Range: 0.0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TETRa:TRIGger:EXTernal:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:TETRa:TRIGger:[EXTernal]:DELay \n
		Snippet: driver.source.bb.tetra.trigger.external.set_delay(delay = 1.0) \n
		Sets the trigger delay. \n
			:param delay: float Range: 0.0 to 65535
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:TETRa:TRIGger:EXTernal:DELay {param}')

	def get_inhibit(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:TETRa:TRIGger:[EXTernal]:INHibit \n
		Snippet: value: int = driver.source.bb.tetra.trigger.external.get_inhibit() \n
		Specifies the duration by which a restart is inhibited. \n
			:return: inhibit: integer Range: 0 to 67108863
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TETRa:TRIGger:EXTernal:INHibit?')
		return Conversions.str_to_int(response)

	def set_inhibit(self, inhibit: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:TETRa:TRIGger:[EXTernal]:INHibit \n
		Snippet: driver.source.bb.tetra.trigger.external.set_inhibit(inhibit = 1) \n
		Specifies the duration by which a restart is inhibited. \n
			:param inhibit: integer Range: 0 to 67108863
		"""
		param = Conversions.decimal_value_to_str(inhibit)
		self._core.io.write(f'SOURce<HwInstance>:BB:TETRa:TRIGger:EXTernal:INHibit {param}')

	def clone(self) -> 'ExternalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ExternalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
