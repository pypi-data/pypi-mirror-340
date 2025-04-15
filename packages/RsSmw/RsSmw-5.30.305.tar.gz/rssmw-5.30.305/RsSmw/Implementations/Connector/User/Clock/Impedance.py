from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ImpedanceCls:
	"""Impedance commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("impedance", core, parent)

	def set(self, impedance: enums.ImpG50G10K, userIx=repcap.UserIx.Default) -> None:
		"""SCPI: CONNector:USER<CH>:CLOCk:IMPedance \n
		Snippet: driver.connector.user.clock.impedance.set(impedance = enums.ImpG50G10K.G10K, userIx = repcap.UserIx.Default) \n
		No command help available \n
			:param impedance: No help available
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
		"""
		param = Conversions.enum_scalar_to_str(impedance, enums.ImpG50G10K)
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		self._core.io.write(f'CONNector:USER{userIx_cmd_val}:CLOCk:IMPedance {param}')

	# noinspection PyTypeChecker
	def get(self, userIx=repcap.UserIx.Default) -> enums.ImpG50G10K:
		"""SCPI: CONNector:USER<CH>:CLOCk:IMPedance \n
		Snippet: value: enums.ImpG50G10K = driver.connector.user.clock.impedance.get(userIx = repcap.UserIx.Default) \n
		No command help available \n
			:param userIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: impedance: No help available"""
		userIx_cmd_val = self._cmd_group.get_repcap_cmd_value(userIx, repcap.UserIx)
		response = self._core.io.query_str(f'CONNector:USER{userIx_cmd_val}:CLOCk:IMPedance?')
		return Conversions.str_to_scalar_enum(response, enums.ImpG50G10K)
