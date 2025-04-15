from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DirectionCls:
	"""Direction commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("direction", core, parent)

	# noinspection PyTypeChecker
	def get(self, digitalIq=repcap.DigitalIq.Default) -> enums.SystConfConnDigStat:
		"""SCPI: SCONfiguration:EXTernal:FADer<CH>:DIRection \n
		Snippet: value: enums.SystConfConnDigStat = driver.sconfiguration.external.fader.direction.get(digitalIq = repcap.DigitalIq.Default) \n
		Queries the connector direction. \n
			:param digitalIq: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fader')
			:return: direction: NONE| IN| OUT"""
		digitalIq_cmd_val = self._cmd_group.get_repcap_cmd_value(digitalIq, repcap.DigitalIq)
		response = self._core.io.query_str(f'SCONfiguration:EXTernal:FADer{digitalIq_cmd_val}:DIRection?')
		return Conversions.str_to_scalar_enum(response, enums.SystConfConnDigStat)
