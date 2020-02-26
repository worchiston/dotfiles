import sys
from glob import glob
from PIL import Image


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: {} [from directory] [to directory]'.format(sys.argv[0]))
        sys.exit(1)
    
    file_index = 1
        
    for filename in glob(sys.argv[1] + '/*.jpg'):
        print(filename)
        image = Image.open(filename);
        
        image.thumbnail((640, 480), Image.ANTIALIAS)
        image.save('{}/{}.jpg'.format(sys.argv[2], file_index), optimise=True, quality=15)
        
        file_index += 1
