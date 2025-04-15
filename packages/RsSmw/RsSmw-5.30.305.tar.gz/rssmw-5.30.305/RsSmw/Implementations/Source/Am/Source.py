from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	def set(self, source: enums.AmSour, generatorIx=repcap.GeneratorIx.Default) -> None:
		"""SCPI: [SOURce<HW>]:AM<CH>:SOURce \n
		Snippet: driver.source.am.source.set(source = enums.AmSour.EXT1, generatorIx = repcap.GeneratorIx.Default) \n
		Selects the modulation source for amplitude modulation. \n
			:param source: LF1| LF2| NOISe| EXT1| EXT2| EXTernal| INTernal LF1|LF2 Uses an internally generated LF signal. EXT1|EXT2 Uses an externally supplied LF signal. NOISe Uses the internally generated noise signal. INTernal Uses the internally generated signal of LF1. EXTernal Uses an external LF signal (EXT1) .
			:param generatorIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Am')
		"""
		param = Conversions.enum_scalar_to_str(source, enums.AmSour)
		generatorIx_cmd_val = self._cmd_group.get_repcap_cmd_value(generatorIx, repcap.GeneratorIx)
		self._core.io.write(f'SOURce<HwInstance>:AM{generatorIx_cmd_val}:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self, generatorIx=repcap.GeneratorIx.Default) -> enums.AmSour:
		"""SCPI: [SOURce<HW>]:AM<CH>:SOURce \n
		Snippet: value: enums.AmSour = driver.source.am.source.get(generatorIx = repcap.GeneratorIx.Default) \n
		Selects the modulation source for amplitude modulation. \n
			:param generatorIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Am')
			:return: source: LF1| LF2| NOISe| EXT1| EXT2| EXTernal| INTernal LF1|LF2 Uses an internally generated LF signal. EXT1|EXT2 Uses an externally supplied LF signal. NOISe Uses the internally generated noise signal. INTernal Uses the internally generated signal of LF1. EXTernal Uses an external LF signal (EXT1) ."""
		generatorIx_cmd_val = self._cmd_group.get_repcap_cmd_value(generatorIx, repcap.GeneratorIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:AM{generatorIx_cmd_val}:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.AmSour)
