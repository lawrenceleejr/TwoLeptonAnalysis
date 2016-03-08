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

directory = "/afs/cern.ch/work/l/leejr/public/TwoLeptonAnalysis/trees/output/"
datadirectory = "/afs/cern.ch/work/l/leejr/public/TwoLeptonAnalysis/trees/output/"
signaldirectory = "/afs/cern.ch/work/l/leejr/public/TwoLeptonAnalysis/trees/output/signal/"


treename = "treesSR"

my_SHs = {}
for sampleHandlerName in [
					"qcd",
					"top",
					"wjets",
					"zjets",
					"diboson",
					"electroweak",
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



for sampleHandlerName in [
						# "371543",
						# "370015",
						# "371693",
						# "371695",
						# "371533",
						"371686",
						"371519",
						"371520",
						"371521",
						"371522",
						# "SS_direct",
						# "GG_direct",
						# "GG_onestepCC_fullsim"
							]:

	# f = ROOT.TFile("%s/%s.root"%(signaldirectory,sampleHandlerName) )
	# treeList = []
	# dirList = ROOT.gDirectory.GetListOfKeys()
	# for k1 in dirList: 
	# 	t1 = k1.ReadObj()
	# 	if (type(t1) is ROOT.TTree  ):
	# 		# print t1.GetName()
	# 		treeList.append(t1.GetName())

	# for treeName in treeList:
	# 	if treename in treeName:
	# 		print treeName
	my_SHs[sampleHandlerName] = ROOT.SH.SampleHandler(); 
	ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s.root"%sampleHandlerName).scan(my_SHs[sampleHandlerName], signaldirectory)
	my_SHs[sampleHandlerName].setMetaString("nc_tree", "%s"%treename )



# for sampleHandlerName in [
# 						"Data_Nov11",
# 							]:
# 	f = ROOT.TFile("%s/%s.root"%(datadirectory,sampleHandlerName) )
# 	treeList = []
# 	dirList = ROOT.gDirectory.GetListOfKeys()
# 	for k1 in dirList: 
# 		t1 = k1.ReadObj()
# 		if (type(t1) is ROOT.TTree  ):
# 			print t1.GetName()
# 			print t1.GetEntries()
# 			treeList.append(t1.GetName())

# 	for treeName in treeList:
# 		if treename in treeName:
# 			print treeName
# 			my_SHs[treeName] = ROOT.SH.SampleHandler(); 
# 			ROOT.SH.ScanDir().sampleDepth(0).samplePattern("%s.root"%sampleHandlerName).scan(my_SHs[treeName], datadirectory)
# 			my_SHs[treeName].setMetaString("nc_tree", "%s"%treeName )




baseline = "(1)"
# baselineMET = "( pT_jet1 > 50.) * ( pT_jet2 > 50.) * ( MET > 200.)"


cuts = {}
limits = {}


## ZL Team


cuts["SRTest"] = []
cuts["SRTest"] += ["( met > 150e3 )"]
cuts["SRTest"] += ["( H2PP > 0. )"]
cuts["SRTest"] += ["( H6PP > 1e6 )"]
# cuts["SRTest"] += ["( R_H2PP_H3PP < 0.8 )"]
cuts["SRTest"] += ["( R_H2PP_H5PP > 0.2 )"]
cuts["SRTest"] += ["( R_H2PP_H5PP < 0.8 )"]
cuts["SRTest"] += ["( RPZ_HT5PP < 0.7 )"]
# cuts["SRTest"] += ["( sangle < 0.3 )"]
cuts["SRTest"] += ["( PP_InvGamma > 0.1 )"]
cuts["SRTest"] += ["( abs(P1_CosTheta) < 0.9 )"]
cuts["SRTest"] += ["( PIoHT1CM > 0. )"]
cuts["SRTest"] += ["( NJa+NJb > 4 )"]

limits["SRTest"] = []
limits["SRTest"] +=  [(50,0,2000e3)]     #["( MET > 200 )"]
limits["SRTest"] +=  [(50,0,2000e3)]     #["( pT_jet1 > 200 )"]
limits["SRTest"] +=  [(50,0,2000e3)]     #["( pT_jet2 > 100 )"]
limits["SRTest"] +=  [(50,0,1.2)]     #["( dphi > 0.4 )"]
limits["SRTest"] +=  [(50,0,1.2)]     #["( dphi > 0.4 )"]
limits["SRTest"] +=  [(50,0,1.2)]     #["( dphi > 0.4 )"]
# limits["SRTest"] +=  [(50,0,1.2)]     #["( dphi > 0.4 )"]
limits["SRTest"] +=  [(50,0,1.2)]     #["( dphi > 0.4 )"]
limits["SRTest"] +=  [(50,0,1.2)]     #["( dphi > 0.4 )"]
limits["SRTest"] +=  [(50,0,1.2)]     #["( dphi > 0.4 )"]
limits["SRTest"] +=  [(15,0,15)]     #["( dphi > 0.4 )"]


cuts["SRTestCo"] = []
# cuts["SRTestCo"] += ["( met > 150e3 )"]
# cuts["SRTestCo"] += ["( H2PP > 0. )"]
# cuts["SRTestCo"] += ["( H6PP > 1e6 )"]
# cuts["SRTestCo"] += ["( R_H2PP_H3PP < 0.8 )"]
# cuts["SRTestCo"] += ["( R_H2PP_H5PP > 0.2 )"]
# cuts["SRTestCo"] += ["( R_H2PP_H5PP < 0.8 )"]
# cuts["SRTestCo"] += ["( RPZ_HT5PP < 0.7 )"]
# cuts["SRTestCo"] += ["( sangle < 0.3 )"]
# cuts["SRTestCo"] += ["( PP_InvGamma > 0.1 )"]
# cuts["SRTestCo"] += ["( abs(P1_CosTheta) < 0.9 )"]
cuts["SRTestCo"] += ["( PIoHT1CM > 0.5 )"]
cuts["SRTestCo"] += ["( NJa+NJb > 5 )"]
cuts["SRTestCo"] += ["( RPT_HT1CM < 0.15 )"]
cuts["SRTestCo"] += ["( MS > 50e3 )"]
cuts["SRTestCo"] += ["( cosS > 0.5 )"]
# cuts["SRTestCo"] += ["( NVS > -1 )"]
cuts["SRTestCo"] += ["( HT1CM > 200e3)"]
cuts["SRTestCo"] += ["( met > 200e3 )"]


limits["SRTestCo"] = []
# limits["SRTestCo"] +=  [(50,0,2000e3)]     #["( MET > 200 )"]
# limits["SRTestCo"] +=  [(50,0,2000e3)]     #["( pT_jet1 > 200 )"]
# limits["SRTestCo"] +=  [(50,0,2000e3)]     #["( pT_jet2 > 100 )"]
# limits["SRTestCo"] +=  [(50,0,1.2)]     #["( dphi > 0.4 )"]
# limits["SRTestCo"] +=  [(50,0,1.2)]     #["( dphi > 0.4 )"]
# limits["SRTestCo"] +=  [(50,0,1.2)]     #["( dphi > 0.4 )"]
# limits["SRTestCo"] +=  [(50,0,1.2)]     #["( dphi > 0.4 )"]
# limits["SRTestCo"] +=  [(50,0,1.2)]     #["( dphi > 0.4 )"]
# limits["SRTestCo"] +=  [(50,0,1.2)]     #["( dphi > 0.4 )"]
limits["SRTestCo"] +=  [(50,0,1.2)]     #["( dphi > 0.4 )"]
limits["SRTestCo"] +=  [(15,0,15)]     #["( dphi > 0.4 )"]
limits["SRTestCo"] +=  [(50,0,1.2)]     #["( dphi > 0.4 )"]
limits["SRTestCo"] +=  [(50,0,1000e3)]     #["( dphi > 0.4 )"]
limits["SRTestCo"] +=  [(50,0,1.2)]     #["( dphi > 0.4 )"]
# limits["SRTestCo"] +=  [(15,0,15)]     #["( dphi > 0.4 )"]
limits["SRTestCo"] +=  [(50,0,1000e3)]     #["( dphi > 0.4 )"]
limits["SRTestCo"] +=  [(50,0,1000e3)]     #["( dphi > 0.4 )"]



# cuts["SR2jl"] = []
# cuts["SR2jl"] += ["( MET > 200 )"]
# cuts["SR2jl"] += ["( pT_jet1 > 200 )"]
# cuts["SR2jl"] += ["( pT_jet2 > 200 )"]
# cuts["SR2jl"] += ["( dphi > 0.8 )"]
# cuts["SR2jl"] += ["( MET/sqrt(Meff-MET) > 15 )"]
# cuts["SR2jl"] += ["( Meff > 1200 )"]

# limits["SR2jl"] = []
# limits["SR2jl"] +=  [(50,0,1000)]     #["( MET > 200 )"]
# limits["SR2jl"] +=  [(50,0,1000)]     #["( pT_jet1 > 200 )"]
# limits["SR2jl"] +=  [(50,0,1000)]     #["( pT_jet2 > 100 )"]
# limits["SR2jl"] +=  [(50,0,4)]     #["( dphi > 0.4 )"]
# limits["SR2jl"] +=  [(50,0,50)]     #["( MET/(MET+pT_jet1+pT_jet2+pT_jet3+pT_jet4+pT_jet5) > 0.25 )"]
# limits["SR2jl"] +=  [(50,0,4000)]     #["( Meff > 1600 )"]



## Define your cut strings here....
regions = {
	"no_cut": "(1)",

	"SRTest": "*".join( ["(%s)"%mycut for mycut in cuts["SRTest"] ]),
	"SRTestCo": "*".join( ["(%s)"%mycut for mycut in cuts["SRTestCo"] ]),

}


for SH_name, mysamplehandler in my_SHs.iteritems():

	job = ROOT.EL.Job()
	job.sampleHandler(mysamplehandler)

	cutflow = {}


	weightstring = "(1)" if "Data" in SH_name else "normweight"
	if "CRWT" in treename:
		weightstring = weightstring + "*(bTagWeight)"

	if "CRY" in treename:
		weightstring = weightstring + "*(phSignal[0]==1 && phPt[0]>130.)*(1.6)"

	for region in regions:

		if "SR" in region:
			# ## This part sets up both N-1 hists and the cutflow histogram for region

			cutflow[region] = ROOT.TH1F ("cutflow_%s"%region, "cutflow_%s"%region, len(cuts[region])+2 , 0, len(cuts[region])+2 );
			cutflow[region].GetXaxis().SetBinLabel(1, weightstring);
			cutflow[region].GetXaxis().SetBinLabel(2, baseline);

			for i,cutpart in enumerate(cuts[region]):

				cutpartname = cutpart.translate(None, " (),.").replace("*","_x_").replace("/","_over_").split(" < ")[0].split(" > ")[0]
				variablename = cutpart.split("<")[0].split(">")[0]+")"

				if "Data" not in SH_name:
					job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("%s_minus_%s"%(region,cutpartname), "%s_%s"%(region,cutpartname), limits[region][i][0], limits[region][i][1], limits[region][i][2] ), variablename ,baseline+"*"+weightstring+"*%s"%"*".join(["(%s)"%mycut for mycut in cuts[region] if mycut!=cutpart ])    )        )
				else:
					flippedcutpart = cutpart.replace(">","%TEMP%").replace("<",">").replace("%TEMP%","<")
					job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("%s_minus_%s"%(region,cutpartname), "%s_%s"%(region,cutpartname), limits[region][i][0], limits[region][i][1], limits[region][i][2] ), variablename ,baseline+"*"+weightstring+"*%s"%"*".join(["(%s)"%mycut for mycut in cuts[region] if mycut!=cutpart ]) + "*" + flippedcutpart  )        )

				cutflow[region].GetXaxis().SetBinLabel (i+3, cutpart);

			job.algsAdd(ROOT.MD.AlgCFlow (cutflow[region]))


		if "CR" in region:
			# ## This part sets up both N-1 hists and the cutflow histogram for region

			cutflow[region] = ROOT.TH1F ("cutflow_%s"%region, "cutflow_%s"%region, len(cuts[region])+2 , 0, len(cuts[region])+2 );
			cutflow[region].GetXaxis().SetBinLabel(1, weightstring);
			cutflow[region].GetXaxis().SetBinLabel(2, baseline);

			for i,cutpart in enumerate(cuts[region]):

				cutpartname = cutpart.translate(None, " (),.").replace("*","_x_").replace("/","_over_").split(" < ")[0].split(" > ")[0]
				variablename = cutpart.split("<")[0].split(">")[0]+")"

				job.algsAdd (ROOT.MD.AlgHist(ROOT.TH1F("%s_minus_%s"%(region,cutpartname), "%s_%s"%(region,cutpartname), limits[region][i][0], limits[region][i][1], limits[region][i][2] ), variablename ,baseline+"*"+weightstring+"*%s"%"*".join(["(%s)"%mycut for mycut in cuts[region] if mycut!=cutpart ])    )        )

				cutflow[region].GetXaxis().SetBinLabel (i+3, cutpart);

			job.algsAdd(ROOT.MD.AlgCFlow (cutflow[region]))

		###################################################################

		## each of this histograms will be made for each region

		if not('QCD' in region):
			for varname,varlimits in commonPlots.items() :
				# print varname
				job.algsAdd(
	            	ROOT.MD.AlgHist(
	            		ROOT.TH1F(varname+"_%s"%region, varname+"_%s"%region, varlimits[0], varlimits[1], varlimits[2]),
						varname,
						weightstring+"*%s"%regions[region]
						)
					)


		# if "QCD" in region:

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



