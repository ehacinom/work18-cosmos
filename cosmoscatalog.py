#!/usr/local/bin/python

# import
from __future__ import print_function
import os, sys
import csv
from functools import wraps


class Cosmos():
    '''Working with the S-COSMOS dataset.

    Description of Data:
    http://irsa.ipac.caltech.edu/data/COSMOS/gator_docs/scosmos_irac_colDescriptions.html
    
    Channels
        1: 3.550um
        2: 4.493um
        3: 5.731um
        4: 7.872um
    
    Apertures
        1: 1.4''
        2: 1.9''
        3: 2.9''
        4: 4.1''
    
    Usage:

    from cosmoscatalog import Cosmos
    fp = '/Volumes/ESSENTIA/cosmos.csv'
    cos = Cosmos(fp)
    cos.process()
    
    '''
    
    def __init__(self,fp='/Volumes/ESSENTIA/cosmos.csv'):
        '''Prepare for processing.'''
        if not os.path.exists(fp):
            sys.exit('File does not exist.')

        # file properties
        self.fp = fp
        self.file = os.path.basename(fp)
        self.fileext = os.path.splitext(self.file)[1]
        self.filesize = os.path.getsize(fp) # bytes
        print(self.file, 'is a', self.fileext, 'file of', self.filesize, 'bytes')
        
        # criteria
        # flux columns and their match to (channel#, aperture#)
        self.colindex = {0:['id', (0,0)],
                         14:['flag', (0,0)],
                         15:['flux_c1_1', (1,1)],
                         16:['err_c1_1', (1,1)],
                         17:['flux_c1_2', (1,2)],
                         18:['err_c1_2', (1,2)],
                         19:['flux_c1_3', (1,3)],
                         20:['err_c1_3', (1,3)],
                         21:['flux_c1_4', (1,4)],
                         22:['err_c1_4', (1,4)],
                         23:['fl_c1', (1,0)],
                         24:['flux_c2_1', (2,1)],
                         25:['err_c2_1', (2,1)],
                         26:['flux_c2_2', (2,2)],
                         27:['err_c2_2', (2,2)],
                         28:['flux_c2_3', (2,3)],
                         29:['err_c2_3', (2,3)],
                         30:['flux_c2_4', (2,4)],
                         31:['err_c2_4', (2,4)],
                         32:['fl_c2', (2,0)],
                         33:['flux_c3_1', (3,1)],
                         34:['err_c3_1', (3,1)],
                         35:['flux_c3_2', (3,2)],
                         36:['err_c3_2', (3,2)],
                         37:['flux_c3_3', (3,3)],
                         38:['err_c3_3', (3,3)],
                         39:['flux_c3_4', (3,4)],
                         40:['err_c3_4', (3,4)],
                         41:['fl_c3', (3,0)],
                         42:['flux_c4_1', (4,1)],
                         43:['err_c4_1', (4,1)],
                         44:['flux_c4_2', (4,2)],
                         45:['err_c4_2', (4,2)],
                         46:['flux_c4_3', (4,3)],
                         47:['err_c4_3', (4,3)],
                         48:['flux_c4_4', (4,4)],
                         49:['err_c4_4', (4,4)],
                         50:['fl_c4', (4,0)]}
        # corrections by self.corr[channel#-1, aperture#-1]
        self.corr = np.array([[0.610,0.765,0.900,0.950],
                              [0.590,0.740,0.900,0.940],
                              [0.490,0.625,0.840,0.940],
                              [0.450,0.580,0.730,0.910]])

    def listify(fn=None, wrapper=list):
        """A decorator which wraps a function's return value in ``list(...)``.

        Useful when an algorithm can be expressed more cleanly as a generator but
        the function should return an list.

        http://stackoverflow.com/questions/12377013

        Example::

            >>> @listify
            ... def get_lengths(iterable):
            ...     for i in iterable:
            ...         yield len(i)
            >>> get_lengths(["spam", "eggs"])
            [4, 4]
            >>>
            >>> @listify(wrapper=tuple)
            ... def get_lengths_tuple(iterable):
            ...     for i in iterable:
            ...         yield len(i)
            >>> get_lengths_tuple(["foo", "bar"])
            (3, 3)
        """
        def listify_return(fn):
            @wraps(fn)
            def listify_helper(*args, **kw):
                return wrapper(fn(*args, **kw))
            return listify_helper
        if fn is None:
            return listify_return
        return listify_return(fn)

    def csvgen(self, criteria):
        '''Read csv file, process flags and fluxes, 

        criteria is list of [[column# to be evaluated, good value]]
        
        http://stackoverflow.com/questions/17444679
        '''
        with open(self.fp, 'rb') as f:
            count = 0
            for row in csv.reader(f):
                # skip headers and comments
                if row[0].startswith('\\') or row[0].startswith('|'):
                    continue
                
                # check all criteria satisfied
                satisfied = True
                for c in criteria:
                    if satisfied:
                        if row[c[0]] != c[1]: 
                            satisfied = False

                # return row to generator if all criteria satisfied
                if satisfied:
                    yield row
                    count += 1
                elif count < 2:
                    continue
                else:
                    return

    def process(self):
        '''Process that file~

        criteria:
        1. lose all rows with flags (print number)
        2. divide all sixteen fluxes (and errors?) by correct flux correction
        3. lose all rows with any flux value < 1 uJy (print number)
        
        convert:
        4. convert to Magnitude
        '''
        # criteria 1
        flagger = [14, 0]

        criteria = flagger + flux_crit

        # if csv
        if self.fileext = '.csv':
            data = self.listify(self.csvgen(criteria))
        else:
            sys.exit('Can only deal with CSV files as of yet.')






    def corrections(self):
        '''Step 1. Divide fluxes by correction factor.
        
        individual correction is f_corr[channel# - 1][aperture# - 1]
        '''
        
        # some sort of lookup

        
    def magnitude(self):
        '''Step 4. Convert to AB Magnitude.
        
        M = -2.5 log(flux) + 23.9
        M_Vega = -2.5 log (flux) + 23.9 + K
            where K = [-2.788, -3.255, -3.743, -4.372] per channel
        '''
        

def getstuff(filename, criterion):
    with open(filename, "rb") as csvfile:
        datareader = csv.reader(csvfile)
        count = 0
        for row in datareader:
            if row[3] in ("column header", criterion):
                yield row
                count += 1
            elif count < 2:
                continue
            else:
                return












