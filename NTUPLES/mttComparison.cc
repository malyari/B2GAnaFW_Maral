/* -------------------------------------------------------------------------------------------------------------------------
  Script for comparing mttbar, mttbar observed and mttbar predicted
  -------------------------------------------------------------------------------------------------------------------------
*/
//  -------------------------------------------------------------------------------------
//  load options & set plot style
//  -------------------------------------------------------------------------------------
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

#include <iostream>
#include <string>
#include <vector>

using namespace std;

void mttComparison() {

    TFile* fQCD;

    TH1D* h_mttMass;
    TH1D* h_mttPredDist_pred;
    TH1D* h_mttPredDist;
    TH1D* h_bkgdEst;
    TH1D* h_bkgdEst_modMass;

    TCanvas* c1;
    TCanvas* c2;

    TH1D* Check;

    // Opening the files
    cout<<"opening the files"<<endl;
    fQCD = new TFile("QCD_Pt_300toInf_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_wbackground_fwlite4fixWithTree_091715.root");
    Check = (TH1D*) fQCD->Get("h_mttMass_tagMassFatMinMass")->Clone();
    cout<<"DEBUG: after reading the file ="<< Check->GetSum()<<endl;

    // Getting the histograms
    cout<<"getting the histograms"<<endl;
    h_mttMass          = (TH1D*) fQCD->Get("h_mttMass_tagMassFatMinMass")->Clone();
    cout<<"Got h_mttMass"<<endl;
    h_mttPredDist_pred = (TH1D*) fQCD->Get("mttPredDist_tagMassFatMinMass_pred")->Clone();
    cout<<"Got h_mttPredDist_pred"<<endl;
    h_mttPredDist      = (TH1D*) fQCD->Get("mttPredDist_tagMassFatMinMass")->Clone();
    cout<<"Got h_mttPredDist"<<endl;
    h_bkgdEst          = (TH1D*) fQCD->Get("h_bkgdEst_tagMassFatMinMass")->Clone();
    cout<<"Got h_bkgdEst"<<endl;
    h_bkgdEst_modMass  = (TH1D*) fQCD->Get("h_bkgdEst_modMass_tagMassFatMinMass")->Clone();
    cout<<"Got h_bkgdEst_modMass"<<endl;

    h_mttPredDist_pred->Sumw2();
    h_mttPredDist->Sumw2();
    h_bkgdEst->Sumw2();
    h_bkgdEst_modMass->Sumw2();

    h_mttMass->Rebin(20);
    h_mttPredDist_pred->Rebin(20);
    h_mttPredDist->Rebin(20);
    h_bkgdEst->Rebin(20);
    h_bkgdEst_modMass->Rebin(20);

    // Plotting the histograms
    cout<<"plotting the mttbar "<<endl;
    c1 = new TCanvas("c" , "" , 800, 600);

    c1->cd();

    gStyle->SetOptStat(0);
    double max  = h_mttMass->GetMaximum();
    double max1 = h_mttPredDist_pred->GetMaximum();
    double max2 = h_mttPredDist->GetMaximum();
    if (max1 > max)
        max = max1;
    if (max2 > max)
        max = max2;

    h_mttMass->Draw("");
    //double maxX = hWeightttbar_m->GetXaxis()->GetXmax();
    //cout<<"max of x axis= "<< maxX <<endl;
    //hWeightttbar_m->SetAxisRange(0,maxX,"X");
    h_mttMass->SetAxisRange(0,max*1.3,"Y");
    h_mttMass->GetXaxis()->SetLabelSize(0.035);
    h_mttMass->GetYaxis()->SetLabelSize(0.035);
    h_mttMass->SetLineColor(1);
    h_mttMass->SetMarkerColor(1);
    h_mttMass->SetLineWidth(2);
    h_mttMass->SetMarkerStyle(24);
    h_mttMass->SetMarkerSize(0.5);
    h_mttMass->Draw("");

    //h_mttPredDist_pred->GetXaxis()->SetRange(0,70); 
    h_mttPredDist_pred->SetLineColor(2);
    h_mttPredDist_pred->SetMarkerColor(2);
    h_mttPredDist_pred->SetLineWidth(2);
    h_mttPredDist_pred->SetMarkerStyle(21);
    h_mttPredDist_pred->SetMarkerSize(0.5);
    h_mttPredDist_pred->Draw("Same E1");

    h_mttPredDist->GetXaxis()->SetRange(0,70); 
    h_mttPredDist->SetLineColor(4);
    h_mttPredDist->SetMarkerColor(4);
    h_mttPredDist->SetLineWidth(2);
    h_mttPredDist->SetMarkerStyle(21);
    h_mttPredDist->SetMarkerSize(0.5);
    h_mttPredDist->Draw("Same");

    TLegend* leg = new TLegend(0.35,0.55,0.9,0.9);  
    leg->AddEntry(h_mttMass,"ttbar mass","l");
    leg->AddEntry(h_mttPredDist_pred,"Predicted ttbar mass from  PredictedDistribution.cc","l");
    leg->AddEntry(h_mttPredDist,"Observed ttbar mass from  PredictedDistribution.cc","l");

    leg->SetFillStyle(0);
    leg->SetBorderSize(0);
    leg->SetTextSize(0.02);
    leg->SetTextFont(42);
    c1->Update();
    leg->Draw();
    c1->Draw();
/*
    c1->cd();
    p2->SetTopMargin(0.05);
    p2->SetBottomMargin(0.4);
    p2->Draw();
    p2->cd();

    hFrac = (TH1D*) hWeightttbar_k->Clone();
    hFrac->SetName("hFrac");
    hFrac->SetTitle(";Kevin's weights/Maral's weights");
    hFrac->Divide((TH1D*) hWeightttbar_m);

    hFrac->SetMaximum(2.0);
    hFrac->SetMinimum(0.0);
    hFrac->UseCurrentStyle();
    hFrac->GetXaxis()->SetTitleSize(0.1);
    hFrac->GetXaxis()->SetLabelSize(0.1);
    hFrac->GetXaxis()->SetTitleOffset(1.3);
    hFrac->GetYaxis()->SetLabelSize(0.1);
    hFrac->GetYaxis()->SetNdivisions(2,4,0,false);

    hFrac->Draw("e");

    c1->Update();

*/
    c1->SaveAs("mttbarComparison.png", "png");


    cout<<"plotting the mttbar "<<endl;
    c2 = new TCanvas("c2" , "" , 800, 600);

    c2->cd();

    gStyle->SetOptStat(0);
    double max3  = h_mttMass->GetMaximum();
    double max4 = h_bkgdEst->GetMaximum();
    double max5 = h_bkgdEst_modMass->GetMaximum();
    if (max4 > max3)
        max3 = max4;
    if (max5 > max3)
        max3 = max5;

    h_mttMass->Draw("");
    //double maxX = hWeightttbar_m->GetXaxis()->GetXmax();
    //cout<<"max of x axis= "<< maxX <<endl;
    //hWeightttbar_m->SetAxisRange(0,maxX,"X");
    h_mttMass->SetAxisRange(0,max*1.3,"Y");
    h_mttMass->GetXaxis()->SetLabelSize(0.035);
    h_mttMass->GetYaxis()->SetLabelSize(0.035);
    h_mttMass->SetLineColor(1);
    h_mttMass->SetMarkerColor(1);
    h_mttMass->SetLineWidth(2);
    h_mttMass->SetMarkerStyle(24);
    h_mttMass->SetMarkerSize(0.5);
    h_mttMass->Draw("");

    //h_bkgdEst->GetXaxis()->SetRange(0,70); 
    h_bkgdEst->SetLineColor(2);
    h_bkgdEst->SetMarkerColor(2);
    h_bkgdEst->SetLineWidth(2);
    h_bkgdEst->SetMarkerStyle(21);
    h_bkgdEst->SetMarkerSize(0.5);
    h_bkgdEst->Draw("Same E1");

    //h_bkgdEst_modMass->GetXaxis()->SetRange(0,70); 
    h_bkgdEst_modMass->SetLineColor(4);
    h_bkgdEst_modMass->SetMarkerColor(4);
    h_bkgdEst_modMass->SetLineWidth(2);
    h_bkgdEst_modMass->SetMarkerStyle(21);
    h_bkgdEst_modMass->SetMarkerSize(0.5);
    h_bkgdEst_modMass->Draw("Same");

    TLegend* leg1 = new TLegend(0.35,0.55,0.9,0.9);  
    leg1->AddEntry(h_mttMass,"ttbar mass","l");
    leg1->AddEntry(h_bkgdEst,"background estiamtion from  PredictedDistribution.cc","l");
    leg1->AddEntry(h_bkgdEst_modMass,"background estiamtion modMass","l");

    leg1->SetFillStyle(0);
    leg1->SetBorderSize(0);
    leg1->SetTextSize(0.02);
    leg1->SetTextFont(42);
    leg1->Draw();
    c2->Update();
    c2->Draw();
    c2->SaveAs("backgroundEstimationComparison.png", "png");



}




