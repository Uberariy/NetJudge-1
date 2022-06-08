"""
appcmd.py
=====================================
Console
"""

import argparse
import tarfile
import sys
import os
import re
import shlex
import cmd
import gettext
import json
from report_analyser.input_checker.Machine_config import Machine
from .translator import translate
from collections import defaultdict
from termcolor import colored, cprint

'''Project l10n & i18n'''
translation = gettext.translation('netjudge', 'po', fallback=True)
_, ngettext = translation.gettext, translation.ngettext

'''Cmd colors'''
print_cyan = lambda x: cprint(x, 'cyan')
'''  For standart system output'''
print_green = lambda x: cprint(x, 'green')
'''  For positive user experience'''
print_red = lambda x: cprint(x, 'red')
'''  For negative user experience'''
print_yellow = lambda x: cprint(x, 'yellow')
'''  For undefined user experience'''
print_blue = lambda x: cprint(x, 'blue')
'''  Standart prompt'''
print_magenta = lambda x: cprint(x, 'magenta')
'''  Regex prompt'''

''' Global structures'''
GL_Files = defaultdict(dict)
''' GL_Files:
  key = participant name (if imported from dir -
                          name of dir with reports)
  value = python3 dictionary:
    key = report name
    value = participant data on this report'''
GL_Result_1 = defaultdict(dict)
GL_Result_2 = defaultdict(dict)
''' GL_Files, GL_Result_#:
  key = participant name (if imported from dir -
                          name of dir with reports)
  value = python3 dictionary:
    key = report name
    value = list:
      list[0] = current grade
      list[1] = maximum grade'''
GL_Regex = []
''' GL_Regex holds regexes used for checking
  GL_Regex[0] = regular expression
  GL_Regex[1] = files, it is applied to'''
RegexPlay_Regex = []
GL_DataBase = []
''' GL_DataBase is struct, that we get from base,
containing info on participants, and their tasks'''
GL_Mode = "brief"
GL_Source = "dir"
'''Detailability of ouput'''


def import_files_from_dir(dir_paths):
    '''Add keys to GF_Files'''
    GL_Source = "dir"
    once = True
    for dir_path in dir_paths:
        '''Find all dirs = users'''
        for user_dir in [dir[0] for dir in os.walk(dir_path)]:
            try:
                file_names = [filename for filename in os.listdir(user_dir) if
                              re.fullmatch(r"report.\d+.[^\.:]*", filename)] 
            except FileNotFoundError as E:
                print_red(E)
                continue
            else:
                if once:
                    print_green(_('Success'))
                    once = False
            for filename in file_names:
                checkname = filename.split(".")
                if checkname[0] != "report":
                    print_red(f"ERROR: Wrong file format \'{filename}\'. It should start with \'report\'!")
                    continue
                try:
                    checknumber = int(checkname[1])
                except Exception as E:
                    print_red(f"ERROR: Wrong file format \'{filename}\'. Report number should be integer!")
                    continue
                print(colored(user_dir, attrs=['bold']), " ", filename)
                GL_Files[user_dir][filename] = ""
                GL_Result_2[user_dir][filename] = [0, 0]
        

def import_files_from_base(dir_paths):
    '''Add keys to GF_Files'''
    GL_Source = "database"
    once = True

    GL_DataBase # = database.functions.collect_data()   TODO: GET STRUCTURE FROM BASE

    for user in GL_DataBase:
        '''Iterate by users. Each user is dict'''
        for task in user['tasks']:
            # try:
            #     file_names = [filename for filename in os.listdir(user_dir) if
            #                   re.fullmatch(r"report.\d+.[^\.:]*", filename)] 
            # except FileNotFoundError as E:
            #     print_red(E)
            #     continue
            # else:
            #     if once:
            #         print_green(_('Success'))
            #         once = False
            for report in task['reports']:
                checkname = report['name'].split(".")
                if checkname[0] != "report":
                    print_red(f"ERROR: Wrong file format \'{report['name']}\'. It should start with \'report\'!")
                    continue
                try:
                    checknumber = int(checkname[1])
                except Exception as E:
                    print_red(f"ERROR: Wrong file format \'{report['name']}\'. Report number should be integer!")
                    continue
                print(colored(user['email']+" "+user['name'], attrs=['bold']), " ", report['name'])
                GL_Files[user['email']+" "+user['name']][report['name']] = ""
                GL_Result_2[user['email']+" "+user['name']][report['name']] = [0, 0]


def import_instructions_from_json(json_paths):
    '''Add keys to GF_Instr'''
    once = True
    global GL_Regex
    for filename in json_paths:
        try:
            with open(filename, 'r') as f:
                datastore = json.load(f)
                try:
                    for record in datastore:
                        record['regex']
                        record['inout']
                        record['files']
                        assert record['inout'] in ['in', 'out']
                except Exception as E:
                    print_red(_('Instruction json file contains invalid structures!'))
                    print_red(_("It must be list: [{'regex': STRING, 'inout': in/out 'files': [STRING, STRING]}, ..."))
                else:
                    GL_Regex += datastore
                    if once:
                        print_green(_('Success'))
                        once = False
                    for record in datastore:
                        print_regex_record(record)
        except FileNotFoundError as E:
            print_red(E)
            continue

def Syntax_correct(source):
    # TODO: Dima's function to proceed data
    """Parse files & Write score in GL_Result_1"""
    machines = {}
    for user_dir, userfiles in GL_Files.items():
        print("Participant: '", user_dir, "', his files:\n\t", end="")
        for userfile in userfiles.keys():
            # TODO: FORDIMA: Modernize this fun
            filename = user_dir + "/" + userfile
            print(filename)
            number = filename.split(".")[-2]
            # machine_name = filename.split("/")[-1]
            if source == "dir":
                obj = tarfile.open(filename)
                obj_members = obj.getmembers()
                text = obj.extractfile('./OUT.txt').read().decode()
            else:
                # text = get_report_text(userfile, user_dir.split()[0], user_dir.split()[1]) TODO: DIMA
                pass
            text = re.sub('\r', '', text)  # re.split работал не совсем так, как надо
            lines = [translate(line) for line in text.split('\n') if line]
            GL_Files[user_dir][userfile] = lines
            # machines[machine_name + number] = Machine(machine_name, number, lines)
            # print(text)
        # print(f'Task number: {int(number)}')
        # for machine in machines.values():
            # machine.print_log()

        # TODO: FORDIMA: Fill GL_Result_1 with score of syntax check. Keys are filenames, same as GL_Files.keys()
        # GL_Result_1 = 1    If files complete Syntax_correct() without issues
        # GL_Result_1 = 0    Otherwise

def Semantic_check(GFiles, GRegex, save_results):
    """Write score in GL_Result_2"""
    global GL_Result_2
    for username, reportdict in GFiles.items():
        print_blue(colored(_("Checking participant '{}':").format(username), attrs=['bold']))
        for reportname, lines in reportdict.items():
            print_blue(_("\n  Checking file {}:").format(reportname))
            regexlist = [regex for regex in GRegex if reportname in regex['files'] or regex['files'] == ['']]
            for regexind, regex in enumerate(regexlist):
                print_cyan(_("    RE {}: '{}' ({}put).").format(regexind, regex['regex'], regex['inout']))
                find = False
                matchind = 0
                linenumber = 0
                for lineind, line in enumerate(lines):
                    if line[0].startswith(regex['inout']):
                        patt = re.compile(regex['regex'])
                        for match in patt.findall(line[1]):
                            find = True
                            matchind += 1
                            print("      "+colored(_("Match {} in line {}:").format(matchind, lineind), attrs=["bold"]))
                            linewithmatch = colored(match, "green", attrs=["underline"]).join(line[1].split(match))
                            print(_("        {}").format(colored(linewithmatch)))
                            linenumber = lineind + 1
                listed_results = [0, 0]
                if not find:
                    print_red(_("      No matches in {} lines!").format(linenumber))
                else:
                    listed_results[0] += 1
                listed_results[1] += 1
            checkeq = f"{listed_results[0]} / {listed_results[1]}"
            if listed_results[0] == listed_results[1]:
                checkeq = colored(checkeq, 'green')
            else:
                checkeq = colored(checkeq, 'red')
            print_blue(_("  {} {} {}").format(checkeq, colored("REGEXs matched in file", 'blue'), colored(reportname, 'blue', attrs=['bold'])))
            if save_results:
                for i in range(0, 2):
                    GL_Result_2[username][reportname][i] += listed_results[i]
        print_blue("\n")

def print_regex_record(record):
    print(_(" Re: {}").format(colored(record['regex'], attrs=['bold'])))
    if record['files'] != ['']:
        print(_("   Files ({}put):").format(record['inout']), end="\t")
        for filename in record['files']:
            print(filename, end="\t")
    else:
        print(_("   Every imported file ({}put).").format(record['inout']), end="\t")
    print("")

def print_exit_message():
    print_cyan(_("\n ==[ Exiting! ]=="))

def print_help():
    pass 
    # TODO: Add help for all the cmd variety

def print_help_regex():
    pass 
    # TODO: Add help for all the cmd variety

class Repl_Regex(cmd.Cmd):
    prompt = colored(_("[ RegexTest ]:~$ "), 'magenta')
    mode = "brief"

    def emptyline(self):
        """Override: Called when an empty line is entered in response to the prompt."""
        if self.lastcmd:
            self.lastcmd = ""
            return self.onecmd('\n')

    def do_re(self, arg):
        """Test regex on imported reports in regextest mode.
        Usage: re [REGEX] ['in'/'out'] {[FILE]}
           or: re [REGEX] ['in'/'out']

        Add a REGEX and specify, if 'in'-put or 'out'-put of FILEs is checked.
        If FILE is not set, every imported file is checked with this regex!
        REGEX and 'in'/'out' parameters must be set!
        
        Note, that in 'regextest' mode, results are not saved, only displayed.
        """
        global RegexPlay_Regex, GL_Files, GL_Source
        args = shlex.split(arg, comments=True)
        if len(args) < 2:
            print_red(_("Not enough arguments"))
        elif args[1] not in ['in', 'out']:
            print_red(_("Wrong argument {}. Use in/out.").format(args[1]))
        else:
            reg = args[0]
            inout = args[1]
            if len(args) >= 3:
                filenames = args[2:]
            else:
                filenames = ['']
            record = {'regex': reg, 'inout': inout, 'files': filenames}
            RegexPlay_Regex.append(record)
            print_green(_('Testing regex:'))
            print_regex_record(record)
            Syntax_correct(GL_Source)
            print_cyan(_("  =[ CHECKING... ]="))
            Semantic_check(GL_Files, RegexPlay_Regex, save_results=False) 
            print_cyan(_("  ==[ CHECK ENDED ]=="))  

    def do_q(self, arg):
        """Easier exit from regex testing mode.
        Usage: q
        """
        return True

    def do_exit(self, arg):
        """Exit regex testing mode.
        Usage: exint
        """
        return True
    # TODO: Make cmd history recover after exiting regex mode

class Repl(cmd.Cmd):
    prompt = colored(_("[ NetJu ]:~$ "), 'blue')
    print_cyan(_(" ==[ Welcome to NET-JUDGE - Check enviroment for iproute2 library! ]==\n"))
    lastcmd = ''

    def emptyline(self):
        """Override: Called when an empty line is entered in response to the prompt.
        """
        if self.lastcmd:
            self.lastcmd = ""
            return self.onecmd('\n')

    def do_q(self, arg):
        """Shorter variant of 'exit' command.
        Usage: q
        """
        print_exit_message()
        return True

    def do_exit(self, arg):
        """Exit application. All unsaved data would be lost!
        Usage: exit
        """
        print_exit_message()
        return True

    def do_reset(self, arg):
        """This function clears all results achieved and imports made.
        Usage: reset
        """
        global GL_Files, GL_Result_1, GL_Result_2, GL_Regex
        GL_Files = GL_Result_1 = GL_Result_2 = defaultdict(dict)
        GL_Regex = []
        print_cyan(_(" ==[ All progress is reset!! ]==\n"))

    def do_importedreports(self, arg):
        """Print imported report files.
        Usage: impoertedreports
        """
        if not GL_Files:
            print_cyan(_("  =[ No reports imported ]="))
        else:
            print_cyan(_("  =[ Imported reports: ]="))
            for username, userfiles in GL_Files.items():
                print(_("Participant: {} His files:\n\t").format(colored(username, attrs=['bold'])), end="")
                for userfile in userfiles.keys():
                    print(userfile, end="\t ")
                print("")

    def do_importedinstructions(self, arg):
        """Print imported instruction files
        Usage: importedinstructions
        """
        if not GL_Regex:
            print_cyan(_("  =[ No instructions imported ]="))
        else:
            print_cyan(_("  =[ Imported instructions: ]="))
            for record in GL_Regex:
                print_regex_record(record)

    def do_addrep(self, arg):
        """Add files to check to the collection from 1 or more dirs.
        Usage: addrep {[DIR]}
        
        Scheme of directory:
            [DIR]---[USER1]---[REPORT1]
                  |         |
                  |         |-[REPORT2]
                  |
                  |-[USER2]---[REPORT1]
        """
        args = shlex.split(arg, comments=True)
        if len(args) == 0:
            print_red(_("Not enough arguments"))
        else:
            dir_paths = args[0:]
            import_files_from_dir(dir_paths)            

    def do_addins(self, arg):
        """Add 1 or more instruction files to the regex collection.
        Usage: addins {[FILE]}

        Instr. files contain regex to check if smth is present in report.
        """
        args = shlex.split(arg, comments=True)
        if len(args) == 0:
            print_red(_("Not enough arguments"))
        else:
            json_path = args[0:]
            import_instructions_from_json(json_path)  

    def do_saveins(self, arg):
        """Save regular expressions imported in project in file in json format.
        Usage: saveins [FILE]

        If file is present, it will be overrided, otherwise, we create new file
        """
        args = shlex.split(arg, comments=True)
        if len(args) not in [1]:
            print_red(_("Wrong number of arguments"))
        else:
            try:
                with open(args[0], 'w') as f:
                    json.dump(GL_Regex, f, indent = 6)
            except FileNotFoundError as E:
                print_red(E)
            else:
                print_green(_("Success: Saved REGEXs in {}").format(args[0]))

    def do_addreg(self, arg):
        """Add a single regular expression to collection.
        Usage: re [REGEX] ['in'/'out'] {[FILE]}
           or: re [REGEX] ['in'/'out']

        Add a REGEX and specify, if 'in'-put or 'out'-put of FILEs is checked.
        If FILE is not set, every imported file is checked with this regex!
        REGEX and 'in'/'out' parameters must be set!
        """
        global GL_Regex
        args = shlex.split(arg, comments=True)
        if len(args) < 2:
            print_red(_("Not enough arguments"))
        elif args[1] not in ['in', 'out']:
            print_red(_("Wrong argument {}. Use in/out.").format(args[1]))
        else:
            reg = args[0]
            inout = args[1]
            if len(args) >= 3:
                filenames = args[2:]
            else:
                filenames = ['']
            record = {'regex': reg, 'inout': inout, 'files': filenames}
            GL_Regex.append(record)
            print_green(_('Success'))
            print_regex_record(record)

    def do_regextest(self, arg):
        """Enter regex mode and test your regex :)
        Usage: regextest
        """
        args = shlex.split(arg, comments=True)
        print_cyan(_("  ==[ ENTERING REGEX TESTING MODE: ]=="))
        Repl_Regex().cmdloop()
        print_cyan(_("  ==[ EXITING REGEX TESTING MODE: ]=="))
        '''Otherwise last cmd is called after return'''
        self.lastcmd = 'nothing'

    def do_mode(self, arg):
        """Modify verbosity mode
        mode ['quiet'/'brief'/'verbose']
        """
        args = shlex.split(arg, comments=True)
        global GL_Mode
        if len(args) != 1:
            print_red(_("Wrong number of arguments"))
        else:
            if args[0] not in ["quiet", "brief", "verbose"]:
                print_red(_('Wrong argument. Use one of "quiet", "brief", "verbose"'))
            else:
                GL_Mode = args[0]
                print_green(_("'{}' mode is set.").format(args[0]))
        self.lastcmd = ''

    def complete_mode(self, text, allcommand, beg, end):
        return [s for s in ["quiet", "brief", "verbose",] if s.startswith(text)]

    def do_start(self, arg):
        """Main function to start checking process. Checking steps:
        Usage: start ['1'/'2']

        1. Parsing & Syntax check;
        2. Parsing & Syntax check & Semantic check.

        No files in collection:              # # steps done
        Files present in collection:         1 # steps done
        Instructions present in collection:  1 2 steps done
        
        Results are saved and can be shown with 'conclude'.
        """
        args = shlex.split(arg, comments=True)
        if len(args) not in [0, 1]:
            print_red(_("Wrong number of arguments"))
        else: 
            if len(args) == 1:
                if args[0] not in ["1", "2"]:
                    print_yellow(_("Wrong number of steps to be done: {}").format(args[0]))
                    steps = 0
                else:
                    steps = int(arg[0])
            else:
                steps = 2
            if not GL_Files.keys():
                steps = min(steps, 0)
                print_yellow(_('''No report files imported! => No steps would be done!\nUse \'addf REPORT_USERS_DIR\''''))
            if not GL_Regex:
                steps = min(steps, 1)
                print_yellow(_('''No instructions imported! => Second step is skipped\nUse \'addins INSTRUCTION_FILE\''''))
                print_yellow(_('''Or  \'addreg REGEX, FILE1, FILE2...\''''))

            print_cyan(_("  ==[ CHECK STARTS:  Going through {} steps ]==").format(steps))
            if steps > 0: 
                print_cyan(_("  =[ SYNTAX CHECK ]="))
                Syntax_correct(GL_Source) 
            if steps > 1: 
                print_cyan(_("  =[ SEMANTIC CHECK ]="))
                global GL_Result_2
                Semantic_check(GL_Files, GL_Regex, save_results=True) 
            print_cyan(_("  ==[ CHECK ENDED ]=="))   

    def complete_start(self, text, allcommand, beg, end):
        return [s for s in ["1", "2",] if s.startswith(text)]

    def do_conclude(self, arg):
        """Function prints general result for each task number presented in collection, and saves this data.
        Usage: conclude
        
        Note, that conclude accumulates all the results during application run, except
        those made in 'regextest' mode.
        """
        print_cyan(_("  ==[ RESULTS ]=="))
        global GL_Result_1, GL_Result_2, GL_DataBase, GL_Source
        for username, reportdict in GL_Files.items():
            print_blue(colored(_("Participant '{}' results:\n").format(username), attrs=['bold']))
            for reportname, lines in reportdict.items():
                checkeq = f"{GL_Result_2[username][reportname][0]} / {GL_Result_2[username][reportname][1]}"
                if GL_Result_2[username][reportname][0] == GL_Result_2[username][reportname][1]:
                    checkeq = colored(checkeq, 'green')
                else:
                    checkeq = colored(checkeq, 'red')
                print_blue(_("  {}:\t{}").format(reportname, checkeq))
            print("")
        """Save results"""
        if GL_Source == "database":
            for userind, user in enumerate(GL_DataBase):
                for taskind, task in enumerate(user['tasks']):
                    for reportind, report in enumerate(task['reports']):
                        GL_DataBase[userind][taskind][reportind]["result_tuple"] = [user['email']+" "+user['name']][report['name']]
            # TODO: DIMA Save this in database