from subprocess import check_output, CalledProcessError, STDOUT, Popen, PIPE
from os import remove, getenv
from shutil import copyfile
from distutils.core import Command
from os.path import isfile, join, dirname, realpath, expanduser, basename
from sys import platform, argv
from optparse import OptionParser


class Setup(object):
    @property
    def altera_path(self):
        # makefile to compile, convert, and upload an altera FPGA image to a jtag
        # device memory.
        if platform == "linux" or platform == "linux2":
            return expanduser("~/altera_lite/15.1/quartus/bin")
        else:
            return "C:\\altera_lite\\15.1\quartus\\bin64"
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

def conversion_file(output_jic_filename, sof_filename, eeprom='EPCS64',
                      flash_device='EP4CE22'):
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
        print("cannot identify: |", getenv('USERPROFILE'), "|", setup.tmp_folder)
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


def check_for_errors(result, operation="upload"):
    result = str(result)
    if result.find("0 errors") < 0:
        print(operation+" error detected")
        lines = result.split("\\n")
        for line in lines:
            if line.find("rror") > 0:
                print(line)
        return False
    else:
        print("no error detected in "+operation)
        return True


def format_assembler_step(project_folder, step='quartus_map'):
    setup = Setup()
    project_name = basename(project_folder)
    return [join(setup.altera_path, step), '--read_settings_files=on',
            '--write_settings_files=off', join(project_folder, project_name),
            '-c', project_name]


def run_assembler_step(project_folder, step='quartus_map'):
    setup = Setup()
    parts = format_assembler_step(project_folder, step)
    print(" ".join(parts))
    proc = Popen(parts, stdout=PIPE, stderr=PIPE, shell=setup.run_shell)
    result, stderr = proc.communicate()
    check_for_errors(result, step)


def run_conversion(project_folder, eeprom, flash_device):
    setup = Setup()
    while True:
        project_name = basename(project_folder)
        _output_jic = join(project_folder, 'db', 'output_file.jic')
        _output_sof = join(project_folder, 'output_files',
                           project_name+'.sof')
        cof_fn = conversion_file(output_jic_filename=_output_jic,
                                 sof_filename=_output_sof, eeprom=eeprom,
                                 flash_device=flash_device)

        parts = [join(setup.altera_path, 'quartus_cpf'), '-c', cof_fn]
        try:
            result = check_output(parts, shell=setup.run_shell)
        except CalledProcessError as e:
            result = 'error'
            print("error message: ", e)
            print("Ran into problem on command:")
            print(" ".join(parts))
        converted = check_for_errors(result, "convert")
        # verify that the jic was actually created
        if converted:
            if not isfile(_output_jic):
                print("output jic not found")
                print(" ".join(parts))
                converted = False
        if converted:
            break


def run_upload(project_folder):
    setup = Setup()
    while True:
        project_name = basename(project_folder)
        _db_foldername = join(project_folder, 'db')+"/"
        cdf_filename = target_file(db_foldername=_db_foldername,
                                   eeprom='EPCS64',
                                   flash_device='EP4CE22')
        # this assumes that the usb jtag chain is device 1
        parts = [join(setup.altera_path, 'quartus_pgm'), '-c', '1', cdf_filename]
        try:
            result = check_output(parts, shell=setup.run_shell)
        except CalledProcessError as e:
            # if the upload fails more than once, delete the jic file and try again
            result = "error"
            print("Ran into problem on command:")
            print(" ".join(parts))
            print("error: "+str(e))
            if platform == "linux" or platform == "linux2":
                print("did you add the udev rules to your system? ")
        programmed = check_for_errors(result, "upload")
        if programmed:
            break


def check_jtag():
    setup = Setup()
    parts = [join(setup.altera_path, 'quartus_pgm'), '-l']
    result = check_output(parts, stderr=STDOUT, shell=setup.run_shell)
    if str(result).find("No JTAG hardware available") >= 0:
        print("Plug in jtag!")
        exit()


class CompileOption(OptionParser):
    def __init__(self):
        OptionParser.__init__(self)
        self.add_option("-p", "--project", action="store", dest="project",
                        default=None, metavar='FOLDERNAME',
                        help="The foldername of the project. By default, "
                             "the project entrypoint verilog file is assumed "
                             "to be the same as the foldername.")

        self.add_option("-f", "--flash", action="store", dest="flash_name",
                        default="EP4CE22", metavar='CHIP',
                        help="The name of the flash chip where the image will "
                             "be loaded.")

        self.add_option("-e", "--eeprom", action="store", dest="eeprom_name",
                        default="EPCS64", metavar='CHIP',
                        help="The name of the eeprom chip where the image will "
                             "be loaded.")


def compile():
    parser = CompileOption()
    (options, args) = parser.parse_args()
    if options.project is None:
        raise NameError("Please specify a project directory with --project")
    project = expanduser(options.project)
    # make sure a jtag chain is plugged in
    check_jtag()

    run_assembler_step(project, 'quartus_map')
    run_assembler_step(project, 'quartus_fit')
    run_assembler_step(project, 'quartus_asm')

    # run_assembler_step('quartus_eda')

    # next, convert the sof to a jic
    # generate the sof file
    run_conversion(project, options.eeprom_name, options.flash_name)
    # finally, upload the jic
    run_upload(project)
    # remember to reset the device!

if __name__ == "__main__":
    compile()