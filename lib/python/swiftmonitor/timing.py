from swiftmonitor import observation, events2dat
from fluxtool import rms_estimator
import sys
import numpy as np

execute = observation.timed_execute

def prepfold(datfile,parfile,nbins):
  """
    Folds pulsar using prepfold with a par file.
  """
  cmd = 'prepfold -timing -par %s -n %d %s' % (parfile, nbins, datfile)
  execute(cmd)

def swiftfold(ob,freq,epoch,nbins=32):
  cmd = 'swiftfold -i %s -o %s -f %f -r %f -b %d' %\
        (ob.path + ob.reg_obsfile, ob.path + ob.obsroot + '.fold', freq, epoch, nbins)
  execute(cmd)

def pulsed_flux(ob, prof_file, twocycles=True, harmonics=5, bg_corrected=False):
  """
  Determine the RMS pulsed flux and pulsed fraction using Anne Archibald's 
    fluxtool. 

    Arguments:
      - ob: the swiftmonior.observation object for the observation.
      - prof_file: string filename of the folded profile. Profile has 
                   3 columns (bin number, counts, error).
    Optional Arguments:
      - twocycles: Whether or not the profile has 2 cycles.
                   Default=True
      - harmonics: Number of harmonics used to determine the RMS pulsed flux.
                   Default=5
      - bg_corrected: Whether or not the profile has been corrected for
                      background counts. Will correct the profile if False
                      before determining the RMS pulsed flux.
                      Default=False
      
    Returns a tuple of pulsed flux, pulsed flux error, pulsed fraction,
    and pulsed fraction error.
  """

  profile = np.loadtxt(prof_file)

  if not bg_corrected:
    ob.get_countrates()
    bg_counts = ob.bg_countrate * ob.exposure

  if not twocycles:
    histogram = profile[:,1]
    uncertainties = profile[:,2]
    if (len(histogram)%2==0 and 
      all(histogram[:len(histogram)//2]==
	     histogram[len(histogram)//2:])):
      sys.stderr.write("Warning: profile appears to contain two cycles\n")
  else:
    histogram = profile[:,1]
    uncertainties = profile[:,2]
    if len(histogram)%2==1:
      sys.stderr.write("Profile was supposed to contain two cycles but has odd length")
    if not all(histogram[:len(histogram)//2]==
	     histogram[len(histogram)//2:]):
      sys.stderr.write("Warning: profile does not appear to contain two cycles\n")
    uncertainties = uncertainties[:len(histogram)//2]    
    histogram = histogram[:len(histogram)//2]    

  if not bg_corrected:
    histogram = histogram - ( bg_counts / len(histogram) )

  total_flux = np.mean(histogram)

  rms_value, rms_uncertainty = rms_estimator(harmonics)(histogram, uncertainties)

  print "RMS pulsed flux:            \t%#0.7g\t+/-\t%#0.7g" % (rms_value, rms_uncertainty)
  print "RMS pulsed fraction:        \t%#0.7g\t+/-\t%#0.7g" % (rms_value/total_flux, rms_uncertainty/total_flux)
  
  return (rms_value, rms_uncertainty, rms_value/total_flux, rms_uncertainty/total_flux)
  

def get_TOA(datfile, template ):
  """
  Get a TOA using the PRESTO script get_TOAs.py.
  """
  cmd = 'get_TOAs.py -e -f -t %s %s' % (template, datfile) 
  execute(cmd)
