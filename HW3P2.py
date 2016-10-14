import fsps
sp = fsps.StellarPopulation(compute_vega_mags=False, sfh=0, zmet=1, dust_type=2, dust2=0.2, sf_start=.1)
hst_bands = fsps.find_filter('wfc_acs')
wanted = [hst_bands[1],hst_bands[-1]]
sp.get_mags(tage=14.1, bands=wanted)

import numpy as np
import emcee

got_absmags = np.array([6.5365, 6.3997])
got_noise = np.array([np.random.normal(.1), np.random.normal(.1)])
got_wave = np.array([8.14e-7, 6.06e-7])

distance = 8.2e3
got_appmags = got_absmags+got_noise+5*np.log10(distance/10.)
got_error = np.array([.1,.1])

def model(theta): # met, age, dist
    sp.params['zmet'] = np.round(theta[0])
    sp.params['sf_start'] = 14.1-theta[1]
    got_absmags1 = sp.get_mags(tage=14.1, bands=wanted)
    got_appmags1 = got_absmags1+5*np.log10(theta[2]/10.)
    return got_appmags1

def logL(theta, data, sigma):
    return -0.5*(np.sum((data-model(theta))**2)/sigma**(2.) + np.log(2*np.pi*sigma**2)) 

def lnprior(theta):
    if theta[1] > 14.:
        return -np.inf
    if theta[1] < 5:
        return -np.inf
    if theta[0] > 5:
        return -np.inf
    if theta[2] > 10e3:
        return -np.inf

def lnprob(theta, data, sigma):
    return logL(theta, data, sigma) + lnprior(theta)
            
ndim, nwalkers = 3, 100
pos = [[7+1e-1*np.random.randn(), 3. + np.random.randn(), 500.+10*np.random.randn() ] for i in range(nwalkers)]

sampler = emcee.EnsembleSampler(nwalkers, ndim, logL, args = [got_appmags, got_error])
sampler.run_mcmc(pos, 10)
