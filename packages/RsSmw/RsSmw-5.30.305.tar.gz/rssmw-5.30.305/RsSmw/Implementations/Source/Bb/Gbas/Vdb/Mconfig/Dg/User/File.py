from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FileCls:
	"""File commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("file", core, parent)

	def set(self, filename: str, vdbTransmitter=repcap.VdbTransmitter.Default) -> None:
		"""SCPI: [SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:DG:USER:FILE \n
		Snippet: driver.source.bb.gbas.vdb.mconfig.dg.user.file.set(filename = 'abc', vdbTransmitter = repcap.VdbTransmitter.Default) \n
		Loads the selected user-defined file (extension *.rs_gbas) . Per default, the instrument saves user-defined files in the
		/var/user/ directory. Use the command method RsSmw.MassMemory.currentDirectory to change the default directory to the
		currently used one. \n
			:param filename: string For files saved in the default directory, only the file name is required.
			:param vdbTransmitter: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
		"""
		param = Conversions.value_to_quoted_str(filename)
		vdbTransmitter_cmd_val = self._cmd_group.get_repcap_cmd_value(vdbTransmitter, repcap.VdbTransmitter)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{vdbTransmitter_cmd_val}:MCONfig:DG:USER:FILE {param}')
