#! /usr/bin/python
"""

@author: Pablo ALINGERY for IAS 06-05-2016
"""

from sitools2.core.pySitools2 import *


def main():

    sitools_url = 'http://idoc-medoc-test.ias.u-psud.fr'

    print("Loading SitoolsClient for", sitools_url)
    SItools1 = Sitools2Instance(sitools_url)
    ds1 = Dataset(sitools_url + "/webs_IAS_SDO_AIA_dataset")
    ds1.display()
    #display() or print works as well
    #        print ds1

    #date__ob
    #Format must be somthing like 2015-11-01T00:00:00.000 in version Sitools2 3.0 that will change 
    param_query1 = [
                    [ds1.fields_dict['date__obs']], 
                    ['2015-11-01T00:00:00.000', '2015-11-02T00:00:00.000'],
                    'DATE_BETWEEN'
    ]
    #series_name 
    param_query2 = [[ds1.fields_dict['series_name']], ['aia.lev1'], 'IN']
    #cadence
    param_query3 = [[ds1.fields_dict['mask_cadence']], ['1 h'], 'CADENCE']
    #wave
    #       param_query2=[[ds1.fields_dict[2]],['aia.lev1'],'IN']

    Q1 = Query(param_query1)
    Q2 = Query(param_query2)
    Q3 = Query(param_query3)

    #Ask recnum, sunum,series_name,date__obs, ias_location,ias_path

    O1 = [
        ds1.fields_dict['recnum'], ds1.fields_dict['sunum'], 
        ds1.fields_dict['series_name'], ds1.fields_dict['date__obs'], 
        ds1.fields_dict['ias_location'], ds1.fields_dict['ias_path']
    ]

    #Sort date__obs ASC
    S1 = [[ds1.fields_dict['date__obs'], 'ASC']]

    #       for field in ds1.fields_dict :
    #               field.display()

    #        print "\nPrint Query  ..."
    Q1.display()
    Q2.display()
    Q3.display()

    result = ds1.search([Q1, Q2, Q3], O1, S1)
    #        result=ds1.search([Q1,Q2],O1,S1,limit_to_nb_res_max=10)
    if len(result) != 0:
        print("Results :")
        for i, data in enumerate(result):
            print("%d) %s" % (i + 1, data))

    recnum_list = []
    for record in result:
        recnum_list.append(str(record['recnum']))


#        ds_hmi=Dataset(sitools_url+"/hmi.sharp_cea_720s_nrt")
#        ds_hmi.display()
#        print recnum_list
#recnum
#        param_query_hmi=[[ds_hmi.fields_dict[0]],recnum_list,'IN']
#        Q_hmi=Query(param_query_hmi)
#        Q_hmi.display()
#output 
#        O1_hmi=[ds_hmi.fields_dict[0],ds_hmi.fields_dict[1],ds_hmi.fields_dict[142]]
#        print "output : ",ds_hmi.fields_dict[142].name
#        S1_hmi=[[ds_hmi.fields_dict[142],'ASC']]
#       for field in ds_aia.fields_dict :
#               field.display()
#        result_hmi=ds_hmi.search([Q_hmi],O1_hmi,S1_hmi)
#        for data in result_hmi:
#                print data

#       print "Download just one recnum\nIn progress please wait ..." 
#       ds1.execute_plugin(plugin_name='pluginDownloadTar', pkey_list=["1878160,hmi.sharp_cea_720s_nrt"], FILENAME='first_download_hmi.tar')
#       print "Download completed"

if __name__ == "__main__":
    main()