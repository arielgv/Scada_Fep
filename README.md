First . SCADA :
   Required Files:
    
    Station.csv
    
    Status.csv
    
    Analog.csv
    
    all_stations_equivalency.csv


  run scada_code 
  run MergingScada

  copy generated 'status_xref.csv' & 'analog_xref.csv' to the FEP folder. 

Second. FEP:
    Required Files:

    all_stations_equivalency.csv
    analog_xref.csv
    Comm.csv
    FEP_GSD_v1.dat
    RTAC SCADA DNP IPs Reordered.csv
    SOURCE_analog.csv
    SOURCE_status.csv
    status_xref.csv
    
  run main
  run MergingFep 
