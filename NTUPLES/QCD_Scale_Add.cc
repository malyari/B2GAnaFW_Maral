// ScaleAdd.cc
// Scale the QCD hists appropriately for each pT and Add them together
// [] .L ScaleAdd.cc+
// [] run()

#include "TROOT.h"
#include "TStyle.h"
#include "TLatex.h"
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TBranch.h"
#include "TLeaf.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TH1.h"
#include "THStack.h"
#include "TH2.h"
#include "TF1.h"
#include "TProfile.h"
#include "TProfile2D.h"
#include "TMath.h"
#include <TStyle.h>

#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
#include <cstdlib>
#include <cmath>

using namespace std;

const int nPt = 10;
TString pT_range[nPt] = {"170to300", "300to470", "470to600", "600to800", "800to1000", 
                         "1000to1400", "1400to1800", "1800to2400", "2400to3200", "3200toInf"};

const int nHist = 123;

void run(){

    TString hists_names[nHist] = {
                                  // Basic plots from all-hadronic preselected events (2 AK8 pT>400 jets); 49 hists
                                  "h_Jet0_MassSoft_CorrNone", "h_Jet0_MassTrim_CorrNone", "h_Jet0_MassFilt_CorrNone", "h_Jet0_MassPrun_CorrNone", "h_Jet0_MinCMSTT_CorrNone",
                                  "h_Jet0_MassSoft_CorrL2L3", "h_Jet0_MassTrim_CorrL2L3", "h_Jet0_MassFilt_CorrL2L3", "h_Jet0_MassPrun_CorrL2L3", "h_Jet0_MinCMSTT_CorrL2L3",
                                  "h_Jet0_Tau1", "h_Jet0_Tau2", "h_Jet0_Tau3", "h_Jet0_Tau21", "h_Jet0_Tau32",
                                  "h_Jet0_Pt", "h_Jet0_Rap", "h_Jet0_NHF", "h_Jet0_CHF", "h_Jet0_NEF", "h_Jet0_CEF", "h_Jet0_NC", "h_Jet0_NCH",
                                  "h_Jet0_MassSoft_CorrOrigSumSubjet", "h_Jet0_MassSoft_RawSumSubjet", "h_Jet0_MassSoft_CorrNewSumSubjet",

                                  "h_Jet1_MassSoft_CorrNone", "h_Jet1_MassTrim_CorrNone", "h_Jet1_MassFilt_CorrNone", "h_Jet1_MassPrun_CorrNone", "h_Jet1_MinCMSTT_CorrNone",
                                  "h_Jet1_MassSoft_CorrL2L3", "h_Jet1_MassTrim_CorrL2L3", "h_Jet1_MassFilt_CorrL2L3", "h_Jet1_MassPrun_CorrL2L3", "h_Jet1_MinCMSTT_CorrL2L3",
                                  "h_Jet1_Tau1", "h_Jet1_Tau2", "h_Jet1_Tau3", "h_Jet1_Tau21", "h_Jet1_Tau32",
                                  "h_Jet1_Pt", "h_Jet1_Rap", "h_Jet1_NHF", "h_Jet1_CHF", "h_Jet1_NEF", "h_Jet1_CEF", "h_Jet1_NC", "h_Jet1_NCH",

                                  // modMass hists with small binning; 6 hists
                                  "h_mAK8_ModMass", "h_mSDropAK8_ModMass", "h_mAK8_ModMass_jet0", "h_mSDropAK8_ModMass_jet0", "h_mAK8_ModMass_jet1", "h_mSDropAK8_ModMass_jet1",

                                  // mistag plots; 48 hists
                                  "h_AntiTagNone_ReqTopMassSD_Probe_jetPt", "h_AntiTagNone_ReqTopMassSD_TagMassSD_jetPt", "h_AntiTagNone_ReqTopMassSD_TagMassSDTau32_jetPt",
                                  "h_AntiTagNone_ReqTopMassSD_TagMassSDMinMass_jetPt", "h_AntiTagNone_ReqTopMassSD_TagMassFat_jetPt", "h_AntiTagNone_ReqTopMassSD_TagMassFatMinMass_jetPt",

                                  "h_AntiTagNone_ReqTopMassFat_Probe_jetPt", "h_AntiTagNone_ReqTopMassFat_TagMassSD_jetPt", "h_AntiTagNone_ReqTopMassFat_TagMassSDTau32_jetPt",
                                  "h_AntiTagNone_ReqTopMassFat_TagMassSDMinMass_jetPt", "h_AntiTagNone_ReqTopMassFat_TagMassFat_jetPt", "h_AntiTagNone_ReqTopMassFat_TagMassFatMinMass_jetPt",

                                  "h_AntiTagMinMass30_ReqTopMassSD_Probe_jetPt", "h_AntiTagMinMass30_ReqTopMassSD_TagMassSD_jetPt", "h_AntiTagMinMass30_ReqTopMassSD_TagMassSDTau32_jetPt",
                                  "h_AntiTagMinMass30_ReqTopMassSD_TagMassSDMinMass_jetPt", "h_AntiTagMinMass30_ReqTopMassSD_TagMassFat_jetPt", "h_AntiTagMinMass30_ReqTopMassSD_TagMassFatMinMass_jetPt",

                                  "h_AntiTagMinMass30_ReqTopMassFat_Probe_jetPt", "h_AntiTagMinMass30_ReqTopMassFat_TagMassSD_jetPt", "h_AntiTagMinMass30_ReqTopMassFat_TagMassSDTau32_jetPt",
                                  "h_AntiTagMinMass30_ReqTopMassFat_TagMassSDMinMass_jetPt", "h_AntiTagMinMass30_ReqTopMassFat_TagMassFat_jetPt", "h_AntiTagMinMass30_ReqTopMassFat_TagMassFatMinMass_jetPt",

                                  "h_AntiTagMinMass50_ReqTopMassSD_Probe_jetPt", "h_AntiTagMinMass50_ReqTopMassSD_TagMassSD_jetPt", "h_AntiTagMinMass50_ReqTopMassSD_TagMassSDTau32_jetPt",
                                  "h_AntiTagMinMass50_ReqTopMassSD_TagMassSDMinMass_jetPt", "h_AntiTagMinMass50_ReqTopMassSD_TagMassFat_jetPt", "h_AntiTagMinMass50_ReqTopMassSD_TagMassFatMinMass_jetPt",

                                  "h_AntiTagMinMass50_ReqTopMassFat_Probe_jetPt", "h_AntiTagMinMass50_ReqTopMassFat_TagMassSD_jetPt", "h_AntiTagMinMass50_ReqTopMassFat_TagMassSDTau32_jetPt",
                                  "h_AntiTagMinMass50_ReqTopMassFat_TagMassSDMinMass_jetPt", "h_AntiTagMinMass50_ReqTopMassFat_TagMassFat_jetPt", "h_AntiTagMinMass50_ReqTopMassFat_TagMassFatMinMass_jetPt",

                                  "h_AntiTagTau32_ReqTopMassSD_Probe_jetPt", "h_AntiTagTau32_ReqTopMassSD_TagMassSD_jetPt", "h_AntiTagTau32_ReqTopMassSD_TagMassSDTau32_jetPt",
                                  "h_AntiTagTau32_ReqTopMassSD_TagMassSDMinMass_jetPt", "h_AntiTagTau32_ReqTopMassSD_TagMassFat_jetPt", "h_AntiTagTau32_ReqTopMassSD_TagMassFatMinMass_jetPt",

                                  "h_AntiTagTau32_ReqTopMassFat_Probe_jetPt", "h_AntiTagTau32_ReqTopMassFat_TagMassSD_jetPt", "h_AntiTagTau32_ReqTopMassFat_TagMassSDTau32_jetPt",
                                  "h_AntiTagTau32_ReqTopMassFat_TagMassSDMinMass_jetPt", "h_AntiTagTau32_ReqTopMassFat_TagMassFat_jetPt", "h_AntiTagTau32_ReqTopMassFat_TagMassFatMinMass_jetPt",

                                  // Hadronic mtt selection and background estimaion; 20 hists
                                  "h_mttMass_tagMassSD", "h_mttMass_tagMassSDTau32", "h_mttMass_tagMassSDMinMass", "h_mttMass_tagMassFat", "h_mttMass_tagMassFatMinMass",

                                  "h_bkgdEst_tagMassSD", "h_bkgdEst_tagMassSDTau32", "h_bkgdEst_tagMassSDMinMass", "h_bkgdEst_tagMassFat", "h_bkgdEst_tagMassFatMinMass",

                                  "h_bkgdEst_modMass_tagMassSD", "h_bkgdEst_modMass_tagMassSDTau32", "h_bkgdEst_modMass_tagMassSDMinMass", "h_bkgdEst_modMass_tagMassFat", "h_bkgdEst_modMass_tagMassFatMinMass",

                                  "h_bkgdEst_modMass_flat_tagMassSD", "h_bkgdEst_modMass_flat_tagMassSDTau32", "h_bkgdEst_modMass_flat_tagMassSDMinMass", "h_bkgdEst_modMass_flat_tagMassFat", "h_bkgdEst_modMass_flat_tagMassFatMinMass"
                                };

    TFile * OutFile = new TFile("QCD_Pt_170toInf_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_wbackground_101215_Scaled.root" , "RECREATE");

    const double lumi = 153.3 ; // pb-1
    double mcscales[nPt] = {
        //xs / nevents * lumi
        117276. / 3468514. * lumi,
        7823 / 2936644. * lumi,
        648.2 / 1971800. * lumi,
        186.9 / 1981608. * lumi,
        32.293 / 1990208. * lumi,
        9.4183 / 1487712. * lumi,
        0.84265 / 197959. * lumi,
        0.114943 / 194924. * lumi,
        0.00682981 / 198383. * lumi,
        0.000165445 / 194528. * lumi
    };


    // Get the 10 QCD files
    TFile* fQCD[nPt];
    TH1F* Check;

    for (int iPt=0; iPt<nPt; iPt++) {
            fQCD[iPt]=new TFile("run_101215/QCD_Pt_"+pT_range[iPt]+"_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A_101215_all.root","READ");
            cout<<"opened file run_101215/QCD_Pt_"+pT_range[iPt]+"_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A_101215_all.root"<<endl;
            }


    Check = (TH1F*) fQCD[9]->Get("AllHad/"+hists_names[122])->Clone();
    cout<<"DEBUG: after reading the file ="<< Check->GetSum()<<endl;


  
    // Get the relevant histograms
    vector<TH1F*> hists_pT_170to300; vector<TH1F*> hists_pT_300to470; vector<TH1F*> hists_pT_470to600; vector<TH1F*> hists_pT_600to800; vector<TH1F*> hists_pT_800to1000;
    vector<TH1F*> hists_pT_1000to1400; vector<TH1F*> hists_pT_1400to1800; vector<TH1F*> hists_pT_1800to2400; vector<TH1F*> hists_pT_2400to3200; vector<TH1F*> hists_pT_3200toInf;
    
    vector< vector<TH1F*> > hists_pT;
    
    for (int iHist=0; iHist<nHist; iHist++) {
        hists_pT_170to300  .push_back( (TH1F*) fQCD[0]->Get("AllHad/"+hists_names[iHist])->Clone() );
        hists_pT_300to470  .push_back( (TH1F*) fQCD[1]->Get("AllHad/"+hists_names[iHist])->Clone() );
        hists_pT_470to600  .push_back( (TH1F*) fQCD[2]->Get("AllHad/"+hists_names[iHist])->Clone() );
        hists_pT_600to800  .push_back( (TH1F*) fQCD[3]->Get("AllHad/"+hists_names[iHist])->Clone() );
        hists_pT_800to1000 .push_back( (TH1F*) fQCD[4]->Get("AllHad/"+hists_names[iHist])->Clone() );
        hists_pT_1000to1400.push_back( (TH1F*) fQCD[5]->Get("AllHad/"+hists_names[iHist])->Clone() );
        hists_pT_1400to1800.push_back( (TH1F*) fQCD[6]->Get("AllHad/"+hists_names[iHist])->Clone() );
        hists_pT_1800to2400.push_back( (TH1F*) fQCD[7]->Get("AllHad/"+hists_names[iHist])->Clone() );
        hists_pT_2400to3200.push_back( (TH1F*) fQCD[8]->Get("AllHad/"+hists_names[iHist])->Clone() );
        hists_pT_3200toInf .push_back( (TH1F*) fQCD[9]->Get("AllHad/"+hists_names[iHist])->Clone() );
    }
    //hists_pT[iPt][iHist]
    hists_pT.push_back(hists_pT_170to300);
    hists_pT.push_back(hists_pT_300to470);
    hists_pT.push_back(hists_pT_470to600);
    hists_pT.push_back(hists_pT_600to800);
    hists_pT.push_back(hists_pT_800to1000);
    hists_pT.push_back(hists_pT_1000to1400);
    hists_pT.push_back(hists_pT_1400to1800);
    hists_pT.push_back(hists_pT_1800to2400);
    hists_pT.push_back(hists_pT_2400to3200);
    hists_pT.push_back(hists_pT_3200toInf);


    // Scale the relevant hists
    for (int iPt=0; iPt<nPt; iPt++) {
        for (int iHist=0; iHist<nHist; iHist++) {
            hists_pT[iPt][iHist]->Scale(mcscales[iPt]);
        }
    }

    // Add all tag hists and all probe hists
    vector<TH1F*> hists_allpT;
    for (int iHist=0; iHist<nHist; iHist++) {
        hists_allpT.push_back( (TH1F*)hists_pT[0][iHist]->Clone() );
    }

    for (int iPt=1; iPt<nPt; iPt++) {
        for (int iHist=0; iHist<nHist; iHist++) {
            hists_allpT[iHist] ->Add( (TH1F*)hists_pT[iPt][iHist], 1 );
        }        
    }
    

    // Write the final tag and probe hists in a root file
    OutFile->cd();
    OutFile->mkdir("AllHad")->cd();

    for (int iHist=0; iHist<nHist; iHist++) {
        hists_allpT[iHist] -> SetName(hists_names[iHist]);
        hists_allpT[iHist] -> Write();
    }


    OutFile->Close();
}







