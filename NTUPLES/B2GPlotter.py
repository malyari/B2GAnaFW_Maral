#!/usr/bin/env python
from optparse import OptionParser
parser = OptionParser()

parser.add_option('--stage', type='string', action='store',
                  dest='stage',
                  default = None,
                  help='Stage of selection; semiLeptonic, allHadronic')

parser.add_option('--hmax', type='float', action='store',
                  dest='hmax',
                  default = None,
                  help='Histogram y max')
(options, args) = parser.parse_args()
argv = []

import ROOT

ROOT.gStyle.SetOptStat(000000)
ROOT.gROOT.Macro("rootlogon.C")
ROOT.gStyle.SetTitleOffset(1.0, "Y")
ROOT.gStyle.SetTitleSize(0.045, "X")
HNAME_NDX = 0
HTITLE_NDX = 1
HMAX_NDX = 2
HXMIN_NDX = 3
HXMAX_NDX = 4
LEGXMIN_NDX = 5
LEGYMIN_NDX = 6
LEGXMAX_NDX = 7
LEGYMAX_NDX = 8
if options.stage == "semiLeptonic" :
    hists = [
        # Name                  Title                                          Max, Xmin , Xmax  , Legend location 
        ['h_ptLep',            ';p_{T}(GeV) of Lepton;Number of Events',       500., 0.  , 1000. , 0.6, 0.6, 0.85, 0.85],
        ['h_etaLep',           ';y of Lepton;Number of Events',                500., -3. , 3.    , 0.6, 0.6, 0.85, 0.85],
        ['h_met',              ';MET(GeV);Number of Events',                   500., 0.  , 1000. , 0.6, 0.6, 0.85, 0.85],
        ['h_dRMin',            ';dRMin;Number of Events',                      500., 0.  , 5.    , 0.6, 0.6, 0.85, 0.85],
        ['h_ptAK4',            ';p_{T}(GeV) of AK4 Jet;Number of Events',      20. , 0.  , 1500. , 0.6, 0.6, 0.85, 0.85],
        ['h_etaAK4',           ';y of AK4 Jet;Number of Events',               20. , -3. , 3.    , 0.6, 0.6, 0.85, 0.85],
        ['h_mAK4',             ';Mass(GeV) of AK4 Jet;Number of Events',       60. , 10. , 300.  , 0.6, 0.6, 0.85, 0.85],
        ['h_bdiscAK4',         ';b discriminator of AK4 Jet;Number of Events', 20. , 0.  , 1.0   , 0.6, 0.6, 0.85, 0.85],
        ['h_ptAK8',            ';p_{T}(GeV) of AK8 Jet;Number of Events',      30. , 400., 1500. , 0.6, 0.6, 0.85, 0.85],
        ['h_etaAK8',           ';y of AK8 Jet;Number of Events',               20. , -3. , 3.    , 0.6, 0.6, 0.85, 0.85],
        ['h_mAK8',             ';Mass(GeV) of AK8 Jet;Number of Events',       40. , 20. , 300.  , 0.6, 0.6, 0.85, 0.85],
        ['h_mprunedAK8',       ';Pruned Mass (GeV);Number of Events',          40. , 20. , 300.  , 0.6, 0.6, 0.85, 0.85],
        ['h_mfilteredAK8',     ';Filtered Mass (GeV);Number of Events',        40. , 20. , 300.  , 0.6, 0.6, 0.85, 0.85],
        ['h_mtrimmedAK8',      ';Trimmed Mass (GeV);Number of Events',         40. , 20. , 300.  , 0.6, 0.6, 0.85, 0.85],
        ['h_mSDropAK8',        ';Soft Drop Mass (GeV);Number of Events',       40. , 20. , 300.  , 0.6, 0.6, 0.85, 0.85],
        ['h_nsjAK8',           ';Number of Subjets;Number of Events',         100. , 0.  , 5.    , 0.6, 0.6, 0.85, 0.85],
        ['h_tau21AK8',         ';#tau_{21};Number of Events',                  20. , 0.  , 1.    , 0.6, 0.6, 0.85, 0.85],
        ['h_tau32AK8',         ';#tau_{32};Number of Events',                  20. , 0.  , 1.    , 0.6, 0.6, 0.85, 0.85],
        ['h_nhfAK8',           ';Neutral hadron fraction;Number of Events',    20. , 0.  , 1.    , 0.6, 0.6, 0.85, 0.85],
        ['h_chfAK8',           ';Charged hadron fraction;Number of Events',    20. , 0.  , 1.    , 0.6, 0.6, 0.85, 0.85],
        ['h_nefAK8',           ';Neutral EM fraction;Number of Events',        20. , 0.  , 1.    , 0.6, 0.6, 0.85, 0.85],
        ['h_cefAK8',           ';Charged EM fraction;Number of Events',        20. , 0.  , 1.    , 0.6, 0.6, 0.85, 0.85],
]
if options.stage == "allHadronic" :
    hists = [
        # Name                                   Title                         Max,  Xmin , Xmax  , Legend location 
        ['h_Jet0_MassSoft_CorrNone' ,           ';h_Jet0_MassSoft_CorrNone',  6200,  0,     500   , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet0_MassTrim_CorrNone' ,           ';h_Jet0_MassTrim_CorrNone',  2000,  0,     500   , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet0_MassFilt_CorrNone' ,           ';h_Jet0_MassFilt_CorrNone',  2000,  0,     500   , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet0_MassPrun_CorrNone' ,           ';h_Jet0_MassPrun_CorrNone',  3200,  0,     500   , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet0_MinCMSTT_CorrNone' ,           ';h_Jet0_MinCMSTT_CorrNone',   600,  0,     500   , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet0_MassSoft_CorrL2L3' ,           ';h_Jet0_MassSoft_CorrL2L3',  3200,  0,     500   , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet0_MassTrim_CorrL2L3' ,           ';h_Jet0_MassTrim_CorrL2L3',  2000,  0,     500   , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet0_MassFilt_CorrL2L3' ,           ';h_Jet0_MassFilt_CorrL2L3',  2000,  0,     500   , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet0_MassPrun_CorrL2L3' ,           ';h_Jet0_MassPrun_CorrL2L3',  3200,  0,     500   , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet0_MinCMSTT_CorrL2L3' ,           ';h_Jet0_MinCMSTT_CorrL2L3',   600,  0,     500   , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet0_Tau1'              ,           ';h_Jet0_Tau1'             ,  2200,  0,       1   , 0.7, 0.6, 0.85, 0.85],             
        ['h_Jet0_Tau2'              ,           ';h_Jet0_Tau2'             ,  3200,  0,       1   , 0.7, 0.6, 0.85, 0.85],             
        ['h_Jet0_Tau3'              ,           ';h_Jet0_Tau3'             ,  4000,  0,       1   , 0.7, 0.6, 0.85, 0.85],             
        ['h_Jet0_Tau21'             ,           ';h_Jet0_Tau21'            ,  1400,  0,       1   , 0.2, 0.6, 0.35, 0.85],             
        ['h_Jet0_Tau32'             ,           ';h_Jet0_Tau32'            ,  2400,  0,       1   , 0.2, 0.6, 0.35, 0.85],             
        ['h_Jet0_Pt'                ,           ';h_Jet0_Pt'               ,  6200,  0,    7000   , 0.7, 0.6, 0.85, 0.85],             
        ['h_Jet0_Rap'               ,           ';h_Jet0_Rap'              ,  1200, -3,       3   , 0.7, 0.6, 0.85, 0.85],             
        ['h_Jet0_NHF'               ,           ';h_Jet0_NHF'              ,   500,  0,     500   , 0.7, 0.6, 0.85, 0.85],
        ['h_Jet0_CHF'               ,           ';h_Jet0_CHF'              ,   500,  0,     500   , 0.7, 0.6, 0.85, 0.85],
        ['h_Jet0_NEF'               ,           ';h_Jet0_NEF'              ,   500,  0,     500   , 0.7, 0.6, 0.85, 0.85],
        ['h_Jet0_CEF'               ,           ';h_Jet0_CEF'              ,   500,  0,     500   , 0.7, 0.6, 0.85, 0.85],
        ['h_Jet0_NC'                ,           ';h_Jet0_NC'               ,  6200,  0,     500   , 0.7, 0.6, 0.85, 0.85],
        ['h_Jet0_NCH'               ,           ';h_Jet0_NCH'              ,  4000,  0,     500   , 0.7, 0.6, 0.85, 0.85],

        ['h_Jet0_MassSoft_CorrOrigSumSubjet',   ';h_Jet0_MassSoft_CorrOrigSumSubjet' ,  6200,  0,  500 , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet0_MassSoft_RawSumSubjet'     ,   ';h_Jet0_MassSoft_RawSumSubjet'      ,  6200,  0,  500 , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet0_MassSoft_CorrNewSumSubjet' ,   ';h_Jet0_MassSoft_CorrNewSumSubjet'  ,  6200,  0,  500 , 0.7, 0.6, 0.85, 0.85], 

        ['h_Jet1_MassSoft_CorrNone'   ,         ';h_Jet1_MassSoft_CorrNone',  6200,  0,  500 , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet1_MassTrim_CorrNone'   ,         ';h_Jet1_MassTrim_CorrNone',  2000,  0,  500 , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet1_MassFilt_CorrNone'   ,         ';h_Jet1_MassFilt_CorrNone',  2000,  0,  500 , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet1_MassPrun_CorrNone'   ,         ';h_Jet1_MassPrun_CorrNone',  3200,  0,  500 , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet1_MinCMSTT_CorrNone'   ,         ';h_Jet1_MinCMSTT_CorrNone',   600,  0,  500 , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet1_MassSoft_CorrL2L3'   ,         ';h_Jet1_MassSoft_CorrL2L3',  3200,  0,  500 , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet1_MassTrim_CorrL2L3'   ,         ';h_Jet1_MassTrim_CorrL2L3',  2000,  0,  500 , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet1_MassFilt_CorrL2L3'   ,         ';h_Jet1_MassFilt_CorrL2L3',  2000,  0,  500 , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet1_MassPrun_CorrL2L3'   ,         ';h_Jet1_MassPrun_CorrL2L3',  3200,  0,  500 , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet1_MinCMSTT_CorrL2L3'   ,         ';h_Jet1_MinCMSTT_CorrL2L3',   600,  0,  500 , 0.7, 0.6, 0.85, 0.85], 
        ['h_Jet1_Tau1'                ,         ';h_Jet1_Tau1'             ,  2200,  0,    1 , 0.7, 0.6, 0.85, 0.85],             
        ['h_Jet1_Tau2'                ,         ';h_Jet1_Tau2'             ,  3200,  0,    1 , 0.7, 0.6, 0.85, 0.85],             
        ['h_Jet1_Tau3'                ,         ';h_Jet1_Tau3'             ,  4000,  0,    1 , 0.7, 0.6, 0.85, 0.85],             
        ['h_Jet1_Tau21'               ,         ';h_Jet1_Tau21'            ,  1400,  0,    1 , 0.2, 0.6, 0.35, 0.85],             
        ['h_Jet1_Tau32'               ,         ';h_Jet1_Tau32'            ,  2400,  0,    1 , 0.2, 0.6, 0.35, 0.85],             
        ['h_Jet1_Pt'                  ,         ';h_Jet1_Pt'               ,  6200,  0, 7000 , 0.7, 0.6, 0.85, 0.85],             
        ['h_Jet1_Rap'                 ,         ';h_Jet1_Rap'              ,  1200, -3,    3 , 0.7, 0.6, 0.85, 0.85],             
        ['h_Jet1_NHF'                 ,         ';h_Jet1_NHF'              ,   500,  0,  500 , 0.7, 0.6, 0.85, 0.85],
        ['h_Jet1_CHF'                 ,         ';h_Jet1_CHF'              ,   500,  0,  500 , 0.7, 0.6, 0.85, 0.85],
        ['h_Jet1_NEF'                 ,         ';h_Jet1_NEF'              ,   500,  0,  500 , 0.7, 0.6, 0.85, 0.85],
        ['h_Jet1_CEF'                 ,         ';h_Jet1_CEF'              ,   500,  0,  500 , 0.7, 0.6, 0.85, 0.85],
        ['h_Jet1_NC'                  ,         ';h_Jet1_NC'               ,  6200,  0,  500 , 0.7, 0.6, 0.85, 0.85],
        ['h_Jet1_NCH'                 ,         ';h_Jet1_NCH'              ,  4000,  0,  500 , 0.7, 0.6, 0.85, 0.85],


        #^ Make modMass hist with small binning
        ['h_mAK8_ModMass'             ,           ';h_mAK8_ModMass'               , 500,   140,  250 , 0.7, 0.6, 0.85, 0.85],
        ['h_mSDropAK8_ModMass'        ,           ';h_mSDropAK8_ModMass'          , 200,   110,  210 , 0.7, 0.6, 0.85, 0.85],
        ['h_mAK8_ModMass_jet0'        ,           ';h_mAK8_ModMass_jet0'          , 220,   140,  250 , 0.7, 0.6, 0.85, 0.85],
        ['h_mSDropAK8_ModMass_jet0'   ,           ';h_mSDropAK8_ModMass_jet0'     , 100,   110,  210 , 0.7, 0.6, 0.85, 0.85],
        ['h_mAK8_ModMass_jet1'        ,           ';h_mAK8_ModMass_jet1'          , 220,   140,  250 , 0.7, 0.6, 0.85, 0.85],
        ['h_mSDropAK8_ModMass_jet1'   ,           ';h_mSDropAK8_ModMass_jet1'     , 150,   110,  210 , 0.7, 0.6, 0.85, 0.85],


        #^ Make mistag plots
        ['h_AntiTagNone_ReqTopMassSD_Probe_jetPt'                   ,           ';h_AntiTagNone_ReqTopMassSD_Probe_jetPt'                  ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagNone_ReqTopMassSD_TagMassSD_jetPt'               ,           ';h_AntiTagNone_ReqTopMassSD_TagMassSD_jetPt'              ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagNone_ReqTopMassSD_TagMassSDTau32_jetPt'          ,           ';h_AntiTagNone_ReqTopMassSD_TagMassSDTau32_jetPt'         ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagNone_ReqTopMassSD_TagMassSDMinMass_jetPt'        ,           ';h_AntiTagNone_ReqTopMassSD_TagMassSDMinMass_jetPt'       ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagNone_ReqTopMassSD_TagMassFat_jetPt'              ,           ';h_AntiTagNone_ReqTopMassSD_TagMassFat_jetPt'             ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagNone_ReqTopMassSD_TagMassFatMinMass_jetPt'       ,           ';h_AntiTagNone_ReqTopMassSD_TagMassFatMinMass_jetPt'      ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
     
        ['h_AntiTagNone_ReqTopMassFat_Probe_jetPt'                  ,           ';h_AntiTagNone_ReqTopMassFat_Probe_jetPt'                  ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagNone_ReqTopMassFat_TagMassSD_jetPt'              ,           ';h_AntiTagNone_ReqTopMassFat_TagMassSD_jetPt'              ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagNone_ReqTopMassFat_TagMassSDTau32_jetPt'         ,           ';h_AntiTagNone_ReqTopMassFat_TagMassSDTau32_jetPt'         ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagNone_ReqTopMassFat_TagMassSDMinMass_jetPt'       ,           ';h_AntiTagNone_ReqTopMassFat_TagMassSDMinMass_jetPt'       ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagNone_ReqTopMassFat_TagMassFat_jetPt'             ,           ';h_AntiTagNone_ReqTopMassFat_TagMassFat_jetPt'             ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagNone_ReqTopMassFat_TagMassFatMinMass_jetPt'      ,           ';h_AntiTagNone_ReqTopMassFat_TagMassFatMinMass_jetPt'      ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 


        ['h_AntiTagMinMass30_ReqTopMassSD_Probe_jetPt'              ,           ';h_AntiTagMinMass30_ReqTopMassSD_Probe_jetPt'              ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass30_ReqTopMassSD_TagMassSD_jetPt'          ,           ';h_AntiTagMinMass30_ReqTopMassSD_TagMassSD_jetPt'          ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass30_ReqTopMassSD_TagMassSDTau32_jetPt'     ,           ';h_AntiTagMinMass30_ReqTopMassSD_TagMassSDTau32_jetPt'     ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass30_ReqTopMassSD_TagMassSDMinMass_jetPt'   ,           ';h_AntiTagMinMass30_ReqTopMassSD_TagMassSDMinMass_jetPt'   ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass30_ReqTopMassSD_TagMassFat_jetPt'         ,           ';h_AntiTagMinMass30_ReqTopMassSD_TagMassFat_jetPt'         ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass30_ReqTopMassSD_TagMassFatMinMass_jetPt'  ,           ';h_AntiTagMinMass30_ReqTopMassSD_TagMassFatMinMass_jetPt'  ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 

        ['h_AntiTagMinMass30_ReqTopMassFat_Probe_jetPt'             ,           ';h_AntiTagMinMass30_ReqTopMassFat_Probe_jetPt'             ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass30_ReqTopMassFat_TagMassSD_jetPt'         ,           ';h_AntiTagMinMass30_ReqTopMassFat_TagMassSD_jetPt'         ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass30_ReqTopMassFat_TagMassSDTau32_jetPt'    ,           ';h_AntiTagMinMass30_ReqTopMassFat_TagMassSDTau32_jetPt'    ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass30_ReqTopMassFat_TagMassSDMinMass_jetPt'  ,           ';h_AntiTagMinMass30_ReqTopMassFat_TagMassSDMinMass_jetPt'  ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass30_ReqTopMassFat_TagMassFat_jetPt'        ,           ';h_AntiTagMinMass30_ReqTopMassFat_TagMassFat_jetPt'        ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass30_ReqTopMassFat_TagMassFatMinMass_jetPt' ,           ';h_AntiTagMinMass30_ReqTopMassFat_TagMassFatMinMass_jetPt' ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 

 
        ['h_AntiTagMinMass50_ReqTopMassSD_Probe_jetPt'              ,           ';h_AntiTagMinMass50_ReqTopMassSD_Probe_jetPt'              ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass50_ReqTopMassSD_TagMassSD_jetPt'          ,           ';h_AntiTagMinMass50_ReqTopMassSD_TagMassSD_jetPt'          ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass50_ReqTopMassSD_TagMassSDTau32_jetPt'     ,           ';h_AntiTagMinMass50_ReqTopMassSD_TagMassSDTau32_jetPt'     ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass50_ReqTopMassSD_TagMassSDMinMass_jetPt'   ,           ';h_AntiTagMinMass50_ReqTopMassSD_TagMassSDMinMass_jetPt'   ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass50_ReqTopMassSD_TagMassFat_jetPt'         ,           ';h_AntiTagMinMass50_ReqTopMassSD_TagMassFat_jetPt'         ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass50_ReqTopMassSD_TagMassFatMinMass_jetPt'  ,           ';h_AntiTagMinMass50_ReqTopMassSD_TagMassFatMinMass_jetPt'  ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 

        ['h_AntiTagMinMass50_ReqTopMassFat_Probe_jetPt'             ,           ';h_AntiTagMinMass50_ReqTopMassFat_Probe_jetPt'             ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass50_ReqTopMassFat_TagMassSD_jetPt'         ,           ';h_AntiTagMinMass50_ReqTopMassFat_TagMassSD_jetPt'         ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass50_ReqTopMassFat_TagMassSDTau32_jetPt'    ,           ';h_AntiTagMinMass50_ReqTopMassFat_TagMassSDTau32_jetPt'    ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass50_ReqTopMassFat_TagMassSDMinMass_jetPt'  ,           ';h_AntiTagMinMass50_ReqTopMassFat_TagMassSDMinMass_jetPt'  ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass50_ReqTopMassFat_TagMassFat_jetPt'        ,           ';h_AntiTagMinMass50_ReqTopMassFat_TagMassFat_jetPt'        ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagMinMass50_ReqTopMassFat_TagMassFatMinMass_jetPt' ,           ';h_AntiTagMinMass50_ReqTopMassFat_TagMassFatMinMass_jetPt' ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 


        ['h_AntiTagTau32_ReqTopMassSD_Probe_jetPt'                  ,           ';h_AntiTagTau32_ReqTopMassSD_Probe_jetPt'                 ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagTau32_ReqTopMassSD_TagMassSD_jetPt'              ,           ';h_AntiTagTau32_ReqTopMassSD_TagMassSD_jetPt'             ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagTau32_ReqTopMassSD_TagMassSDTau32_jetPt'         ,           ';h_AntiTagTau32_ReqTopMassSD_TagMassSDTau32_jetPt'        ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagTau32_ReqTopMassSD_TagMassSDMinMass_jetPt'       ,           ';h_AntiTagTau32_ReqTopMassSD_TagMassSDMinMass_jetPt'      ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagTau32_ReqTopMassSD_TagMassFat_jetPt'             ,           ';h_AntiTagTau32_ReqTopMassSD_TagMassFat_jetPt'            ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagTau32_ReqTopMassSD_TagMassFatMinMass_jetPt'      ,           ';h_AntiTagTau32_ReqTopMassSD_TagMassFatMinMass_jetPt'     ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
    
        ['h_AntiTagTau32_ReqTopMassFat_Probe_jetPt'                 ,           ';h_AntiTagTau32_ReqTopMassFat_Probe_jetPt'                ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagTau32_ReqTopMassFat_TagMassSD_jetPt'             ,           ';h_AntiTagTau32_ReqTopMassFat_TagMassSD_jetPt'            ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagTau32_ReqTopMassFat_TagMassSDTau32_jetPt'        ,           ';h_AntiTagTau32_ReqTopMassFat_TagMassSDTau32_jetPt'       ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagTau32_ReqTopMassFat_TagMassSDMinMass_jetPt'      ,           ';h_AntiTagTau32_ReqTopMassFat_TagMassSDMinMass_jetPt'     ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagTau32_ReqTopMassFat_TagMassFat_jetPt'            ,           ';h_AntiTagTau32_ReqTopMassFat_TagMassFat_jetPt'           ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 
        ['h_AntiTagTau32_ReqTopMassFat_TagMassFatMinMass_jetPt'     ,           ';h_AntiTagTau32_ReqTopMassFat_TagMassFatMinMass_jetPt'    ,  1400, 0, 7000 , 0.7, 0.6, 0.85, 0.85], 


        #^ Hadronic mtt selection and background estimaion
        ['h_mttMass_tagMassSD'                      ,           ';h_mttMass_tagMassSD'                     ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],
        ['h_mttMass_tagMassSDTau32'                 ,           ';h_mttMass_tagMassSDTau32'                ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],
        ['h_mttMass_tagMassSDMinMass'               ,           ';h_mttMass_tagMassSDMinMass'              ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],
        ['h_mttMass_tagMassFat'                     ,           ';h_mttMass_tagMassFat'                    ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],
        ['h_mttMass_tagMassFatMinMass'              ,           ';h_mttMass_tagMassFatMinMass'             ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],

        ['h_bkgdEst_tagMassSD'                      ,           ';h_bkgdEst_tagMassSD'                     ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],
        ['h_bkgdEst_tagMassSDTau32'                 ,           ';h_bkgdEst_tagMassSDTau32'                ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],
        ['h_bkgdEst_tagMassSDMinMass'               ,           ';h_bkgdEst_tagMassSDMinMass'              ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],
        ['h_bkgdEst_tagMassFat'                     ,           ';h_bkgdEst_tagMassFat'                    ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],
        ['h_bkgdEst_tagMassFatMinMass'              ,           ';h_bkgdEst_tagMassFatMinMass'             ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],

        ['h_bkgdEst_modMass_tagMassSD'              ,           ';h_bkgdEst_modMass_tagMassSD'             ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],
        ['h_bkgdEst_modMass_tagMassSDTau32'         ,           ';h_bkgdEst_modMass_tagMassSDTau32'        ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],
        ['h_bkgdEst_modMass_tagMassSDMinMass'       ,           ';h_bkgdEst_modMass_tagMassSDMinMass'      ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],
        ['h_bkgdEst_modMass_tagMassFat'             ,           ';h_bkgdEst_modMass_tagMassFat'            ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],
        ['h_bkgdEst_modMass_tagMassFatMinMass'      ,           ';h_bkgdEst_modMass_tagMassFatMinMass'     ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],

        ['h_bkgdEst_modMass_flat_tagMassSD'         ,           ';h_bkgdEst_modMass_flat_tagMassSD'        ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],
        ['h_bkgdEst_modMass_flat_tagMassSDTau32'    ,           ';h_bkgdEst_modMass_flat_tagMassSDTau32'   ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],
        ['h_bkgdEst_modMass_flat_tagMassSDMinMass'  ,           ';h_bkgdEst_modMass_flat_tagMassSDMinMass' ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],
        ['h_bkgdEst_modMass_flat_tagMassFat'        ,           ';h_bkgdEst_modMass_flat_tagMassFat'       ,  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85],
        ['h_bkgdEst_modMass_flat_tagMassFatMinMass' ,           ';h_bkgdEst_modMass_flat_tagMassFatMinMass',  100, 0, 7000 , 0.7, 0.6, 0.85, 0.85]
    ]



#if options.stage != None :
#    for ihist in hists :
#        ihist[HNAME_NDX] += '_' + options.stage
#        print 'Getting histogram : ' + ihist[HNAME_NDX]

FILE_NDX = 0
NAME_NDX = 1
TITLE_NDX = 2
SCALE_NDX = 3
COLOR_NDX = 4
lumi = 153.3

if options.stage == "semiLeptonic" :
    print "Getting the Samples for semiLeptonic"
    samples = [
        ["ttjets_b2ganafw_v5_sel1_synced.root",             'ttbar',  't#bar{t}',          831.76 * lumi / 19665194., ROOT.kRed + 1],
        ["wjets_b2ganafw_v5_sel1_synced.root",              'wjets',  'W + Jets',         20508.9 * lumi / 24089991., ROOT.kGreen + 1 ],
        ["singletop_v74x_v4.3_tchan_local_sel1_synced.root",'st',     'Single Top Quark',  216.99 * lumi / 3999910.,  ROOT.kMagenta + 1 ],
        ["zjets_b2ganafw_v4_sel1_synced.root",              'zjets',  'Z + Jets',          2008.4 * lumi / 19925500., ROOT.kBlue - 4 ], 
        ["singlemu_v74x_v5_sel1_synced.root",                  'mudata', 'Data',              1.0,                       0 ],
        ["singleel_v74x_v5_sel1_synced.root",                  'eldata', 'Data',              1.0,                       0  ],
    ]
    print "Got the Samples for allHadronic"


if options.stage == "allHadronic" :
    print "Getting the Samples for stage 2"
    samples = [
        ["run_101215/ttjets_b2ganafw_v6_101215_all.root",                                                                       'ttbar', 't#bar{t}', 831.76 * lumi / 19665194. , ROOT.kRed + 1],
        ["run_101215/QCD_Pt_170toInf_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_wbackground_101215_Scaled.root",   'QCD',   'QCD',      1.0,                        ROOT.kYellow + 1],
        ["run_101215/JetHT_knash_crab_Run2015D_PromptReco_v3_Sep25_v74x_V7_25ns_101215_all.root",                               'data',  'Data',     1.0,                        0]
    ]
    print "Got the Samples for stage 2"

histsMC = []
histsData = []
hstacks = []
canvs = []
files = []
legs = []
hmax = []

if options.stage == "allHadronic" :
    DIR = "AllHad/";

for sample in samples :
    ifile = ROOT.TFile( sample[FILE_NDX] )
    files.append(ifile)

for ihist,shist in enumerate( hists ) :
    hstack = ROOT.THStack( shist[HNAME_NDX], shist[HTITLE_NDX] )
    hdata = None
    leg = ROOT.TLegend( shist[LEGXMIN_NDX],shist[LEGYMIN_NDX],shist[LEGXMAX_NDX],shist[LEGYMAX_NDX])
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.06)
    leg.SetTextFont(42)
    print 'Getting histogram ' + shist[HNAME_NDX]
    for isample,sample in enumerate(samples) :
        iname = sample[NAME_NDX]
        print '   -- Sample : ' + iname
        
        ihist = files[isample].Get( DIR + shist[HNAME_NDX] ).Clone()
        ihist.UseCurrentStyle()
        ihist.SetName( ihist.GetName() + '_' + iname )
        ihist.Scale( sample[SCALE_NDX] )
        if iname in ['ttbar', 'wjets', 'st', 'zjets', 'QCD' ] :
            ihist.SetFillColor( sample[COLOR_NDX] )
            ihist.Rebin(25)
            hmax.append( ihist.GetMaximum() )
            hstack.Add( ihist )
            histsMC.append( ihist )
            leg.AddEntry( ihist, sample[TITLE_NDX], 'f')
            print '    ====> Added to MC'
        elif iname == 'mudata' :
            ihist.Rebin(25)
            hmax.append( ihist.GetMaximum() )
            hdata = ihist.Clone()
            hdata.SetName( ihist.GetName() + '_' + 'data' )
            histsData.append( hdata )
            print '    ====> Initialized data with mu'
        elif iname == 'eldata' :
            ihist.Rebin(25)
            hmax.append( ihist.GetMaximum() )
            hdata.Add ( ihist )
            histsData.append( ihist )
            print '    ====> Added to data with el'
            hdata.SetMarkerStyle(20)
            leg.AddEntry( hdata, 'Data', 'p')
        elif iname == 'data' :
            ihist.Rebin(25)
            hmax.append( ihist.GetMaximum() )
            hdata = ihist.Clone()
            hdata.SetName( ihist.GetName() + '_' + 'data' )
            histsData.append( ihist )
            print '    ====> Added to data'
            hdata.SetMarkerStyle(20)
            leg.AddEntry( hdata, 'Data', 'p')
        
    
    if options.hmax != None : 
        hstack.SetMaximum( options.hmax  )
    else :
        #hstack.SetMaximum( shist[HMAX_NDX] )
        for iMax in xrange(0, len(hmax)) :
            hmax1 = hmax[0]
            hmax2 = hmax[iMax]
            print 'hmax2=', hmax2
            if hmax2 > hmax1:
                hmax1 = hmax2
                print 'hmax1=', hmax1
        hstack.SetMaximum( hmax1 * 1.4)
    canv = ROOT.TCanvas( 'c'+ shist[HNAME_NDX], 'c'+ shist[HNAME_NDX] )
    hstack.Draw('hist')
    hdata.Draw('e same')


    hstack.GetXaxis().SetRangeUser( shist[HXMIN_NDX], shist[HXMAX_NDX] )
    leg.Draw()

    tlx = ROOT.TLatex()
    tlx.SetNDC()
    tlx.SetTextFont(42)
    tlx.SetTextSize(0.057)
    tlx.DrawLatex(0.2, 0.905, "CMS Preliminary #sqrt{s}=13 TeV, " + str(lumi) + " pb^{-1}")
    # tlx.DrawLatex(0.77, 0.86, "#bf{CMS}")
    # tlx.DrawLatex(0.72, 0.83, "#it{very preliminary}")
    tlx.SetTextSize(0.025)
    #xInfo = 0.48
    yInfoTop = 0.84
    if shist[HNAME_NDX] == "h_Jet0_Rap": 
        xInfo = 0.20
    elif shist[HNAME_NDX] == "h_Jet1_Rap":
        xInfo = 0.20
    else:
        xInfo = 0.48
        

    yInfo2 = yInfoTop-0.042
    yInfo3 = yInfo2-0.042
    yInfo4 = yInfo3-0.042
    yInfo5 = yInfo4-0.042
    yInfo6 = yInfo5-0.042
    tlx.DrawLatex(xInfo, yInfoTop, "#bf{CMS Top Tagger}") # same for AK4 and AK8
    tlx.DrawLatex(xInfo, yInfo2 , "#bf{Madgraph}") # same for AK4 and AK8 
    tlx.DrawLatex(xInfo, yInfo4, "#bf{|#eta| < 2.4 }")  # same for AK4 and AK8
    if options.stage == "semiLeptonic" :
        tlx.DrawLatex(xInfo, yInfo3, "#bf{AK R= 0.4}") # 0.8 or 0.4 for AK8 and AK4              change with histo
        tlx.DrawLatex(xInfo, yInfo5, "#bf{P_{T} > 30 GeV}")# > 400 for AK8 and > 30 for AK4     change with histo
    
    if options.stage == "allHadronic" :
        tlx.DrawLatex(xInfo, yInfo3, "#bf{AK R= 0.8}") # 0.8 or 0.4 for AK8 and AK4              change with histo
        tlx.DrawLatex(xInfo, yInfo5, "#bf{P_{T} > 400 GeV}")# > 400 for AK8 and > 30 for AK4     change with histo
        
    tlx.DrawLatex(xInfo, yInfo6, "#bf{50 ns}")  # change with 25 or 50 ns bunchcrossings     change with root files
    
    canv.Draw()

    legs.append(leg)
    canvs.append(canv)
    hstacks.append(hstack)
    canv.Print(shist[HNAME_NDX] + '.png', 'png')
    canv.Print(shist[HNAME_NDX] + '.pdf', 'pdf')    
    
    
