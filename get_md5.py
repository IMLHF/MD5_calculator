import pathlib
import hashlib
import time
from itertools import takewhile
from itertools import repeat


def md5_sum4(filename:pathlib.Path):
    total_size = filename.stat().st_size
    buffer = 1024*1024
    i = 0
    with open(filename, "rb") as f:
      buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
      md5 = hashlib.md5()

      for line in buf_gen:
        if i%(buffer*10)==0:
          print('\rcurrent file:%s, %d%%'%(str(filename), int(i/total_size*100)), end='')
        md5.update(line)
        i += buffer
    f_md5 = md5.hexdigest()
    print('')
    return f_md5

if __name__ == "__main__":
  root_dir = '.'
  ans_file = './local_file_list.lst'

  files = list(pathlib.Path(root_dir).rglob("*"))
  files.sort()
  ans_f = open(ans_file, 'x')
  for f in files:
    if not f.is_dir():
      stime = time.time()
      md5sum_ans = md5_sum4(f)
      etime = time.time()
      # print(type(md5sum_ans))
      md5str = md5sum_ans+"  ./"+str(f).replace("\\", "/")
      ans_f.write(md5str+"\n")
      print(md5str, 'cost%ds\n'%(etime-stime), sep='  ')
  ans_f.close()
