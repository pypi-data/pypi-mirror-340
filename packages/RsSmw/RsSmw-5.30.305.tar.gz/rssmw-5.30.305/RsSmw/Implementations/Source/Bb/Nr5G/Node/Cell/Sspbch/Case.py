from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CaseCls:
	"""Case commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("case", core, parent)

	def set(self, pbsch_case: enums.Nr5GpbschCase, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:CASE \n
		Snippet: driver.source.bb.nr5G.node.cell.sspbch.case.set(pbsch_case = enums.Nr5GpbschCase.A, cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Selects one of the SS/PBCH cases, as specified in . \n
			:param pbsch_case: A|B|C|D|E F|G Requires R&S SMW-K171.
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
		"""
		param = Conversions.enum_scalar_to_str(pbsch_case, enums.Nr5GpbschCase)
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:CASE {param}')

	# noinspection PyTypeChecker
	def get(self, cellNull=repcap.CellNull.Default, indexNull=repcap.IndexNull.Default) -> enums.Nr5GpbschCase:
		"""SCPI: [SOURce<HW>]:BB:NR5G:NODE:CELL<CC(CH0)>:SSPBch<SSB(ST0)>:CASE \n
		Snippet: value: enums.Nr5GpbschCase = driver.source.bb.nr5G.node.cell.sspbch.case.get(cellNull = repcap.CellNull.Default, indexNull = repcap.IndexNull.Default) \n
		Selects one of the SS/PBCH cases, as specified in . \n
			:param cellNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Cell')
			:param indexNull: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Sspbch')
			:return: pbsch_case: A|B|C|D|E F|G Requires R&S SMW-K171."""
		cellNull_cmd_val = self._cmd_group.get_repcap_cmd_value(cellNull, repcap.CellNull)
		indexNull_cmd_val = self._cmd_group.get_repcap_cmd_value(indexNull, repcap.IndexNull)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{cellNull_cmd_val}:SSPBch{indexNull_cmd_val}:CASE?')
		return Conversions.str_to_scalar_enum(response, enums.Nr5GpbschCase)
