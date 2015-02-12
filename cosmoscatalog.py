#!/usr/local/bin/python

# import
from __future__ import print_function
import os, sys
import numpy
import shutil, subprocess
import csv
import seaborn as sns


class Cosmos():
    '''Working with the S-COSMOS dataset.

    Description of Data:
    http://irsa.ipac.caltech.edu/data/COSMOS/gator_docs/scosmos_irac_colDescriptions.html
    
    Channels            Apertures
        1: 3.550um          1: 1.4''
        2: 4.493um          2: 1.9''            
        3: 5.731um          3: 2.9''
        4: 7.872um          4: 4.1''

    MAXFLAG: meaning of additive values
        0 perfect source               16 incomplete aperture data
        1 bright/close neighbors       32 incomplete isophotal data
        2 blended/overlapping          64 deblending caused mem overflow
        4 pixels saturated             128 extraction caused mem overflow
        8 image boundary object

    USAGE



    from cosmoscatalog import Cosmos
    
    fp = '/Volumes/ESSENTIA/cosmos.csv'
    MAXFLAG = 0                         # max flag
    MINFLUX = 1.0                       # minimum flux across all channels 
                                        # and apertures
    HEADER = 119                        # int number of header lines to skip

    cos = Cosmos(fp, HEADER, MINFLUX, MAXFLAG)
    cos.process()                       # applying constraints to data
    cos.color(r=3, g=2, b=1)            # channels for red/green/blue

    '''

    def __init__(self, fp='/Volumes/ESSENTIA/cosmosNOHEADER.csv', 
                 HEADER=0, MINFLUX=1.0, MAXFLAG=0):
        '''Prepare for processing.'''
        if not os.path.exists(fp):
            sys.exit('File does not exist.')

        # file properties
        self.fp = fp
        self.file = os.path.basename(fp)
        self.fileext = os.path.splitext(self.file)[1]
        self.filesize = os.path.getsize(fp)
        print(self.file, 'is a', self.fileext, 'file of', 
              self.filesize, 'bytes.')

        # constraints
        self.MINFLUX = MINFLUX
        self.MAXFLAG = MAXFLAG
        # flux columns and their match to (channel#, aperture#)
        self.indx = {0:['id', (0,0)],
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
        self.corr = numpy.array([[0.610,0.765,0.900,0.950],
                                 [0.590,0.740,0.900,0.940],
                                 [0.490,0.625,0.840,0.940],
                                 [0.450,0.580,0.730,0.910]])

        # create play file without header
        if HEADER > 0:
            newfp = self.fp[:-4] + 'NOHEADER' + self.fileext
            shutil.copyfile(self.fp, newfp)
            self.fp = newfp
            delstmt = '1,%i d' % int(HEADER)
            sub = subprocess.call(['sed', '-i', '', delstmt, self.fp])

    def _csvgen(self, constraints):
        '''Applies constraints and returns a generator of good data.

        constraints is list of [[column index # to be evaluated, value]]

        http://stackoverflow.com/questions/17444679
        http://stackoverflow.com/questions/14158868
        '''

        # apply constraints and return generator
        with open(self.fp, 'rb') as f:
            self.n, self.n_flag, self.n_flux = 0,0,0

            for row in csv.reader(f, quoting = csv.QUOTE_NONNUMERIC):
                self.n += 1

                # satisfy constraints
                satisfied = True
                for i, c in enumerate(constraints):
                    if satisfied:
                        if i > 0: # flux constraint
                            row[c[0]] = row[c[0]]/c[1]

                            if self.indx[c[0]][0].startswith('flux'):
                                if row[c[0]] < self.MINFLUX:
                                    satisfied = False
                                    self.n_flux += 1
                        else: # flag constraint
                            if row[c[0]] > self.MAXFLAG:
                                satisfied = False
                                self.n_flag += 1

                # yield row to generator if all constraints satisfied
                if satisfied:
                    yield row

    def process(self):
        '''Process that file :p

        constraints:
        1. lose all rows with flags 
        2. divide all sixteen fluxes (and errors) by correct flux correction
        3. lose all rows with any flux value < 1 uJy
        '''
        # constraints
        flagger = [[14, self.MAXFLAG]]
        flux_crit = [[i, self.corr[self.indx[i][1][0]-1][self.indx[i][1][1]-1]] 
                      for i in self.indx.keys() 
                      if self.indx[i][0].startswith(('flux','err'))]
        constraints = flagger + flux_crit

        if self.fileext == '.csv':
            data = []
            for row in self._csvgen(constraints):
                data.append(row)

            # check n_flag + n_flux = n_lost = n - len(data)
            print('flag',self.n_flag/float(self.n),
                  'flux',self.n_flux/float(self.n),
                  'saved',len(data)/float(self.n),
                  'total',self.n)

            # attach to self
            self.data = numpy.array(data)
        else:
            sys.exit('Can only deal with CSV files as of yet.')

    def color(self, r=3, g=2, b=1):
        '''Color plot.

        Choose channels for your red/green/blue where
        r/g := f(b/g)
        
        Eq. Let aperture a.
        rgb[a-1] = [x, y, xerr, yerr]
        x = blue(a)/green(a)
        y = red(a)/green(a)
        xerr = x * Sqrt[ (db(a)/blue(a))^2 + (dg(a)/green(a))^2 ] 
        yerr = y * Sqrt[ (dr(a)/red(a))^2 + (dg(a)/green(a))^2 ] 

        blue(a)  = data[:, fAC[a-1][b-1]]
        red(a)   = data[:, fAC[a-1][r-1]]
        green(a) = data[:, fAC[a-1][g-1]]
        db(a)    = data[:, eAC[a-1][b-1]]
        dr(a)    = data[:, eAC[a-1][r-1]]
        dg(a)    = data[:, eAC[a-1][g-1]]

        Returns
        rgb[a-1] = [x, y, xerr, yerr]

        '''
        # these are indicies for flux and error as function of a and c.
        # flux at aperture a and channel c is found at data[:, fAC[a-1][c-1]]
        fAC = [[k for k in self.indx.keys() if self.indx[k][0].startswith('flux') 
                and self.indx[k][1][1] == a+1] for a in xrange(4)]
        eAC = [[k for k in self.indx.keys() if self.indx[k][0].startswith('err') 
                and self.indx[k][1][1] == a+1] for a in xrange(4)]

        # colors rgb[a] = [x, y, xerr, yerr]
        rgb = []
        for a in xrange(4):
            x = self.data[:, fAC[a-1][b-1]] / self.data[:, fAC[a][g-1]]
            y = self.data[:, fAC[a-1][r-1]] / self.data[:, fAC[a][g-1]]
            xerr = x * numpy.sqrt( numpy.power(self.data[:, eAC[a][b-1]] 
                                             / self.data[:, fAC[a][b-1]],2) 
                                 + numpy.power(self.data[:, eAC[a][g-1]] 
                                             / self.data[:, fAC[a][g-1]],2))
            yerr = y * numpy.sqrt( numpy.power(self.data[:, eAC[a][r-1]] 
                                             / self.data[:, fAC[a][r-1]],2) 
                                 + numpy.power(self.data[:, eAC[a][g-1]] 
                                             / self.data[:, fAC[a][g-1]],2))
            rgb.append([x, y, xerr, yerr])

        # attach to self
        self.rgb = numpy.array(rgb)
        
        # plot using seaborn+pandas? see ipython notebook
        
        return self.rgb
        











    def magnitude(self):
        '''Convert to Magnitude.
        
        M = -2.5 log(flux) + 23.9
        M_Vega = -2.5 log (flux) + 23.9 + K
            where K = [-2.788, -3.255, -3.743, -4.372] per channel
        '''
        pass