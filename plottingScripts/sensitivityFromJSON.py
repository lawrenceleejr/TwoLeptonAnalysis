#!/usr/bin/env python


import ROOT
import numpy as np
from rootpy import asrootpy
from rootpy.plotting import Hist, HistStack, Legend, Canvas, Graph
from rootpy.plotting.style import get_style, set_style
from rootpy.plotting.utils import get_limits
from rootpy.interactive import wait
from rootpy.io import root_open
import rootpy.plotting.root2matplotlib as rplt
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from pylab import *
import os

from ATLASStyle import *

from copy import deepcopy


from interpolateGrid import *

# import style_mpl

import seaborn as sns
sns.set(style="whitegrid")

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

mpl.rcParams['text.latex.preamble'] = [
       r'\usepackage{siunitx}',   # i need upright \micro symbols, but you need...
       r'\sisetup{detect-all}',   # ...this to force siunitx to actually use your fonts
       r'\usepackage{helvet}',    # set the normal font here
       r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
       r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
]  



# Config ##########################################################

def GetSigma( p ):
    # // double pres limit:
    if p > (1.0-1e-16):
        return -7.4;
    # // double pres limit:
    if (p < 1e-16) :
        return 7.4;
    # // convert p-value in standard deviations ("nsigma")
    nsigma = 0.;
    if (p > 1.0e-16): 
        nsigma = ROOT.TMath.ErfInverse( 1.0 - 2.0 * p )*sqrt(2.0);
    elif (p > 0) :
        # // use approximation, ok for sigma > 1.5
        u = -2.0 * ROOT.TMath.Log( p*ROOT.TMath.Sqrt( 2.*ROOT.TMath.Pi() ) );
        nsigma = ROOT.TMath.Sqrt( u - ROOT.TMath.Log(u) );
    else:
        nsigma = -1;

    return nsigma;



samples = [
			# 'Data',
			# 'QCD',
			'Top',
			'W',
			'Z',
			'Diboson'
			]

lumiscale = 3.2
writePlots = True
combineRegions = 1
compareToMeff = 1

# SignalGrids = ["SS_direct","GG_direct"]
SignalGrids = ["GG_direct"]
# SignalGrids = ["SS_direct"]
# SignalGrids = ["GG_onestepCC"]


myxlabel = {}
myxlabel["SS_direct"] = r"$m_{\tilde{q}}$ [GeV]"
myxlabel["GG_direct"] = r"$m_{\tilde{g}}$ [GeV]"
myxlabel["GG_onestepCC"] = r"$m_{\tilde{g}}$ [GeV]"


MeffRegions = [

"SR2jl",
"SR2jm",
"SR2jt",
"SR4jt",
"SR5j",
"SR6jm",
"SR6jt",

]


cuts = MeffRegions+[
		"SRJigsawSRG1a",
		"SRJigsawSRG1b",
		"SRJigsawSRG1c",
		"SRJigsawSRG2a",
		"SRJigsawSRG2b",
		"SRJigsawSRG2c",
		"SRJigsawSRG3a",
		"SRJigsawSRG3b",
		"SRJigsawSRG3c",

		"SRJigsawSRS1a",
		"SRJigsawSRS1b",
		"SRJigsawSRS2a",
		"SRJigsawSRS2b",
		"SRJigsawSRS3a",
		"SRJigsawSRS3b",

		"SRJigsawSRC1a",
		"SRJigsawSRC1b",
		"SRJigsawSRC2a",
		"SRJigsawSRC2b",
		"SRJigsawSRC3a",
		"SRJigsawSRC3b",
		"SRJigsawSRC4a",
		"SRJigsawSRC4b",

] 


colorpal = sns.color_palette("husl", 4 )





figSens = plt.figure(figsize=(8,5), dpi=100 )

from ROOT import RooStats


import json

for SignalGrid in SignalGrids:

	bestZbi = {}
	bestmeffZbi = {}

	for tmpcut in cuts:

		jsonfilename = 'JSON/%s_%s__1_harvest_list.json'%(tmpcut,SignalGrid)
		if os.path.exists(jsonfilename):
			with open(jsonfilename) as data_file:    
			    data = json.load(data_file)
		else:
			print "can't find the json file for %s" % tmpcut
			continue

		plt.clf()

		x = []
		y = []
		z = []

		print tmpcut

		for ipoint in data:

			myx = ipoint["mgl"]
			myy = ipoint["mlsp"]
			myz = ROOT.RooStats.PValueToSignificance( ipoint["p0"] )

			myz = ipoint["CLsexp"] 
			myz = ROOT.RooStats.PValueToSignificance( ipoint["CLsexp"] )
			# myz = ipoint["p0"]

			if np.isinf(myx) or np.isinf(myy) or np.isinf(myz):
				continue

			x.append(myx)
			y.append(myy)
			z.append(myz)

			# bestZbi[(myx,myy)] = (0,"")
			# bestmeffZbi[(myx,myy)] = (0,"")


			# if compareToMeff != tmpcut:
			try:
				if not(tmpcut in MeffRegions) and myz > bestZbi[(myx,myy)][0]:
					bestZbi[(myx,myy)] = (myz,tmpcut)

				if tmpcut in MeffRegions and myz > bestmeffZbi[(myx,myy)][0]:
					bestmeffZbi[(myx,myy)] = (myz,tmpcut)

			except:
				if tmpcut in MeffRegions:
					bestmeffZbi[(myx,myy)] = (myz,tmpcut)
				else:
					bestZbi[(myx,myy)] = (myz,tmpcut)




		xarray, yarray, zarray = deepcopy(x),deepcopy(y),deepcopy(z)

		(x,y,z,xi,yi,zi) = interpolateGridArray(x,y,z,withZeros=1)

		# figSens = plt.figure(  figsize=(8,5), dpi=100  )

		plt.imshow(zi, vmin=0, vmax=7, origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], cmap='jet', alpha=0.8)


		plt.colorbar(label=r"Expected CLs Z Value [$\sigma$]")

		# CS = plt.contour(zi, [2,3,4,5], vmin=0, vmax=7, origin='lower',
		#            extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		# plt.clabel(CS, fontsize=9, inline=1, colors="k", linecolor="white", fmt='%1.0f $\\sigma$')


		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="black", linecolor="black", fmt='%1.0f $\\sigma$')


		CS2 = plt.contour(zi, [ROOT.RooStats.PValueToSignificance( 0.05 ) ], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="white")
		fmt = {}
		fmt[ CS2.levels[0] ] = r"95\% CLs"
		plt.clabel(CS2, fontsize=9, inline=1, colors="white", linecolor="black" , fmt=fmt)


		(x,y,z,xi,yi,zi) = interpolateGridArray(xarray,yarray,zarray,withZeros=0)


		plt.scatter(x, y, c=z, vmin=0, vmax=7, cmap='jet')

		plt.xlabel(myxlabel[SignalGrid])
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])


		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"HistFitter, %s, %s"%(tmpcut,SignalGrid.translate(None, "_") ),xy=(420,1150),color="white") 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100), color="white") 
		if writePlots:
			figSens.savefig("plots/massPlaneSensitivity_%s_HF_%d_%s.png"%(SignalGrid,lumiscale,tmpcut) )


	# test = {}
	# test["jd"]


	if MeffRegions and compareToMeff:

		plt.clf()

		(x,y,z,zSR,xi,yi,zi) = interpolateGridDictionary(bestZbi,bestmeffZbi,withZeros=1)

		plt.imshow(zi, vmin=-2, vmax=4, origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], cmap='jet', alpha=0.8)
		plt.colorbar(label=r"Difference in Z Value [$\sigma$]")

		CS = plt.contour(zi, [-1,0,0.5,1,2], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="black", linecolor="white", fmt='%+1.1f $\\sigma$')

		(x,y,z,zSR,xi,yi,zi) = interpolateGridDictionary(bestZbi,bestmeffZbi,withZeros=0)

		plt.scatter(x, y, c=z, vmin=-2, vmax=4, cmap='jet')

		plt.xlabel(myxlabel[SignalGrid])
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])

		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"HistFitter, Best SR Z - Best MEff SR Z, %s"%(SignalGrid.translate(None, "_") )  ,xy=(420,1150),color="white") 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100), color="white") 
		# plt.show()

		if writePlots:
			figSens.savefig("plots/massPlaneSensitivity_%s_%s_%d_CompareToBestMeff.png"%(SignalGrid,"HistFitter",lumiscale) )




	if combineRegions:

		plt.clf()

		(x,y,z,zSR,xi,yi,zi)=interpolateGridDictionary(bestZbi,withZeros=1)

		plt.imshow(zi, vmin=0, vmax=7, origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], cmap='jet', alpha=0.8)
		plt.colorbar(label=r"Expected CLs Z Value [$\sigma$]")

		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="black", linecolor="black", fmt='%1.0f $\\sigma$')


		CS2 = plt.contour(zi, [ROOT.RooStats.PValueToSignificance( 0.05 ) ], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="white")
		fmt = {}
		fmt[ CS2.levels[0] ] = r"95\% CLs"
		plt.clabel(CS2, fontsize=7, inline=1, colors="white", linecolor="black" , fmt=fmt)


		(x,y,z,zSR,xi,yi,zi)=interpolateGridDictionary(bestZbi,withZeros=0)

		plt.scatter(x, y, c=z, vmin=0, vmax=7, cmap='jet')

		plt.xlabel(myxlabel[SignalGrid])
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])

		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"HistFitter, Best SR, %s"%(SignalGrid.translate(None, "_") ),xy=(420,1150),color="white") 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100), color="white") 
		# plt.show()

		if writePlots:
			figSens.savefig("plots/massPlaneSensitivity_%s_HF_%d_BestSR.png"%(SignalGrid,lumiscale) )


		(x,y,z,zSR,xi,yi,zi)=interpolateGridDictionary(bestZbi,withZeros=1)

		#with chosen SR
		plt.clf()
		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="black", fmt='%1.0f $\\sigma$')


		CS2 = plt.contour(zi, [ROOT.RooStats.PValueToSignificance( 0.05 ) ], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		fmt = {}
		fmt[ CS2.levels[0] ] = r"95\% CLs"
		plt.clabel(CS2, fontsize=7, inline=1, colors="black", linecolor="black" , fmt=fmt)



		for i,j,k in zip(x,y,zSR):
			plt.annotate(k.replace("SRJigsaw",""), xy=(i,j), size=6, horizontalalignment='center', verticalalignment='center' )

		plt.xlabel(myxlabel[SignalGrid])
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])

		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"HistFitter, Best SR, %s"%(SignalGrid.translate(None, "_") ),xy=(420,1150)) 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100)) 
		# plt.show()

		if writePlots:
			figSens.savefig("plots/massPlaneSensitivity_%s_HF_%d_BestSR_Text.png"%(SignalGrid,lumiscale) )


	if combineRegions and MeffRegions:


		####### Plotting best Meff regions #############################


		plt.clf()

		(x,y,z,zSR,xi,yi,zi)=interpolateGridDictionary(bestmeffZbi,withZeros=1)

		print zSR 

		plt.imshow(zi, vmin=0, vmax=7, origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], cmap='jet', alpha=0.8)
		plt.colorbar(label=r"Expected CLs Z Value [$\sigma$]")

		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="white", linecolor="white", fmt='%1.0f $\\sigma$')



		CS2 = plt.contour(zi, [ROOT.RooStats.PValueToSignificance( 0.05 ) ], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="white")
		fmt = {}
		fmt[ CS2.levels[0] ] = r"95\% CLs"
		plt.clabel(CS2, fontsize=7, inline=1, colors="black", linecolor="black" , fmt=fmt)

		(x,y,z,zSR,xi,yi,zi)=interpolateGridDictionary(bestmeffZbi,withZeros=0)

		plt.scatter(x, y, c=z, vmin=0, vmax=7, cmap='jet')

		plt.xlabel(myxlabel[SignalGrid])
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])

		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"HistFitter, Best MEff SR, %s"%(SignalGrid.translate(None, "_") ),xy=(420,1150),color="white") 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100), color="white") 
		# plt.show()

		if writePlots:
			figSens.savefig("plots/massPlaneSensitivity_%s_%s_%d_BestMEffSR.png"%(SignalGrid,"HistFitter",lumiscale) )


		(x,y,z,zSR,xi,yi,zi)=interpolateGridDictionary(bestmeffZbi,withZeros=1)

		#with chosen SR
		plt.clf()
		CS = plt.contour(zi, [2,3,4,5], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		plt.clabel(CS, fontsize=9, inline=1, colors="black", fmt='%1.0f $\\sigma$')



		CS2 = plt.contour(zi, [ROOT.RooStats.PValueToSignificance( 0.05 ) ], vmin=z.min(), vmax=z.max(), origin='lower',
		           extent=[x.min(), x.max(), y.min(), y.max()], colors="black")
		fmt = {}
		fmt[ CS2.levels[0] ] = r"95\% CLs"
		plt.clabel(CS2, fontsize=7, inline=1, colors="black", linecolor="black" , fmt=fmt)


		print zSR
		for i,j,k in zip(x,y,zSR):
			plt.annotate(k, xy=(i,j), size=6, horizontalalignment='center', verticalalignment='center' )

		plt.xlabel(myxlabel[SignalGrid])
		plt.ylabel(r"$m_{\chi^0_1}$ [GeV]")
		axes = plt.gca()
		axes.set_xlim([400,1800])
		axes.set_ylim([0,1200])

		plt.annotate(r'\textbf{\textit{ATLAS}} Internal',xy=(0.7,1.01),xycoords='axes fraction') 

		plt.annotate(r"HistFitter, Best MEff SR, %s"%(SignalGrid.translate(None, "_") ),xy=(420,1150)) 
		plt.annotate(r"$\int L \sim %.1f$ fb$^{-1}, 13$ TeV"%(lumiscale),xy=(420,1100)) 
		# plt.show()

		if writePlots:
			figSens.savefig("plots/massPlaneSensitivity_%s_%s_%d_BestMEffSR_Text.png"%(SignalGrid,"HistFitter",lumiscale) )












