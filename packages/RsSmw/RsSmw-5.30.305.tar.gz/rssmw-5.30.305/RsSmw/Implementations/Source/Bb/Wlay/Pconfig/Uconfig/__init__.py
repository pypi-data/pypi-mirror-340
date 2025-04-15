from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UconfigCls:
	"""Uconfig commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("uconfig", core, parent)

	@property
	def mimo(self):
		"""mimo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mimo'):
			from .Mimo import MimoCls
			self._mimo = MimoCls(self._core, self._cmd_group)
		return self._mimo

	@property
	def user(self):
		"""user commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_user'):
			from .User import UserCls
			self._user = UserCls(self._core, self._cmd_group)
		return self._user

	def get_us_id(self) -> int:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:UCONfig:USID \n
		Snippet: value: int = driver.source.bb.wlay.pconfig.uconfig.get_us_id() \n
		Sets the station ID, the 11 least significant bits of the association identifier (AID) . \n
			:return: usr_state_id: integer Range: 1 to 2047
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAY:PCONfig:UCONfig:USID?')
		return Conversions.str_to_int(response)

	def set_us_id(self, usr_state_id: int) -> None:
		"""SCPI: [SOURce<HW>]:BB:WLAY:PCONfig:UCONfig:USID \n
		Snippet: driver.source.bb.wlay.pconfig.uconfig.set_us_id(usr_state_id = 1) \n
		Sets the station ID, the 11 least significant bits of the association identifier (AID) . \n
			:param usr_state_id: integer Range: 1 to 2047
		"""
		param = Conversions.decimal_value_to_str(usr_state_id)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAY:PCONfig:UCONfig:USID {param}')

	def clone(self) -> 'UconfigCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = UconfigCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
