#!/usr/local/bin/python3
import os, sys, getopt, hashlib
import requests

class SubtitlesDownloader():
    """Used to download subtitles from SubDB"""

    def __init__(self, inputfile, outputfile=None):
        self.inputfile = inputfile
        self.outputfile = outputfile

        if self.outputfile is None:
            self.outputfile = f"{os.path.splitext(inputfile)[0]}.srt"

    def __save_srt_file(self, r):
        with open(self.outputfile, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)

    def __call_sub_db_api(self, hash):
        url = 'http://api.thesubdb.com/'
        payload = {'action': 'download', 'hash': hash, 'language': 'es'}
        headers = {'user-agent': 'SubDB/1.0 (subDownoader/0.1; https://github.com/antar88/subDownoader)'}
        return requests.get(url, params=payload, headers=headers)

    def __get_hash(self):
        readsize = 64 * 1024
        name = self.inputfile
        with open(name, 'rb') as f:
            size = os.path.getsize(name)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

    def download(self):
        print("Downloading...")
        hash = self.__get_hash()
        response = self.__call_sub_db_api(hash)
        self.__save_srt_file(response)
        print("Download finished!")


def main(argv):
   inputfile = None
   outputfile = None

   try:
       opts, args = getopt.getopt(argv,'i:o',['input=','output='])
   except getopt.GetoptError:
      print('Error. You should use the command sub_downloader.py -i <inputfile> [-o <outputfile>]')
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         print('sub_downloader.py -i <inputfile> [-o <outputfile>]')
         sys.exit()
      elif opt in ["-i", "--ifile"]:
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   print(inputfile)
   if inputfile is None:
       print('You need to specify input file')
       sys.exit(1)
   else:
       subs_downloader = SubtitlesDownloader(inputfile, outputfile)
       subs_downloader.download()

main(sys.argv[1:])
