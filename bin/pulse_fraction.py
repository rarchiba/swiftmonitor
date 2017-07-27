#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import swiftmonitor.utils as smu
from swiftmonitor import model_profile
from optparse import OptionParser
from fluxtool import rms_estimator

parser = OptionParser("Usage: %prog [options] fitsfile \n Returns: name pulseflux pulsefluxerr pulse_fraction pulse_fraction_error ",version="%prog 1.0")
parser.add_option("-p", "--par",
    dest="parfile", type='string',
    help="Name of par file with pulsar ephemeris.",
    default=None)
parser.add_option("-n", "--nbins",
    dest="nbins", type='int',
    help="Number of bins to fold. Default is 16.",
    default=16)
parser.add_option("--scope",
    dest="scope", type='string',
    help="Event files are from this telescope, default swift.",
    default='swift')
parser.add_option("--Emin",
    dest="emin", type='float',
    help="Minimum energy of events to use (works only for Swift, Nustar).",
    default=None)
parser.add_option("--Emax",
    dest="emax", type='float',
    help="Maximum energy of events to use (works only for Swift, Nustar).",
     default=None)		  		  
parser.add_option("-l", "--list",
    dest="list", type='string',
    help="File with list of event files to get events from.",
    default=None)      
parser.add_option("--normed",action="store_true",
    dest="normed",
    help="If flagged,  normalized by exposure.")  
(options,args) = parser.parse_args()

if options.list:
    EVTs = np.loadtxt(options.list, dtype='S')#.T[0]
    phases = np.zeros(0)
    for evt in EVTs:     
        pulsed_flux, pulsed_flux_err = smu.pulsed_flux_rms(evt, options.parfile,normed = options.normed, nbins = options.nbins, scope=options.scope, Emin=options.emin,Emax=options.emax)
        p_frac, p_frac_err = smu.pulsed_fraction_rms(evt, options.parfile, nbins= options.nbins, scope=options.scope, Emin=options.emin,Emax=options.emax)
        date = np.mean(smu.fits2times(evt,scope=options.scope, Emin=options.emin,Emax=options.emax))
        print evt, date , pulsed_flux, pulsed_flux_err, p_frac, p_frac_err 
        
else:                      
    pulsed_flux, pulsed_flux_err = smu.pulsed_flux_rms(args[0], options.parfile,normed = options.normed, nbins = options.nbins, scope=options.scope, Emin=options.emin,Emax=options.emax)
    p_frac, p_frac_err = smu.pulsed_fraction_rms(args[0], options.parfile, nbins= options.nbins, scope=options.scope, Emin=options.emin,Emax=options.emax)
    date = np.mean(smu.fits2times(args[0],scope=options.scope, Emin=options.emin,Emax=options.emax))
    print args[0], date , pulsed_flux, pulsed_flux_err, p_frac, p_frac_err 
