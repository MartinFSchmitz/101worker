import os
import sys
import commands

if (len(sys.argv) == 3):
   repo = sys.argv[1]
   result = sys.argv[2]
   for dir, subdirs, _ in os.walk(repo+"/languages"):
      for s in subdirs:
         if (s=="geshi"):
            subdir = os.path.join(dir, s)
            for _, _, files in os.walk(subdir):             
               for f in files:
                  file = os.path.join(subdir, f)
                  command = 'cp '+file+' '+result
                  status, output = commands.getstatusoutput(command)
   sys.exit(0)
else:
   sys.exit(-1)