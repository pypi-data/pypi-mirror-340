from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OutputCls:
	"""Output commands group definition. 16 total commands, 7 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("output", core, parent)

	@property
	def afixed(self):
		"""afixed commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_afixed'):
			from .Afixed import AfixedCls
			self._afixed = AfixedCls(self._core, self._cmd_group)
		return self._afixed

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .All import AllCls
			self._all = AllCls(self._core, self._cmd_group)
		return self._all

	@property
	def blank(self):
		"""blank commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_blank'):
			from .Blank import BlankCls
			self._blank = BlankCls(self._core, self._cmd_group)
		return self._blank

	@property
	def protection(self):
		"""protection commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_protection'):
			from .Protection import ProtectionCls
			self._protection = ProtectionCls(self._core, self._cmd_group)
		return self._protection

	@property
	def tm(self):
		"""tm commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tm'):
			from .Tm import TmCls
			self._tm = TmCls(self._core, self._cmd_group)
		return self._tm

	@property
	def user(self):
		"""user commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_user'):
			from .User import UserCls
			self._user = UserCls(self._core, self._cmd_group)
		return self._user

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	# noinspection PyTypeChecker
	def get_amode(self) -> enums.PowAttModeSzu:
		"""SCPI: OUTPut<HW>:AMODe \n
		Snippet: value: enums.PowAttModeSzu = driver.output.get_amode() \n
		Sets the step attenuator mode at the RF output. Note: The setting [:SOURce<hw>]:POWer:ATTenuation:RFOFf:MODE FATTenuation
		has higher priority than the attenuator modes FIXed and MANual. \n
			:return: amode: FIXed| MANual| AUTO AUTO The step attenuator adjusts the level settings automatically, within the full variation range. FIXed The step attenuator and amplifier stages are fixed at the current position, providing level settings with constant output VSWR. The resulting variation range is calculated according to the position. To use this mode, activate the ALC (see [:SOURcehw]:POWer:ALC[:STATe]) . MANual You can set the level manually, in 10 dB steps.
		"""
		response = self._core.io.query_str('OUTPut<HwInstance>:AMODe?')
		return Conversions.str_to_scalar_enum(response, enums.PowAttModeSzu)

	def set_amode(self, amode: enums.PowAttModeSzu) -> None:
		"""SCPI: OUTPut<HW>:AMODe \n
		Snippet: driver.output.set_amode(amode = enums.PowAttModeSzu.AUTO) \n
		Sets the step attenuator mode at the RF output. Note: The setting [:SOURce<hw>]:POWer:ATTenuation:RFOFf:MODE FATTenuation
		has higher priority than the attenuator modes FIXed and MANual. \n
			:param amode: FIXed| MANual| AUTO AUTO The step attenuator adjusts the level settings automatically, within the full variation range. FIXed The step attenuator and amplifier stages are fixed at the current position, providing level settings with constant output VSWR. The resulting variation range is calculated according to the position. To use this mode, activate the ALC (see [:SOURcehw]:POWer:ALC[:STATe]) . MANual You can set the level manually, in 10 dB steps.
		"""
		param = Conversions.enum_scalar_to_str(amode, enums.PowAttModeSzu)
		self._core.io.write(f'OUTPut<HwInstance>:AMODe {param}')

	# noinspection PyTypeChecker
	def get_impedance(self) -> enums.InputImpRf:
		"""SCPI: OUTPut<HW>:IMPedance \n
		Snippet: value: enums.InputImpRf = driver.output.get_impedance() \n
		Queries the impedance of the RF outputs. \n
			:return: impedance: G1K| G50| G10K
		"""
		response = self._core.io.query_str('OUTPut<HwInstance>:IMPedance?')
		return Conversions.str_to_scalar_enum(response, enums.InputImpRf)

	def clone(self) -> 'OutputCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = OutputCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
