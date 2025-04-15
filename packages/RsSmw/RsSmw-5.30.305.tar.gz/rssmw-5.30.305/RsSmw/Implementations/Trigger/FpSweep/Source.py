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

	def set(self, fp_trig_source: enums.SingExtAuto, inputIx=repcap.InputIx.Default) -> None:
		"""SCPI: TRIGger<HW>:FPSWeep:SOURce \n
		Snippet: driver.trigger.fpSweep.source.set(fp_trig_source = enums.SingExtAuto.AUTO, inputIx = repcap.InputIx.Default) \n
		No command help available \n
			:param fp_trig_source: No help available
			:param inputIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trigger')
		"""
		param = Conversions.enum_scalar_to_str(fp_trig_source, enums.SingExtAuto)
		inputIx_cmd_val = self._cmd_group.get_repcap_cmd_value(inputIx, repcap.InputIx)
		self._core.io.write(f'TRIGger{inputIx_cmd_val}:FPSWeep:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self, inputIx=repcap.InputIx.Default) -> enums.SingExtAuto:
		"""SCPI: TRIGger<HW>:FPSWeep:SOURce \n
		Snippet: value: enums.SingExtAuto = driver.trigger.fpSweep.source.get(inputIx = repcap.InputIx.Default) \n
		No command help available \n
			:param inputIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trigger')
			:return: fp_trig_source: No help available"""
		inputIx_cmd_val = self._cmd_group.get_repcap_cmd_value(inputIx, repcap.InputIx)
		response = self._core.io.query_str(f'TRIGger{inputIx_cmd_val}:FPSWeep:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SingExtAuto)
