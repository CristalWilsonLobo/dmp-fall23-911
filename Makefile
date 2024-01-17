DATA_DIR := data

data_dir:
	@mkdir -p $(DATA_DIR)

eda_plots: data/processeddataCA.zip
	python -B src/EDA/EDA_Cardiac_Arrest.py
	python -B src/EDA/EDA_EMS_Worker_Injury.py
	python -B src/EDA/EDA_Resuscitation_Attempted.py
	python -B src/EDA/EDA_Patient_Vitals.py
	python -B src/EDA/EDA_Patients_Acuity_Triage.py
	python -B src/EDA/EDA_Patients_Age_Gender.py
	python -B src/EDA/EDA_Patients_Race.py
	python -B src/EDA/EDA_Protocols.py
	python -B src/EDA/EDA_Trauma_Triage_High_Risks.py
	python -B src/EDA/EDA_Trauma_Triage_Moderate_Risk.py
	python -B src/EDA/EDA_Type_Dispatch_Delay.py
	python -B src/EDA/EDA_Type_Response_Delay.py
	python -B src/EDA/EDA_Type_Scene_Delay.py
	python -B src/EDA/EDA_Type_Transport_Delay.py
	python -B src/EDA/EDA_Type_Turnaround_Delay.py
	python -B src/EDA/EDA_Urbanicity.py
	python -B src/DataPreprocessing.py

combine_data: data/processeddataCA.zip
	python -B src/data_load/Data_CodeUpdate.py

clean_data: data/combined_Data.csv
	python -B src/run_clean_data.py $(param1)

select_features: data/cleaned_Data.csv
	python -B src/run_feature_selection.py $(filename) --balance $(balance) --feature_selection $(feature_selection)


models: data/cleaned_Data.csv
	python -B src/run_models.py $(filename) --balance $(balance) --feature_selection $(feature_selection) --model_types $(model_types)

