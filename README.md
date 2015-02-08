# work18-cosmos

Working with the S-COSMOS dataset.

    Description of Data:
    http://irsa.ipac.caltech.edu/data/COSMOS/gator_docs/scosmos_irac_colDescriptions.html
    
    Fix header issues by ignoring comments:
    http://stackoverflow.com/questions/14158868
    
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
