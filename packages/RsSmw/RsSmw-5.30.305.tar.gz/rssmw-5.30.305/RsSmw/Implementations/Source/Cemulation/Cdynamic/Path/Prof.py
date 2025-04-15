from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ProfCls:
	"""Prof commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("prof", core, parent)

	def set(self, prof: enums.FadProfUdyn, path=repcap.Path.Default) -> None:
		"""SCPI: [SOURce<HW>]:CEMulation:CDYNamic:PATH<CH>:PROF \n
		Snippet: driver.source.cemulation.cdynamic.path.prof.set(prof = enums.FadProfUdyn.PDOPpler, path = repcap.Path.Default) \n
		No command help available \n
			:param prof: No help available
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Path')
		"""
		param = Conversions.enum_scalar_to_str(prof, enums.FadProfUdyn)
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		self._core.io.write(f'SOURce<HwInstance>:CEMulation:CDYNamic:PATH{path_cmd_val}:PROF {param}')

	# noinspection PyTypeChecker
	def get(self, path=repcap.Path.Default) -> enums.FadProfUdyn:
		"""SCPI: [SOURce<HW>]:CEMulation:CDYNamic:PATH<CH>:PROF \n
		Snippet: value: enums.FadProfUdyn = driver.source.cemulation.cdynamic.path.prof.get(path = repcap.Path.Default) \n
		No command help available \n
			:param path: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Path')
			:return: prof: No help available"""
		path_cmd_val = self._cmd_group.get_repcap_cmd_value(path, repcap.Path)
		response = self._core.io.query_str(f'SOURce<HwInstance>:CEMulation:CDYNamic:PATH{path_cmd_val}:PROF?')
		return Conversions.str_to_scalar_enum(response, enums.FadProfUdyn)
