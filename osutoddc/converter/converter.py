import os
import sys
import argparse
import shutil
import json
from osutoddc import osu_to_ddc

def make_new_file(filename, exist_ok=True):
   if not exist_ok:
      if os.path.isfile(filename):
         raise FileExistsError()
   with open(filename, 'w') as file:
      pass

def one_file(input,output):
   if not input.endswith('.osu'):
      raise ValueError("this file is not an .osu file!")
   make_new_file(output, exist_ok=True)
   d = osu_to_ddc(input)
   d = json.dumps(d,indent=4)
   with open(output,'w') as file:
      file.write(d)

def one_folder(input,output):
   if not os.path.isdir(input):
      raise ValueError("Not a valid directory")
   os.makedirs(output, exist_ok=True)

   if input != output:
      shutil.copytree(input,output,dirs_exist_ok=True)

   osu_files = [os.path.join(output,filename) for filename in os.listdir(output)
                if filename.endswith(".osu")]
   for filename in osu_files:
      d = osu_to_ddc(filename)
      d = json.dumps(d,indent=4)
      with open(f"{filename}.json",'w') as file:
         file.write(d)
      os.remove(filename)

def many_folder(input,output):
   if not os.path.isdir(input):
      raise ValueError("Not a valid directory")
   os.makedirs(output,exist_ok=True)
   shutil.copytree(input,output,dirs_exist_ok=True)

   folders = [os.path.join(output, e) for e in os.listdir(output) 
                  if os.path.isdir(os.path.join(output,e))]
   for folder in folders:
      one_folder(folder,folder)

def run(input,output):
   if input==output:
      raise ValueError("input must be .osu, output must be .json")
   if os.path.isfile(input):
      one_file(input,output)
   elif os.path.isdir(input):
      listing =[os.path.join(input,e) for e in os.listdir(input)
                if e.endswith(".osu")]
      if len(listing)>0:
         one_folder(input,output)
      else:
         many_folder(input,output)
   else:
      raise ValueError("input does not exist?")

if __name__=="__main__":
   parser = argparse.ArgumentParser( 
                               description="utility to convert osu mania beatmaps to ddc-compatible json",
                               epilog="for more information please contact jayeonyi@snu.ac.kr")
   parser.add_argument("path",help="path to file or folder to convert to ddc json format")
   parser.add_argument("output_path",help="output path")
   args = parser.parse_args()
   print(args)

   run(args.path, args.output_path)