#!/usr/bin/python


#-------------------------------------------------------------------------------------------------
# Name: Image Stitcher
# Author: Stephen Akiki
# Website: http://akiscode.com
# Language: Python
# Usage: 
#  python sparkdownloader.py [options] [FinalImageFilename] "image1" "image2" etc
#  python imgstitch.py  [OPTION] -D [DIRECTORY] [FILENAME
#     
# Dependencies:
#  PIL 
#
# Disclaimer:
#  By using this program you do so at your own risk. I assume no liability
#  for anything that happens to you because you used this program.
#  
#  Enjoy
#
# License - GNU GPL (See LICENSE.txt for full text):
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Find this useful?
#  If you want to use this code (in compliance with the GPL) then I would
#  appreciate it if you included this somewhere in your code comments header:
#  
#   Thanks to Stephen Akiki (http://akiscode.com) for image stitcher code
#
#-------------------------------------------------------------------------------------------------
# Copyright (C) 2010 Stephen Akiki. All rights reserved.
#-------------------------------------------------------------------------------------------------


import getopt, sys, os
from PIL import Image



class Argument:

  def __init__(self):
    self.v = 0
    self.D = "" 
    self.t = '*'
    self.f = ""
    self.c = "black"


def usage():
  print """
  
Usage: python imgstitch.py  [OPTION]... [FILENAME] [FILES]
Combine together [FILES] into one image
Example: python imgstitch.py image1.jpg image2.jpg

python imgstitch.py  [OPTION] -D [DIRECTORY] [FILENAME]

-D Directory		Scan entire directory instead of multiple files.
-t [TYPE1]			Only get images of extension TYPE.  Only used in conjunction with -D
-c					Change background filler color
-v					Verbose output
"""


args = Argument()
MasterWidth = 0
MasterHeight = 0
filename = ""
deletename = False 


# List that holds all the image files
ImageFileList = []

def vprint(str):
  global args
  if args.v == 1:
    print str


def main(argv):
  global args, MasterWidth, MasterHeight, ImageFileList, filename, deletename
  try:
      opts, args_files = getopt.getopt(argv, "vD:t:c:", ["help"])

    
  except getopt.GetoptError:
    print "Illegal arguments"
    print "Try 'python imgstitch.py --help' for more info"
    sys.exit(-1)
    
  for opt, arg in opts:

    if opt == '-v':
      args.v = 1      
    
    elif opt == '-c':
      args.c = arg

    elif opt == '-D':
      if not os.path.exists (arg):
        print 'Directory does not exist'
        sys.exit()
      args.D = arg 
      
    
    elif opt == '-t':
      args.t = arg
      
      
    elif opt == '--help':
      usage()
      sys.exit(-1)
      
    
  else:
  
    filename = args_files.pop(0)
    
    


    if args.D != "":
      import glob
      args_files = glob.glob((os.path.join(args.D,  ('*.'+ args.t))))
      vprint('Finding all files in directory: ' + args.D)
      for x in args_files:
        vprint(x)
    
		

    vprint('Combining the following images:')
    for x in args_files:
      
      try:
        im = Image.open(x)
        vprint(x)
        
        
        MasterWidth += im.size[0]
        if im.size[1] > MasterHeight:
          MasterHeight = im.size[1]
        else:
          MasterHeight = MasterHeight
          
          
        ImageFileList.append(x)      
        
      except:
       if args.D != "":
        pass
       else:
        raise

    final_image = Image.new("RGB", (MasterWidth, MasterHeight), args.c)
    offset = 0
    for x in ImageFileList:
     temp_image = Image.open(x)
     final_image.paste(temp_image, (offset, 0))
     offset += temp_image.size[0]

    
  
    final_image.save(filename)

      
      
    
if __name__ == "__main__":
  try:
    main(sys.argv[1:])
  except IOError:
    print 'One of the files listed is not a valid image file'
    sys.exit(-1)
    
  except SystemExit:
    pass

  except ValueError:
    print 'That color value is not valid'


  except:
    import traceback
    traceback.print_exc()
    print 'weird exception'
