import os

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.utils import LayerMapping

from projects.models import Project


class Command(BaseCommand):
    args = 'projects'
    help = 'Imports projects.shp from the data directory.'

    config = {
        'projects': {
            'file': 'data/projects.shp',
            'model': Project,
            'mapping': {
                'dd_id': 'DD_ID',
                'name' : 'DDname',
                'completion' : 'ComplYr',
                'area' : 'PrjAcrs',
                'website' : 'DD_URL',
                'total_housing_units' : 'TotHU',
                'detached_single_fam' : 'SingFamHU',
                'townhouse_small_multi_fam' : 'TwnhSmMult',
                'med_large_multi_fam' : 'LgMultiFam',
                'age_restricted_pct' : 'Ovr55',
                'affordable_pct' : 'PctAffAll',
                'group_quarters' : 'GQpop',
                'nonres_dev' : 'CommSF', 
                'hotel_rooms' : 'HotelRms',
                'retail_restaurant_pct' : 'RetPct',
                'office_medical_pct' : 'OfcMdPct',
                'manufacturing_industrial_pct' : 'IndMfPct',
                'warehouse_trucking_pct' : 'WhsPct',
                'lab_RandD_pct' : 'RnDPct',
                'edu_institution_pct' : 'EdInstPct',  
                'other_pct' : 'OthPct',
                'est_emp' : 'RptdEmp',
                'est_emp_loss' : 'EmpLoss',
                'metro_future_discount_pct' : 'MFDisc',
                'redevelopment' : 'Rdv',
                'cluster_subdivision' : 'ClustOSRD',
                'mixed_use' : 'MxdUse',
                'comment' : 'DD_info',
                'location' : 'POINT',
                'legacy_status' : 'Status', 
                'legacy_mf_hu' : 'MF_HU', 
                'legacy_ch40' : 'Ch40', 
                'legacy_totempl' : 'TotEmp', 
                'legacy_mf_empl' : 'MF_Emp', 
                'legacy_dvttype' : 'DvtType', 
                'legacy_mftot00_10' : 'MFTot00_10', 
                'legacy_mftot10_20' : 'MFTot10_20', 
                'legacy_mftot20_30' : 'MFTot20_30', 
                'legacy_mftot30_35' : 'MFTot30_35', 
                'legacy_mfhu00_10' : 'MFHU00_10', 
                'legacy_mfhu10_20' : 'MFHU10_20', 
                'legacy_mfhu20_30' : 'MFHU20_30', 
                'legacy_mfhu30_35' : 'MFHU30_35', 
                'legacy_mfgq00_10' : 'MFGQ00_10', 
                'legacy_mfgq10_20' : 'MFGQ10_20', 
                'legacy_mfgq20_30' : 'MFGQ20_30', 
                'legacy_mfgq30_35' : 'MFGQ30_35', 
            }
        }
    }

    def handle(self, *args, **options):
        for shp in args:
            try:
                lm = LayerMapping(self.config[shp]['model'], self.config[shp]['file'], self.config[shp]['mapping'], 
                    encoding='iso-8859-1')
                lm.save(strict=True, verbose=True)

                self.stdout.write('Successfully imported "%s"\n' % shp)
            except:
                 raise CommandError('%s does not exist' % shp)
