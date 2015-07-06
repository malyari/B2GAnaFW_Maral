#! /usr/bin/env python

##################
# Finding the mistag rate plots
##################

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--files', type='string', action='store',
                  dest='files',
                  help='Input files')

parser.add_option('--outname', type='string', action='store',
                  default='probe_and_tag_hist.root',
                  dest='outname',
                  help='Name of output file')
 
parser.add_option('--verbose', action='store_true',
                  default=False,
                  dest='verbose',
                  help='Print debugging info')

parser.add_option('--maxevents', type='int', action='store',
                  default=-1,
                  dest='maxevents',
                  help='Number of events to run. -1 is all events')


parser.add_option('--minAK8Pt', type='float', action='store',
                  default=200.,
                  dest='minAK8Pt',
                  help='Minimum PT for AK8 jets')

parser.add_option('--maxAK8Rapidity', type='float', action='store',
                  default=2.4,
                  dest='maxAK8Rapidity',
                  help='Maximum AK8 rapidity')
parser.add_option('--FlatSample', action='store_true',
                  default=False,
                  dest='deweightFlat',
                  help='unweights flat samples')



(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF

import ROOT
import sys
from DataFormats.FWLite import Events, Handle
ROOT.gROOT.Macro("rootlogon.C")
import copy
import random


#generator info

h_generator = Handle("GenEventInfoProduct")
l_generator = ("generator" , "" )

h_NPV = Handle("std::int")
l_NPV = ( "eventUserData" , "npv" )

h_jetsAK8Area = Handle("std::vector<float>")
l_jetsAK8Area = ( "jetsAK8" , "jetAK8jetArea" )


h_rho = Handle("double")
l_rho = ("fixedGridRhoFastjetAll", "")

#MET label and Handles
h_metPt = Handle("std::vector<float>")
l_metPt = ("met" , "metPt")
h_metPx = Handle("std::vector<float>")
l_metPx = ("met" , "metPx")
h_metPy = Handle("std::vector<float>")
l_metPy = ("met" , "metPy")
h_metPhi = Handle("std::vector<float>")
l_metPhi = ("met" , "metPhi")

#AK8 Jets label and Handles
h_jetsAK8Pt = Handle("std::vector<float>")
l_jetsAK8Pt = ("jetsAK8" , "jetAK8Pt") #
h_jetsAK8Eta = Handle("std::vector<float>")
l_jetsAK8Eta = ("jetsAK8" , "jetAK8Eta")
h_jetsAK8Phi = Handle("std::vector<float>")
l_jetsAK8Phi = ("jetsAK8" , "jetAK8Phi")
h_jetsAK8Mass = Handle("std::vector<float>")
l_jetsAK8Mass = ("jetsAK8" , "jetAK8Mass")
h_jetsAK8Energy = Handle("std::vector<float>")
l_jetsAK8Energy = ("jetsAK8" , "jetAK8E") 
h_jetsAK8JEC = Handle("std::vector<float>")
l_jetsAK8JEC = ("jetsAK8" , "jetAK8jecFactor0")
h_jetsAK8Y = Handle("std::vector<float>")
l_jetsAK8Y = ("jetsAK8" , "jetAK8Y")
#h_jetsAK8CSV = Handle("std::vector<float>")
#l_jetsAK8CSV = ("jetsAK8" , "jetAK8CSV")

h_jetsAK8nHadEnergy = Handle("std::vector<float>")
l_jetsAK8nHadEnergy = ("jetsAK8" , "jetAK8neutralHadronEnergy")
h_jetsAK8nEMEnergy = Handle("std::vector<float>")
l_jetsAK8nEMEnergy = ("jetsAK8" , "jetAK8neutralEmEnergy")
h_jetsAK8HFHadronEnergy = Handle("std::vector<float>")
l_jetsAK8HFHadronEnergy = ("jetsAK8" , "jetAK8HFHadronEnergy")
h_jetsAK8cHadEnergy = Handle("std::vector<float>")
l_jetsAK8cHadEnergy = ("jetsAK8" , "jetAK8chargedHadronEnergy")
h_jetsAK8cEMEnergy = Handle("std::vector<float>")
l_jetsAK8cEMEnergy = ("jetsAK8" , "jetAK8chargedEmEnergy")
h_jetsAK8numDaughters = Handle("std::vector<float>")
l_jetsAK8numDaughters = ("jetsAK8" , "jetAK8numberOfDaughters")
h_jetsAK8cMultip = Handle("std::vector<float>")
l_jetsAK8cMultip = ("jetsAK8" , "jetAK8chargedMultiplicity")
h_jetsAK8Y = Handle("std::vector<float>")
l_jetsAK8Y = ("jetsAK8" , "jetAK8Y")

h_jetsAK8TrimMass = Handle("std::vector<float>")
l_jetsAK8TrimMass = ("jetsAK8", "jetAK8trimmedMass" )
h_jetsAK8PrunMass = Handle("std::vector<float>")
l_jetsAK8PrunMass = ("jetsAK8", "jetAK8prunedMass" )
h_jetsAK8FiltMass = Handle("std::vector<float>")
l_jetsAK8FiltMass = ("jetsAK8", "jetAK8filteredMass" )
h_jetsAK8SoftDropMass = Handle("std::vector<float>")
l_jetsAK8SoftDropMass = ("jetsAK8", "jetAK8softDropMass" )
h_jetsAK8Tau1 = Handle("std::vector<float>")
l_jetsAK8Tau1 = ("jetsAK8", "jetAK8tau1" )
h_jetsAK8Tau2 = Handle("std::vector<float>")
l_jetsAK8Tau2 = ("jetsAK8", "jetAK8tau2" )
h_jetsAK8Tau3 = Handle("std::vector<float>")
l_jetsAK8Tau3 = ("jetsAK8", "jetAK8tau3" )
h_jetsAK8nSubJets = Handle("std::vector<float>")
l_jetsAK8nSubJets = ("jetsAK8", "jetAK8nSubJets" )
h_jetsAK8minmass = Handle("std::vector<float>")
l_jetsAK8minmass = ("jetsAK8", "jetAK8minmass" )

h_jetsAK8vSubjetIndex0 = Handle("std::vector<float>")
l_jetsAK8vSubjetIndex0 = ("jetsAK8", "jetAK8vSubjetIndex0")
h_jetsAK8vSubjetIndex1 = Handle("std::vector<float>")
l_jetsAK8vSubjetIndex1 = ("jetsAK8", "jetAK8vSubjetIndex1")

h_jetsAK8TopSubjetIndex0 = Handle("std::vector<float>")
l_jetsAK8TopSubjetIndex0 = ("jetsAK8", "jetAK8topSubjetIndex0")
h_jetsAK8TopSubjetIndex1 = Handle("std::vector<float>")
l_jetsAK8TopSubjetIndex1 = ("jetsAK8", "jetAK8topSubjetIndex1")
h_jetsAK8TopSubjetIndex2 = Handle("std::vector<float>")
l_jetsAK8TopSubjetIndex2 = ("jetsAK8", "jetAK8topSubjetIndex2")
h_jetsAK8TopSubjetIndex3 = Handle("std::vector<float>")
l_jetsAK8TopSubjetIndex3 = ("jetsAK8", "jetAK8topSubjetIndex3")

h_subjetsAK8BDisc = Handle( "std::vector<float>")
l_subjetsAK8BDisc = ("subjetsCmsTopTag", "subjetCmsTopTagCSV")
h_subjetsAK8Pt = Handle( "std::vector<float>")
l_subjetsAK8Pt = ("subjetsCmsTopTag", "subjetCmsTopTagPt")
h_subjetsAK8Eta = Handle( "std::vector<float>")
l_subjetsAK8Eta = ("subjetsCmsTopTag", "subjetCmsTopTagEta")
h_subjetsAK8Phi = Handle( "std::vector<float>")
l_subjetsAK8Phi = ("subjetsCmsTopTag", "subjetCmsTopTagPhi")
h_subjetsAK8Mass = Handle( "std::vector<float>")
l_subjetsAK8Mass = ("subjetsCmsTopTag", "subjetCmsTopTagMass")

## Booking the histograms
print 'Booking histograms'
f = ROOT.TFile( options.outname , "RECREATE")
f.cd()




h_topTagPtSD        = ROOT.TH1D("topTagPtSD", "Top Tag Pt", 400,  0,  2000 )
h_topProbePtSD      = ROOT.TH1D("topProbePtSD", "Top Probe Pt", 400,  0,  2000 )
h_topTagPtFJ        = ROOT.TH1D("topTagPtFJ", "Top Tag Pt", 400,  0,  2000 )
h_topProbePtFJ      = ROOT.TH1D("topProbePtFJ", "Top Probe Pt", 400,  0,  2000 )
h_topTagPtNM        = ROOT.TH1D("topTagPtNM", "Top Tag Pt", 400,  0,  2000 )
h_topProbePtNM      = ROOT.TH1D("topProbePtNM", "Top Probe Pt", 400,  0,  2000 )
h_topTagPtSDT        = ROOT.TH1D("topTagPtSDT", "Top Tag Pt", 400,  0,  2000 )
h_topProbePtSDT      = ROOT.TH1D("topProbePtSDT", "Top Probe Pt", 400,  0,  2000 )
h_topTagPtFJT        = ROOT.TH1D("topTagPtFJT", "Top Tag Pt", 400,  0,  2000 )
h_topProbePtFJT      = ROOT.TH1D("topProbePtFJT", "Top Probe Pt", 400,  0,  2000 )
h_topTagPtNMT        = ROOT.TH1D("topTagPtNMT", "Top Tag Pt", 400,  0,  2000 )
h_topProbePtNMT      = ROOT.TH1D("topProbePtNMT", "Top Probe Pt", 400,  0,  2000)
h_topTagPtFree        = ROOT.TH1D("topTagPtFree", "Top Tag Pt", 400,  0,  2000 )
h_topProbePtFree      = ROOT.TH1D("topProbePtFree", "Top Probe Pt", 400,  0,  2000 )
h_testTagPt       = ROOT.TH1D("testTagPt", "Top Tag Pt", 400,  0,  2000 )
h_testProbePt     = ROOT.TH1D("testProbePt", "Top Probe Pt", 400,  0,  2000 )
h_lowmMinTagPt    = ROOT.TH1D("lowmMinTagPt", "Top Tag Pt", 400,  0,  2000 )
h_lowmMinTagWP1Pt = ROOT.TH1D("lowmMinTagPtWP1", "Top Tag Pt WP1", 400,  0,  2000 )
h_lowmMinTagWP2Pt = ROOT.TH1D("lowmMinTagPtWP2", "Top Tag Pt WP2", 400,  0,  2000 )
h_lowmMinTagWP3Pt = ROOT.TH1D("lowmMinTagPtWP3", "Top Tag Pt WP3", 400,  0,  2000 )
h_lowmMinTagWP4Pt = ROOT.TH1D("lowmMinTagPtWP4", "Top Tag Pt WP4", 400,  0,  2000 )
h_lowmMinTagWP5Pt = ROOT.TH1D("lowmMinTagPtWP5", "Top Tag Pt WP5", 400,  0,  2000 )
h_lowmMinProbePt  = ROOT.TH1D("lowmMinProbePt", "Top Probe Pt", 400,  0,  2000 )
h_lowmMinBTagPt   = ROOT.TH1D("lowmMinBTagPt", "Top Tag Pt", 400,  0,  2000 )
h_lowmMinBProbePt = ROOT.TH1D("lowmMinBProbePt", "Top Probe Pt", 400,  0,  2000 )
h_lowmMin2BTagPt  = ROOT.TH1D("lowmMin2BTagPt", "Top Tag Pt", 400,  0,  2000 )
h_lowmMin2BProbePt= ROOT.TH1D("lowmMin2BProbePt", "Top Probe Pt", 400,  0,  2000 )
h_antiBTagPt      = ROOT.TH1D("antiBTagPt", "Top Tag Pt", 400,  0,  2000 ) 
h_antiBProbePt    = ROOT.TH1D("antiBProbePt", "Top Probe Pt", 400,  0,  2000 ) 
h_pt    = ROOT.TH1D("Pt", "AK8 Pt", 400,  0,  2000 )

h_topProbemmSD        = ROOT.TH1D("topProbemmSD", "minMass", 100,  0,  200 )
h_topProbeak8mSD      = ROOT.TH1D("topProbeak8mSD", "AK8 Mass", 100,  0,  300 )
h_topProbeSDmSD        = ROOT.TH1D("topProbeSDmSD", "Soft Drop Mass", 100,  0,  300 )
h_topProbeTau32SD      = ROOT.TH1D("topProbeTau32SD", "Tau32", 100,  0.0,  1.0 )
h_topProbePhiSD        = ROOT.TH1D("topProbePhiSD", "Phi", 100,  -3.14,  3.14 )
h_topProbeYSD      = ROOT.TH1D("topProbeYSD", "eta", 100,  -5.0,  5.0 )


h_topProbemmFJ        = ROOT.TH1D("topProbemmFJ", "minMass", 100,  0,  200 )
h_topProbeak8mFJ      = ROOT.TH1D("topProbeak8mFJ", "AK8 Mass", 100,  0,  300 )
h_topProbeSDmFJ        = ROOT.TH1D("topProbeSDmFJ", "Soft Drop Mass", 100,  0,  300 )
h_topProbeTau32FJ      = ROOT.TH1D("topProbeTau32FJ", "Tau32", 100,  0.0,  1.0 )
h_topProbePhiFJ        = ROOT.TH1D("topProbePhiFJ", "Phi", 100,  -3.14,  3.14 )
h_topProbeYFJ      = ROOT.TH1D("topProbeYFJ", "eta", 100,  -5.0,  5.0 )


h_topProbemmNM        = ROOT.TH1D("topProbemmNM", "minMass", 100,  0,  200 )
h_topProbeak8mNM      = ROOT.TH1D("topProbeak8mNM", "AK8 Mass", 100,  0,  300 )
h_topProbeSDmNM        = ROOT.TH1D("topProbeSDmNM", "Soft Drop Mass", 100,  0,  300 )
h_topProbeTau32NM      = ROOT.TH1D("topProbeTau32NM", "Tau32", 100,  0.0,  1.0 )
h_topProbePhiNM        = ROOT.TH1D("topProbePhiNM", "Phi", 100,  -3.14,  3.14 )
h_topProbeYNM      = ROOT.TH1D("topProbeYNM", "eta", 100,  -5.0,  5.0 )


h_topProbemmSDT        = ROOT.TH1D("topProbemmSDT", "minMass", 100,  0,  200 )
h_topProbeak8mSDT      = ROOT.TH1D("topProbeak8mSDT", "AK8 Mass", 100,  0,  300 )
h_topProbeSDmSDT        = ROOT.TH1D("topProbeSDmSDT", "Soft Drop Mass", 100,  0,  300 )
h_topProbeTau32SDT      = ROOT.TH1D("topProbeTau32SDT", "Tau32", 100,  0.0,  1.0 )
h_topProbePhiSDT        = ROOT.TH1D("topProbePhiSDT", "Phi", 100,  -3.14,  3.14 )
h_topProbeYSDT      = ROOT.TH1D("topProbeYSDT", "eta", 100,  -5.0,  5.0 )


h_topProbemmFJT        = ROOT.TH1D("topProbemmFJT", "minMass", 100,  0,  200 )
h_topProbeak8mFJT      = ROOT.TH1D("topProbeak8mFJT", "AK8 Mass", 100,  0,  300 )
h_topProbeSDmFJT        = ROOT.TH1D("topProbeSDmFJT", "Soft Drop Mass", 100,  0,  300 )
h_topProbeTau32FJT      = ROOT.TH1D("topProbeTau32FJT", "Tau32", 100,  0.0,  1.0 )
h_topProbePhiFJT        = ROOT.TH1D("topProbePhiFJT", "Phi", 100,  -3.14,  3.14 )
h_topProbeYFJT      = ROOT.TH1D("topProbeYFJT", "eta", 100,  -5.0,  5.0 )


h_topProbemmNMT        = ROOT.TH1D("topProbemmNMT", "minMass", 100,  0,  200 )
h_topProbeak8mNMT      = ROOT.TH1D("topProbeak8mNMT", "AK8 Mass", 100,  0,  300 )
h_topProbeSDmNMT        = ROOT.TH1D("topProbeSDmNMT", "Soft Drop Mass", 100,  0,  300 )
h_topProbeTau32NMT      = ROOT.TH1D("topProbeTau32NMT", "Tau32", 100,  0.0,  1.0 )
h_topProbePhiNMT        = ROOT.TH1D("topProbePhiNMT", "Phi", 100,  -3.14,  3.14 )
h_topProbeYNMT      = ROOT.TH1D("topProbeYNMT", "eta", 100,  -5.0,  5.0 )


h_topProbemmFree        = ROOT.TH1D("topProbemmFree", "minMass", 100,  0,  200 )
h_topProbeak8mFree      = ROOT.TH1D("topProbeak8mFree", "AK8 Mass", 100,  0,  300 )
h_topProbeSDmFree        = ROOT.TH1D("topProbeSDmFree", "Soft Drop Mass", 100,  0,  300 )
h_topProbeTau32Free      = ROOT.TH1D("topProbeTau32Free", "Tau32", 100,  0.0,  1.0 )
h_topProbePhiFree        = ROOT.TH1D("topProbePhiFree", "Phi", 100,  -3.14,  3.14 )
h_topProbeYFree      = ROOT.TH1D("topProbeYFree", "eta", 100,  -5.0,  5.0 )




h_topTagPtSD.Sumw2()
h_topProbePtSD.Sumw2()
h_topTagPtFJ.Sumw2()
h_topProbePtFJ.Sumw2()
h_topTagPtNM.Sumw2()
h_topProbePtNM.Sumw2()
h_topTagPtSDT.Sumw2()
h_topProbePtSDT.Sumw2()
h_topTagPtFJT.Sumw2()
h_topProbePtFJT.Sumw2()
h_topTagPtNMT.Sumw2()
h_topProbePtNMT.Sumw2()
h_topTagPtFree.Sumw2()
h_topProbePtFree.Sumw2()
h_testTagPt.Sumw2()
h_testProbePt.Sumw2()
h_lowmMinTagPt.Sumw2()
h_lowmMinTagWP1Pt.Sumw2()
h_lowmMinTagWP2Pt.Sumw2()
h_lowmMinTagWP3Pt.Sumw2()
h_lowmMinTagWP4Pt.Sumw2()
h_lowmMinTagWP5Pt.Sumw2()
h_lowmMinProbePt.Sumw2()
h_lowmMinBTagPt.Sumw2()
h_lowmMinBProbePt.Sumw2()
h_lowmMin2BTagPt.Sumw2()
h_lowmMin2BProbePt.Sumw2()
h_antiBTagPt.Sumw2()
h_antiBProbePt.Sumw2()
h_pt.Sumw2()

h_topProbemmSD.Sumw2()
h_topProbeak8mSD.Sumw2()
h_topProbeSDmSD.Sumw2()
h_topProbeTau32SD.Sumw2()
h_topProbePhiSD.Sumw2()
h_topProbeYSD.Sumw2()

h_topProbemmFJ.Sumw2()
h_topProbeak8mFJ.Sumw2()
h_topProbeSDmFJ.Sumw2()
h_topProbeTau32FJ.Sumw2()
h_topProbePhiFJ.Sumw2()
h_topProbeYFJ.Sumw2()


h_topProbemmNM.Sumw2()
h_topProbeak8mNM.Sumw2()
h_topProbeSDmNM.Sumw2()
h_topProbeTau32NM.Sumw2()
h_topProbePhiNM.Sumw2()
h_topProbeYNM.Sumw2()


h_topProbemmSDT.Sumw2()
h_topProbeak8mSDT.Sumw2()
h_topProbeSDmSDT.Sumw2()
h_topProbeTau32SDT.Sumw2()
h_topProbePhiSDT.Sumw2()
h_topProbeYSDT.Sumw2()


h_topProbemmFJT.Sumw2()
h_topProbeak8mFJT.Sumw2()
h_topProbeSDmFJT.Sumw2()
h_topProbeTau32FJT.Sumw2()
h_topProbePhiFJT.Sumw2()
h_topProbeYFJT.Sumw2()
h_topProbemmNMT.Sumw2()
h_topProbeak8mNMT.Sumw2()
h_topProbeSDmNMT.Sumw2()
h_topProbeTau32NMT.Sumw2()
h_topProbePhiNMT.Sumw2()
h_topProbeYNMT.Sumw2()
h_topProbemmFree.Sumw2()
h_topProbeak8mFree.Sumw2()
h_topProbeSDmFree.Sumw2()
h_topProbeTau32Free.Sumw2()
h_topProbePhiFree.Sumw2()
h_topProbeYFree.Sumw2()





#JET CORRECTIONS

ROOT.gSystem.Load('libCondFormatsJetMETObjects')

print 'Getting L3 for AK8'
L3JetParAK8  = ROOT.JetCorrectorParameters("JECs/PHYS14_25_V2_L3Absolute_AK8PFchs.txt");
print 'Getting L2 for AK8'
L2JetParAK8  = ROOT.JetCorrectorParameters("JECs/PHYS14_25_V2_L2Relative_AK8PFchs.txt");
print 'Getting L1 for AK8'
L1JetParAK8  = ROOT.JetCorrectorParameters("JECs/PHYS14_25_V2_L1FastJet_AK8PFchs.txt");
# for data only :
#ResJetParAK8 = ROOT.JetCorrectorParameters("JECs/PHYS14_25_V2_L2L3Residual_AK8PFchs.txt"); 

#  Load the JetCorrectorParameter objects into a vector, IMPORTANT: THE ORDER MATTERS HERE !!!! 
vParJecAK8 = ROOT.vector('JetCorrectorParameters')()
vParJecAK8.push_back(L1JetParAK8)
vParJecAK8.push_back(L2JetParAK8)
vParJecAK8.push_back(L3JetParAK8)
# for data only :
#vParJecAK8.push_back(ResJetPar)

ak8JetCorrector = ROOT.FactorizedJetCorrector(vParJecAK8)


#EVENT LOOP
filelist = file( options.files )
filesraw = filelist.readlines()
files = []
nevents = 0
for ifile in filesraw:
    if len( ifile ) > 2 : 
        #s = 'root://cmsxrootd.fnal.gov/' + ifile.rstrip()
        s = ifile.rstrip()
        files.append( s )
        print 'Added ' + s
       
NGoodAK8Jets = 0
NGoodAntiTaggedEventsSD = 0
NGoodAntiTagTopTagPairsSD = 0
NGoodAntiTaggedEventsFJ = 0
NGoodAntiTagTopTagPairsFJ = 0
NGoodAntiTaggedEventsNM = 0
NGoodAntiTagTopTagPairsNM = 0
NGoodAntiTaggedEventsSDT = 0
NGoodAntiTagTopTagPairsSDT = 0
NGoodAntiTaggedEventsFJT = 0
NGoodAntiTagTopTagPairsFJT = 0
NGoodAntiTaggedEventsNMT = 0
NGoodAntiTagTopTagPairsNMT = 0
NGoodAntiTagTopTagPairsFree = 0
NPassDiJetCut = 0
NPassptCut = 0
NPassetaCut = 0
NPassdPhiCut = 0
NPassAllCuts = 0
# loop over files
for ifile in files : #{ Loop over root files
    print 'Processing file ' + ifile
    events = Events (ifile)
    if options.maxevents > 0 and nevents > options.maxevents :
        break

    # loop over events in this file
    for event in events: #{ Loop over events in root files
        if options.maxevents > 0 and nevents > options.maxevents :
            break
        nevents += 1

        if nevents % 1000 == 0 : 
            print '    ---> Event ' + str(nevents)
        if options.verbose :
            print '==============================================='
            print '    ---> Event ' + str(nevents)

        
        # Vertex Sets
        event.getByLabel( l_NPV, h_NPV )
        if len(h_NPV.product()) == 0 :
            if options.verbose :
                print "Event has no good primary vertex."
            continue
        NPV = h_NPV.product()[0]
        #@ RHO VALUE
        event.getByLabel( l_rho, h_rho )
        if len(h_rho.product()) == 0 :
            print "Event has no rho values."
            continue
        else:
            rho = h_rho.product()[0]
            if options.verbose :
                print 'rho = {0:6.2f}'.format( rho )

        ############################################
        # Get the AK8 jets
        ############################################

        event.getByLabel ( l_jetsAK8Eta, h_jetsAK8Eta )
        event.getByLabel ( l_jetsAK8Pt, h_jetsAK8Pt )
        event.getByLabel ( l_jetsAK8Phi, h_jetsAK8Phi )
        event.getByLabel ( l_jetsAK8Mass, h_jetsAK8Mass )
        event.getByLabel ( l_jetsAK8Energy, h_jetsAK8Energy )
        event.getByLabel ( l_jetsAK8JEC, h_jetsAK8JEC )
        event.getByLabel ( l_jetsAK8Y, h_jetsAK8Y )
        event.getByLabel ( l_jetsAK8Area, h_jetsAK8Area )

        event.getByLabel ( l_jetsAK8nHadEnergy, h_jetsAK8nHadEnergy)
        event.getByLabel ( l_jetsAK8nEMEnergy, h_jetsAK8nEMEnergy )
        event.getByLabel ( l_jetsAK8cHadEnergy, h_jetsAK8cHadEnergy )
        event.getByLabel ( l_jetsAK8HFHadronEnergy, h_jetsAK8HFHadronEnergy )
        event.getByLabel ( l_jetsAK8cEMEnergy, h_jetsAK8cEMEnergy )
        event.getByLabel ( l_jetsAK8numDaughters, h_jetsAK8numDaughters )
        event.getByLabel ( l_jetsAK8cMultip, h_jetsAK8cMultip )

        event.getByLabel ( l_jetsAK8TrimMass, h_jetsAK8TrimMass )
        event.getByLabel ( l_jetsAK8PrunMass, h_jetsAK8PrunMass )
        event.getByLabel ( l_jetsAK8FiltMass, h_jetsAK8FiltMass )
        event.getByLabel ( l_jetsAK8SoftDropMass, h_jetsAK8SoftDropMass )
        event.getByLabel ( l_jetsAK8Tau1, h_jetsAK8Tau1 )
        event.getByLabel ( l_jetsAK8Tau2, h_jetsAK8Tau2 )
        event.getByLabel ( l_jetsAK8Tau3, h_jetsAK8Tau3 )
        event.getByLabel ( l_jetsAK8nSubJets, h_jetsAK8nSubJets )
        event.getByLabel ( l_jetsAK8minmass, h_jetsAK8minmass )

        event.getByLabel ( l_jetsAK8TopSubjetIndex0, h_jetsAK8TopSubjetIndex0 )
        event.getByLabel ( l_jetsAK8TopSubjetIndex1, h_jetsAK8TopSubjetIndex1 )
        event.getByLabel ( l_jetsAK8TopSubjetIndex2, h_jetsAK8TopSubjetIndex2 )
        event.getByLabel ( l_jetsAK8TopSubjetIndex3, h_jetsAK8TopSubjetIndex3 )

        event.getByLabel ( l_subjetsAK8BDisc, h_subjetsAK8BDisc)
        event.getByLabel ( l_subjetsAK8Pt, h_subjetsAK8Pt)
        event.getByLabel ( l_subjetsAK8Eta, h_subjetsAK8Eta)
        event.getByLabel ( l_subjetsAK8Phi, h_subjetsAK8Phi)
        if options.deweightFlat : 
            #@ Event weights
            gotGenerator = event.getByLabel( l_generator, h_generator )

        evWeight = -1

        ak8JetsGood = []
        ak8JetsGoodTrimMass = []
        ak8JetsGoodPrunMass = []
        ak8JetsGoodFiltMass = []
        ak8JetsGoodSDropMass = []
        ak8JetsGoodTau1 = []
        ak8JetsGoodTau2 = []
        ak8JetsGoodTau3 = []
        ak8JetsGoodNSubJets = []
        ak8JetsGoodMinMass = []
        ak8JetsGoodMass = []
        ak8JetsGoodPhi = []
        ak8JetsGoodY = []
        ak8JetsGoodPt = []
        ak8JetsGoodTopSubjetIndex0 = []
        ak8JetsGoodTopSubjetIndex1 = []
        ak8JetsGoodTopSubjetIndex2 = []
        ak8JetsGoodTopSubjetIndex3 = []

        AK8SubJetsBDisc = []
        AK8SubJetsPt = []
        AK8SubJetsEta = []
        AK8SubJetsPhi = []


        if len( h_jetsAK8Pt.product()) > 0 and len( h_subjetsAK8BDisc.product() ) > 0:

            AK8Pt = h_jetsAK8Pt.product()
            AK8Eta = h_jetsAK8Eta.product()
            AK8Phi = h_jetsAK8Phi.product()
            AK8Mass = h_jetsAK8Mass.product()
            AK8Energy = h_jetsAK8Energy.product()
            AK8Y = h_jetsAK8Y.product()

            AK8JEC = h_jetsAK8JEC.product()
            AK8Area = h_jetsAK8Area.product()

            AK8nHadE = h_jetsAK8nHadEnergy.product()
            AK8nEME = h_jetsAK8nEMEnergy.product()
            AK8cHadE =  h_jetsAK8cHadEnergy.product()
            AK8HFHadE = h_jetsAK8HFHadronEnergy.product()
            AK8cEME =  h_jetsAK8cEMEnergy.product()
            AK8numDaughters = h_jetsAK8numDaughters.product()
            AK8cMultip =  h_jetsAK8cMultip.product()

            AK8TrimmedM = h_jetsAK8TrimMass.product()
            AK8PrunedM = h_jetsAK8PrunMass.product()
            AK8FilteredM = h_jetsAK8FiltMass.product()
            AK8SDropM = h_jetsAK8SoftDropMass.product()
            AK8Tau1 = h_jetsAK8Tau1.product()
            AK8Tau2 = h_jetsAK8Tau2.product()
            AK8Tau3 = h_jetsAK8Tau3.product()
            AK8nSubJets = h_jetsAK8nSubJets.product()
            AK8minmass = h_jetsAK8minmass.product()
            AK8TopSubjetIndex0 = h_jetsAK8TopSubjetIndex0.product()
            AK8TopSubjetIndex1 = h_jetsAK8TopSubjetIndex1.product()
            AK8TopSubjetIndex2 = h_jetsAK8TopSubjetIndex2.product()
            AK8TopSubjetIndex3 = h_jetsAK8TopSubjetIndex3.product()
            AK8SubJetsBDisc = h_subjetsAK8BDisc.product()
            AK8SubJetsPt = h_subjetsAK8Pt.product()
            AK8SubJetsEta = h_subjetsAK8Eta.product()
            AK8SubJetsPhi = h_subjetsAK8Phi.product()
            if options.deweightFlat :
                pthat = 0.0
                if h_generator.product().hasBinningValues() :
                    pthat = h_generator.product().binningValues()[0]
                    evWeight = 1/pow(pthat/15.,4.5)
        else :
            continue
        for ak8Jet in range(0,len(AK8Pt)):
            BadStuff = False
            if len(AK8Pt) <= 0 or len(AK8Eta) <= 0 or len(AK8Phi) <= 0 or len(AK8Mass) <= 0 :
                continue
            AK8JECFromB2GAnaFW = AK8JEC[ak8Jet]
            AK8P4Raw = ROOT.TLorentzVector()
            AK8P4Raw.SetPtEtaPhiM( AK8Pt[ak8Jet] , AK8Eta[ak8Jet], AK8Phi[ak8Jet], AK8Mass[ak8Jet])
            # Remove the old JEC's to get raw energy
            AK8P4Raw *= AK8JECFromB2GAnaFW 
            RawAK8Energy = AK8P4Raw.Energy()

            #$ Cut based on charged and neutral energy for AK8 jets
            nhf = AK8nHadE[ak8Jet] / AK8P4Raw.E()
            nef = AK8nEME[ak8Jet] / AK8P4Raw.E()
            chf = AK8cHadE[ak8Jet] / AK8P4Raw.E()
            cef = AK8cEME[ak8Jet] / AK8P4Raw.E()
            nconstituents = AK8numDaughters[ak8Jet]
            nch = AK8cMultip[ak8Jet] 
            goodJet = \
                nhf < 0.99 and \
                nef < 0.99 and \
                chf > 0.00 and \
                cef < 0.99 and \
                nconstituents > 1 and \
                nch > 0

            if not goodJet :
                if options.verbose :
                    print '   bad jet pt = {0:6.2f}, y = {1:6.2f}, phi = {2:6.2f}, m = {3:6.2f}'.format (
                            AK8P4Raw.Perp(), AK8P4Raw.Rapidity(), AK8P4Raw.Phi(), AK8P4Raw.M()
                            )
                continue
            if options.verbose :
                  print '   raw jet pt = {0:6.2f}, y = {1:6.2f}, phi = {2:6.2f}, m = {3:6.2f}'.format (
                        AK8P4Raw.Perp(), AK8P4Raw.Rapidity(), AK8P4Raw.Phi(), AK8P4Raw.M()
                        )

            #@ JEC Scaling for AK8 Jets
            ak8JetCorrector.setJetEta( AK8P4Raw.Eta() )
            ak8JetCorrector.setJetPt ( AK8P4Raw.Perp() )
            ak8JetCorrector.setJetE  ( AK8P4Raw.E() )
            ak8JetCorrector.setJetA  ( AK8Area[ak8Jet] )
            ak8JetCorrector.setRho   ( rho )
            ak8JetCorrector.setNPV   ( NPV )
            newJEC = ak8JetCorrector.getCorrection()
            AK8P4Corr = AK8P4Raw*newJEC

            if options.verbose :
                print '  len(AK8SubJetsPt) : '+str(len(AK8SubJetsPt))
            for check in  [AK8TopSubjetIndex0[ak8Jet],
                           AK8TopSubjetIndex1[ak8Jet],
                           AK8TopSubjetIndex2[ak8Jet],
                           AK8TopSubjetIndex3[ak8Jet]] :
                if options.verbose :
                    print ' check: '+str(int(check))
                if int(check) > len(AK8SubJetsPt) :
                    print '===================='
                    print ' Catastrophic failure. Index is out of range. Setup is completely wrong.'
                    print '===================='
                    BadStuff = True
                    break
            if BadStuff :
                break

            if options.verbose :
                print '    ak8TopSubjetIndex0[ak8Jet] '+str(AK8TopSubjetIndex0[ak8Jet])
                print '    ak8TopSubjetIndex1[ak8Jet] '+str(AK8TopSubjetIndex1[ak8Jet])
                print '    ak8TopSubjetIndex2[ak8Jet] '+str(AK8TopSubjetIndex2[ak8Jet])
                print '    ak8TopSubjetIndex3[ak8Jet] '+str(AK8TopSubjetIndex3[ak8Jet])
            h_pt.Fill(AK8P4Raw.Perp(), evWeight)

            #$ Cuts based on pt and rapidity
            if AK8P4Raw.Perp() < options.minAK8Pt or abs(AK8P4Raw.Rapidity()) > options.maxAK8Rapidity :
                  continue

            #if AK8nSubJets[i] >= 3 and AK8minmass[i] > 50 and AK8P4Corr.M() > 100 :
            ak8JetsGood.append(AK8P4Corr)
            ak8JetsGoodTrimMass.append( AK8TrimmedM[ak8Jet])
            ak8JetsGoodPrunMass.append( AK8PrunedM[ak8Jet])
            ak8JetsGoodFiltMass.append( AK8FilteredM[ak8Jet])
            ak8JetsGoodSDropMass.append( AK8SDropM[ak8Jet])
            ak8JetsGoodTau1.append( AK8Tau1[ak8Jet])
            ak8JetsGoodTau2.append( AK8Tau2[ak8Jet])
            ak8JetsGoodTau3.append( AK8Tau3[ak8Jet])
            ak8JetsGoodNSubJets.append( AK8nSubJets[ak8Jet])
            ak8JetsGoodMinMass.append( AK8minmass[ak8Jet] )
            ak8JetsGoodPhi.append( AK8Phi[ak8Jet] )
            ak8JetsGoodY.append( AK8Y[ak8Jet] )
            ak8JetsGoodPt.append( AK8Pt[ak8Jet] )
            ak8JetsGoodMass.append( AK8Mass[ak8Jet] )
            ak8JetsGoodTopSubjetIndex0.append( AK8TopSubjetIndex0[ak8Jet] )
            ak8JetsGoodTopSubjetIndex1.append( AK8TopSubjetIndex1[ak8Jet] )
            ak8JetsGoodTopSubjetIndex2.append( AK8TopSubjetIndex2[ak8Jet] )
            ak8JetsGoodTopSubjetIndex3.append( AK8TopSubjetIndex3[ak8Jet] )
            NGoodAK8Jets= NGoodAK8Jets + 1


        if len(ak8JetsGood) < 1 :
            if options.verbose :
                print 'Not enough AK8 jets, skipping'
            continue
        #print 'len ak8JetsGood', len(ak8JetsGood)
        subJetBDiscs = [None]*4
        subJetBDiscs[0] = []
        subJetBDiscs[1] = []
        subJetBDiscs[2] = []
        subJetBDiscs[3] = []

        #Looping over ak8 jets
        if options.verbose :
            print 'starting good jet loop'
        for goodAK8 in range(0,len(ak8JetsGood)): 
            if ak8JetsGood[goodAK8].Perp() < options.minAK8Pt :
                continue
            #subJetBDiscs.append([])
            if BadStuff : 
                break
            BadStuff = False
            sbdisc0 = -1.
            sbdisc1 = -1.
            sbdisc2 = -1.
            sbdisc3 = -1.
            spt0 = -1.
            spt1 = -1.
            spt2 = -1.
            spt3 = -1.
            seta0 = -1.
            seta1 = -1.
            seta2 = -1.
            seta3 = -1.
            sphi0 = -1.
            sphi1 = -1.
            sphi2 = -1.
            sphi3 = -1.
            if options.verbose :
                print 'len(AK8SubJetsPt) : '+str(len(AK8SubJetsPt))
            for check in [ak8JetsGoodTopSubjetIndex0[goodAK8],
                          ak8JetsGoodTopSubjetIndex1[goodAK8],
                          ak8JetsGoodTopSubjetIndex2[goodAK8],
                          ak8JetsGoodTopSubjetIndex3[goodAK8]] :
                if options.verbose :
                    print ' check: '+str(int(check))
                if int(check) > len(AK8SubJetsPt) :
                    print '===================='
                    print ' Catastrophic failure. Index is out of range. Setup is completely wrong.'
                    print '===================='
                    BadStuff = True
                    break
            if BadStuff :
                break
            #if options.verbose :
             #   print 'ak8JetsGoodTopSubjetIndex0[goodAK8] '+str(ak8JetsGoodTopSubjetIndex0[goodAK8])
             #   print 'ak8JetsGoodTopSubjetIndex1[goodAK8] '+str(ak8JetsGoodTopSubjetIndex1[goodAK8])
             #   print 'ak8JetsGoodTopSubjetIndex2[goodAK8] '+str(ak8JetsGoodTopSubjetIndex2[goodAK8])
             #   print 'ak8JetsGoodTopSubjetIndex3[goodAK8] '+str(ak8JetsGoodTopSubjetIndex3[goodAK8])

            

            #if ak8JetsGoodTopSubjetIndex0[goodAK8] > -1 :
             #   sbdisc0 = AK8SubJetsBDisc[ int(ak8JetsGoodTopSubjetIndex0[goodAK8]) ]
             #   spt0    = AK8SubJetsPt[ int(ak8JetsGoodTopSubjetIndex0[goodAK8]) ]
             #   seta0   = AK8SubJetsEta[ int(ak8JetsGoodTopSubjetIndex0[goodAK8]) ]
             #   sphi0   = AK8SubJetsPhi[ int(ak8JetsGoodTopSubjetIndex0[goodAK8]) ]
             #   if len( subJetBDiscs ) > 1 :
             #       subJetBDiscs[0].append(sbdisc0)

            #if ak8JetsGoodTopSubjetIndex1[goodAK8] > -1 :
            #    sbdisc1 = AK8SubJetsBDisc[ int(ak8JetsGoodTopSubjetIndex1[goodAK8]) ]
            #    spt1    = AK8SubJetsPt[ int(ak8JetsGoodTopSubjetIndex1[goodAK8]) ]
            #    seta1   = AK8SubJetsEta[ int(ak8JetsGoodTopSubjetIndex1[goodAK8]) ]
            #    sphi1   = AK8SubJetsPhi[ int(ak8JetsGoodTopSubjetIndex1[goodAK8]) ]
            #    if len( subJetBDiscs ) > 1 :
            #        subJetBDiscs[1].append(sbdisc1)

            #if ak8JetsGoodTopSubjetIndex2[goodAK8] > -1 :
            #    sbdisc2 = AK8SubJetsBDisc[ int(ak8JetsGoodTopSubjetIndex2[goodAK8]) ]
            #    spt2    = AK8SubJetsPt[ int(ak8JetsGoodTopSubjetIndex2[goodAK8]) ]
            #    seta2   = AK8SubJetsEta[ int(ak8JetsGoodTopSubjetIndex2[goodAK8]) ]
            #    sphi2   = AK8SubJetsPhi[ int(ak8JetsGoodTopSubjetIndex2[goodAK8]) ]
            #    if len( subJetBDiscs ) > 1 :
            #        subJetBDiscs[2].append(sbdisc2)

           # if ak8JetsGoodTopSubjetIndex3[goodAK8] > -1 :
           #     sbdisc3 = AK8SubJetsBDisc[ int(ak8JetsGoodTopSubjetIndex3[goodAK8]) ]
           #     spt3    = AK8SubJetsPt[ int(ak8JetsGoodTopSubjetIndex3[goodAK8]) ]
           #     seta3   = AK8SubJetsEta[ int(ak8JetsGoodTopSubjetIndex3[goodAK8]) ]
           #     sphi3   = AK8SubJetsPhi[ int(ak8JetsGoodTopSubjetIndex3[goodAK8]) ]
           #     if len( subJetBDiscs ) > 1 :
           #         subJetBDiscs[3].append(sbdisc3)


        # Make sure there are at least 2 jets
        if len(ak8JetsGood) < 2 :
            continue
        NPassDiJetCut = NPassDiJetCut + 1
        if options.verbose :
            print 'len ak8JetsGood', len(ak8JetsGood)

        # deltaPhi cut assures the 2 jets are back to back
        deltaPhi = ak8JetsGoodPhi[0] - ak8JetsGoodPhi[1]
        if deltaPhi > ROOT.TMath.Pi():
            deltaPhi = deltaPhi - 2*ROOT.TMath.Pi()
        if deltaPhi < -ROOT.TMath.Pi():
            deltaPhi = deltaPhi + 2*ROOT.TMath.Pi()

        # apply the pt, Y, eta and deltaPhi cuts
        ptCuts = ak8JetsGoodPt[0] > 350 and ak8JetsGoodPt[1] > 350
        deltaY = (ak8JetsGoodY[0] - ak8JetsGoodY[1])
        etaCuts = abs(ak8JetsGoodY[0]) < 2.4 and abs(ak8JetsGoodY[1]) < 2.4
        deltaPhiCut = abs(deltaPhi)>2.1
        passType11KinCuts   = ptCuts and etaCuts and deltaPhiCut
        
        if ptCuts : 
            NPassptCut = NPassptCut + 1
        if etaCuts :
            NPassetaCut = NPassetaCut + 1
        if deltaPhiCut :
            NPassdPhiCut = NPassdPhiCut + 1

        # for the first 2 jets get the subjetBDiscs
        Jet0BDiscs = []
        Jet1BDiscs = []

        #i = 0
        #while i < (ak8JetsGoodNSubJets[0]):
        #    Jet0BDiscs.append( subJetBDiscs[0][i] )
        #    i = i + 1

        #i = 0
        #while i < (ak8JetsGoodNSubJets[1]):
        #    Jet1BDiscs.append( subJetBDiscs[1][i] )
        #    i = i + 1

        #if len( subJetBDiscs ) > 1 :
        #    for j in xrange ( 0, len( subJetBDiscs[0]) ) :
        #        Jet0BDiscs.append( subJetBDiscs[0][j] )
        #    for j in xrange ( 0, len( subJetBDiscs[1]) ) :
        #        Jet1BDiscs.append( subJetBDiscs[1][j] )


        # find the maximum bDisc (of all the subjets probably one is a b with the biggest bDisc)
        #jet0_maxB = max(Jet0BDiscs)
        #jet1_maxB = max(Jet1BDiscs)
        #if len( Jet0BDiscs ) > 0 : 
        #    jet0_maxB = max(Jet0BDiscs)
        #else :
        #    jet0_maxB = -999.
        #if len( Jet1BDiscs ) > 0 : 
       #     jet1_maxB = max(Jet1BDiscs)
       # else :
       #     jet1_maxB = -999.
        if ak8JetsGoodTau2[0] != 0 :
            jet1tau32Val = ak8JetsGoodTau3[0] / ak8JetsGoodTau2[0]
        else :
            jet1tau32Val = -1
        if ak8JetsGoodTau2[1] != 0 :            
            jet2tau32Val = ak8JetsGoodTau3[1] / ak8JetsGoodTau2[1]
        else : 
            jet2tau32Val = -1

        # different cuts, finding where the top-tag is, and different working points for the top-tagger
        #failMinMass0    = ak8JetsGoodMass[0] > 140 and ak8JetsGoodMass[0] < 250 and ak8JetsGoodMinMass[0] < 50 
        #failMinMass1    = ak8JetsGoodMass[1] > 140 and ak8JetsGoodMass[1] < 250 and ak8JetsGoodMinMass[1] < 50
        #failMinMassLow0 = ak8JetsGoodMass[0] > 140 and ak8JetsGoodMass[0] < 250 and ak8JetsGoodMinMass[0] < 30
        #failMinMassLow1 = ak8JetsGoodMass[1] > 140 and ak8JetsGoodMass[1] < 250 and ak8JetsGoodMinMass[1] < 30
        #fail2Nsub0      = ak8JetsGoodMass[0] > 140 and ak8JetsGoodMass[0] < 250 and ak8JetsGoodNSubJets[0] < 2
        #fail2Nsub1      = ak8JetsGoodMass[1] > 140 and ak8JetsGoodMass[1] < 250 and ak8JetsGoodNSubJets[1] < 2
        #fail3Nsub0      = ak8JetsGoodMass[0] > 140 and ak8JetsGoodMass[0] < 250 and ak8JetsGoodNSubJets[0] < 3
        #fail3Nsub1      = ak8JetsGoodMass[1] > 140 and ak8JetsGoodMass[1] < 250 and ak8JetsGoodNSubJets[1] < 3

        failMinMass0    = ak8JetsGoodSDropMass[0] > 140 and ak8JetsGoodSDropMass[0] < 200 and ak8JetsGoodMinMass[0] < 50
        failMinMass1    = ak8JetsGoodSDropMass[1] > 140 and ak8JetsGoodSDropMass[1] < 200 and ak8JetsGoodMinMass[1] < 50
        failMinMassLow0 = ak8JetsGoodSDropMass[0] > 140 and ak8JetsGoodSDropMass[0] < 200 and ak8JetsGoodMinMass[0] < 30
        failMinMassLow1 = ak8JetsGoodSDropMass[1] > 140 and ak8JetsGoodSDropMass[1] < 200 and ak8JetsGoodMinMass[1] < 30
        fail2Nsub0      = ak8JetsGoodSDropMass[0] > 140 and ak8JetsGoodSDropMass[0] < 200 and ak8JetsGoodNSubJets[0] < 2
        fail2Nsub1      = ak8JetsGoodSDropMass[1] > 140 and ak8JetsGoodSDropMass[1] < 200 and ak8JetsGoodNSubJets[1] < 2
        fail3Nsub0      = ak8JetsGoodSDropMass[0] > 140 and ak8JetsGoodSDropMass[0] < 200 and ak8JetsGoodNSubJets[0] < 3
        fail3Nsub1      = ak8JetsGoodSDropMass[1] > 140 and ak8JetsGoodSDropMass[1] < 200 and ak8JetsGoodNSubJets[1] < 3

        bTag0 = .99#jet0_maxB
        bTag1 = .99#jet1_maxB
            
        #topTag0        = ak8JetsGoodSDropMass[0] > 140 and ak8JetsGoodSDropMass[0] < 200 and ak8JetsGoodMinMass[0] > 50 and ak8JetsGoodNSubJets[0] > 2 and jet1tau32Val < 0.7
        #topTag1        = ak8JetsGoodSDropMass[1] > 140 and ak8JetsGoodSDropMass[1] < 200 and ak8JetsGoodMinMass[1] > 50 and ak8JetsGoodNSubJets[1] > 2 and jet2tau32Val < 0.7
        topTag0        = ak8JetsGoodSDropMass[0] > 110 and ak8JetsGoodSDropMass[0] < 210 and  jet1tau32Val < 0.7
        topTag1        = ak8JetsGoodSDropMass[1] > 110 and ak8JetsGoodSDropMass[1] < 210 and  jet2tau32Val < 0.7

        AntiTag0SD = ak8JetsGoodSDropMass[0] > 140 and ak8JetsGoodSDropMass[0] < 200# and ak8JetsGoodMinMass[0] < 50 
        AntiTag1SD = ak8JetsGoodSDropMass[1] > 140 and ak8JetsGoodSDropMass[1] < 200# and ak8JetsGoodMinMass[1] < 50
        AntiTag0NM = ak8JetsGoodMinMass[0] < 50 
        AntiTag1NM = ak8JetsGoodMinMass[1] < 50
        AntiTag0FJ = ak8JetsGoodMass[0] > 140 and ak8JetsGoodMass[0] < 250# and ak8JetsGoodMinMass[0] < 50 
        AntiTag1FJ = ak8JetsGoodMass[1] > 140 and ak8JetsGoodMass[1] < 250# and ak8JetsGoodMinMass[1] < 50
        MinMass0 = ak8JetsGoodMinMass[0] < 50
        MinMass1 = ak8JetsGoodMinMass[1] < 50
        Tau32Cut0 = jet1tau32Val > .7
        Tau32Cut1 = jet2tau32Val > .7
        topTag0WP1        = jet1tau32Val < 0.7 and bTag0 > 0.244 and ak8JetsGoodMass[0] > 140 and ak8JetsGoodMass[0] < 250 and ak8JetsGoodMinMass[0] > 50 and ak8JetsGoodNSubJets[0] > 2
        topTag1WP1        = jet2tau32Val < 0.7 and bTag1 > 0.244 and ak8JetsGoodMass[1] > 140 and ak8JetsGoodMass[1] < 250 and ak8JetsGoodMinMass[1] > 50 and ak8JetsGoodNSubJets[1] > 2
        topTag0WP2        = jet1tau32Val < 0.6 and bTag0 > 0.244 and ak8JetsGoodMass[0] > 140 and ak8JetsGoodMass[0] < 250 and ak8JetsGoodMinMass[0] > 50 and ak8JetsGoodNSubJets[0] > 2
        topTag1WP2        = jet2tau32Val < 0.6 and bTag1 > 0.244 and ak8JetsGoodMass[1] > 140 and ak8JetsGoodMass[1] < 250 and ak8JetsGoodMinMass[1] > 50 and ak8JetsGoodNSubJets[1] > 2
        topTag0WP3        = jet1tau32Val < 0.55 and bTag0 > 0.679 and ak8JetsGoodMass[0] > 140 and ak8JetsGoodMass[0] < 250 and ak8JetsGoodMinMass[0] > 50 and ak8JetsGoodNSubJets[0] > 2
        topTag1WP3        = jet2tau32Val < 0.55 and bTag1 > 0.679 and ak8JetsGoodMass[1] > 140 and ak8JetsGoodMass[1] < 250 and ak8JetsGoodMinMass[1] > 50 and ak8JetsGoodNSubJets[1] > 2
        topTag0WP4        = jet1tau32Val < 0.5 and bTag0 > 0.679 and ak8JetsGoodMass[0] > 140 and ak8JetsGoodMass[0] < 250 and ak8JetsGoodMinMass[0] > 65 and ak8JetsGoodNSubJets[0] > 2
        topTag1WP4        = jet2tau32Val < 0.5 and bTag1 > 0.679 and ak8JetsGoodMass[1] > 140 and ak8JetsGoodMass[1] < 250 and ak8JetsGoodMinMass[1] > 65 and ak8JetsGoodNSubJets[1] > 2
        topTag0WP5        = jet1tau32Val < 0.4 and bTag0 > 0.679 and ak8JetsGoodMass[0] > 140 and ak8JetsGoodMass[0] < 250 and ak8JetsGoodMinMass[0] > 55 and ak8JetsGoodNSubJets[0] > 2
        topTag1WP5        = jet2tau32Val < 0.4 and bTag1 > 0.679 and ak8JetsGoodMass[1] > 140 and ak8JetsGoodMass[1] < 250 and ak8JetsGoodMinMass[1] > 55 and ak8JetsGoodNSubJets[1] > 2


        if evWeight != -1 :
            Weight = evWeight
        else :
            Weight = 1
            
        # Randomly selecting a jet, getting the probe jet and the tag.
        if passType11KinCuts :
            NPassAllCuts = NPassAllCuts + 1
            x = ROOT.gRandom.Uniform(1.0)
            if x < 0.5 :
                h_topProbePtFree.Fill( ak8JetsGoodPt[1], Weight )
                h_topProbemmFree.Fill( ak8JetsGoodMinMass[1], Weight )
                h_topProbeak8mFree.Fill( ak8JetsGoodMass[1], Weight )
                h_topProbeSDmFree.Fill( ak8JetsGoodSDropMass[1], Weight )  
                h_topProbeTau32Free.Fill( jet2tau32Val, Weight )
                h_topProbePhiFree.Fill( ak8JetsGoodPhi[1], Weight)
                h_topProbeYFree.Fill( ak8JetsGoodY[1], Weight) 
                if topTag1 :
                    NGoodAntiTagTopTagPairsFree = NGoodAntiTagTopTagPairsFree + 1
                    h_topTagPtFree.Fill( ak8JetsGoodPt[1], Weight )
                if AntiTag0SD and MinMass0 :
                    NGoodAntiTaggedEventsSD = NGoodAntiTaggedEventsSD + 1
                    h_topProbePtSD.Fill ( ak8JetsGoodPt[1], Weight )
                    h_topProbemmSD.Fill( ak8JetsGoodMinMass[1], Weight )
                    h_topProbeak8mSD.Fill( ak8JetsGoodMass[1], Weight )
                    h_topProbeSDmSD.Fill( ak8JetsGoodSDropMass[1], Weight )  
                    h_topProbeTau32SD.Fill( jet2tau32Val, Weight )
                    h_topProbePhiSD.Fill( ak8JetsGoodPhi[1], Weight)
                    h_topProbeYSD.Fill( ak8JetsGoodY[1], Weight)
                    if topTag1 :
                        NGoodAntiTagTopTagPairsSD = NGoodAntiTagTopTagPairsSD + 1
                        h_topTagPtSD.Fill( ak8JetsGoodPt[1], Weight )
                if AntiTag0NM :
                    NGoodAntiTaggedEventsNM = NGoodAntiTaggedEventsNM + 1
                    h_topProbePtNM.Fill ( ak8JetsGoodPt[1], Weight )
                    h_topProbemmNM.Fill( ak8JetsGoodMinMass[1], Weight )
                    h_topProbeak8mNM.Fill( ak8JetsGoodMass[1], Weight )
                    h_topProbeSDmNM.Fill( ak8JetsGoodSDropMass[1], Weight )  
                    h_topProbeTau32NM.Fill( jet2tau32Val, Weight )
                    h_topProbePhiNM.Fill( ak8JetsGoodPhi[1], Weight)
                    h_topProbeYNM.Fill( ak8JetsGoodY[1], Weight) 
                    if topTag1 :
                        NGoodAntiTagTopTagPairsNM = NGoodAntiTagTopTagPairsNM + 1
                        h_topTagPtNM.Fill( ak8JetsGoodPt[1], Weight )
                if AntiTag0FJ and MinMass0 :
                    NGoodAntiTaggedEventsFJ = NGoodAntiTaggedEventsFJ + 1
                    h_topProbePtFJ.Fill ( ak8JetsGoodPt[1], Weight )
                    h_topProbemmFJ.Fill( ak8JetsGoodMinMass[1], Weight )
                    h_topProbeak8mFJ.Fill( ak8JetsGoodMass[1], Weight )
                    h_topProbeSDmFJ.Fill( ak8JetsGoodSDropMass[1], Weight )  
                    h_topProbeTau32FJ.Fill( jet2tau32Val, Weight )
                    h_topProbePhiFJ.Fill( ak8JetsGoodPhi[1], Weight)
                    h_topProbeYFJ.Fill( ak8JetsGoodY[1], Weight) 
                    if topTag1 :
                        NGoodAntiTagTopTagPairsFJ = NGoodAntiTagTopTagPairsFJ + 1
                        h_topTagPtFJ.Fill( ak8JetsGoodPt[1], Weight )
                if AntiTag0SD and Tau32Cut0 :
                    NGoodAntiTaggedEventsSDT = NGoodAntiTaggedEventsSDT + 1
                    h_topProbePtSDT.Fill ( ak8JetsGoodPt[1], Weight )
                    h_topProbemmSDT.Fill( ak8JetsGoodMinMass[1], Weight )
                    h_topProbeak8mSDT.Fill( ak8JetsGoodMass[1], Weight )
                    h_topProbeSDmSDT.Fill( ak8JetsGoodSDropMass[1], Weight )  
                    h_topProbeTau32SDT.Fill( jet2tau32Val, Weight )
                    h_topProbePhiSDT.Fill( ak8JetsGoodPhi[1], Weight)
                    h_topProbeYSDT.Fill( ak8JetsGoodY[1], Weight) 
                    if topTag1 :
                        NGoodAntiTagTopTagPairsSDT = NGoodAntiTagTopTagPairsSDT + 1
                        h_topTagPtSDT.Fill( ak8JetsGoodPt[1], Weight )
                if Tau32Cut0 :
                    NGoodAntiTaggedEventsNMT = NGoodAntiTaggedEventsNMT + 1
                    h_topProbePtNMT.Fill ( ak8JetsGoodPt[1], Weight )
                    h_topProbemmNMT.Fill( ak8JetsGoodMinMass[1], Weight )
                    h_topProbeak8mNMT.Fill( ak8JetsGoodMass[1], Weight )
                    h_topProbeSDmNMT.Fill( ak8JetsGoodSDropMass[1], Weight )  
                    h_topProbeTau32NMT.Fill( jet2tau32Val, Weight )
                    h_topProbePhiNMT.Fill( ak8JetsGoodPhi[1], Weight)
                    h_topProbeYNMT.Fill( ak8JetsGoodY[1], Weight) 
                    if topTag1 :
                        NGoodAntiTagTopTagPairsNMT = NGoodAntiTagTopTagPairsNMT + 1
                        h_topTagPtNMT.Fill( ak8JetsGoodPt[1], Weight )
                if AntiTag0FJ and Tau32Cut0 :
                    NGoodAntiTaggedEventsFJT = NGoodAntiTaggedEventsFJT + 1
                    h_topProbePtFJT.Fill ( ak8JetsGoodPt[1], Weight )
                    h_topProbemmFJT.Fill( ak8JetsGoodMinMass[1], Weight )
                    h_topProbeak8mFJT.Fill( ak8JetsGoodMass[1], Weight )
                    h_topProbeSDmFJT.Fill( ak8JetsGoodSDropMass[1], Weight )  
                    h_topProbeTau32FJT.Fill( jet2tau32Val, Weight )
                    h_topProbePhiFJT.Fill( ak8JetsGoodPhi[1], Weight)
                    h_topProbeYFJT.Fill( ak8JetsGoodY[1], Weight) 
 
                    if topTag1 :
                        NGoodAntiTagTopTagPairsFJT = NGoodAntiTagTopTagPairsFJT + 1
                        h_topTagPtFJT.Fill( ak8JetsGoodPt[1], Weight )
                if failMinMass0 :
                    h_testProbePt.Fill( ak8JetsGoodPt[1], Weight )
                    if topTag1 :
                        h_testTagPt.Fill( ak8JetsGoodPt[1], Weight )
                if failMinMassLow0 :
                    h_lowmMinProbePt.Fill( ak8JetsGoodPt[1], Weight )
                    if topTag1WP1:
                        h_lowmMinTagWP1Pt.Fill( ak8JetsGoodPt[1], Weight )
                    if topTag1WP2:
                        h_lowmMinTagWP2Pt.Fill( ak8JetsGoodPt[1],Weight )
                    if topTag1WP3:
                        h_lowmMinTagWP3Pt.Fill( ak8JetsGoodPt[1], Weight )
                    if topTag1WP4:
                        h_lowmMinTagWP4Pt.Fill( ak8JetsGoodPt[1], Weight )
                    if topTag1WP5:
                        h_lowmMinTagWP5Pt.Fill( ak8JetsGoodPt[1], Weight )
                    if topTag1:
                        h_lowmMinTagPt.Fill( ak8JetsGoodPt[1], Weight )
                        if not bTag0:
                            h_lowmMinBProbePt.Fill( ak8JetsGoodPt[1], Weight )
                            if bTag1 :
                                h_lowmMinBTagPt.Fill( ak8JetsGoodPt[1], Weight ) 
                    if bTag1 and bTag0:
                        h_lowmMin2BProbePt.Fill( ak8JetsGoodPt[1], Weight )
                    if topTag1 and bTag1 and bTag0:
                        h_lowmMin2BTagPt.Fill( ak8JetsGoodPt[1], Weight )
                if topTag0 and topTag1 and not bTag0:
                    h_antiBProbePt.Fill( ak8JetsGoodPt[1], Weight )
                    if bTag1:
                        h_antiBTagPt.Fill( ak8JetsGoodPt[1], Weight )  



            if x >= 0.5 :
                h_topProbePtFree.Fill( ak8JetsGoodPt[0], Weight)
                h_topProbemmFree.Fill( ak8JetsGoodMinMass[0], Weight )
                h_topProbeak8mFree.Fill( ak8JetsGoodMass[0], Weight )
                h_topProbeSDmFree.Fill( ak8JetsGoodSDropMass[0], Weight )  
                h_topProbeTau32Free.Fill( jet1tau32Val, Weight )
                h_topProbePhiFree.Fill( ak8JetsGoodPhi[0], Weight)
                h_topProbeYFree.Fill( ak8JetsGoodY[0], Weight)  
                if topTag0 :
                    NGoodAntiTagTopTagPairsFree = NGoodAntiTagTopTagPairsFree + 1
                    h_topTagPtFree.Fill(ak8JetsGoodPt[0], Weight )
                if AntiTag1SD and MinMass1 :
                    NGoodAntiTaggedEventsSD = NGoodAntiTaggedEventsSD + 1
                    h_topProbePtSD.Fill( ak8JetsGoodPt[0], Weight )
                    h_topProbemmSD.Fill( ak8JetsGoodMinMass[0], Weight )
                    h_topProbeak8mSD.Fill( ak8JetsGoodMass[0], Weight )
                    h_topProbeSDmSD.Fill( ak8JetsGoodSDropMass[0], Weight )  
                    h_topProbeTau32SD.Fill( jet1tau32Val, Weight )
                    h_topProbePhiSD.Fill( ak8JetsGoodPhi[0], Weight)
                    h_topProbeYSD.Fill( ak8JetsGoodY[0], Weight) 
                    if topTag0 :
                        NGoodAntiTagTopTagPairsSD = NGoodAntiTagTopTagPairsSD + 1
                        h_topTagPtSD.Fill( ak8JetsGoodPt[0], Weight )
                if AntiTag1NM:
                    NGoodAntiTaggedEventsNM = NGoodAntiTaggedEventsNM + 1
                    h_topProbePtNM.Fill( ak8JetsGoodPt[0], Weight )
                    h_topProbemmNM.Fill( ak8JetsGoodMinMass[0], Weight )
                    h_topProbeak8mNM.Fill( ak8JetsGoodMass[0], Weight )
                    h_topProbeSDmNM.Fill( ak8JetsGoodSDropMass[0], Weight )  
                    h_topProbeTau32NM.Fill( jet1tau32Val, Weight )
                    h_topProbePhiNM.Fill( ak8JetsGoodPhi[0], Weight)
                    h_topProbeYNM.Fill( ak8JetsGoodY[0], Weight) 
                    if topTag0 :
                        NGoodAntiTagTopTagPairsNM = NGoodAntiTagTopTagPairsNM + 1
                        h_topTagPtNM.Fill( ak8JetsGoodPt[0], Weight )
                if AntiTag1FJ and MinMass1 :
                    NGoodAntiTaggedEventsFJ = NGoodAntiTaggedEventsFJ + 1
                    h_topProbePtFJ.Fill( ak8JetsGoodPt[0], Weight )
                    h_topProbemmFJ.Fill( ak8JetsGoodMinMass[0], Weight )
                    h_topProbeak8mFJ.Fill( ak8JetsGoodMass[0], Weight )
                    h_topProbeSDmFJ.Fill( ak8JetsGoodSDropMass[0], Weight )  
                    h_topProbeTau32FJ.Fill( jet1tau32Val, Weight )
                    h_topProbePhiFJ.Fill( ak8JetsGoodPhi[0], Weight)
                    h_topProbeYFJ.Fill( ak8JetsGoodY[0], Weight)
                    if topTag0 :
                        NGoodAntiTagTopTagPairsFJ = NGoodAntiTagTopTagPairsFJ + 1
                        h_topTagPtFJ.Fill( ak8JetsGoodPt[0], Weight )
                if AntiTag1SD and Tau32Cut1 :
                    NGoodAntiTaggedEventsSDT = NGoodAntiTaggedEventsSDT + 1
                    h_topProbePtSDT.Fill( ak8JetsGoodPt[0], Weight )
                    h_topProbemmSDT.Fill( ak8JetsGoodMinMass[0], Weight )
                    h_topProbeak8mSDT.Fill( ak8JetsGoodMass[0], Weight )
                    h_topProbeSDmSDT.Fill( ak8JetsGoodSDropMass[0], Weight )  
                    h_topProbeTau32SDT.Fill( jet1tau32Val, Weight )
                    h_topProbePhiSDT.Fill( ak8JetsGoodPhi[0], Weight)
                    h_topProbeYSDT.Fill( ak8JetsGoodY[0], Weight)
                    if topTag0 :
                        NGoodAntiTagTopTagPairsSDT = NGoodAntiTagTopTagPairsSDT + 1
                        h_topTagPtSDT.Fill( ak8JetsGoodPt[0], Weight )
                if Tau32Cut1 :
                    NGoodAntiTaggedEventsNMT = NGoodAntiTaggedEventsNMT + 1
                    h_topProbePtNMT.Fill( ak8JetsGoodPt[0], Weight )
                    h_topProbemmNMT.Fill( ak8JetsGoodMinMass[0], Weight )
                    h_topProbeak8mNMT.Fill( ak8JetsGoodMass[0], Weight )
                    h_topProbeSDmNMT.Fill( ak8JetsGoodSDropMass[0], Weight )  
                    h_topProbeTau32NMT.Fill( jet1tau32Val, Weight )
                    h_topProbePhiNMT.Fill( ak8JetsGoodPhi[0], Weight)
                    h_topProbeYNMT.Fill( ak8JetsGoodY[0], Weight)
                    if topTag0 :
                        NGoodAntiTagTopTagPairsNMT = NGoodAntiTagTopTagPairsNMT + 1
                        h_topTagPtNMT.Fill( ak8JetsGoodPt[0], Weight )
                if AntiTag1FJ and Tau32Cut1 :
                    NGoodAntiTaggedEventsFJT = NGoodAntiTaggedEventsFJT + 1
                    h_topProbePtFJT.Fill( ak8JetsGoodPt[0], Weight )
                    h_topProbemmFJT.Fill( ak8JetsGoodMinMass[0], Weight )
                    h_topProbeak8mFJT.Fill( ak8JetsGoodMass[0], Weight )
                    h_topProbeSDmFJT.Fill( ak8JetsGoodSDropMass[0], Weight )  
                    h_topProbeTau32FJT.Fill( jet1tau32Val, Weight )
                    h_topProbePhiFJT.Fill( ak8JetsGoodPhi[0], Weight)
                    h_topProbeYFJT.Fill( ak8JetsGoodY[0], Weight)
                    if topTag0 :
                        NGoodAntiTagTopTagPairsFJT = NGoodAntiTagTopTagPairsFJT + 1
                        h_topTagPtFJT.Fill( ak8JetsGoodPt[0], Weight )
                if failMinMass1 :
                    h_testProbePt.Fill( ak8JetsGoodPt[0], Weight )
                    if topTag0 :
                        h_testTagPt.Fill( ak8JetsGoodPt[0], Weight )
                if failMinMassLow1 :
                    h_lowmMinProbePt.Fill( ak8JetsGoodPt[0], Weight )
                    if topTag0WP1:
                        h_lowmMinTagWP1Pt.Fill( ak8JetsGoodPt[0], Weight )
                    if topTag0WP2:
                        h_lowmMinTagWP2Pt.Fill( ak8JetsGoodPt[0], Weight )
                    if topTag0WP3:
                        h_lowmMinTagWP3Pt.Fill( ak8JetsGoodPt[0], Weight )
                    if topTag0WP4:
                        h_lowmMinTagWP4Pt.Fill( ak8JetsGoodPt[0], Weight )
                    if topTag0WP5:
                        h_lowmMinTagWP5Pt.Fill( ak8JetsGoodPt[0] , Weight )
                    if topTag0:
                        h_lowmMinTagPt.Fill( ak8JetsGoodPt[0] , Weight )
                        if not bTag1:
                            h_lowmMinBProbePt.Fill( ak8JetsGoodPt[0] , Weight )
                            if bTag0 :
                                h_lowmMinBTagPt.Fill( ak8JetsGoodPt[0] , Weight ) 
                    if bTag1 and bTag0:
                        h_lowmMin2BProbePt.Fill( ak8JetsGoodPt[0] , Weight )
                    if topTag0 and bTag0 and bTag1 :
                        h_lowmMin2BTagPt.Fill( ak8JetsGoodPt[0] , Weight )
                if topTag0 and topTag1 and not bTag1:
                    h_antiBProbePt.Fill( ak8JetsGoodPt[0] , Weight )
                    if bTag0:
                        h_antiBTagPt.Fill( ak8JetsGoodPt[0] , Weight ) 

print "======================"
print "~~~ Cut Flow Table ~~~"
print "======================"
print "Good AK8 Jets: " + str(NGoodAK8Jets)
print " "
print "Passing 2 Jets Cut: " + str(NPassDiJetCut)
print " "
print "Passing pt Cut (>350 GeV): " + str(NPassptCut)
print "Passing eta Cut (<2.4): " + str(NPassetaCut)
print "Passing \Delta \phi Cut (>2.1): " + str(NPassdPhiCut)
print "Passing pt, eta, and \Delta \phi Cut: " + str(NPassAllCuts)
print " "
print "~~~~ Soft Drop Mass req ~~~~"
print "Good AntiTagged Jets: " + str(NGoodAntiTaggedEventsSD)
print "Good AntiTag TopTag Jet Pairs: " + str(NGoodAntiTagTopTagPairsSD)
print "~~~~~~~ AK8 Mass req ~~~~~~~"
print "Good AntiTagged Jets: " + str(NGoodAntiTaggedEventsFJ)
print "Good AntiTag TopTag Jet Pairs: " + str(NGoodAntiTagTopTagPairsFJ)
print "~~~~~~~~ No Mass req ~~~~~~~"
print "Good AntiTagged Jets: " + str(NGoodAntiTaggedEventsNM)
print "Good AntiTag TopTag Jet Pairs: " + str(NGoodAntiTagTopTagPairsNM)
print " "
print "====== Tau32 > .7 Anti-tags ======="
print "~~~~ Soft Drop Mass req ~~~~"
print "Good AntiTagged Jets: " + str(NGoodAntiTaggedEventsSDT)
print "Good AntiTag TopTag Jet Pairs: " + str(NGoodAntiTagTopTagPairsSDT)
print "~~~~~~~ AK8 Mass req ~~~~~~~"
print "Good AntiTagged Jets: " + str(NGoodAntiTaggedEventsFJT)
print "Good AntiTag TopTag Jet Pairs: " + str(NGoodAntiTagTopTagPairsFJT)
print "~~~~~~~~ No Mass req ~~~~~~~"
print "Good AntiTagged Jets: " + str(NGoodAntiTaggedEventsNMT)
print "Good AntiTag TopTag Jet Pairs: " + str(NGoodAntiTagTopTagPairsNMT)
print " "
print "~~~~~~~~ No Anti-tag ~~~~~~~"
print "TopTag Jet Pairs: " + str(NGoodAntiTagTopTagPairsFree)
f.cd()
f.Write()
f.Close()
