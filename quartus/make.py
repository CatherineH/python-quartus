from subprocess import check_output, CalledProcessError, STDOUT, Popen, PIPE
from os.path import isfile, join, expanduser, basename
from sys import platform
from optparse import OptionParser

from quartus import Setup, conversion_file, target_file


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
        self.add_option("-u", "--upload", action="store", dest="project",
                        default=False, metavar='OPTION',
                        help="")
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