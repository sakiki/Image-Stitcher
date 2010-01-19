#!/usr/bin/python


#-------------------------------------------------------------------------------------------------
# Name: Image Stitcher
# Author: Stephen Akiki
# Website: http://akiscode.com
# Language: Python
# Usage: 
#  python sparkdownloader.py [options] [FinalImageFilename] "image1" "image2" etc
#     
# Dependencies:
#  none
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


import getopt, sys, Image



class Argument:

  def __init__(self):
    self.b = None
    self.D = 0
    self.t = []
    self.delete = 0
    self.f = ""
    self.s = 0
		self.c = ""


def usage():
  print """
  
Usage: python imgstitch.py  [OPTION]... [FILENAME] [FILES]
Combine together [FILES] into one image
Example: python imgstitch.py image1.jpg image2.jpg


-b [WIDTH]		Final image is no wider than WIDTH images.
-D			Scan entire directory instead of multiple files.
-t [TYPE1]		Only get images of extension TYPE.  
--delete		Delete images used to make up final image after.
-s			Read in arguments from Standard Input.
-c			Change background filler color
"""


args = Argument()
MasterWidth = 0
MasterHeight = 0
filename = ""

# List that holds all the image files
ImageFileList = []


def main(argv):
  global args, MasterWidth, MasterHeight, ImageFileList, filename
  try:
			opts, args_files = getopt.getopt(argv, "b:Dt:sc:", ["delete", "help"])
      if len(args_files) <= 1:
        usage()
        sys.exit(-1)

      filename = args_files.pop(0)
    
  except getopt.GetoptError:
    print 'Usage: python imgstitch.py  [OPTION]... [FILENAME] [FILES]'
    print "Try 'python imgstitch.py --help' for more info"
    sys.exit(-1)
    
  for opt, arg in opts:
    if opt == '-b':
      args.b = arg
      
    
    elif opt == '-D':
      args.D = 1
    
    elif opt == '-t':
      args.t.append(arg)
      
    elif opt == '--delete':
      args.delete = 1
      
    elif opt == '-s':
      args.s = arg
    
    elif opt == '--help':
      usage()
      sys.exit(-1)
      
  
  if (args.s == 1):
    print 'read from stdin' # update later
    
  else:

    for x in args_files:
      try:
        im = Image.open(x)
        
        
        MasterWidth += im.size[0]
        if im.size[1] > MasterHeight:
          MasterHeight = im.size[1]
        else:
          MasterHeight = MasterHeight
          
          
        ImageFileList.append(x)      
        
      except:
        raise
    final_image = Image.new("RGB", (MasterWidth, MasterHeight))
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

  except:
    import traceback
    traceback.print_exc()
    print 'weird exception'
