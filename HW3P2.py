# parts a and b

import fsps
sp = fsps.StellarPopulation(compute_vega_mags=False, sfh=0, zmet=1, dust_type=1, uvb = .08, sf_start=.1)
hst_bands = fsps.find_filter('wfc_acs')
wanted = [hst_bands[1],hst_bands[-1]]
got_absmags = sp.get_mags(tage=14.1, bands=wanted)

import numpy as np
import emcee

got_noise = np.array([np.random.normal(.1), np.random.normal(.1)])
got_wave = np.array([8.14e-7, 6.06e-7])

distance = 8.2e3
got_appmags = got_absmags+got_noise+5*np.log10(distance/10.)
got_error = np.array([.1,.1])

def model(theta): # met, age, dist, extinction
    
    sp.params['zmet'] = np.round(theta[0])
    sp.params['sf_start'] = 14.1-theta[1]
    sp.params['uvb'] = theta[3]
    got_absmags1 = sp.get_mags(tage=14.1, bands=wanted)
    got_appmags1 = got_absmags1+5*np.log10(theta[2]/10.)
    return got_appmags1

def logL(theta, data, sigma):
    return -0.5*(np.sum((data-model(theta))**2/sigma**(2.) + np.log(2*np.pi*sigma**2))) 

def lnprob(theta, data, sigma):
    if theta[1] > 14.:
        return -np.inf
    if theta[1] < 9:
        return -np.inf
    if theta[0] > 5:
        return -np.inf
    if theta[0] < 1:
        return -np.inf
    if theta[2] > 1e5:
        return -np.inf
    if theta[2] < 1e2:
        return -np.inf
    if theta[3] > 3:
        return -np.inf
    if theta[3] < 0.001:
        return -np.inf
    else:
        return logL(theta, data, sigma) 
            
ndim, nwalkers = 4, 100
pos = [[3+1e-1*np.random.randn(), 9. + np.random.randn(), 500.+10*np.random.randn(), .01+.002*np.random.randn() ] for i in range(nwalkers)]

sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args = [got_appmags, got_error])
sampler.run_mcmc(pos, 1000)


plt.figure(figsize = (10,10))
[plt.plot(sampler.lnprobability[i,250:]) for i in range(100)]
plt.xlabel('step number', fontsize = 20)
plt.ylabel('lnP', fontsize = 20)



import corner

samples = sampler.chain[:,250:, :].reshape((-1, ndim))
corner.corner(samples, labels=['$met$', '$age$', '$dist$', '$uvb$'], fontsize = 20, show_titles = True, quantiles=[0.16, 0.5, 0.84])

# part c

wanted = [hst_bands[1],hst_bands[-1]]
got_absmags = sp.get_mags(tage=14.1, bands=wanted)
got_noise = np.array([np.random.normal(.01), np.random.normal(.01)])
got_appmags = got_absmags+got_noise+5*np.log10(distance/10.)
got_error = np.array([.01,.01])

# part d

wfc3_bands = fsps.find_filter('wfc3_uvis')
wanted = [hst_bands[1],wfc3_bands[4], wfc3_bands[7], hst_bands[-1]]
got_absmags = sp.get_mags(tage=14.1, bands=wanted)

import numpy as np
import emcee

got_noise = np.array([np.random.normal(.01), np.random.normal(.01),np.random.normal(.01), np.random.normal(.01)])
got_wave = np.array([8.14e-7, 3.36e-7, 4.38e-7, 6.06e-7])

distance = 8.2e3
got_appmags = got_absmags+got_noise+5*np.log10(distance/10.)
got_error = np.array([.01,.01,.01,.01])

ndim, nwalkers = 4, 100
pos = [[3+1e-1*np.random.randn(), 9. + np.random.randn(), 500.+10*np.random.randn(), .01+.002*np.random.randn() ] for i in range(nwalkers)]

sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args = [got_appmags, got_error])
sampler.run_mcmc(pos, 1000)

# part e

galex_fuv = fsps.find_filter('galex_fuv')
wanted = [hst_bands[1],wfc3_bands[4], wfc3_bands[7], hst_bands[-1], galex_fuv[0]]
got_absmags = sp.get_mags(tage=14.1, bands=wanted)

got_noise = np.array([np.random.normal(.01), np.random.normal(.01),np.random.normal(.01), np.random.normal(.01), np.random.normal(.01)])
got_wave = np.array([8.14e-7, 3.36e-7, 4.38e-7, 6.06e-7, 1.53e-7])
got_appmags = got_absmags+got_noise+5*np.log10(distance/10.)
got_error = np.array([.01,.01,.01,.01,.01])

ndim, nwalkers = 4, 100
pos = [[3+1e-1*np.random.randn(), 9. + np.random.randn(), 500.+10*np.random.randn(), .01+.002*np.random.randn() ] for i in range(nwalkers)]

sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args = [got_appmags, got_error])
sampler.run_mcmc(pos, 1000)
