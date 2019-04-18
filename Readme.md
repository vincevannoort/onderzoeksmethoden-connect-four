# How to use the new scripts

To generate models for the columnchoice classifier you use this command:
```bash
python3 classifier_columnchoice.py -w {amount winning states} -b {amount blocking states} -rw {amount random winning states} -a {amount models}
```

To generate models for the winlose classifier you use this command:
```bash
python3 classifier_winlose.py -w {amount winning states} -b {amount blocking states} -rw {amount random winning states} -rl {amount random losing states} -a {amount models}
```

To test two models you use this command:
```bash
python3 statistic_analysis.py -w1 {amount winning states} -b1 {amount blocking states} -rw1 {amount random winning states} -rl1 {amount random losing states} -c1 {which classifier (2 options: columnchoice/winlose)} -n1 {name of model (unique name which describes the model)} -w2 {amount winning states} -b2 {amount blocking states} -rw2 {amount random winning states} -rl2 {amount random losing states} -c2 {which classifier (2 options: columnchoice/winlose)} -n2 {name of model (unique name which describes the model)} -a {amount of models}
```

To visualize the test data, you use this command:
```bash
python3 statistic_visualization.py -n1 {name of model} -n2 {name of model} -a {amount of models}
```