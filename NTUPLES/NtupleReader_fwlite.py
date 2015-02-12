#! /usr/bin/env python

#CONFIGURATION

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--files', type='string', action='store',
                  dest='files',
                  help='Input files')

parser.add_option('--outname', type='string', action='store',
                  default='outplots.root',
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

parser.add_option('--maxjets', type='int', action='store',
                  default=999,
                  dest='maxjets',
                  help='Number of jets to plot. To plot all jets, set to a big number like 999')


parser.add_option('--bdisc', type='string', action='store',
                  default='combinedInclusiveSecondaryVertexV2BJetTags',
                  dest='bdisc',
                  help='Name of output file')


parser.add_option('--bDiscMin', type='float', action='store',
                  default=0.679,
                  dest='bDiscMin',
                  help='Minimum b discriminator')

parser.add_option('--minMuonPt', type='float', action='store',
                  default=30.,
                  dest='minMuonPt',
                  help='Minimum PT for muons')

parser.add_option('--maxMuonEta', type='float', action='store',
                  default=2.1,
                  dest='maxMuonEta',
                  help='Maximum muon pseudorapidity')

parser.add_option('--minElectronPt', type='float', action='store',
                  default=30.,
                  dest='minElectronPt',
                  help='Minimum PT for electrons')

parser.add_option('--maxElectronEta', type='float', action='store',
                  default=2.5,
                  dest='maxElectronEta',
                  help='Maximum electron pseudorapidity')


parser.add_option('--minAK4Pt', type='float', action='store',
                  default=30.,
                  dest='minAK4Pt',
                  help='Minimum PT for AK4 jets')

parser.add_option('--maxAK4Rapidity', type='float', action='store',
                  default=2.4,
                  dest='maxAK4Rapidity',
                  help='Maximum AK4 rapidity')

parser.add_option('--minAK8Pt', type='float', action='store',
                  default=400.,
                  dest='minAK8Pt',
                  help='Minimum PT for AK8 jets')

parser.add_option('--maxAK8Rapidity', type='float', action='store',
                  default=2.4,
                  dest='maxAK8Rapidity',
                  help='Maximum AK8 rapidity')

(options, args) = parser.parse_args()
argv = []


#FWLITE STUFF

import ROOT
import sys
from DataFormats.FWLite import Events, Handle
ROOT.gROOT.Macro("rootlogon.C")
from leptonic_nu_z_component import solve_nu_tmass, solve_nu
import copy


#muon labels
h_muPt = Handle("std::vector<float>")
l_muPt = ("muons" , "muPt")
h_muEta = Handle("std::vector<float>")
l_muEta = ("muons" , "muEta")
h_muPhi = Handle("std::vector<float>")
l_muPhi = ("muons" , "muPhi")
h_muTight = Handle("std::vector<float>")
l_muTight = ("muons" , "muIsTightMuon" )
h_muLoose = Handle("std::vector<float>")
l_muLoose = ("muons" , "muIsLooseMuon" )
h_muMass = Handle("std::vector<float>")
l_muMass = ("muons" , "muMass")
h_muDz = Handle("std::vector<float>")
l_muDz = ("muons", "muDz")

#electron label and handles
h_elPt = Handle("std::vector<float>")
l_elPt = ("electrons" , "elPt")
h_elEta = Handle("std::vector<float>")
l_elEta = ("electrons" , "elEta")
h_elPhi = Handle("std::vector<float>")
l_elPhi = ("electrons" , "elPhi")
h_elTight = Handle("std::vector<float>")
l_elTight = ("electrons" , "elisTight" )
h_elLoose = Handle("std::vector<float>")
l_elLoose = ("electrons" , "elisLoose" )
h_eldEtaIn = Handle("std::vector<float>")
l_eldEtaIn = ( "electrons" , "eldEtaIn" )
h_eldPhiIn = Handle("std::vector<float>")
l_eldPhiIn = ( "electrons" , "eldPhiIn" )
h_elHoE = Handle("std::vector<float>")
l_elHoE = ( "electrons" , "elHoE" )
h_elfull5x5siee = Handle("std::vector<float>")
l_elfull5x5siee = ( "electrons" , "elfull5x5siee")
h_elE = Handle("std::vector<float>")
l_elE = ( "electrons" , "elE" )
h_elD0 = Handle("std::vector<float>")
l_elD0 = ( "electrons" , "elD0" )
h_elDz = Handle("std::vector<float>")
l_elDz = ( "electrons" , "elDz")
h_elIso03 = Handle("std::vector<float>")
l_elIso03 = ( "electrons" , "elIso03" )
h_elisVeto = Handle("std::vector<float>")
l_elisVeto = ( "electrons" , "elisVeto" )
h_elhasMatchedConVeto = Handle("std::vector<float>")
l_elhasMatchedConVeto = ( "electrons" , "elhasMatchedConVeto" )
h_elooEmooP = Handle("std::vector<float>")
l_elooEmooP = ( "electrons" , "elooEmooP" )
h_elMass = Handle("std::vector<float>")
l_elMass = ( "electrons" , "elMass" )
h_elscEta = Handle("std::vector<float>")
l_elscEta = ( "electrons" , "elscEta" )

#AK4 Jet Label and Handles
h_jetsAK4Pt = Handle("std::vector<float>")
l_jetsAK4Pt = ("jetsAK4" , "jetAK4Pt") #
h_jetsAK4Eta = Handle("std::vector<float>")
l_jetsAK4Eta = ("jetsAK4" , "jetAK4Eta")
h_jetsAK4Phi = Handle("std::vector<float>")
l_jetsAK4Phi = ("jetsAK4" , "jetAK4Phi")
h_jetsAK4Mass = Handle("std::vector<float>")
l_jetsAK4Mass = ("jetsAK4" , "jetAK4Mass")
h_jetsAK4Energy = Handle("std::vector<float>")
l_jetsAK4Energy = ("jetsAK4" , "jetAK4E") #check! is this energy?
h_jetsAK4JEC = Handle("std::vector<float>")
l_jetsAK4JEC = ("jetsAK4" , "jetAK4jecFactor0") 
h_jetsAK4CSV = Handle("std::vector<float>")
l_jetsAK4CSV = ("jetsAK4" , "jetAK4CSV")

h_jetsAK4nHadEnergyFrac = Handle("std::vector<float>")
l_jetsAK4nHadEnergyFrac = ("jetsAK4" , "jetAK4neutralHadronEnergy")
h_jetsAK4nEMEnergyFrac = Handle("std::vector<float>")
l_jetsAK4nEMEnergyFrac = ("jetsAK4" , "jetAK4neutralEmEnergy")
h_jetsAK4HFHadronEnergy = Handle("std::vector<float>")
l_jetsAK4HFHadronEnergy = ("jetsAK4" , "jetAK4HFHadronEnergy")
h_jetsAK4cEMEnergyFrac = Handle("std::vector<float>")
l_jetsAK4cEMEnergyFrac = ("jetsAK4" , "jetAK4chargedEmEnergy")
h_jetsAK4numDaughters = Handle("std::vector<float>")
l_jetsAK4numDaughters = ("jetsAK4" , "jetAK4numberOfDaughters")
h_jetsAK4cMultip = Handle("std::vector<float>")
l_jetsAK4cMultip = ("jetsAK4" , "jetAK4chargedMultiplicity")
h_jetsAK4Y = Handle("std::vector<float>")
l_jetsAK4Y = ("jetsAK4" , "jetAK4Y")

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
l_jetsAK8Energy = ("jetsAK8" , "jetAK8E") #check! is this energy?
h_jetsAK8JEC = Handle("std::vector<float>")
l_jetsAK8JEC = ("jetsAK8" , "jetAK8jecFactor0")
h_jetsAK8Y = Handle("std::vector<float>")
l_jetsAK8Y = ("jetsAK8" , "jetAK8Y")
#h_jetsAK8CSV = Handle("std::vector<float>")
#l_jetsAK8CSV = ("jetsAK8" , "jetAK8CSV")
#HISTOGRAMS

f = ROOT.TFile(options.outname, "RECREATE")
f.cd()

#Need to add these in


#JET CORRECTIONS

ROOT.gSystem.Load('libCondFormatsJetMETObjects')
#jecParStrAK4 = ROOT.std.string('JECs/PHYS14_25_V2_AK4PFchs.txt')
#jecUncAK4 = ROOT.JetCorrectionUncertainty( jecParStrAK4 )
#jecParStrAK8 = ROOT.std.string('JECs/PHYS14_25_V2_AK8PFchs.txt')
#jecUncAK8 = ROOT.JetCorrectionUncertainty( jecParStrAK8 )

print 'Getting L3 for AK4'
L3JetParAK4  = ROOT.JetCorrectorParameters("JECs/PHYS14_25_V2_L3Absolute_AK4PFchs.txt");
print 'Getting L2 for AK4'
L2JetParAK4  = ROOT.JetCorrectorParameters("JECs/PHYS14_25_V2_L2Relative_AK4PFchs.txt");
print 'Getting L1 for AK4'
L1JetParAK4  = ROOT.JetCorrectorParameters("JECs/PHYS14_25_V2_L1FastJet_AK4PFchs.txt");
# for data only :
#ResJetParAK4 = ROOT.JetCorrectorParameters("JECs/PHYS14_25_V2_L2L3Residual_AK4PFchs.txt");

print 'Getting L3 for AK8'
L3JetParAK8  = ROOT.JetCorrectorParameters("JECs/PHYS14_25_V2_L3Absolute_AK8PFchs.txt");
print 'Getting L2 for AK8'
L2JetParAK8  = ROOT.JetCorrectorParameters("JECs/PHYS14_25_V2_L2Relative_AK8PFchs.txt");
print 'Getting L1 for AK8'
L1JetParAK8  = ROOT.JetCorrectorParameters("JECs/PHYS14_25_V2_L1FastJet_AK8PFchs.txt");
# for data only :
#ResJetParAK8 = ROOT.JetCorrectorParameters("JECs/PHYS14_25_V2_L2L3Residual_AK8PFchs.txt"); 


#  Load the JetCorrectorParameter objects into a vector, IMPORTANT: THE ORDER MATTERS HERE !!!! 
vParJecAK4 = ROOT.vector('JetCorrectorParameters')()
vParJecAK4.push_back(L1JetParAK4)
vParJecAK4.push_back(L2JetParAK4)
vParJecAK4.push_back(L3JetParAK4)
# for data only :
#vParJecAK4.push_back(ResJetPar)

ak4JetCorrector = ROOT.FactorizedJetCorrector(vParJecAK4)

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
for ifile in filesraw :
    if len( ifile ) > 2 : 
        #s = 'root://cmsxrootd.fnal.gov/' + ifile.rstrip()
        s = ifile.rstrip()
        files.append( s )
        print 'Added ' + s


# loop over files
for ifile in files :
    print 'Processing file ' + ifile
    events = Events (ifile)
    if options.maxevents > 0 and nevents > options.maxevents :
        break

    # loop over events in this file
    i = 0
    for event in events:
        if options.maxevents > 0 and nevents > options.maxevents :
            break
        i += 1
        nevents += 1

        if nevents % 1000 == 0 : 
            print '    ---> Event ' + str(nevents)
        if options.verbose :
            print '==============================================='
            print '    ---> Event ' + str(nevents)

        #EVENT HANDLE FILLING

        event.getByLabel ( l_muPt, h_muPt )
        event.getByLabel ( l_muEta, h_muEta )
        event.getByLabel ( l_muPhi, h_muPhi )
        event.getByLabel ( l_muTight, h_muTight )
        event.getByLabel ( l_muLoose, h_muLoose )
        event.getByLabel ( l_muMass, h_muMass ) 
        event.getByLabel ( l_muDz, h_muDz )


        #Muon Selection

        goodmuonPt = []
        goodmuonEta = []
        goodmuonPhi = []
        goodmuonMass = []

        #Use MuPt as iterater due to no definite value in ntuples
        if len(h_muPt.product()) > 0:
            muonPt = h_muPt.product()
            muonEta = h_muEta.product()
            muonPhi = h_muPhi.product()
            muonTight = h_muTight.product()
            muonLoose = h_muLoose.product()
            muonMass = h_muMass.product()
            muonDz = h_muDz.product()
            for i in range(0,len(muonPt)):
                if muonPt[i] > options.minMuonPt and abs(muonEta[i]) < options.maxMuonEta and muonDz[i] < 5.0 and muonTight[i] :
                    goodmuonPt.append(muonPt[i])
                    goodmuonEta.append(muonEta[i])
                    goodmuonPhi.append(muonPhi[i])
                    goodmuonMass.append(muonMass[i])
                    if options.verbose :
                        print "muon %2d: pt %4.1f, eta %+5.3f phi %+5.3f dz(PV) %+5.3f, POG loose id %d, tight id %d." % ( i, muonPt[i], muonEta[i],
                                                                                                                muonPhi[i], muonDz[i], muonLoose[i], muonTight[i])

        #Electron Selection
        event.getByLabel ( l_elPt, h_elPt )
        event.getByLabel ( l_elEta, h_elEta )
        event.getByLabel ( l_elPhi, h_elPhi )
        event.getByLabel ( l_elTight, h_elTight )
        event.getByLabel ( l_elLoose, h_elLoose )
        event.getByLabel ( l_eldEtaIn, h_eldEtaIn )
        event.getByLabel ( l_eldPhiIn, h_eldPhiIn )
        event.getByLabel ( l_elHoE, h_elHoE )
        event.getByLabel ( l_elfull5x5siee, h_elfull5x5siee )
        event.getByLabel ( l_elE, h_elE )
        event.getByLabel ( l_elD0, h_elD0)
        event.getByLabel ( l_elDz, h_elDz)
        event.getByLabel ( l_elIso03, h_elIso03)
        event.getByLabel ( l_elhasMatchedConVeto, h_elhasMatchedConVeto)
        event.getByLabel ( l_elooEmooP, h_elooEmooP)
        event.getByLabel ( l_elMass, h_elMass )
        # event.getByLabel ( l_isotropy, h_isotropy)
        event.getByLabel ( l_elscEta , h_elscEta )
        
        
        goodelectronsPt = []
        goodelectronsEta = []
        goodelectronsPhi = []
        goodelectronsMass = []



        if len(h_elPt.product()) > 0:
            electronPt = h_elPt.product()
            electronEta = h_elEta.product()
            electronPhi = h_elPhi.product()
            electronTight = h_elTight.product()
            electronLoose = h_elLoose.product()
            electronecalEnergy = h_elE.product()
            electrondEtaIn = h_eldEtaIn.product()
            electrondPhiIn = h_eldPhiIn.product()
            electronHoE=h_elHoE.product()
            electronfullsiee=h_elfull5x5siee.product()
            electronooEmooP=h_elooEmooP.product()
            electronD0 = h_elD0.product()
            electronDz = h_elDz.product()
            #electroniso = h_isotropy.product()
            electronabsiso = h_elIso03.product()
            electronMass = h_elMass.product()
            electronscEta = h_elscEta.product()
            #h_eldEtaIn.
            passConversionVeto = h_elhasMatchedConVeto.product()
            #for i in xrange( len(electronPt.size() ) ) :
            if len(electronPt) > 0 :
                for i in range(0,len(electronPt)):
                    iePt = electronPt[i]   ### << access like this
                    ieEta = electronEta[i]
                    iePhi = electronPhi[i]
                    ieEtaIn = electrondEtaIn[i]
                    iePhiIn = electronPhi[i]
                    ietight = electronTight[i]
                    ieloose = electronLoose[i]
                    ieEcal = electronecalEnergy[i]
                    ieooEmooP = electronooEmooP[i]
                    ieD0 = electronD0[i]
                    ieDz = electronDz[i]
                    ieMass = electronMass[i]
                    pfIso = electronabsiso[i]
                    ielscEta = electronscEta[i]
                    #electronpfIso = h_elIso03.product()
            
                    #for i in range(0,len(electronPt)):
                
                
                    if iePt < iePt and abs(ieEta) < options.maxElectronEta :
                        continue
            
            
                    ieHoE = electronHoE[i]
                
                    iefull = electronfullsiee[i]
                
                    #ieabsiso = electronabsiso[i]
                
                    ieabsiso = abs(pfIso)
                
                    if abs(ieEcal) < 0.0 :
                        ieooEmooP = 1.0e30
                        
                    #absIso = electronabsiso[i]
                    #absIso = electronpfIso[i]
                    relIso = ieabsiso / iePt
                    iepass = passConversionVeto[i]
                                
                    goodElectron = False
                    # Barrel ECAL cuts
                    ####????????????     if abs(electron.superCluster().eta()) < 1.479 :
                    if abs(ielscEta) < 1.479 :
                        goodElectron = \
                          abs( ieEtaIn ) < 0.0091 and \
                          abs( iePhiIn ) < 0.031 and \
                          iefull < 0.0106 and \
                          ieHoE < 0.0532 and \
                          abs(ieD0) < 0.0126 and \
                          abs(ieDz) < 0.0116 and \
                          abs( ieooEmooP ) < 0.0609 and \
                          iepass
                                                                        
                                                                        
                    # Endcap ECAL cuts
                    elif abs(ielscEta) < 2.5 and abs(ielscEta) > 1.479 :
                                                                            
                        goodElectron = \
                          abs(  ieEtaIn  ) < 0.0106 and \
                          abs(iePhiIn) < 0.0359 and \
                          iefull < 0.0305 and \
                          ieHoE < 0.0835 and \
                          abs(ieD0) < 0.0163 and \
                          abs(ieDz) < .5999 and \
                          abs(ieooEmooP) < 0.1126 and \
                          iepass
                    
                    if goodElectron == True :
                        #goodelectronsPt.append( electronPt[i] )
                        goodelectronsPt.append( iePt )
                        #goodelectronsEta.append( electronEta[i] )
                        goodelectronsEta.append( ieEta )
                        goodelectronsPhi.append( iePhi )
                        goodelectronsMass.append( ieMass )
                        if options.verbose :
                            print "elec %2d: pt %4.1f, supercluster eta %+5.3f, phi %+5.3f sigmaIetaIeta %.3f (%.3f with full5x5 shower shapes), pass conv veto %d" % ( i, electronPt, electronSCeta, electronPhi, electron.sigmaIetaIeta(), full5x5_sigmaIetaIeta, passConversionVeto)
            
                
                    #h_ptLep.Fill(goodelectronsPt)
                    #h_etaLep.Fill(goodelectronsEta)
        if len(goodmuonPt) + len(goodelectronsPt) != 1 :
           continue
        elif len(goodmuonPt) > 0 :
            theLepton = ROOT.TLorentzVector( goodmuonPt[0],
                                             goodmuonEta[0],
                                             goodmuonPhi[0],
                                             goodmuonMass[0] )
            #Might Need Object Key
        else :
            theLepton = ROOT.TLorentzVector( goodelectronsPt[0],
                                             goodelectronsEta[0],
                                             goodelectronsPhi[0],
                                             goodelectronsMass[0] )

        event.getByLabel ( l_jetsAK4Pt, h_jetsAK4Pt )
        event.getByLabel ( l_jetsAK4Eta, h_jetsAK4Eta )
        event.getByLabel ( l_jetsAK4Phi, h_jetsAK4Phi )
        event.getByLabel ( l_jetsAK4Mass, h_jetsAK4Mass )
        event.getByLabel ( l_jetsAK4Energy, h_jetsAK4Energy )
        event.getByLabel ( l_jetsAK4JEC, h_jetsAK4JEC )
        event.getByLabel ( l_jetsAK4CSV, h_jetsAK4CSV )

        event.getByLabel ( l_jetsAK4nHadEnergyFrac, h_jetsAK4nHadEnergyFrac)
        event.getByLabel ( l_jetsAK4nEMEnergyFrac, h_jetsAK4nEMEnergyFrac )
        event.getByLabel ( l_jetsAK4HFHadronEnergy, h_jetsAK4HFHadronEnergy )
        event.getByLabel ( l_jetsAK4cEMEnergyFrac, h_jetsAK4cEMEnergyFrac )
        event.getByLabel ( l_jetsAK4numDaughters, h_jetsAK4numDaughters )
        event.getByLabel ( l_jetsAK4cMultip, h_jetsAK4cMultip )
        event.getByLabel ( l_jetsAK4Y, h_jetsAK4Y )

        event.getByLabel ( l_jetsAK8Eta, h_jetsAK8Eta )
        event.getByLabel ( l_jetsAK8Pt, h_jetsAK8Pt )
        event.getByLabel ( l_jetsAK8Phi, h_jetsAK8Phi )
        event.getByLabel ( l_jetsAK8Mass, h_jetsAK8Mass )
        event.getByLabel ( l_jetsAK8Energy, h_jetsAK8Energy )
        event.getByLabel ( l_jetsAK8JEC, h_jetsAK8JEC )
        event.getByLabel ( l_jetsAK8Y, h_jetsAK8Y )

        event.getByLabel ( l_metPt, h_metPt )
        event.getByLabel ( l_metPx, h_metPx )
        event.getByLabel ( l_metPy, h_metPy )
        event.getByLabel ( l_metPhi, h_metPhi )

        #!!!Skipped Rhos for now

        ijet = 0


        # These will hold all of the jets we need for the selection
        ak4JetsGoodPt = []
        ak8JetsGoodPt = []
        ak4JetsGoodP4Pt = []
        ak8JetsGoodP4Pt = []

        ak4JetsGoodEta = []
        ak8JetsGoodEta = []
        ak4JetsGoodP4Eta = []
        ak8JetsGoodP4Eta = []

        ak4JetsGoodPhi = []
        ak8JetsGoodPhi = []
        ak4JetsGoodP4Phi = []
        ak8JetsGoodP4Phi = []

        ak4JetsGoodMass = []
        ak8JetsGoodMass = []
        ak4JetsGoodP4Mass = []
        ak8JetsGoodP4Mass = []

        ak4JetsGoodEnergy = []
        ak8JetsGoodEnergy = []
        ak4JetsGoodP4Energy = []
        ak8JetsGoodP4Energy = []

        # For selecting leptons, look at 2-d cut of dRMin, ptRel of
        # lepton and nearest jet that has pt > 30 GeV
        dRMin = 9999.0
        inearestJet = -1    # Index of nearest jet
        nearestJet = None   # Nearest jet

        if len(h_jetsAK4Pt.product()) > 0:
            AK4Pt = h_jetsAK4Pt.product()
            AK4Eta = h_jetsAK4Eta.product()
            AK4Phi = h_jetsAK4Phi.product()
            AK4Mass = h_jetsAK4Mass.product()
            AK4Energy = h_jetsAK4Energy.product()
            AK4CSV = h_jetsAK4CSV.product()

            AK4JEC = h_jetsAK4JEC.product()
            AK4nHadEFrac = h_jetsAK4nHadEnergyFrac.product()
            AK4nEMEFrac = h_jetsAK4nEMEnergyFrac.product()
            AK4HFHadE = h_jetsAK4HFHadronEnergy.product()
            AK4cEMEFrac =  h_jetsAK4cEMEnergyFrac.product()
            AK4numDaughters = h_jetsAK4numDaughters.product()
            AK4cMultip =  h_jetsAK4cMultip.product()
            AK4Y =  h_jetsAK4Y.product()    

            AK8Pt = h_jetsAK8Pt.product()
            AK8Eta = h_jetsAK8Eta.product()
            AK8Phi = h_jetsAK8Phi.product()
            AK8Mass = h_jetsAK8Mass.product()
            AK8Energy = h_jetsAK8Energy.product()
            AK8Y = h_jetsAK8Y.product()

            AK8JEC = h_jetsAK8JEC.product()

            metPt = h_metPt.product()
            metPx = h_metPx.product()
            metPy = h_metPy.product()
            metPhi = h_metPhi.product()

        for i in range(0,len(AK4Pt)):
            #get the jets transverse energy, Eta, Phi and Mass ( essentially mom-energy 4 vector)
            #v = TLorentzVector()
            v = ROOT.TLorentzVector( AK4Pt[i], AK4Eta[i], AK4Phi[i], AK4Mass[i])

            # Get correction applied to B2G ntuples
            AK4JECFromB2GAnaFW = AK4JEC[i]
            
            # Remove the old JEC's to get raw energy
            v *= AK4JEC[i] #!!! I don't think this correction is right since v is not the mom-energy 4 vector
            RawAK4Energy = AK4Energy[i] * AK4JECFromB2GAnaFW
            
            jetP4 = v #!!! should be v * newJEC

            if jetP4[0] < options.minAK4Pt or abs(AK4Y[i]) > options.maxAK4Rapidity :
                continue
            dR = jetP4.DeltaR(theLepton ) #!!! This wasn't updated
            ak4JetsGoodPt.append(AK4Pt[i])
            ak4JetsGoodEta.append(AK4Eta[i])
            ak4JetsGoodPhi.append(AK4Phi[i])
            ak4JetsGoodMass.append(AK4Mass[i])
            ak4JetsGoodEnergy.append(AK4Energy[i])
            #ak4JetsGoodP4.append( jetP4 ) #!!! will use these after " new JEC " section of script is fixed
            if options.verbose :
                print 'corrjet pt = {0:6.2f}, y = {1:6.2f}, phi = {2:6.2f}, m = {3:6.2f}, bdisc = {4:6.2f}'.format (
                    jetP4[0], AK4Y[i], jetP4[2], jetP4[3], AK4CSV[i] )
            if dR < dRMin :
                inearestJet = ijet
                nearestJetPt = v[0]
                nearestJetEta = v[1]
                nearestJetPhi = v[2]
                nearestJetMass = v[3] 
                nearestJetRapidity = AK4Y[i]        
                nearestJetP4Pt = jetP4[0]
                nearestJetP4Eta = jetP4[1]
                nearestJetP4Phi = jetP4[2]
                nearestJetP4Mass = jetP4[3] 
                dRMin = dR
                nearestJetbDiscrim = AK4CSV[i]

        if nearestJetMass == None :
            continue
        LepJetUnoPt = nearestJetP4Pt 
        LepJetUnoEta = nearestJetP4Eta
        LepJetUnoPhi = nearestJetP4Phi 
        LepJetUnoMass = nearestJetP4Mass 
        LepJetUnoRapidity = nearestJetRapidity

        # Fill some plots related to the jets
   
        # Fill some plots related to the lepton, the MET, and the 2-d cut

        ptRel = 21.0 #theLepJet.Perp( theLepton.Vect() ) # not sure what to do here?
#        h_ptLep.Fill(theLeptonPt) # CREAtE THIS theLeptonPt and Eta ABOVE

        pass2D = ptRel > 20.0 or dRMin > 0.4
        if options.verbose : 
            print '2d cut : dRMin = {0:6.2f}, ptRel = {1:6.2}'.format( dRMin, ptRel )
        if pass2D == False :
            continue

        ############################################
        # Get the AK8 jet away from the lepton
        ############################################
        for i in range(0,len(AK8Pt)):

            #v8 = TLorentzVector()
            v8 = ROOT.TLorentzVector( AK8Pt[i], AK8Eta[i], AK8Phi[i], AK8Mass[i])
            
            AK8JECFromB2GAnaFW = AK8JEC[i]   
            #AK8P4Raw = TLorentzVector()
            AK8P4Raw = ROOT.TLorentzVector( AK8Pt[i] , AK8Eta[i], AK8Phi[i], AK8Mass[i])
      # Remove the old JEC's to get raw energy
            AK8P4Raw *= AK8JECFromB2GAnaFW # I don't think this correction is right since the vector is not the mom-energy 4 vector
         
            RawAK8Energy = AK8Energy[i] * AK8JECFromB2GAnaFW 
            

            if AK8P4Raw[0] < options.minAK8Pt or abs(AK8Y[i]) > options.maxAK8Rapidity :
                continue
            # Only keep AK8 jets "away" from the lepton, so we do not need
            # lepton-jet cleaning here. There's no double counting. 
            dR = jetP4.DeltaR(theLepton ) #!!! NOT sure how to change this, what is DeltaR?
            if dR > ROOT.TMath.Pi()/2.0 :
                ak8JetsGoodPt.append(v8[0])
                ak8JetsGoodP4Pt.append( AK8P4Raw[0] )
                ak8JetsGoodEta.append(v8[1])
                ak8JetsGoodP4Eta.append( AK8P4Raw[0] )
                ak8JetsGoodPhi.append(v8[2])
                ak8JetsGoodP4Phi.append( AK8P4Raw[0] )
                ak8JetsGoodMass.append(v8[3])
                ak8JetsGoodP4Mass.append(AK8P4Raw[0] )
                ak8JetsGoodRapidity.append(AK8Y[i] )

        #Tagging
        if len(ak4JetsGoodP4Mass) < 1 or len(ak8JetsGoodP4Mass) < 1 :
            continue

            
        nttags = 0

        tJetsPt = []
        tJetsEta = []
        tJetsPhi = []
        tJetsMass = []
        for i in range(0,len(ak8JetsGoodPt)):
            if ak8JetsGoodP4Pt[i] < options.minAK8Pt :
                continue

            mAK8Pruned = 10.0 #AK8PrunedM[i] # "jetsAK8" "jetAK8prunedMass" CREATE THESE ABOVE
            mAK8Filtered = 10.0 #AK8FilteredM[i] #"jetsAK8" "jetAK8filteredMass"
            mAK8Trimmed = 11.0 #AK8TrimmedM[i]#"jetsAK8" "jetAK8trimmedMass"
            # Make sure there are top tags if we want to plot them
            minMass = -1.0
            nsubjets = -1 
            tau1 = 5.0# AK8tau1[i]  #!!! MUST CREATE TAU ARRAYS ABOVE, APEAR HERE FIRST TIME IN SCRIPT
            tau2 = 3.0 #AK8tau2[i] 
            tau3 = 2.0 #AK8tau3[i]
            
            if options.verbose : 
                print 'minMass = {0:6.2f}, trimmed mass = {1:6.2f}, tau32 = {2:6.2f}'.format(
                    minMass, mAK8Trimmed, tau32
                    ), 
            if minMass > options.minMassCut and mAK8Trimmed > options.mAK8TrimmedCut and tau32 > options.tau32Cut :
                nttags += 1
                tJetsPt.append(ak8JetsGoodP4Pt[i]  )
                tJetsEta.append( ak8JetsGoodP4Eta[i] )
                tJetsPhi.append( ak8JetsGoodP4Phi[i] )
                tJetsMass.append(ak8JetsGoodP4Mass[i]  )
                tJetsRapidity.append(ak8JetsGoodRapidity[i]  )

                if options.verbose : 
                    print ' --->Tagged jet!'
            else :
                if options.verbose : 
                    print ''

        #KINEMATICS
        if nttags == 0 :
            if options.verbose : 
                print 'No top tags'
        else :

            
            hadTopCandP4 = TLorentzVector()
            hadTopCandP4.SetPtEtaPhiM( tJetsPt[i], tJetsEta[i], tJetsPhi[i], tJetsMass[i])
            
            lepTopCandP4 = None
            
            # Check if the nearest jet to the lepton is b-tagged
            if theLepJetBDisc < options.bDiscMin :
                if options.verbose : 
                    print 'closest jet to lepton is not b-tagged'
            else  :

                if options.verbose :
                    print 'Event is fully tagged.'
                # Get the z-component of the lepton from the W mass constraint
                #bJetCandP4 = TLorentzVector()
                bJetCandP4 = ROOT.TLorentzVector(ak4JetsGoodP4Pt[inearestJet],ak4JetsGoodP4Eta[inearestJet], ak4JetsGoodP4Phi[inearestJet], ak4JetsGoodP4Mass[inearestJet])
                #nuCandP4 = TLorentzVector()
                nuCandP4 = ROOT.TLorentzVector(metPx[i], metPy[i] ,0.0, metEnergy[i])

                solution, nuz1, nuz2 = solve_nu( vlep=theLepton, vnu=nuCandP4 )
                # If there is at least one real solution, pick it up
                if solution :
                    if options.verbose : 
                        print '--- Have a solution --- '
                    nuCandP4[2] = nuz1
                else :
                    if options.verbose : 
                        print '--- No solution for neutrino z ---'
                    nuCandP4[2] = nuz1.real 

                lepTopCandP4 = nuCandP4 + theLepton + bJetCandP4 # be sure theLepton is also a TLorentzVector and that this is a valid command

                ttbarCandMass = hadTopCandP4[3] + lepTopCandP4[3]
                
                if haveGenSolution == False :
                    print 'Very strange. No gen solution, but it is a perfectly good event. mttbar = ' + str(ttbarCandMass )
        

#CLEANUP

f.cd()
f.Write()
f.Close()
