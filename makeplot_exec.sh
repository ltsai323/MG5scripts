function the_exit() { echo $1; exit; }
python3 makeplot_mcLeadingByield.py || the_exit "faile 1";
python3 makeplot_mcLeadingC_barrelOVERendcap.py || the_exit "faile 2";
python3 makeplot_mcLeadingCvsB.py || the_exit "faile 3";
python3 makeplot_mcLeadingCyield.py || the_exit "faile 4";

python3 makeplot_mcMatchEfficiency_LeadingToPredictedC.py || the_exit "faile 5";

python3 makeplot_mcPredictedByield.py || the_exit "faile 6";
python3 makeplot_mcPredictedC_barrelOVERendcap.py || the_exit "faile 7";
python3 makeplot_mcPredictedCvsB.py || the_exit "faile 8";
python3 makeplot_mcPredictedCyield.py || the_exit "faile 9";
