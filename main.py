from src.aux import Aux
from src.dataset_output import DatasetOutput



def main():

    aux = Aux()
    get = DatasetOutput()

    aux.new_line
    aux.hline
    aux.hline

    tic = aux.initiate_timer("Building GDP datasets...")
    print("""
Regions Covered: US and EA19
- Metrics: Nominal GDP and Real GDP

----- US Data -----
- Real GDP base year: 2012

----- EA19 Data -----
- Real GDP original base year: 2012
- Adjusted Real GDP base year: 2015

Note: Datasets are saved in th folers us/ and euro/, respectively.
          """)
    get.gdp('US')
    get.gdp('EU19')
    aux.end_timer(tic)

    aux.hline
    aux.hline
    aux.new_line

    tic = aux.initiate_timer("Building potential GDP datasets...")
    print("""
Regions Covered: US and EA19
- Metrics: Potential GDP

----- US Data -----
- Real GDP base year: 2012

----- EA19 Data -----
- Real GDP original base year: 2012
- Adjusted Real GDP base year: 2015

Note: Datasets are saved in th folers us/ and euro/, respectively.
          """)
    get.gdppot('US')
    get.gdppot('EU19')
    aux.end_timer(tic)

    aux.hline
    aux.hline
    aux.new_line
    
    tic = aux.initiate_timer("Building output gap datasets...")
    print("""
Regions Covered: US and EA19
- Metrics: Output Gap 

----- US Data -----
- Real GDP base year: 2012

----- EA19 Data -----
- Real GDP original base year: 2012
- Adjusted Real GDP base year: 2015

Note: Datasets are saved in th folers us/ and euro/, respectively.
          """)
    get.output_gap('US')
    get.output_gap('EU19')
    aux.end_timer(tic)

    aux.hline
    aux.hline
    aux.new_line


if __name__ == '__main__':
    main()