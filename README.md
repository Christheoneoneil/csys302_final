# csys302_final: 

## **Directory:**

**MOCS_final_simple.ipynb** Interactive Python notebook to run model (Designed to execute in a Google Colaboratory Environment)

**/harvey_workstation/** : This sub-directory contains the code used for Patrick Harvey's virtual environment.

  **harvey_ox.yml**  : Virtual environment used for .py files below.

  **gen_simple_net.py** Generate a simple version of the network.

  **gen_complex_net.py** Generate a complex version of the network.

  **complex_model.py** Set-up and run the complex version of the network.

  **burlington_traffic.py** Run all necessary scripts to model traffic within 20km of Burlington, VT.

## **Disclaimer**

This work is provided as is, and is not guaranteed to work on another workstation without a fresh install of the necessary dependencies in an isolated virtual environment. An environment named 'ox' was used for the branch harvey_workstation is included as harvey_ox.yml.

complex_model.py: creates traffic model with fixed starting and ending nodes

model_stats.py: computes simple stats for model

gen_complex_net.py: generates complex networkx object used in modeling 

gen_total_net.py: generates network of all of Vermont's road ways 
