from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardCls:
	"""Standard commands group definition. 5 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("standard", core, parent)

	@property
	def ulist(self):
		"""ulist commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_ulist'):
			from .Ulist import UlistCls
			self._ulist = UlistCls(self._core, self._cmd_group)
		return self._ulist

	# noinspection PyTypeChecker
	def get_value(self) -> enums.DmStan:
		"""SCPI: [SOURce<HW>]:BB:DM:STANdard \n
		Snippet: value: enums.DmStan = driver.source.bb.dm.standard.get_value() \n
		Selects predefined set of settings according to the selected standard, see Table 'Predefined settings for communication
		standards'. \n
			:return: standard: USER| BLUetooth| DECT| ETC| GSM| GSMEdge| NADC| PDC| PHS| TETRa| W3GPp| TDSCdma| CFORward| CREVerse| WORLdspace| TFTS| APCOPH1C4fm| APCOPH1CQpsk| APCOPH2HCpm| APCOPH2HDQpsk| APCOPH2HD8PSKW| APCOPH2HD8PSKN| APCOPH1Lsm| APCOPH1Wcqpsk| CWBPsk| SOQPSKTG A query returns the value USER if settings deviate from standard-compliant settings.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:STANdard?')
		return Conversions.str_to_scalar_enum(response, enums.DmStan)

	def set_value(self, standard: enums.DmStan) -> None:
		"""SCPI: [SOURce<HW>]:BB:DM:STANdard \n
		Snippet: driver.source.bb.dm.standard.set_value(standard = enums.DmStan.APCOPH1C4fm) \n
		Selects predefined set of settings according to the selected standard, see Table 'Predefined settings for communication
		standards'. \n
			:param standard: USER| BLUetooth| DECT| ETC| GSM| GSMEdge| NADC| PDC| PHS| TETRa| W3GPp| TDSCdma| CFORward| CREVerse| WORLdspace| TFTS| APCOPH1C4fm| APCOPH1CQpsk| APCOPH2HCpm| APCOPH2HDQpsk| APCOPH2HD8PSKW| APCOPH2HD8PSKN| APCOPH1Lsm| APCOPH1Wcqpsk| CWBPsk| SOQPSKTG A query returns the value USER if settings deviate from standard-compliant settings.
		"""
		param = Conversions.enum_scalar_to_str(standard, enums.DmStan)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:STANdard {param}')

	def clone(self) -> 'StandardCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = StandardCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
