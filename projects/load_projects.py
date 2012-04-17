import os
from django.contrib.gis.utils import LayerMapping
#from models import Project
from projects.models import *

project_mapping = {"dd_id": "DD_ID",
                   "name" : "DDname",
                   "completion" : "ComplYr",
                   "area" : "PrjAcrs",
                   "website" : "DD_URL",
                   "total_housing_units" : "TotHU",
                   "detached_single_fam" : "SingFamHU",
                   "townhouse_small_multi_fam" : "TwnhSmMult",
                   "med_large_multi_fam" : "LgMultiFam",
                   "age_restricted_pct" : "Ovr55",
                   "affordable_pct" : "PctAffAll",
                   "group_quarters" : "GQpop",
                   "nonres_dev" : "CommSF", 
                   "hotel_rooms" : "HotelRms",
                   "retail_restaurant_pct" : "RetPct",
                   "office_medical_pct" : "OfcMdPct",
                   "manufacturing_industrial_pct" : "IndMfPct",
                   "warehouse_trucking_pct" : "WhsPct",
                   "lab_RandD_pct" : "RnDPct",
                   "edu_institution_pct" : "EdInstPct",  
                   "other_pct" : "OthPct",
                   "est_emp" : "RptdEmp",
                   "est_emp_loss" : "EmpLoss",
                   "metero_future_discount_pct" : "MFDisc",
                   "redevelopment" : "Rdv",
                   "cluster_subdivision" : "ClustOSRD",
                   "mixed_use" : "MxdUse",
                   "comment" : "DD_info",
                   'location' : 'POINT',
                   }

#project_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/MAPC_DevtDatabase_V1_03_19_12.shp"))

project_shp = "/vagrant/git/data/MAPC_DevtDatabase_V1_04_17_12.shp"
def run(verbose=True):
    lm = LayerMapping(Project, project_shp, project_mapping, transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)