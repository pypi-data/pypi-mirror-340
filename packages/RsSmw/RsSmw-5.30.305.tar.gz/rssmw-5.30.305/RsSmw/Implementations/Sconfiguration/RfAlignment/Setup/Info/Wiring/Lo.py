from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LoCls:
	"""Lo commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lo", core, parent)

	# noinspection PyTypeChecker
	def get_constellation(self) -> enums.RfPortWiringConf:
		"""SCPI: SCONfiguration:RFALignment:SETup:INFO:WIRing:LO:CONStellation \n
		Snippet: value: enums.RfPortWiringConf = driver.sconfiguration.rfAlignment.setup.info.wiring.lo.get_constellation() \n
		Queries the connection method used to distribute the LO frequency signal. \n
			:return: constellation: DCHain| STAR DCHain Daisy chain STAR Star
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:INFO:WIRing:LO:CONStellation?')
		return Conversions.str_to_scalar_enum(response, enums.RfPortWiringConf)

	# noinspection PyTypeChecker
	def get_source(self) -> enums.RfPortWiringSour:
		"""SCPI: SCONfiguration:RFALignment:SETup:INFO:WIRing:LO:SOURce \n
		Snippet: value: enums.RfPortWiringSour = driver.sconfiguration.rfAlignment.setup.info.wiring.lo.get_source() \n
		Queries if the current instrument uses its own or an external LO signal. \n
			:return: source: PRIMary| EXTernal PRIMary The instrument uses its LO signal and provides it to the other instruments. EXTernal The instrument uses an external LO signal, for example from other R&S SMW200A (the one with SCONfiguration:RFALignment:SETup:INFO:WIRing:LO:SOURce PRIMary) .
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:INFO:WIRing:LO:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.RfPortWiringSour)
