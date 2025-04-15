from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TxmCls:
	"""Txm commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("txm", core, parent)

	def set(self, tx_mode: enums.V5GtxMode, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:USER<CH>:TXM \n
		Snippet: driver.source.bb.v5G.downlink.user.txm.set(tx_mode = enums.V5GtxMode.M1, userIx = repcap.UserIx.Default) \n
		Queries the transmission mode of the corresponding user as defined in specification. \n
			:param tx_mode: M1| M2| M3
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.enum_scalar_to_str(tx_mode, enums.V5GtxMode)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:V5G:DL:USER{userIx_cmd_val}:TXM {param}')

	# noinspection PyTypeChecker
	def get(self, userIx=repcap.UserIx.Default) -> enums.V5GtxMode:
		"""SCPI: [SOURce<HW>]:BB:V5G:DL:USER<CH>:TXM \n
		Snippet: value: enums.V5GtxMode = driver.source.bb.v5G.downlink.user.txm.get(userIx = repcap.UserIx.Default) \n
		Queries the transmission mode of the corresponding user as defined in specification. \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: tx_mode: M1| M2| M3"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:V5G:DL:USER{userIx_cmd_val}:TXM?')
		return Conversions.str_to_scalar_enum(response, enums.V5GtxMode)
