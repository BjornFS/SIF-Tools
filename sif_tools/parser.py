import warnings
from collections import OrderedDict

import numpy as np


# Read Andor Technology Multi-Channel files with PIL.
# Based on Marcel Leutenegger's MATLAB script.

_MAGIC = 'Andor Technology Multi-Channel File\n'

# --------------------------------------------------------------------
# SIF parser
def _to_string(c):
    ''' convert bytes to string. c: string or bytes'''
    return c if not isinstance(c, bytes) else c.decode('utf-8')

def _read_string(fp, length=None):
    '''Read a string of the given length. If no length is provided, the
    length is read from the file.'''
    if length is None:
        length = int(_to_string(fp.readline()))        
    return fp.read(length)

def _read_until(fp, terminator=' '):
    '''Read a space-delimited word.'''
    word = ''
    while True:
        c = _to_string(fp.read(1))
        if c == terminator or c == '\n':
            if len(word) > 0:
                break
        word += c
    return word

def _skip_spaces(fp):
    '''Read until something other than space or line end '''
    while True:
        offset = fp.tell()
        c = _to_string(fp.read(1))
        if c not in [' ', '\n']:
            fp.seek(offset)
            return fp
    raise ValueError('Reached the end of the file')

def _read_int(fp):
    return int(_read_until(fp, ' '))

def _read_float(fp):
    return float(_read_until(fp, ' '))

def inspect(fp):
    """
    A helper function to read SIF file.

    Parameters
    -----------
    fp: File pointing to SIF file

    Returns
    -------
    tile: list
        A list of tuples, that contains the image location in the file.
    size: a tuple, (wdith, height)
    n_frames: integer
        number of frames
    info: dict
        Dictionary containing misc data.
    """
    info = OrderedDict()

    # Line 1 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if _to_string(fp.read(36)) != _MAGIC:
        raise SyntaxError('not a SIF file')
   
    # Line 2 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    fp.readline() # 65538 number_of_images? Maybe it is oldest version to open?

    # Line 3 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    info['SifVersion'] = int(_read_until(fp, ' ')) # 65559, newest 65567
    
    _read_until(fp, ' ') # 0
    _read_until(fp, ' ') # 0
    _read_until(fp, ' ') # 1

    info['ExperimentTime'] = _read_int(fp) # 1540956289
    info['DetectorTemperature'] = _read_float(fp)

    
    _read_string(fp, 10) # blanks
    
    _read_until(fp, ' ') # 0

    info['ExposureTime'] = _read_float(fp)
    info['CycleTime'] = _read_float(fp)
    info['AccumulatedCycleTime'] = _read_float(fp)
    info['AccumulatedCycles'] = _read_int(fp)

    fp.read(1) # NULL
    fp.read(1) # space

    info['StackCycleTime'] = _read_float(fp)
    info['PixelReadoutTime'] = _read_float(fp) # 1.78571e-09 or 1e-06    

    _read_until(fp, ' ') # 0
    _read_until(fp, ' ') # 1
    info['GainDAC'] = _read_float(fp)

    _read_until(fp, ' ') # 0
    _read_until(fp, ' ') # 0
    info['GateWidth'] = _read_float(fp)

    for _ in range(16):
        _read_until(fp, ' ')
    info['GratingBlaze'] = _read_float(fp)

    # What is the rest of the line?
    _read_until(fp, '\n')
    
    # Line 4 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    info['DetectorType'] = _to_string(fp.readline()).strip()
    # Line 5 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    info['DetectorDimensions'] = (_read_int(fp), _read_int(fp))
    # Lines 5 -> 6    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    info['OriginalFilename'] = _read_string(fp)   
    
    fp.read(2) # space newline
    # Line 7 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    _read_until(fp, ' ') # 65538
    # Line 8 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    info['user_text'] = _read_string(fp)
    fp.read(1) # newline
    # Line 9 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    
    _read_int(fp) # 65538
    fp.read(8) # spaces and binary
    info['ShutterTime'] = (_read_float(fp), _read_float(fp)) # ends in newline

    if (65548 <= info['SifVersion'] &
            info['SifVersion'] <= 65557):
        for _ in range(2):
            fp.readline()
    elif info['SifVersion'] == 65558:
        for _ in range(5):
            fp.readline()
    elif info['SifVersion'] in [65559, 65564]:
        for _ in range(8):
            fp.readline() # Skip to Line 18
        info['spectrograph'] = _to_string(fp.readline().split()[1])
    elif info['SifVersion'] == 65565:
        for _ in range(15):
            fp.readline()
    elif info['SifVersion'] > 65565:
        # skipping bunch of lines from 20 to 37, modified to read the Spectrograph name
        for _ in range(8):
            fp.readline() # Skip to Line 22
        info['spectrograph'] = _to_string(fp.readline().split()[1])
        for _ in range(9):
            fp.readline() # skipping bunch of lines from 20 to 37 
    
    if 'spectrograph' not in info.keys():
        info['spectrograph'] = 'sif version not checked yet'

    info['SifCalbVersion'] = int(_read_until(fp, ' ')) # 65539
    # additional skip for this version
    if info['SifCalbVersion'] == 65540:
        fp.readline()
    
    # 0x01 space NULL space 0x01 space NULL space 0x01 space NULL newline
    # Polinomial coeffitients for pixel to wavelenght convertion 
    # for Mechelle spectrograph    
    if 'Mechelle' in info['spectrograph']:
    #if info['SifCalbVersion'] == 65540:
        info['PixelCalibration'] = [float(jj) for jj in fp.readline().strip().split()]
    else:
        info['Calibration_data'] = fp.readline()

    fp.readline() # 0 1 0 0 newline
    fp.readline() # 0 1 0 0 newline
    raman = fp.readline()
    try: 
        info['RamanExWavelength'] = float(raman)
    except: 
        info['RamanExWavelength'] = np.nan

    fp.readline() # 422 newline or 433 newline

    fp.readline() # 13 newline or 6.5
    fp.readline() # 13 newline or 6.5
    
    info['FrameAxis'] = _read_string(fp) # Line 26 or 39
    info['DataType'] = _read_string(fp)
    info['ImageAxis'] = _read_string(fp)    

    _read_until(fp, ' ') # 65541 or 65539

    _read_until(fp, ' ') # x0? left? -> x0
    _read_until(fp, ' ') # x1? bottom? -> y1
    _read_until(fp, ' ') # y1? right? -> x1
    _read_until(fp, ' ') # y0? top? -> y0

    no_images = int(_read_until(fp, ' '))
    no_subimages = int(_read_until(fp, ' '))
    total_length = int(_read_until(fp, ' '))
    image_length = int(_read_until(fp, ' '))
    info['NumberOfFrames'] = no_images
    info['NumberOfSubImages'] = no_subimages
    info['TotalLength'] = total_length
    info['ImageLength'] = image_length

    for i in range(no_subimages):
        # read subimage information
        _read_until(fp, ' ') # 65538

        frame_area = fp.readline().strip().split()
        x0, y1, x1, y0, ybin, xbin = map(int,frame_area[:6])
        width = int((1 + x1 - x0) / xbin)
        height = int((1 + y1 - y0) / ybin)
        
    size = (int(width), int(height) * no_subimages)
    tile = []
    info['xbin'] = xbin
    info['ybin'] = ybin
    
    fp = _skip_spaces(fp)
    for f in range(no_images):
        info['timestamp_of_{0:d}'.format(f)] = int(fp.readline())
    
    offset = fp.tell()
    try: # remove extra 0 if it exits.
        flag = int(fp.readline())
        if flag == 0:
            offset = fp.tell()
        # remove another extra 1
        if flag == 1:
            if info['SifVersion'] == 65567:
                """
                In version 65567 after timestamp_array there is 1 and array of bigger numbers
                total of number of frames
                Maybe offset should be moved further in this case
                """
                for i in range(no_images):
                    fp.readline()
                    
                offset = fp.tell()
    except:
        fp.seek(offset)

    tile = [("raw",(0,0)+size, offset+f*width*height*no_subimages*4,
                     ('F;32F', 0, 1)) for f in range(no_images)]
                     
    info['size'] = size
    info['tile'] = tile
    info['offset'] = offset
    
    info = extract_user_text(info)
    return tile, size, no_images, info


def extract_user_text(info):
    """
    Extract known information from info['user_text'].
    Current known info is
    + 'Calibration data for frame %d'
    """
    user_text = info['user_text']
    if b'Calibration data for' in user_text[:20]:
        texts = user_text.split(b'\n')
        for i in range(info['NumberOfFrames']):
            key = 'Calibration_data_for_frame_{:d}'.format(i+1)
            coefs = texts[i][len(key)+2:].strip().split(b',')
            info[key] = [float(c) for c in coefs]
        # Calibration data should be None for this case
        info['Calibration_data'] = None
    else:
        coefs = info['Calibration_data'].strip().split()
        try:
            info['Calibration_data'] = [float(c) for c in coefs]
        except ValueError:
            del info['Calibration_data']
    del info['user_text']
    return info

def parser(sif_file, ignore_corrupt=False):
    """
    Open sif_file and return as np.array.

    Parameters
    ----------
    sif_file: 
        path to the file
    ignore_corrupt: 
        True if ignore the corrupted frames.
    lazy: either of None | 'memmap' | 'dask'
        None: load all the data into the memory
        'memmap': returns np.memmap pointing on the disk
        'dask': returns dask.Array that consists of np.memmap
            This requires dask installed into the computer.
    """
    
    will_close = False
    try:
        f = sif_file
        tile, size, no_images, info = inspect(f)
    except AttributeError:
        f = open(sif_file,'rb')
        tile, size, no_images, info = inspect(f)
        will_close = True

    data = np.ndarray((no_images, size[1], size[0]), dtype=np.float32)

    for i, tile1 in enumerate(tile):
        f.seek(tile1[2])  # offset
        try:
            data[i] = np.fromfile(f, count=size[0]*size[1],dtype='<f').reshape(size[1],size[0])

        except ValueError:
            data = data[:i]
            if not ignore_corrupt:
                raise ValueError(
                    'The file might be corrupt. Number of files should be {} '
                    'according to the header, but only {} is found in the file.'
                    'Use "ignore_corrupt=True" keyword argument to ignore.'.format(
                        no_images, len(data)
                    )
                )
            else:
                warnings.warn(
                    'The file might be corrupt. Number of files should be {} '
                    'according to the header, but only {} is found in the file.'.format(
                        no_images, len(data)
                    )
                )

    if will_close:
        f.close()
          
    return data, info



