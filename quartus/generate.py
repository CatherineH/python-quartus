# generate the new files needed by quartus for compilation
from fnmatch import fnmatch
from os import getenv, remove, listdir, walk
from os.path import expanduser, join, isfile, basename, dirname
from sys import platform
from re import match


class Setup(object):
    """
    Set up path variables for compilation
    """
    def __init__(self):
        self._altera_path = None

    @property
    def altera_path(self):
        # makefile to compile, convert, and upload an altera FPGA image to a
        # jtag device memory.
        if self._altera_path is None:
            found = False
            for path, subdirs, files in walk("/"):
                for x in files:
                    if x.endswith('quartus_stp') and not path.endswith("linux64"):
                        self._altera_path = path
                        found = True
                    if found:
                        break
                if found:
                    break
        return self._altera_path

    @property
    def run_shell(self):
        if platform == "linux" or platform == "linux2":
            return False
        else:
            # windows requires running as shell
            return True

    @property
    def tmp_folder(self):
        if platform == "linux" or platform == "linux2":
            return '/tmp'
        else:
            return join(getenv('USERPROFILE'), 'AppData\Local\Temp')

    @property
    def devices(self):
        filename_synplify = join(dirname(self.altera_path),
                        "common/tcl/internal/nativelink/qeda_synplify.dat")
        lines = open(filename_synplify, "r").read(-1).split("\n")

        copied_lines = []
        for line in lines:
            if line.find("#") != 0:
                copied_lines.append(line)
        return copied_lines

    def lookup_device(self, device):
        lines = self.devices

        for line in lines:
            parts = line.split(":")
            if len(parts) < 2:
                continue
            _family = parts[0]
            _device = parts[1]
            if _device == "AUTO":
                continue
            _match = match(_device, device)
            if _match is not None:
                return _family
        return None


def settings_file(output_qsf_filename, device='EP4CE22F17C6'):
    """
    Generates a settings file. Assumes that the project name is the basename of
     output_qsf_filename.

    Does the output settings file must be in the same directory as the project?

    :param str output_qsf_filename: the output filename. At the moment,
     it must be in the same folder as the project
    :param str device: the altera device part number
    """
    project_dir = dirname(output_qsf_filename)
    filetypes = [('v', 'VERILOG'), ('vh', 'VERILOG'),
                 ('tcl', 'SOURCE_TCL_SCRIPT'),
                 ('bdf', 'BDF'), ('bsf', 'BSF'), ('h', 'SOURCE')]
    
    def format_output(values):
        output = ''
        for item in values:
            output += 'set_global_assignment -name '+item[0]+' '+item[1]+'\n'
        return output
    _names = []
    top_level_entry = basename(output_qsf_filename).replace(".qsf", "")
    _setup = Setup()
    _family = _setup.lookup_device(device)
    # Cyclone IV E
    _names.append(('FAMILY', '"'+_family+'"'))
    _names.append(('DEVICE', device))
    _names.append(('TOP_LEVEL_ENTITY', top_level_entry))
    # add any found verilog and tcl files
    for _file in listdir(project_dir):
        for filetype in filetypes:
            if fnmatch(_file, '*.'+filetype[0]):
                _names.append((filetype[1]+'_FILE', join(project_dir, _file)))

    _file = open(output_qsf_filename, 'w+')
    _file.write(format_output(_names))
    _file.close()


def conversion_file(output_jic_filename, sof_filename, eeprom='EPCS64',
                      flash_device='EP4CE22'):
    """
    Create the conversion file between the eeprom .sof file and the flash
    memory device jic.
    :param output_jic_filename: The target output filename
    :type output_jic_filename: str
    :param sof_filename: The compiled SRAM object file.
    :type sof_filename: str
    :param eeprom: The name of the eeprom chip.
    :type eeprom: str
    :param flash_device: The name of flash chip.
    :type flash_device: str
    :return: The filename of the conversion file.
    :rtype: str
    """
    setup = Setup()
    output = '<?xml version="1.0" encoding="US-ASCII" standalone="yes"?>\n' \
             '<cof>\n' \
             '  <eprom_name>'+eeprom+'</eprom_name>\n' \
             '  <flash_loader_device>'+flash_device+'</flash_loader_device>\n' \
             '	<output_filename>'+output_jic_filename+'</output_filename>\n' \
             '	<n_pages>1</n_pages>\n' \
             '	<width>1</width>\n' \
             '	<mode>7</mode>\n' \
             '	<sof_data>\n' \
             '		<user_name>Page_0</user_name>\n' \
             '		<page_flags>1</page_flags>\n' \
             '		<bit0>\n' \
             '			<sof_filename>'+sof_filename+'</sof_filename>\n' \
             '		</bit0>\n' \
             '	</sof_data>\n' \
             '	<version>9</version>\n' \
             '	<create_cvp_file>0</create_cvp_file>\n' \
             '	<create_hps_iocsr>0</create_hps_iocsr>\n' \
             '	<auto_create_rpd>0</auto_create_rpd>\n' \
             '	<create_fif_file>0</create_fif_file>\n' \
             '	<options>\n' \
             '		<map_file>1</map_file>\n' \
             '	</options>\n' \
             '	<advanced_options>\n' \
             '		<ignore_epcs_id_check>2</ignore_epcs_id_check>\n' \
             '		<ignore_condone_check>2</ignore_condone_check>\n' \
             '		<plc_adjustment>0</plc_adjustment>\n' \
             '		<post_chain_bitstream_pad_bytes>-1' \
             '</post_chain_bitstream_pad_bytes>\n' \
             '		<post_device_bitstream_pad_bytes>-1' \
             '</post_device_bitstream_pad_bytes>\n' \
             '		<bitslice_pre_padding>1</bitslice_pre_padding>\n' \
             '	</advanced_options>\n' \
             '</cof>\n'
    filename = join(setup.tmp_folder, 'conversion_setup.cof')
    if isfile(filename):
        remove(filename)
    try:
        _file = open(filename, 'w+')
        _file.write(output)
        _file.close()
    except IOError as e:
        print("cannot identify: |", getenv('USERPROFILE'), "|",
              setup.tmp_folder)
    return filename


def target_file(db_foldername, eeprom='EPCS64', flash_device='EP4CE22'):
    setup = Setup()
    output = 'JedecChain;\n' \
             '	FileRevision(JESD32A);\n' \
             '	DefaultMfr(6E);\n' \
             '	P ActionCode(Cfg)\n' \
             '		Device PartName('+flash_device+')' \
             'Path(\"'+db_foldername+'\")' \
             'File(\"output_file.jic\") MfrSpec' \
             '		(OpMask(1) SEC_Device('+eeprom+') Child_OpMask(1 ' \
             '7));\n' \
             'ChainEnd;\n' \
             'AlteraBegin;\n' \
             '	ChainType(JTAG);\n' \
             'AlteraEnd;\n'
    filename = join(setup.tmp_folder, 'target_memory.cdf')
    if isfile(filename):
        remove(filename)
    _file = open(filename, 'w+')
    _file.write(output)
    _file.close()
    return filename

