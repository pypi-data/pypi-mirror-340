from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LeapCls:
	"""Leap commands group definition. 5 total commands, 2 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("leap", core, parent)

	@property
	def date(self):
		"""date commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_date'):
			from .Date import DateCls
			self._date = DateCls(self._core, self._cmd_group)
		return self._date

	@property
	def seconds(self):
		"""seconds commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_seconds'):
			from .Seconds import SecondsCls
			self._seconds = SecondsCls(self._core, self._cmd_group)
		return self._seconds

	def get_state(self) -> bool:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:INDependent:LEAP:STATe \n
		Snippet: value: bool = driver.source.bb.gnss.time.conversion.independent.leap.get_state() \n
		Enables the leap second transition. \n
			:return: state: 1| ON| 0| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:INDependent:LEAP:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:INDependent:LEAP:STATe \n
		Snippet: driver.source.bb.gnss.time.conversion.independent.leap.set_state(state = False) \n
		Enables the leap second transition. \n
			:param state: 1| ON| 0| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:INDependent:LEAP:STATe {param}')

	# noinspection PyTypeChecker
	def get_system(self) -> enums.HybridLs:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:INDependent:LEAP:SYSTem \n
		Snippet: value: enums.HybridLs = driver.source.bb.gnss.time.conversion.independent.leap.get_system() \n
		Queries the GNSS for leap second transition that is the BeiDou GNSS. \n
			:return: system: BEIDou
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:INDependent:LEAP:SYSTem?')
		return Conversions.str_to_scalar_enum(response, enums.HybridLs)

	def set_system(self, system: enums.HybridLs) -> None:
		"""SCPI: [SOURce<HW>]:BB:GNSS:TIME:CONVersion:INDependent:LEAP:SYSTem \n
		Snippet: driver.source.bb.gnss.time.conversion.independent.leap.set_system(system = enums.HybridLs.BEIDou) \n
		Queries the GNSS for leap second transition that is the BeiDou GNSS. \n
			:param system: BEIDou
		"""
		param = Conversions.enum_scalar_to_str(system, enums.HybridLs)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:INDependent:LEAP:SYSTem {param}')

	def clone(self) -> 'LeapCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LeapCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
