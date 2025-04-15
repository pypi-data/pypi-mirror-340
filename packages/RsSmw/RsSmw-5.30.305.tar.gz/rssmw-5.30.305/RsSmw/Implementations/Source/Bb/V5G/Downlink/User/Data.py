from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DataCls:
	"""Data commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("data", core, parent)

	def set(self, data: enums.DataSourceA, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:USER<CH>:DATA \n
		Snippet: driver.source.bb.v5G.downlink.user.data.set(data = enums.DataSourceA.DLISt, userIx = repcap.UserIx.Default) \n
		Selects the data source for the selected user configuration. \n
			:param data: PN9| PN11| PN15| PN16| PN20| PN21| PN23| PATTern| DLISt| ZERO| ONE PNxx Pseudo-random bit sequences (PRBS) of a length of xx bits. The length in bit can be 9, 11, 15, 16, 20, 21, or 23. PATTern User-defined pattern. The pattern can be specified via: [:SOURcehw]:BB:V5G:DL:USERch:PATTern DLISt Internal data list is used. The data list can be specified via: [:SOURcehw]:BB:V5G:DL:USERch:DSELect ZERO / ONE All 0 or all 1 pattern
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.enum_scalar_to_str(data, enums.DataSourceA)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:DL:USER{userIx_cmd_val}:DATA {param}')

	# noinspection PyTypeChecker
	def get(self, userIx=repcap.UserIx.Default) -> enums.DataSourceA:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:USER<CH>:DATA \n
		Snippet: value: enums.DataSourceA = driver.source.bb.v5G.downlink.user.data.get(userIx = repcap.UserIx.Default) \n
		Selects the data source for the selected user configuration. \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: data: PN9| PN11| PN15| PN16| PN20| PN21| PN23| PATTern| DLISt| ZERO| ONE PNxx Pseudo-random bit sequences (PRBS) of a length of xx bits. The length in bit can be 9, 11, 15, 16, 20, 21, or 23. PATTern User-defined pattern. The pattern can be specified via: [:SOURcehw]:BB:V5G:DL:USERch:PATTern DLISt Internal data list is used. The data list can be specified via: [:SOURcehw]:BB:V5G:DL:USERch:DSELect ZERO / ONE All 0 or all 1 pattern"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:V5G:DL:USER{userIx_cmd_val}:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.DataSourceA)
