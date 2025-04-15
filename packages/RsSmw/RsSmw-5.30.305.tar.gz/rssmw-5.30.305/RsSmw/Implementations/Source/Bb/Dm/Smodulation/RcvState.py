from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RcvStateCls:
	"""RcvState commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rcvState", core, parent)

	# noinspection PyTypeChecker
	def get(self, rcv_state: enums.DmExtRcvStateType) -> enums.DmExtRcvStateType:
		"""SCPI: [SOURce<HW>]:BB:DM:SMODulation:RCVState \n
		Snippet: value: enums.DmExtRcvStateType = driver.source.bb.dm.smodulation.rcvState.get(rcv_state = enums.DmExtRcvStateType.INValid) \n
		Queries the current state of the receiver of the external data. \n
			:param rcv_state: OFF| OPERational| UFLow| OFLow
			:return: rcv_state: OFF| OPERational| UFLow| OFLow"""
		param = Conversions.enum_scalar_to_str(rcv_state, enums.DmExtRcvStateType)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DM:SMODulation:RCVState? {param}')
		return Conversions.str_to_scalar_enum(response, enums.DmExtRcvStateType)
