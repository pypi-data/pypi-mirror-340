from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RefCls:
	"""Ref commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ref", core, parent)

	# noinspection PyTypeChecker
	def get_source(self) -> enums.RfPortWiringSour:
		"""SCPI: SCONfiguration:RFALignment:SETup:INFO:WIRing:REF:SOURce \n
		Snippet: value: enums.RfPortWiringSour = driver.sconfiguration.rfAlignment.setup.info.wiring.ref.get_source() \n
		Queries if the current instrument uses its own or an external reference signal. \n
			:return: source: PRIMary| EXTernal PRIMary The instrument uses its reference signal and provides it to the other instruments. EXTernal The instrument uses an external reference frequency source, for example from other R&S SMW200A (the one with SCONfiguration:RFALignment:SETup:INFO:WIRing:REF:SOURce PRIMary) or from R&S(R)SMA100B.
		"""
		response = self._core.io.query_str('SCONfiguration:RFALignment:SETup:INFO:WIRing:REF:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.RfPortWiringSour)
