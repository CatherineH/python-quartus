from os import listdir
from subprocess import check_output, CalledProcessError, STDOUT, Popen, PIPE
from os.path import isfile, join, expanduser, basename, isdir
from sys import platform
from optparse import OptionParser
import logging
from shutil import copytree, rmtree, copy
from time import time

from quartus import Setup, conversion_file, target_file, settings_file


def check_for_errors(result):
    result = str(result)
    if result.find(" 0 errors") < 0:
        lines = result.split("\n")
        if len(lines) == 1:
            lines = lines[0].split("\\n")

        for line in lines:
            if line.find("Error (") == 0:
                print('\033[1;31m'+line+'\033[0m')
            elif line.find("Warning") == 0:
                print('\033[1;33m'+line+'\033[0m')
        return False
    else:
        return True


def format_assembler_step(options, step='quartus_map'):
    setup = Setup()
    project_name = basename(options.project)
    parts = [join(setup.altera_path, step), '--read_settings_files=on',
             '--write_settings_files=off']
    if options.parallel > 1:
        parts.append('--parallel='+str(options.parallel))
    parts.append(join(options.project, project_name))
    return parts


def run_assembler_step(options, step='quartus_map'):
    if options.time:
        start = time()
    setup = Setup()
    parts = format_assembler_step(options, step)
    print(" ".join(parts))
    procedure = Popen(parts, stdout=PIPE, stderr=PIPE, shell=setup.run_shell)
    result, error = procedure.communicate()
    #print("result: ", result)
    #print("error: ", error)
    _return_values = check_for_errors(result)
    if options.time:
        end = time()
        line = "Time elapsed: "+str(step)+" "+str(end-start)
        print('\033[1;96m'+line+'\033[0m')
    return _return_values


def run_conversion(options):
    setup = Setup()
    project_name = basename(options.project)
    _output_jic = join(options.project, 'db', 'output_file.jic')
    _output_sof = join(options.project, project_name+'.sof')
    cof_fn = conversion_file(output_jic_filename=_output_jic,
                             sof_filename=_output_sof,
                             eeprom=options.eeprom_name,
                             flash_device=options.flash_name)

    parts = [join(setup.altera_path, 'quartus_cpf'), '-c', cof_fn]
    proc = Popen(parts, stdout=PIPE, stderr=PIPE, shell=setup.run_shell)
    result, stderr = proc.communicate()

    return check_for_errors(result)


def run_upload(options, log=False):
    """
    Generate target file and continuously attempt to upload until it succeeds.

    :param CompileOption options: the compilation options.
    :param TextIOWrapper log_fh: If present, the number of failures and elapsed time
    will be recorded.
    """
    setup = Setup()
    num_failures = 0
    while True:
        start_upload = time()
        _db_foldername = join(options.project, 'db')+"/"
        cdf_filename = target_file(db_foldername=_db_foldername,
                                   eeprom=options.eeprom_name,
                                   flash_device=options.flash_name)
        # this assumes that the usb jtag chain is device 1
        parts = [join(setup.altera_path, 'quartus_pgm'), '-c', '1',
                 cdf_filename]
        try:
            result = check_output(parts, shell=setup.run_shell)
        except CalledProcessError as e:
            num_failures += 1
            end_upload = time()
            if log:
                logging.warning("Upload failed: "+str(num_failures)+" times, elapsed: " +
                             str(end_upload-start_upload) + ".\n")
            result = "error"
            print("Ran into problem on command:")
            print(" ".join(parts))
            print("error: "+str(e))
            if platform == "linux" or platform == "linux2":
                print("did you add the udev rules to your system? ")
        programmed = check_for_errors(result)
        if programmed:
            break


def check_jtag():
    """
    Make sure that a jtag cable is plugged in.
    """
    setup = Setup()
    parts = [join(setup.altera_path, 'quartus_pgm'), '-l']
    result = check_output(parts, stderr=STDOUT, shell=setup.run_shell)
    if str(result).find("No JTAG hardware available") >= 0:
        print("Plug in jtag!")
        exit()


class CompileOption(OptionParser):
    def __init__(self):
        OptionParser.__init__(self)
        self.add_option("-c", "--clear", action="store_true", dest="clear",
                        default=False, metavar='OPTION',
                        help="If the tag is present, any existing generated "
                             "files will be cleared. bloop")
        self.add_option("-d", "--device", action="store", dest="device_name",
                        default="EP4CE22F17C6", metavar='CHIP',
                        help="The name of the target device.")
        self.add_option("-e", "--eeprom", action="store", dest="eeprom_name",
                        default="EPCS64", metavar='CHIP',
                        help="The name of the eeprom chip where the image "
                             "will be loaded.")
        self.add_option("-i", "--include", action="store", dest="include_dirs",
                        help="A list of folders to include. Deliminate multiple "
                             "directories by a comma.")
        self.add_option("-l", "--log", action="store_true", dest="logging",
                        default=False, metavar='OPTION',
                        help="If the tag is present, this build will be logged.")
        self.add_option("--parallel", action="store", dest="parallel",
                        default=1, metavar='NUM_PROCESSORS',
                        help="Number of parallel processes. More than 1 "
                             "requires license.")
        self.add_option("-p", "--project", action="store", dest="project",
                        default=None, metavar='FOLDERNAME',
                        help="The foldername of the project. By default, "
                             "the project entrypoint verilog file is assumed "
                             "to be the same as the foldername.")
        self.add_option("-t", "--time", action="store_true", dest="time",
                        default=False, metavar='OPTION',
                        help="If the tag is present, report the elapsed time "
                             "will be measured and reported.")
        self.add_option("-u", "--upload", action="store_true", dest="upload",
                        default=False, metavar='OPTION',
                        help="If the tag is present, upload the compiled "
                             "file over the first JTAG cable found.")
        self.add_option("-v", "--verbose", action="store_true", dest="verbose",
                        default=False, metavar='OPTION',
                        help="If the tag is present, verbose output will be printed to "
                             "the screen.")


def compile_quartus():
    parser = CompileOption()
    (options, args) = parser.parse_args()
    start = None
    if options.time or options.logging:
        start = time()
    if options.project is None:
        raise NameError("Please specify a project directory with --project")
    options.project = expanduser(options.project)
    if options.project[-1] == "/":
        options.project = options.project[:-1]
    # create a folder in the temporary directory, and copy all of the files
    # in the supplied directory to this directory
    if options.verbose:
        print("Setting up project.")
    setup = Setup()
    log_fh = None
    if options.logging:
        logging.basicConfig(filename=setup.log_file(options.project),
                            level=logging.DEBUG)
        logging.info("Started compiling "+str(options.project)+" at: "+str(start)+"\n")
    tmp_project_folder = join(setup.tmp_folder, basename(options.project))
    # remove the existing files
    if options.clear:
        if options.verbose:
            print("Clearing previous files.")
        if isdir(tmp_project_folder):
            try:
                rmtree(tmp_project_folder)
            except OSError as e:
                print("Could not remove folder: ", tmp_project_folder)
    if options.verbose:
        print("Copying source files.")
    # copy all files in the current folder to the tmp folder
    copytree(options.project, tmp_project_folder)
    if options.include_dirs is not None:
        options.include_dirs = options.include_dirs.split(",")
        for item in options.include_dirs:
            for _filename in listdir(item):
                copy(join(item, _filename),
                     join(tmp_project_folder, _filename))
    options.project = tmp_project_folder
    # flash name is the device name with the pin information removed
    options.flash_name = options.device_name.split("F")[0]
    if options.upload:
        if options.verbose:
            print("Checking JTAG chain.")
        # make sure a jtag chain is plugged in
        check_jtag()

    # check for the settings file
    _settings_file = join(options.project, basename(options.project)+".qsf")
    if not isfile(_settings_file):
        settings_file(_settings_file, device=options.device_name)

    steps = ['quartus_map', 'quartus_fit', 'quartus_asm', 'quartus_eda']
    # run through each step, return on detected failure
    for step in steps:
        if options.verbose:
            print("Running step: ", step)
        if not run_assembler_step(options, step):
            return

    # next, convert the sof to a jic
    # generate the sof file
    print("Converting output file.")
    run_conversion(options)
    if options.upload:
        if options.verbose:
            print("Uploading.")
        # finally, upload the jic
        run_upload(options, log=True)
    # remember to reset the device!
    if options.time or options.logging:
        end = time()
        if options.logging:
            logging.info("Build completed at: "+str(end)+" duration: "+str(
                end-start)+"\n")
        line = "Total time elapsed:" + str(end-start)
        print('\033[1;96m'+line+'\033[0m')

if __name__ == "__main__":
    compile_quartus()