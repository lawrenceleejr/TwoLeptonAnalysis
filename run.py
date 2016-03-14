#!/usr/bin/env python

########### Initialization ######################################
##
##

import ROOT
import logging
import shutil
import os
import itertools
import re


from collections import OrderedDict


logging.basicConfig(level=logging.INFO)
from optparse import OptionParser

from copy import deepcopy

import atexit
@atexit.register
def quite_exit():
	ROOT.gSystem.Exit(0)


logging.info("loading packages")
ROOT.gROOT.Macro("$ROOTCOREDIR/scripts/load_packages.C")

ROOT.TH1.SetDefaultSumw2() 

directory = "/afs/cern.ch/work/l/leejr/public/MergedSamples/031316a_tls/"
datadirectory = "/afs/cern.ch/work/l/leejr/public/MergedSamples/031316a_tls/"
signaldirectory = "/afs/cern.ch/work/l/leejr/public/MergedSamples/031316a_tls/signal/"


treename = "trees_SR_"

defaultweight = "(normweight*mcEventWeight*elSF*muSF)"


my_SHs = {}
for sampleHandlerName in [
					# "qcd",
					"top",
					"wjets",
					"zjets",
					"diboson",
					# "electroweak",
							]:

	print sampleHandlerName
	my_SHs[sampleHandlerName] = ROOT.SH.SampleHandler(); 
	ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s*"%sampleHandlerName).scan(my_SHs[sampleHandlerName], directory+"/" ) 
	print my_SHs[sampleHandlerName]
	print len(my_SHs[sampleHandlerName])

	my_SHs[sampleHandlerName].setMetaString("nc_tree", treename)
	pass





commonPlots  = {
# "H5PP" : [50, 0, 10000],      
# "MET"  : [100, 0, 10000],     
# "Meff" : [100, 0, 10000],      
}


commonPlots2D  = {
# ("MET","Meff") : ([50, 0, 3000] , [50, 0, 3000]   ),      
# ("deltaQCD","R_H2PP_H3PP") : ([50, -1, 1] , [50, 0, 1]   ),      
}


my_SHs["signal"] = ROOT.SH.SampleHandler(); 
ROOT.SH.ScanDir().sampleDepth(0).samplePattern("*.root").scan(my_SHs["signal"], signaldirectory)
my_SHs["signal"].setMetaString("nc_tree", "%s"%treename )



baseline = "(1)"
# baselineMET = "( pT_jet1 > 50.) * ( pT_jet2 > 50.) * ( MET > 200.)"


cuts = {}


cuts["SRTestCo"] = OrderedDict()
cuts["SRTestCo"]["( H3PP > 0 )"]         =  (50,0,2000e3)        
cuts["SRTestCo"]["( met > 100e3 )"]      =  (50,0,2000e3)           
cuts["SRTestCo"]["( PIoHT1CM > 0.5 )"]   =  (50,0,1.2)                 
cuts["SRTestCo"]["( NJa+NJb > 2 )"]      =  (15,0,15)               
cuts["SRTestCo"]["( RPT_HT1CM < 0.25 )"] =  (50,0,1.2)                   
cuts["SRTestCo"]["( MS > 50e3 )"]        =  (50,0,1000e3)         
cuts["SRTestCo"]["( cosS > 0.5 )"]       =  (50,0,1.2)             
cuts["SRTestCo"]["( NVS > 2 )"]          =  (15,0,15)           
cuts["SRTestCo"]["( HT1CM > 200e3)"]     =  (50,0,1000e3)            
cuts["SRTestCo"]["( isSS < 1 )"]         =  (2,0,2)             
cuts["SRTestCo"]["( isSF > 0 )"]         =  (2,0,2)             
cuts["SRTestCo"]["( isSameHemi > -1 )"]  =  (2,0,2)                    
cuts["SRTestCo"]["( cosLINV_0 < 1. )"]   =  (50,-1,1)                  
cuts["SRTestCo"]["( cosLINV_1 < 1. )"]   =  (50,-1,1)                  
cuts["SRTestCo"]["( dphiCML_0 > 0 )"]    =  (50,-1,4)                 
cuts["SRTestCo"]["( dphiCML_1 > 0 )"]    =  (50,-1,4)                 
cuts["SRTestCo"]["( dphiCMV > 1 )"]      =  (50,-1,4) 

cuts["SRTestCoEdge"] = OrderedDict()
cuts["SRTestCoEdge"]["( H3PP > 0 )"]         =  (50,0,2000e3)    
cuts["SRTestCoEdge"]["( met > 300e3 )"]      =  (50,0,2000e3)       
cuts["SRTestCoEdge"]["( PIoHT1CM > 0.6 )"]   =  (50,0,1.2)             
cuts["SRTestCoEdge"]["( NJa+NJb > 4 )"]      =  (15,0,15)           
cuts["SRTestCoEdge"]["( RPT_HT1CM < 0.25 )"] =  (50,0,1.2)               
cuts["SRTestCoEdge"]["( MS > 100e3 )"]       =  (50,0,1000e3)      
cuts["SRTestCoEdge"]["( cosS > 0 )"]         =  (50,0,1.2)       
cuts["SRTestCoEdge"]["( NVS > 2 )"]          =  (15,0,15)       
cuts["SRTestCoEdge"]["( HT1CM > 200e3)"]     =  (50,0,1000e3)        
cuts["SRTestCoEdge"]["( isSS < 1 )"]         =  (2,0,2)         
cuts["SRTestCoEdge"]["( isSF > 0 )"]         =  (2,0,2)         
cuts["SRTestCoEdge"]["( isSameHemi > 0 )"]   =  (2,0,2)               
cuts["SRTestCoEdge"]["( cosLINV_0 < -0.7 )"] =  (50,-1,1)                
cuts["SRTestCoEdge"]["( cosLINV_1 < -0.7 )"] =  (50,-1,1)                
cuts["SRTestCoEdge"]["( dphiCML_0 > 0 )"]    =  (50,-1,4)             
cuts["SRTestCoEdge"]["( dphiCML_1 > 0 )"]    =  (50,-1,4)             
cuts["SRTestCoEdge"]["( dphiCMV > 0 )"]      =  (50,-1,4)           


cuts["SRTestOneStep"] = OrderedDict()
cuts["SRTestOneStep"]["( H2PP > 100e3 )"]          = (50,0,2000e3)   
cuts["SRTestOneStep"]["( H3PP > 500e3 )"]          = (50,0,2000e3)   
cuts["SRTestOneStep"]["( R_H2PP_H5PP > 0.1 )"]          = (50,0,2000e3)   
cuts["SRTestOneStep"]["( met > 50e3 )"]       = (50,0,2000e3)      
cuts["SRTestOneStep"]["( NJa+NJb > 5 )"]       = (15,0,15)          
cuts["SRTestOneStep"]["( RPT_HT5PP < 0.07 )"]   = (50,0,0.5)             
# cuts["SRTestOneStep"]["( MS > 100e3 )"]        = (50,0,1000e3)     
# cuts["SRTestOneStep"]["( cosS > 0 )"]          = (50,0,1.2)      
# cuts["SRTestOneStep"]["( NVS > 2 )"]           = (15,0,15)      
# cuts["SRTestOneStep"]["( HT1CM > 200e3)"]      = (50,0,1000e3)       
cuts["SRTestOneStep"]["( isSS < 1 )"]          = (2,0,2)    
# cuts["SRTestOneStep"]["( isSF < 1 )"]          = (2,0,2)    
# cuts["SRTestOneStep"]["( isSameHemi < 1 )"]    = (2,0,2)          
# cuts["SRTestOneStep"]["( cosLINV_0 < -0.4 )"]  = (50,-1,1)               
# cuts["SRTestOneStep"]["( cosLINV_1 < -0.4 )"]  = (50,-1,1)           
# cuts["SRTestOneStep"] += ["( met > 200e3 )"]
cuts["SRTestOneStep"]["( maxR_H1PPi_H2PPi > 0.7 )"]          = (50,0,1) 
cuts["SRTestOneStep"]["( PP_MDeltaR > 100e3 )"]          = (50,0,2e6)    
cuts["SRTestOneStep"]["( PP_dPhiVis > 2 )"]          = (50,0,4)    
cuts["SRTestOneStep"]["( P1_CosTheta > -1 )"]          = (50,-1,1)    



## Define your cut strings here....
regions = {
	# "no_cut": "(1)",

	"SRTestCo": "*".join(  cuts["SRTestCo"].keys() ),
	"SRTestCoEdge": "*".join(  cuts["SRTestCoEdge"].keys() ),
	"SRTestOneStep": "*".join(  cuts["SRTestOneStep"].keys() ),


	# "SRTest": "*".join( ["(%s)"%mycut for mycut in cuts["SRTest"] ]),
	# "SRTestCo": "*".join( ["(%s)"%mycut for mycut in cuts["SRTestCo"] ]),
	# "SRTestCoEdge": "*".join( ["(%s)"%mycut for mycut in cuts["SRTestCoEdge"] ]),
	# "SRTestOneStep": "*".join( ["(%s)"%mycut for mycut in cuts["SRTestOneStep"] ]),

}


for SH_name, mysamplehandler in my_SHs.iteritems():

	job = ROOT.EL.Job()
	job.sampleHandler(mysamplehandler)

	cutflow = {}


	weightstring = "(1)" if "Data" in SH_name else defaultweight
	if "CRWT" in treename:
		weightstring = weightstring + "*(bTagWeight)"

	if "CRY" in treename:
		weightstring = weightstring + "*(phSignal[0]==1 && phPt[0]>130.)"

	for region in regions:

		if "SR" in region:
			# ## This part sets up both N-1 hists and the cutflow histogram for region

			cutflow[region] = ROOT.TH1F ("cutflow_%s"%region, "cutflow_%s"%region, len(cuts[region])+2 , 0, len(cuts[region])+2 );
			cutflow[region].GetXaxis().SetBinLabel(1, weightstring);
			cutflow[region].GetXaxis().SetBinLabel(2, baseline);

			for i,cutpart in enumerate(cuts[region].keys() ):

				cutpartname = cutpart.translate(None, " (),.").replace("*","_x_").replace("/","_over_").split(" < ")[0].split(" > ")[0]
				variablename = cutpart.split("<")[0].split(">")[0]+")"

				if "Data" not in SH_name:
					job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("%s_minus_%s"%(region,cutpartname), "%s_%s"%(region,cutpartname), cuts[region][cutpart][0], cuts[region][cutpart][1], cuts[region][cutpart][2] ), variablename ,baseline+"*"+weightstring+"*%s"%"*".join([ x for x in cuts[region].keys() if x!=cutpart ])    )        )
				else:
					flippedcutpart = cutpart.replace(">","%TEMP%").replace("<",">").replace("%TEMP%","<")
					job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("%s_minus_%s"%(region,cutpartname), "%s_%s"%(region,cutpartname), cuts[region][cutpart][0], cuts[region][cutpart][1], cuts[region][cutpart][2] ), variablename ,baseline+"*"+weightstring+"*%s"%"*".join([x for x in cuts[region].keys() if x!=cutpart ]) + "*" + flippedcutpart  )        )

				cutflow[region].GetXaxis().SetBinLabel (i+3, cutpart);

			job.algsAdd(ROOT.MD.AlgCFlow (cutflow[region]))

		for varname,varlimits in commonPlots.items() :
			# print varname
			job.algsAdd(
            	ROOT.MD.AlgHist(
            		ROOT.TH1F(varname+"_%s"%region, varname+"_%s"%region, varlimits[0], varlimits[1], varlimits[2]),
					varname,
					weightstring+"*%s"%regions[region]
					)
				)

		for varname,varlimits in commonPlots2D.items():
			# print varname
			job.algsAdd(
            	ROOT.MD.AlgHist(
            		ROOT.TH2F("%s_%s_%s"%(varname[0], varname[1], region), "%s_%s_%s"%(varname[0], varname[1], region), varlimits[0][0], varlimits[0][1], varlimits[0][2], varlimits[1][0], varlimits[1][1], varlimits[1][2]),
					varname[0], varname[1],
					weightstring+"*%s"%regions[region]
					)
				)

	driver = ROOT.EL.DirectDriver()
	if os.path.exists( "output/"+SH_name ):
		shutil.rmtree( "output/"+SH_name )
	driver.submit(job, "output/"+SH_name )



