from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TgdCls:
	"""Tgd commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tgd", core, parent)

	def set(self, tgd: int, mobileStation=repcap.MobileStation.Default, patternIx=repcap.PatternIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:CMODe:PATTern<CH>:TGD \n
		Snippet: driver.source.bb.w3Gpp.mstation.cmode.pattern.tgd.set(tgd = 1, mobileStation = repcap.MobileStation.Default, patternIx = repcap.PatternIx.Default) \n
		Sets the transmission gap distances. \n
			:param tgd: integer Range: 3 to 100
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param patternIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pattern')
		"""
		param = Conversions.decimal_value_to_str(tgd)
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		patternIx_cmd_val = self._cmd_group.get_repcap_cmd_value(patternIx, repcap.PatternIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:CMODe:PATTern{patternIx_cmd_val}:TGD {param}')

	def get(self, mobileStation=repcap.MobileStation.Default, patternIx=repcap.PatternIx.Default) -> int:
		"""SCPI: [SOURce<HW>]:BB:W3GPp:MSTation<ST>:CMODe:PATTern<CH>:TGD \n
		Snippet: value: int = driver.source.bb.w3Gpp.mstation.cmode.pattern.tgd.get(mobileStation = repcap.MobileStation.Default, patternIx = repcap.PatternIx.Default) \n
		Sets the transmission gap distances. \n
			:param mobileStation: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param patternIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pattern')
			:return: tgd: integer Range: 3 to 100"""
		mobileStation_cmd_val = self._cmd_group.get_repcap_cmd_value(mobileStation, repcap.MobileStation)
		patternIx_cmd_val = self._cmd_group.get_repcap_cmd_value(patternIx, repcap.PatternIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{mobileStation_cmd_val}:CMODe:PATTern{patternIx_cmd_val}:TGD?')
		return Conversions.str_to_int(response)
