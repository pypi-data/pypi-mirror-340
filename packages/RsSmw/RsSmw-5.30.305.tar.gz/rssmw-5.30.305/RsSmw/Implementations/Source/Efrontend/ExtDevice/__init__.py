from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExtDeviceCls:
	"""ExtDevice commands group definition. 9 total commands, 6 Subgroups, 1 group commands
	Repeated Capability: ExternalDevice, default value after init: ExternalDevice.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("extDevice", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_externalDevice_get', 'repcap_externalDevice_set', repcap.ExternalDevice.Nr1)

	def repcap_externalDevice_set(self, externalDevice: repcap.ExternalDevice) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ExternalDevice.Default.
		Default value after init: ExternalDevice.Nr1"""
		self._cmd_group.set_repcap_enum_value(externalDevice)

	def repcap_externalDevice_get(self) -> repcap.ExternalDevice:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def correction(self):
		"""correction commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_correction'):
			from .Correction import CorrectionCls
			self._correction = CorrectionCls(self._core, self._cmd_group)
		return self._correction

	@property
	def frequency(self):
		"""frequency commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import FrequencyCls
			self._frequency = FrequencyCls(self._core, self._cmd_group)
		return self._frequency

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gain'):
			from .Gain import GainCls
			self._gain = GainCls(self._core, self._cmd_group)
		return self._gain

	@property
	def name(self):
		"""name commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_name'):
			from .Name import NameCls
			self._name = NameCls(self._core, self._cmd_group)
		return self._name

	@property
	def refresh(self):
		"""refresh commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_refresh'):
			from .Refresh import RefreshCls
			self._refresh = RefreshCls(self._core, self._cmd_group)
		return self._refresh

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePyCls
			self._typePy = TypePyCls(self._core, self._cmd_group)
		return self._typePy

	def get_list_py(self) -> List[str]:
		"""SCPI: [SOURce<HW>]:EFRontend:EXTDevice:LIST \n
		Snippet: value: List[str] = driver.source.efrontend.extDevice.get_list_py() \n
		Queries the external devices connected to the external frontend in a comma-separated list. \n
			:return: id_pi_db_freq_conv_fes_pi_dev_list: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:EFRontend:EXTDevice:LIST?')
		return Conversions.str_to_str_list(response)

	def clone(self) -> 'ExtDeviceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ExtDeviceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
