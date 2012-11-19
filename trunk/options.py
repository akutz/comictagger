"""
CLI options class for comictagger app
"""

"""
Copyright 2012  Anthony Beville

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import getopt
import platform
import os

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

class MetaDataStyle:
	CBI = 0
	CIX = 1
	name = [ 'ComicBookLover', 'ComicRack' ]


class Options:
	help_text = """	
Usage: {0} [OPTION]... [FILE]

A utility for read and writing metadata to comic archives.

If no options are given, {0} will run in windowed mode

  -p, --print                Print out tag info from file.  Specify type
                             (via -t) to get only info of that tag type
  -d, --delete               Deletes the tag block of specified type (via -t)
  -s, --save                 Save out tags as specified type (via -t)
                             Must specify also at least -o, -p, or -m
  -n, --dryrun               Don't actually modify file (only relevent for -d, -s, or -r)
  -t, --type=TYPE            Specify TYPE as either "CR" or "CBL", (as either 
                             ComicRack or ComicBookLover style tags, respectivly)
  -f, --parsefilename        Parse the filename to get some info, specifically
                             series name, issue number, volume, and publication 
                             year
  -o, --online               Search online and attempt to identify file using 
                             existing metadata and images in archive. May be used
                             in conjuntion with -p and -m
  -m, --metadata=LIST        Explicity define some tags to be used as a list                            
                             ....TBD........
                             ....TBD........
  -r, --rename               Rename the file based on metadata as indicated.  TBD!
  -a, --abort                Abort save operation when online match is of low confidence TBD!  
  -v, --verbose              Be noisy when doing what it does                            
  -h, --help                 Display this message                            
		"""


	def __init__(self):
		self.data_style = None
		self.no_gui = False
		self.filename = None  
		self.verbose = False
		self.md_settings = None
		self.print_tags = False
		self.delete_tags = False
		self.search_online = False
		self.dryrun = True  # keep this true for now!
		self.save_tags = False
		self.parse_filename = False
		self.rename_file = False
		
	def display_help_and_quit( self, msg, code ):
		appname = os.path.basename(sys.argv[0])
		if msg is not None:
			print( msg )
		print self.help_text.format(appname)
		sys.exit(code)
		
		
	def parseCmdLineArgs(self):
		
			
		# mac no likey this from .app bundle
		if platform.system() == "Darwin" and getattr(sys, 'frozen', None):
			 return 


		# parse command line options
		try:
			opts, args = getopt.getopt(sys.argv[1:], 
			           "hpdt:fm:vonsr", 
			           [ "help", "print", "delete", "type=", "parsefilename", "metadata=", "verbose", "online", "dryrun", "save", "rename"  ])
			           
		except getopt.GetoptError as err:
			self.display_help_and_quit( str(err), 2 )
			
		# process options
		for o, a in opts:
			if o in ("-h", "--help"):
				self.display_help_and_quit( None, 0 )
			if o in ("-v", "--verbose"):
				self.verbose = True
			if o in ("-p", "--print"):
				self.print_tags = True
			if o in ("-d", "--delete"):
				self.delete_tags = True
			if o in ("-o", "--online"):
				self.search_online = True
			if o in ("-n", "--dryrun"):
				self.dryrun = True
			if o in ("-m", "--metadata"):
				self.md_settings = a
			if o in ("-s", "--save"):
				self.save_tags = True
			if o in ("-r", "--rename"):
				self.rename_file = True
			if o in ("-f", "--parsefilename"):
				self.parse_filename = True
			if o in ("-t", "--type"):
				if a.lower() == "cr":
					self.data_style = MetaDataStyle.CIX
				elif a.lower() == "cbl":
					self.data_style = MetaDataStyle.CBI
				else:
					self.display_help_and_quit( "Invalid tag type", 1 )
			
		if self.print_tags or self.delete_tags or self.save_tags or self.rename_file:
			self.no_gui = True

		count = 0
		if self.print_tags: count += 1
		if self.delete_tags: count += 1
		if self.save_tags: count += 1
		if self.rename_file: count += 1
		
		if count > 1:
			self.display_help_and_quit( "Must choose only one action of print, delete, save, or rename", 1 )
		
		if len(args) > 0:
			self.filename = args[0]

		if self.no_gui and self.filename is None:
			self.display_help_and_quit( "Command requires a filename!", 1 )
			
		if self.delete_tags and self.data_style is None:
			self.display_help_and_quit( "Please specify the type to delete with -t", 1 )
			
		if self.save_tags and self.data_style is None:
			self.display_help_and_quit( "Please specify the type to save with -t", 1 )
			
		
