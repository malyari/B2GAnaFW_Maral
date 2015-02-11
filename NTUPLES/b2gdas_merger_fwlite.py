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



#CLEANUP

f.cd()
f.Write()
f.Close()
