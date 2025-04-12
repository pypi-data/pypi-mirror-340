#!/usr/bin/env python
""" Utilitary functions to parse and read audio and text files. """
#
# Authors:  Juan Sebastian ULLOA <lisofomia@gmail.com>
#           Sylvain HAUPERT <sylvain.haupert@mnhn.fr>
#
# License: New BSD License

#%%
# =============================================================================
# Load the modules
# =============================================================================
# Import external modules
import numpy as np 
import pandas as pd
import re
import os
import glob
from datetime import datetime
from pathlib import Path # in order to be Windows/linux/MacOS compatible


#%%
# =============================================================================
# Private functions
# =============================================================================
def _date_from_filename (filename):
    """
    Extract date and time from the filename. Return a datetime object
    
    Parameters
    ----------
    filename : string
    The filename must follow this format :
    XXXX_yyyymmdd_hhmmss.wav
    with yyyy : year / mm : month / dd: day / hh : hour (24hours) /
    mm : minutes / ss : seconds
            
    Returns
    -------
    date : object datetime
        This object contains the date of creation of the file extracted from
        the filename postfix. 
    """
    # date by default
    date = datetime(1900,1,1,0,0,0,0)
    # test if it is possible to extract the recording date from the filename
    if filename[9:13].isdigit(): 
        yy=int(filename[9:13])
    else:
        return date
    if filename[13:15].isdigit(): 
        mm=int(filename[13:15])
    else:
        return date
    if filename[15:17].isdigit(): 
        dd=int(filename[15:17])
    else:
        return date
    if filename[18:20].isdigit(): 
        HH=int(filename[18:20])
    else:
        return date
    if filename[20:22].isdigit(): 
        MM=int(filename[20:22])
    else:
        return date
    if filename[22:24].isdigit(): 
        SS=int(filename[22:24])
    else:
        return date

    # extract date and time from the filename
    date = datetime(year=yy, month=mm, day=dd, hour=HH, minute=MM, second=SS, 
                    microsecond=0)
    
    return date


#%%
# =============================================================================
# Public functions
# =============================================================================
def read_audacity_annot (audacity_filename):
    """
    Read Audacity annotations file (or labeling file) and return a Pandas Dataframe
    with the bounding box and the label of each region of interest (ROI). Allows to
    read annotations with standard Audacity style (temporal selection) and with
    spectral selection style (spectro-temporal selection). If the file exists but has no 
    annotations, the function returns and empty dataframe.
    
    Parameters
    ----------
    audacity_filename : String
        Path to the audacity file

    Returns
    -------
    tab_out : Pandas Dataframe 
        Region of interest with time-frequency limits and manual annotation label
    
    References
    ----------
    https://manual.audacityteam.org/man/label_tracks.html  
    
    Examples
    --------
    >>> from maad import sound
    >>> from maad.util import power2dB, read_audacity_annot, format_features, overlay_rois
    >>> s, fs = sound.load('../data/cold_forest_daylight.wav')
    >>> Sxx_power, tn, fn, ext = sound.spectrogram(s, fs, nperseg=1024, noverlap=1024//2)
    >>> Sxx_db = power2dB(Sxx_power) + 96
    >>> df_rois = read_audacity_annot('../data/cold_forest_daylight_label.txt') 
    >>> df_rois = format_features(df_rois, tn, fn)
    >>> overlay_rois(Sxx_db, df_rois, **{'vmin':0,'vmax':96,'extent':ext})
    
    """
    # try to read file with tab delimiter (if the file is not empty)
    try:
        tab_in = pd.read_csv(audacity_filename, delimiter='\t', header=None)

        # test if time-frequency annotation (1st column contain '/')
        # Hack to force the type of the column to be string in order to test if 
        # the column contains a character
        tab_in[0] = tab_in[0].astype('str')
        if (tab_in[0].str.contains(r"\\", na = False).sum() > 0) :

            # arrange data
            t_info = tab_in.loc[np.arange(0, len(tab_in), 2), :]
            t_info = t_info.rename(index=str, columns={
                                0: 'min_t', 1: 'max_t', 2: 'label'})
            t_info = t_info.reset_index(drop=True)
    
            f_info = tab_in.loc[np.arange(1, len(tab_in)+1, 2), :]
            f_info = f_info.rename(index=str, columns={
                                0: 'slash', 1: 'min_f', 2: 'max_f'})
            f_info = f_info.reset_index(drop=True)
    
            # return dataframe
            tab_out = pd.concat(
                                [t_info['label'].astype('str'),
                                t_info['min_t'].astype('float32'),
                                f_info['min_f'].astype('float32'),
                                t_info['max_t'].astype('float32'),
                                f_info['max_f'].astype('float32')],  axis=1)
        else :
            tab_in = tab_in.rename(index=str, columns={
                                0: 'min_t', 1: 'max_t', 2: 'label'})
            tab_in['min_f'] = np.nan
            tab_in['max_f'] = np.nan
            
            # return dataframe
            tab_out = pd.concat([
                                tab_in['label'].astype('str'),
                                tab_in['min_t'].astype('float32'),
                                tab_in['min_f'].astype('float32'),
                                tab_in['max_t'].astype('float32'),
                                tab_in['max_f'].astype('float32')],  axis=1)
    except :
        tab_out = pd.DataFrame()

    return tab_out

#%%
def write_audacity_annot(fname, df_rois, save_file=True):
    """ 
    Write audio segmentation to text file in Audacity format, a file that can be imported
    and modified with Audacity. If the dataframe has no frequency delimiters, annotations
    are saved with standard Audacity format (temporal segmentation). If the dataframe has
    temporal and frequencial delimiters, the annotations are saved as spectral selection 
    style (spectro-temporal selection). If the dataframe is empty, the function saves an 
    empty file.
    
    Parameters
    ----------
    fname: str
        filename to save the segmentation
    df_rois: pandas dataframe
        Dataframe containing the coordinates corresponding to sound signatures
        In case of only temporal annotations : df_rois must contain at least
        the columns 'mint_t', 'max_t' 
        In case of bounding box (temporal eand frequency limits) :: df_rois 
        must contain at least the columns 'min_t', 'max_t', 'min_f', 'max_f'
    save_file: bool, optional, default=True
        If True, the file is saved. If False, the file is not saved.

    Returns
    -------
    df_to_save
        Dataframe that has been saved
    
    Examples
    --------
    >>> s, fs = maad.sound.load('../data/cold_forest_daylight.wav')
    >>> Sxx_power, tn, fn, ext = maad.sound.spectrogram(s, fs)
    >>> Sxx_db = maad.util.power2dB(Sxx_power) + 96
    >>> Sxx_power_noNoise= maad.sound.median_equalizer(Sxx_power)
    >>> Sxx_db_noNoise = maad.util.power2dB(Sxx_power_noNoise)
    >>> Sxx_db_noNoise_smooth = maad.sound.smooth(Sxx_db_noNoise, std=0.5)
    >>> im_mask = maad.rois.create_mask(im=Sxx_db_noNoise_smooth, mode_bin ='relative', 
                                        bin_std=8, bin_per=0.5)
    >>> im_rois, df_rois = maad.rois.select_rois(im_mask, min_roi=25, max_roi=None)
    >>> df_rois = maad.util.format_features(df_rois, tn, fn)
    
    Change path to save the file containing the labels position
    
    >>> df_to_save = maad.util.write_audacity_annot('save.txt', df_rois)
    
    Import the wav file then the label file in Audacity
    
    """
    if df_rois.empty:  # empty DataFrame
        print(f'{fname} > No detection found')
        df_to_save = pd.DataFrame(data=None)
        
    else:  
        # if there is no label, create a vector with incremental values
        if 'label' not in df_rois:
            df_rois['label'] = np.arange(0,len(df_rois))
        
        # if no frequency coordinates, only temporal annotations
        if ('min_f' not in df_rois) or ('max_f' not in df_rois):
            df_to_save = pd.DataFrame({'min_t':df_rois.min_t, 
                                    'max_t':df_rois.max_t, 
                                    'label':df_rois.label})
        else:
            df_to_save_odd = pd.DataFrame({'index': np.arange(0,len(df_rois)*2,2),
                                        'min_t':df_rois.min_t, 
                                        'max_t':df_rois.max_t, 
                                        'label':df_rois.label})
            df_to_save_even = pd.DataFrame({'index': np.arange(1,len(df_rois)*2,2),
                                        'min_t':'\\', 
                                        'max_t':df_rois.min_f, 
                                        'label':df_rois.max_f})
            df_to_save = pd.concat([df_to_save_odd,df_to_save_even])
            df_to_save = df_to_save.set_index('index')
            df_to_save = df_to_save.sort_index()
            
    if save_file:
        df_to_save.to_csv(fname, index=False, header=False, sep='\t') 
    else:
        pass
    
    return df_to_save

#%% 
def read_raven_annot(raven_filename):
    """
    Read Raven annotations file (or labeling file) and return a Pandas Dataframe
    with the bounding box and the label of each region of interest (ROI). If the file 
    exists but has no annotations, the function returns and empty dataframe.
    
    Parameters
    ----------
    raven_filename : string
        Path to the annotation file

    Returns
    -------
    tab_out : Pandas Dataframe 
        Region of interest with time-frequency limits and manual annotation label
    
    References
    ----------
    http://ravensoundsoftware.com/wp-content/uploads/2017/11/Raven14UsersManual.pdf
        
    """
    df_out = pd.read_csv(raven_filename, sep='\t')
    return df_out
    
#%%
def write_raven_annot(fname, df_rois, save_file=True):
    """ 
    Write audio segmentation to text file in Raven format, a file that can be imported
    and modified with Raven. If the dataframe has no frequency delimiters, annotations
    are saved with standard Audacity format (temporal segmentation). If the dataframe has
    temporal and frequencial delimiters, the annotations are saved as spectral selection 
    style (spectro-temporal selection). If the dataframe is empty, the function saves an 
    empty file.
    
    Parameters
    ----------
    fname: str
        filename to save the segmentation
    df_rois: pandas dataframe
        Dataframe containing the coordinates corresponding to sound signatures
        For bounding box (temporal eand frequency limits) :: df_rois 
        must contain at least the columns 'min_t', 'max_t', 'min_f', 'max_f'
            
    Returns
    -------
    df_out: pandas dataframe
        Dataframe that has been saved in Raven format
    
    Examples
    --------
    >>> from maad import sound, rois, util
    >>> s, fs = sound.load('../data/spinetail.wav')
    >>> df_rois = rois.find_rois_cwt(s, fs, flims=(3000,8000), tlen=2, th=0)
    >>> df_rois['Label'] = 'Spinetail'
    >>> df_raven = util.write_raven_annot('spinetail_annotations.txt', df_rois)
    
    """
    df_out = df_rois.copy()
    # Save empty file if dataframe is empty
    if df_out.size==0:
        print(fname, '> No detection found')
        df = pd.DataFrame(data=None)
        df.to_csv(fname, sep='\t', header=False, index=False)
        
    else:
        # Format dataframe and save
        # add basic raven columns if needed
        if not('Selection' in df_out.columns):
            df_out['Selection'] = np.arange(1, len(df_out)+1)
        
        if not('View' in df_out.columns):
            df_out['View'] = 'Spectrogram 1'
        
        if not('Channel' in df_out.columns):
            df_out['Channel'] = 1
        
        # change column names
        df_out.rename(columns={
                        'min_t': 'Begin Time (s)', 
                        'max_t': 'End Time (s)',
                        'min_f': 'Low Freq (Hz)',
                        'max_f': 'High Freq (Hz)'}, inplace=True)
        
        # reorder column names
        colname_raven = ['Selection', 'View', 'Channel', 'Begin Time (s)',
                        'End Time (s)', 'Low Freq (Hz)', 'High Freq (Hz)']
        colname_order = colname_raven + df_out.columns[~df_out.columns.isin(colname_raven)].tolist()
        df_out = df_out.reindex(columns=colname_order)
        
        if save_file:
            df_out.to_csv(fname, sep='\t', index=False)
        else:
            pass
    
    return df_out

#%%
def date_parser(datadir, dateformat='%Y%m%d_%H%M%S', extension='.wav', prefix = '', verbose=False):
    """
    Extracts dates from filenames in a given folder and subfolders.

    Parameters
    ----------
    datadir : str
        Path to the folder to search for files.
    dateformat : str, optional
        Format string specifying the datetime pattern to extract.
        The default is'%Y%m%d_%H%M%S'
        For more information about the format codes, refer to the
        `strftime format documentation <https://strftime.org/>`_.
    extension : str, optional, 
        File extension to filter files by (e.g., '.wav', '.mp3').
        The default is '.wav'.
    prefix : str, optional, 
        Prefix of the filenames to match.
        The default is ''.
    verbose : bool, optional
        If True, print the filenames as they are processed.
        The default is False.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the extracted dates as the index 'Date',
        and the full file paths in a 'file' column.

    Raises
    ------
    ValueError
        If the datetime_format is invalid or does not match the filenames.

    Notes
    -----
    This function searches for files in the specified folder and its subfolders
    that have the given extension and match the specified prefix. It extracts
    the dates from the filenames using the provided datetime_format.

    The extracted dates are set as the index of the resulting DataFrame. The
    'file' column contains the full file paths.

    Examples
    --------
    >>> folder_path = '../../data/indices/'
    >>> ext = '.wav'
    >>> datetime_format = '%Y%m%d_%H%M%S'
    >>> df = maad.util.date_parser(datadir=folder_path, dateformat=datetime_format, extension=ext)
    >>> df
                                                                    file
    Date	
    2019-05-22 00:00:00	../../data/indices/S4A03895_20190522_000000.wav
    2019-05-22 00:15:00	../../data/indices/S4A03895_20190522_001500.wav
    2019-05-22 00:30:00	../../data/indices/S4A03895_20190522_003000.wav
    2019-05-22 00:45:00	../../data/indices/S4A03895_20190522_004500.wav
    2019-05-22 01:00:00	../../data/indices/S4A03895_20190522_010000.wav
                    ...	                                            ...
    2019-05-22 22:45:00	../../data/indices/S4A03895_20190522_224500.wav
    2019-05-22 23:00:00	../../data/indices/S4A03895_20190522_230000.wav
    2019-05-22 23:15:00	../../data/indices/S4A03895_20190522_231500.wav
    2019-05-22 23:30:00	../../data/indices/S4A03895_20190522_233000.wav
    2019-05-22 23:45:00	../../data/indices/S4A03895_20190522_234500.wav


    >>> df = maad.util.date_parser("../../data/indices/", dateformat='SM4', verbose=False)
    >>> list(df)
    >>> df
                                                                    file
    Date	
    2019-05-22 00:00:00	../../data/indices/S4A03895_20190522_000000.wav
    2019-05-22 00:15:00	../../data/indices/S4A03895_20190522_001500.wav
    2019-05-22 00:30:00	../../data/indices/S4A03895_20190522_003000.wav
    2019-05-22 00:45:00	../../data/indices/S4A03895_20190522_004500.wav
    2019-05-22 01:00:00	../../data/indices/S4A03895_20190522_010000.wav
                    ...	                                            ...
    2019-05-22 22:45:00	../../data/indices/S4A03895_20190522_224500.wav
    2019-05-22 23:00:00	../../data/indices/S4A03895_20190522_230000.wav
    2019-05-22 23:15:00	../../data/indices/S4A03895_20190522_231500.wav
    2019-05-22 23:30:00	../../data/indices/S4A03895_20190522_233000.wav
    2019-05-22 23:45:00	../../data/indices/S4A03895_20190522_234500.wav


    """    

    file_pattern = os.path.join(datadir, f'**/{prefix}*{extension}')
    file_list = glob.glob(file_pattern, recursive=True)
    data = []

    for file_path in file_list:

        # Extract the filename from the full path
        filename = os.path.basename(file_path)

        if dateformat == 'SM4':
            date =_date_from_filename(filename)
            data.append({'Date': date, 'file': file_path})
        
        elif dateformat == 'POSIX':
            posix_time = int(Path(filename).stem, 16)
            date = datetime.utcfromtimestamp(posix_time).strftime('%Y-%m-%d %H:%M:%S')
            data.append({'Date': date, 'file': file_path})

        else: 
            # Construct a regex pattern to extract the date from the filename
            pattern = _construct_pattern(dateformat)
            # Search for the date in the filename
            match = pattern.search(filename)
            # If a match is found, extract the date
            if match:
                if verbose:
                    print(f'File: {filename}')
                # Extract the date from the filename
                date_str = match.group()
                # Parse the date string
                try:
                    date = datetime.strptime(date_str, dateformat)
                    data.append({'Date': date, 'file': file_path})
                except ValueError:
                    print(f"Error parsing date: {date_str} in file: {filename}. The default date and time 1900-01-01 00:00:00 will be used.")
                    # date by default
                    data.append({'Date': "1900-01-01 00:00:01", 'file': file_path})
            else:
                print(f"No date found in file: {file_path}. The default date and time 1900-01-01 00:00:00 will be used.")
                # date by default 1900-01-01 00:00:00
                data.append({'Date': "1900-01-01 00:00:01", 'file': file_path})
    if len(data) > 0:
        df = pd.DataFrame(data)
        df.set_index('Date', inplace=True)
        # convert index to datetime 
        df.index = pd.DatetimeIndex(df.index)
        # sort dataframe by date
        df = df.sort_index(axis=0)
    else:
        df = pd.DataFrame()

    return df

def _construct_pattern(datetime_format):
    format_dict = {
        '%Y': r'(\d{4})',
        '%y': r'(\d{2})',
        '%m': r'(0[1-9]|1[0-2])',
        '%d': r'(0[1-9]|1\d|2[0-9]|3[01])',
        '%H': r'([01]\d|2[0-3])',
        '%I': r'(0[1-9]|1[0-2])',
        '%p': r'(AM|PM)',
        '%M': r'([0-5]\d)',
        '%S': r'([0-5]\d)',
        '%f': r'(\d{6})',
        '%j': r'(\d{3})',
        '%U': r'(\d{2})',
        '%W': r'(\d{2})',
        '%w': r'(\d)',
        '%A': r'(\w+)',
        '%a': r'(\w+)',
        '%B': r'(\w+)',
        '%b': r'(\w+)',
        '%c': r'(.+)',
        '%x': r'(.+)',
        '%X': r'(.+)',
        '%%': r'%',
    }
    pattern = datetime_format
    for code, regex in format_dict.items():
        pattern = pattern.replace(code, regex)
    pattern = re.compile(pattern)

    return pattern
