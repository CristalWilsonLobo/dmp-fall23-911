# Project Proposal for 911

## Story:

Cardiac arrests continue to be one of the largest health issues facing America, with over 356,000 people experiencing a cardiac 
arrest outside a hospital in 2022. One of the largest factors that influences the outcome of a cardiac arrest is
whether it occurs in an urban or rural area - a 2021 study found around a 20% difference in survival rates between people 
experiencing cardiac arrests in urban vs rural municipalities. Researchers at the Roux Institute, namely Qingchu Jin, 
are collaborating with Theresa May, a critical care doctor working for MaineHealth, to investigate this issue and attempt to
identify the primary factors related to the pre-hospital scenario and care that predict the outcome of a cardiac arrest. 
Ultimately, this project aims to leverage data on EMS responses to cardiac arrests to improve the odds of survival. A key source 
of this data for this project is the  NEMSIS (National Emergency Medical System (EMS) Information System) dataset, a comprehensive 
repository that captures every 911 call across the nation. 

The new project plan recognizes the need to tackle the significant difference in survival rates between rural and urban heart attack 
patients by using advanced data prediction techniques. Transitioning from its original exploratory nature, the project looks to leverage 
a sophisticated series of statistical methods to predict patient outcomes through supervised learning. This phase required a complex 
strategy for feature and model selection, blending algorithmic techniques such as lasso or random forest for with analysis of medical 
literature. It acknowledges inherent risks, including substantial missing data, dimensionality issues, and the proposition of data 
imputation methods to address the missing data problem. Additionally, by discovering important but overlooked factors in their data 
analysis, this project has the potential to leave far-reaching impact on emergency procedures used to respond to cardiac arrests.

## Approach

Our project is dedicated to refining the predictive models for outcomes in cardiac arrest patients, with a primary focus on an 
in-depth feature selection and correlation analysis. Given the size and diversity of the dataset, our work aims to 
support future research into this topic by producing a well-supported list of factors worth including in models of cardiac
arrest 911 calls. This critical process involves extracting key variables from the complex dataset and discovering potentially 
overlooked features that may significantly influence patient outcomes. Our approach leans heavily on specialized algorithms 
capable of navigating high-dimensional data, aiming to uncover potentially unknown variables that enhance our understanding of what 
affects the outcome of a cardiac event( alive, in a coma, or dead). The results of these feature selection techniques are then
combined with results from clinical literature about 911 responses to cardiac arrests. Rather than rely on any single method for 
feature selection, our project looks to create a more complete picture by contextualizing feature selection algorithms within
existing medical and scientific knowledge.


The subsequent phase, time permitting, involves the development of a suite of supervised learning models—specifically 
Naive Bayes, Random Forest, and XGBoost—to incorporate our identified features and predict patient outcomes with 
heightened accuracy. While our primary focus remains on isolating the variables that are most critical for inclusion, 
we are committed to validating the effectiveness of our analysis by deploying these models to predict the outcome of 
cardiac arrest patients. To optimize each model's performance, we will employ hyperparameter tuning and cross-validation
techniques, ensuring that we harness the most predictive power from our data. Part of this analytical progression 
includes conducting an ablation study, where we systematically exclude each identified feature to evaluate its impact 
on each model's predictive capability. We recognize the challenges and risks inherent in this project, from ensuring 
our discoveries are clinically relevant to the efficient handling of vast datasets. To mitigate these risks, including 
those not yet identified, we emphasize continual collaboration with stakeholders and methodical data exploration 
techniques. An ablation table will be crucial in this endeavor, providing a clear comparison of each model's 
performance to guide the selection of the most effective one. The end goal steadfastly remains to equip healthcare 
practitioners with a more nuanced, data-informed perspective that could potentially revolutionize the decision-making 
process in cardiac arrest cases. Even if the timeline constraints limit the completion of the supervised model 
development, our research and findings in feature correlations and selections are poised to offer valuable insight

## Sources
Connolly MS, Goldstein Pcp JP, Currie M, Carter AJE, Doucette SP, Giddens K, Allan KS, Travers AH, Ahrens B, Rainham D, 
Sapp JL. Urban-Rural Differences in Cardiac Arrest Outcomes: A Retrospective Population-Based Cohort Study. CJC Open. 
2021 Dec 30;4(4):383-389. doi: 10.1016/j.cjco.2021.12.010. PMID: 35495857; PMCID: PMC9039571.