#!/usr/bin/env python

"Convert a Microsoft RTF file to XML"

# set this variable only if you cannot use create
# an .rtf2xml file in an appropriate directory (see docs)
configuration_file = ''

#########################################################################
#                                                                       #
#                                                                       #
#   copyright 2002 Paul Henry Tremblay                                  #
#                                                                       #
#   This program is distributed in the hope that it will be useful,     #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of      #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU    #
#   General Public License for more details.                            #
#                                                                       #
#   You should have received a copy of the GNU General Public License   #
#   along with this program; if not, write to the Free Software         #
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA            #
#   02111-1307 USA                                                      #
#                                                                       #
#                                                                       #
#########################################################################



# levels:
# greater than 3: script will raise an error
# less than 3: no error raised, no message produced



debug_run = 0

# debug_profile
# used for developers, to see how much time each function takes.
debug_profile = 0

import os, sys
# get directory of script
if os.path.basename(sys.argv[0]) == 'rtf2xml.py':
    current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    #  determine if current dir in sys.path
    current_in_path = 0
    if current_dir in current_dir:
        current_in_path = 1
    temp = []
    # copy all of sys.path to temp except for current dir
    for path in sys.path:
        if path != current_dir:
            temp.append(path)

    # copy temp to sys.pah
    sys.path = []
    for path in temp:
        sys.path.append(path)

    # if current dir in sys.path, make it last
    if current_in_path:
        sys.path.append(current_dir)




import tempfile 
import rtf2xml.ParseRtf
import rtf2xml.get_options

__version__ = '1.32'
__author__ = "Paul Henry Tremblay"
__date__ = '$Date: 2008-03-28 12:06:46 +0100 (Fri, 28 Mar 2008) $'


if configuration_file and not os.path.isfile(configuration_file):
    sys.stderr.write('the configuration_file "%s" cannot be found\n' % configuration_file)
    sys.stderr.write('Please change the script "%s"\n' % sys.path[0])
    sys.exit(1)


def make_debug_dir(out_file):
    if out_file:
        dir_name = os.path.dirname(out_file)
    else:
        dir_name = os.getcwd()
    debug_dir = os.path.join(dir_name, 'rtf2xml_debug_dir')
    if not os.path.isdir(debug_dir):
        try:
            os.mkdir(debug_dir)
        except OSError, msg:
            sys.stderr.write('Sorry, but cannot make a debug directory:\n')
            sys.stderr.write(msg)
            sys.stderr.wrtie('Script will now quit.\n')
            sys.exit(1)
    return debug_dir





def print_help_message():
    sys.stderr.write(
"""
rtf2xml [ -h | --help ]

rtf2xml [ --config ]

rtf2xml [ --version ]

rtf2xml [ --caps ] [ --no-caps  ] 
        [ --indent=<n> ]
        [ --no-lists ] [ --lists ]
        [ --empty-para ] [ --no-empty-para]
        [ --group-styles ] [ --no-group-styles ]
        [ --group-borders ] [ --no-group-borders]
        [ --headings-to-sections ] [ --no-headings-to-sections ]
        [ --level <level> ]
        [--output=<file> | -o=<file>]
        file

"""
    )
def print_config_message(options_dict):
    config = options_dict.get('config-location')
    if not config:
        config = 'No configuration file found.\n'
    else:
        config = 'configuration path is "%s"\n' % options_dict['config-location']
    sys.stdout.write(config)

    in_file = options_dict.get('in-file') 
    out_file = options_dict.get('the-out-file')
    out_dir = options_dict.get('out-dir')
    dtd = options_dict.get('raw-dtd-path') 
    char_data = options_dict.get('char-data') 
    debug = options_dict.get('debug-dir')
    convert_symbol = options_dict.get('convert-symbol')
    convert_zapf = options_dict.get('convert-zapf')
    convert_caps = options_dict.get('convert-caps')
    convert_wingdings = options_dict.get('convert-wingdings')
    run_level = options_dict.get('level')
    indent = options_dict.get('indent')
    form_lists = options_dict.get('form-lists')
    headings_to_sections = options_dict.get('headings-to-sections')
    group_styles = options_dict.get('group-styles')
    group_borders = options_dict.get('group-borders')
    empty_paragraphs = options_dict.get('empty-paragraphs')
    no_dtd = options_dict.get('no-dtd')

    if in_file:
        print "in file is %s" % in_file
    else:
        print "No input file specified"
    if out_file:
        print "out file is %s" % out_file
    else:
        print "No output file specified"

    if convert_symbol:
        print "script will convert Symbol font"
    else:
        print "script will not convert Symol font"

    if convert_zapf:
        print "script will convert Zapf Dingbat font"
    else:
        print "script will not convert Zapf Dingbat font"

    if convert_wingdings:
        print "script will convert Wingdings font"
    else:
        print "script will not convert Wingdings font"

    print "the run level = '%s'" % run_level

    if indent:
        print 'script will indent resulting XML'
    else:
        print 'script will not indent resulting XML'

    if form_lists:
        print 'script will form lists'
    else:
        print 'script will not form lists'

    if headings_to_sections:
        print 'script will convert headings to sections'
    else:
        print 'script will not convert headings to sections'

    if group_styles:
        print 'script will group styles with the same name'
    else:
        print 'script will not group styles with the same name'

    if group_borders:
        print 'script will group borders'
    else:
        print 'script will not group borders'

    if empty_paragraphs:
        print 'script will print out empty paragraphs'
    else:
        print 'script will ignore empty paragraphs'

    print 'the script will print out the following dtd: "%s"' % dtd
    
def handle_options():

        
    get_options_obj = rtf2xml.get_options.GetOptions(

        system_arguments = sys.argv,
        rtf_dir = None,
        configuration_file = configuration_file,
        bug_handler = rtf2xml.ParseRtf.RtfInvalidCodeException,
        )
    options_dict = get_options_obj.get_options()


    if not options_dict['valid']:
        print_help_message()
        sys.stderr.write('script will now quit\n')
        sys.exit(1)




    if options_dict['help']:
        print_help_message()
        sys.exit(0)

    if options_dict['config']:
        print_config_message(options_dict)
        sys.exit(0)

    
    if options_dict['version']:
        print_version()
        sys.exit(0)

    if options_dict['format'] == 'sdoc' or options_dict['format'] == 'tei':
        # options_dict['no-namespace'] = 1
        pass
    options_dict['the-out-file'] = options_dict['out-file']


    level = options_dict.get('level')
    if level == None:
        options_dict['level'] = 0

    if options_dict['level'] > 2:
       debug_dir = make_debug_dir(options_dict['out-file']) 
       options_dict['debug-dir'] = debug_dir
    else:
        options_dict['debug-dir'] = 0


    tei_list = options_dict.get('tei-list')
    if not tei_list:
        options_dict['tei-list'] = None
    sdoc_list = options_dict.get('sdoc-list')
    if not sdoc_list:
        options_dict['sdoc-list'] = None

    current_dir = os.getcwd()
    options_dict['current-dir'] = current_dir

    return options_dict

    
    
def print_version():
    sys.stderr.write(
"""
rtf2xml %s
Written by Paul Tremblay.


This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
St, Fifth Floor, Boston, MA  02110-1301  USA

"""
% __version__ 
            )
def Handle_Main():
    """Handles options and creates a parse object if the script is used directly"""
    
    options_dict = handle_options()


    this_run_level = options_dict.get('level')
    if this_run_level > 3:
        parse_obj =rtf2xml.ParseRtf.ParseRtf(   
                in_file = options_dict['in-file'], 
                out_file = options_dict['the-out-file'],
                out_dir = options_dict['out-dir'],
                dtd = options_dict.get('raw-dtd-path'), 
                char_data = options_dict.get('char-data'), 
                debug = options_dict['debug-dir'],
                convert_symbol = options_dict['convert-symbol'],
                convert_zapf = options_dict.get('convert-zapf'),
                convert_caps = options_dict.get('convert-caps'),
                convert_wingdings = options_dict.get('convert-wingdings'),
                run_level = options_dict.get('level'),
                indent = options_dict.get('indent'),
                form_lists = options_dict.get('form-lists'),
                headings_to_sections = options_dict.get('headings-to-sections'),
                group_styles = options_dict.get('group-styles'),
                group_borders = options_dict.get('group-borders'),
                empty_paragraphs = options_dict.get('empty-paragraphs'),
                no_dtd = 1,
        ) 

        parse_obj.parse_rtf()
    else:
        try:
            parse_obj =rtf2xml.ParseRtf.ParseRtf(   
                    in_file = options_dict['in-file'], 
                    out_file = options_dict['the-out-file'],
                    out_dir = options_dict['out-dir'],
                    dtd = options_dict.get('raw-dtd-path'), 
                    char_data = options_dict.get('char-data'), 
                    debug = options_dict['debug-dir'],
                    convert_symbol = options_dict['convert-symbol'],
                    convert_zapf = options_dict.get('convert-zapf'),
                    convert_caps = options_dict.get('convert-caps'),
                    convert_wingdings = options_dict.get('convert-wingdings'),
                    run_level = options_dict.get('level'),
                    indent = options_dict.get('indent'),
                    form_lists = options_dict.get('form-lists'),
                    headings_to_sections = options_dict.get('headings-to-sections'),
                    group_styles = options_dict.get('group-styles'),
                    group_borders = options_dict.get('group-borders'),
                    empty_paragraphs = options_dict.get('empty-paragraphs'),
                    no_dtd = 1,
            ) 

            parse_obj.parse_rtf()
        except rtf2xml.ParseRtf.InvalidRtfException, msg:
            quit(msg = msg)

        except rtf2xml.ParseRtf.RtfInvalidCodeException, msg:
            quit(msg = msg)




def quit(msg, level=1):
    sys.stderr.write(str(msg))
    sys.exit(level)




if __name__=='__main__':
    if debug_profile:
        import profile
        file_obj = open('/home/paul/paultemp/profile_args.data', 'w')
        file_obj.truncate(0)
        file_obj.close()
        profile.run('Handle_Main(),', '/home/paul/paultemp/profile_args.data')
        import pstats
        p = pstats.Stats('/home/paul/paultemp/profile_args.data')
        p.strip_dirs().sort_stats('time').print_stats()
    else:
        Handle_Main()

