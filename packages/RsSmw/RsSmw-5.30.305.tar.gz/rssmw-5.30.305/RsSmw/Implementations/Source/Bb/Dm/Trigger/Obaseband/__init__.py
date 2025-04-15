from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ObasebandCls:
	"""Obaseband commands group definition. 4 total commands, 2 Subgroups, 2 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("obaseband", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def repcap_channel_set(self, channel: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default.
		Default value after init: Channel.Nr1"""
		self._cmd_group.set_repcap_enum_value(channel)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def rdelay(self):
		"""rdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rdelay'):
			from .Rdelay import RdelayCls
			self._rdelay = RdelayCls(self._core, self._cmd_group)
		return self._rdelay

	@property
	def tdelay(self):
		"""tdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdelay'):
			from .Tdelay import TdelayCls
			self._tdelay = TdelayCls(self._core, self._cmd_group)
		return self._tdelay

	def get_delay(self) -> float:
		"""SCPI: [SOURce<HW>]:BB:DM:TRIGger:OBASeband:DELay \n
		Snippet: value: float = driver.source.bb.dm.trigger.obaseband.get_delay() \n
		Specifies the trigger delay (expressed as a number of symbols) for triggering by the trigger signal from the other path. \n
			:return: delay: float Range: 0 to 2147483647
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:TRIGger:OBASeband:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""SCPI: [SOURce<HW>]:BB:DM:TRIGger:OBASeband:DELay \n
		Snippet: driver.source.bb.dm.trigger.obaseband.set_delay(delay = 1.0) \n
		Specifies the trigger delay (expressed as a number of symbols) for triggering by the trigger signal from the other path. \n
			:param delay: float Range: 0 to 2147483647
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:TRIGger:OBASeband:DELay {param}')

	def get_inhibit(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:DM:TRIGger:OBASeband:INHibit \n
		Snippet: value: int = driver.source.bb.dm.trigger.obaseband.get_inhibit() \n
		Specifies the number of symbols by which a restart is inhibited. This command applies only for triggering by the second
		path. \n
			:return: inhibit: integer Range: 0 to 67108863, Unit: symbol
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:TRIGger:OBASeband:INHibit?')
		return Conversions.str_to_int(response)

	def set_inhibit(self, inhibit: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:DM:TRIGger:OBASeband:INHibit \n
		Snippet: driver.source.bb.dm.trigger.obaseband.set_inhibit(inhibit = 1) \n
		Specifies the number of symbols by which a restart is inhibited. This command applies only for triggering by the second
		path. \n
			:param inhibit: integer Range: 0 to 67108863, Unit: symbol
		"""
		param = Conversions.decimal_value_to_str(inhibit)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:TRIGger:OBASeband:INHibit {param}')

	def clone(self) -> 'ObasebandCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ObasebandCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
