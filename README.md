## TwoLeptonAnalysis

This package is designed to study the ntuples created by [https://github.com/rsmith54/RJigsawTools] for a 2-lepton SUSY search. This is originally based on the similar set of scripts from ZeroLeptonAnalysis [https://github.com/lawrenceleejr/ZeroLeptonAnalysis]. 

The histogram-making scripts available here make heavy use of SampleHandler and MultiDraw. The final plotting scripts make heavy use of rootpy+matplotlib so if you wish to use them, make sure to install those dependencies. [https://github.com/rootpy]

An implementation of HistFitter will eventually find its way into this package as well.

### Use

Once you've obtained the package from

```
git clone https://github.com/lawrenceleejr/TwoLeptonAnalysis.git
```

one should be able to set up and run via

```
cd TwoLeptonAnalysis
source setup.sh
python run.py
```

assuming the run script is pointing to the proper ntuples. Here, it is always assumed that you have ntuples from the RJigsawTools package *post merging*. (Follow the instructions in RJigsawTools for how to merge the grid output into some handy ntuples.)



