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

const int nPt = 9;
TString pT_range[nPt] = {//"170to300", 
                         "300to470", "470to600", "600to800", "800to1000", 
                         "1000to1400", "1400to1800", "1800to2400", "2400to3200", "3200toInf"};

const int nHist = 5;

void run(){

    TString hists_names[nHist] = {"h_mttMass_tagMassFatMinMass", "mttPredDist_tagMassFatMinMass_pred", "mttPredDist_tagMassFatMinMass", 
                            "h_bkgdEst_tagMassFatMinMass", "h_bkgdEst_modMass_tagMassFatMinMass"};

    TFile * OutFile = new TFile("QCD_Pt_300toInf_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_wbackground_fwlite4fixWithTree_091715.root" , "RECREATE");

    const double lumi = 40.03 ; // pb-1
    double mcscales[nPt] = {
        //xs / nevents * lumi
        //117276. / 3468514. * lumi,
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
            fQCD[iPt]=new TFile("QCD_Pt_"+pT_range[iPt]+"_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_wbackground_fwlite4fixWithTree_091715.root","READ");
            cout<<"opened file QCD_Pt_"+pT_range[iPt]+"_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_wbackground_fwlite4fixWithTree_091715.root"<<endl;
            }
    Check = (TH1F*) fQCD[8]->Get(hists_names[4])->Clone();
    cout<<"DEBUG: after reading the file ="<< Check->GetSum()<<endl;

    // Get the relevant histograms
    vector<TH1F*> hists_h_mttMass;
    for (int iPt=0; iPt<nPt; iPt++) {
        hists_h_mttMass.push_back( (TH1F*) fQCD[iPt]->Get(hists_names[0])->Clone() );
    }
    vector<TH1F*> hists_mttPredDist_pred;
    for (int iPt=0; iPt<nPt; iPt++) {
        hists_mttPredDist_pred.push_back( (TH1F*) fQCD[iPt]->Get(hists_names[1])->Clone() );
    }
    vector<TH1F*> hists_mttPredDist;
    for (int iPt=0; iPt<nPt; iPt++) {
        hists_mttPredDist.push_back( (TH1F*) fQCD[iPt]->Get(hists_names[2])->Clone() );
    }
    vector<TH1F*> hists_h_bkgdEst;
    for (int iPt=0; iPt<nPt; iPt++) {
        hists_h_bkgdEst.push_back( (TH1F*) fQCD[iPt]->Get(hists_names[3])->Clone() );
    }
    vector<TH1F*> hists_h_bkgdEst_modMass;
    for (int iPt=0; iPt<nPt; iPt++) {
        hists_h_bkgdEst_modMass.push_back( (TH1F*) fQCD[iPt]->Get(hists_names[4])->Clone() );
    }


    // Scale the relevant hists
    for (int iPt=0; iPt<nPt; iPt++) {
        hists_h_mttMass[iPt]->Scale(mcscales[iPt]);
        hists_mttPredDist_pred[iPt]->Scale(mcscales[iPt]);
        hists_mttPredDist[iPt]->Scale(mcscales[iPt]);
        hists_h_bkgdEst[iPt]->Scale(mcscales[iPt]);
        hists_h_bkgdEst_modMass[iPt]->Scale(mcscales[iPt]);
    }

    // Add all tag hists and all probe hists
    TH1F* hists_h_mttMass_allpT; TH1F* hists_mttPredDist_pred_allpT; TH1F* hists_mttPredDist_allpT; TH1F* hists_h_bkgdEst_allpT; TH1F* hists_h_bkgdEst_modMass_allpT;
    hists_h_mttMass_allpT         = (TH1F*)hists_h_mttMass[0]->Clone();
    hists_mttPredDist_pred_allpT  = (TH1F*)hists_mttPredDist_pred[0]->Clone();
    hists_mttPredDist_allpT       = (TH1F*)hists_mttPredDist[0]->Clone();
    hists_h_bkgdEst_allpT         = (TH1F*)hists_h_bkgdEst[0]->Clone();
    hists_h_bkgdEst_modMass_allpT = (TH1F*)hists_h_bkgdEst_modMass[0]->Clone();

    for (int iPt=1; iPt<nPt; iPt++) {
        hists_h_mttMass_allpT         ->Add( (TH1F*)hists_h_mttMass[iPt], 1);
        hists_mttPredDist_pred_allpT  ->Add( (TH1F*)hists_mttPredDist_pred[iPt], 1);
        hists_mttPredDist_allpT       ->Add( (TH1F*)hists_mttPredDist[iPt], 1);
        hists_h_bkgdEst_allpT         ->Add( (TH1F*)hists_h_bkgdEst[iPt], 1);
        hists_h_bkgdEst_modMass_allpT ->Add( (TH1F*)hists_h_bkgdEst_modMass[iPt], 1);
    }
    

    // Write the final tag and probe hists in a root file
    OutFile->cd();
    hists_h_mttMass_allpT->SetName(hists_names[0]);
    hists_h_mttMass_allpT->Write();

    hists_mttPredDist_pred_allpT->SetName(hists_names[1]);
    hists_mttPredDist_pred_allpT->Write();

    hists_mttPredDist_allpT->SetName(hists_names[2]);
    hists_mttPredDist_allpT->Write();

    hists_h_bkgdEst_allpT->SetName(hists_names[3]);
    hists_h_bkgdEst_allpT->Write();

    hists_h_bkgdEst_modMass_allpT->SetName(hists_names[4]);
    hists_h_bkgdEst_modMass_allpT->Write();
    
    OutFile->Close();
}







