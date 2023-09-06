import datetime as dt
import eikon as ek
import eurostat as euro
import numpy as np
import pandas as pd
import requests as r
import os

from src.aux import Aux

class DatasetOutput():

    def __init__(self) -> None:

        #ek.set_app_key("b055e8b439474a4fa4ce91c9e4f61b72b3891ab5") 
        self._aux = Aux()
        self._base_year = 2015

    def change_base(self,nominal_gdp, real_gdp, new_base_year):
        ''' 
            Description:
            This function changes the base with respect to which real values are computed.
            Data must be quarterly here.
        '''
        df = pd.merge(nominal_gdp["value"], real_gdp["value"], left_index=True, right_index=True)
        df.columns = ["real", "nominal"]

        a_df = df.groupby(df.index.year).sum()
        factor = a_df.at[new_base_year,"nominal"]/(a_df.at[new_base_year, "real"])
        df["new_real"] = df["real"]*factor
        return df
    
    def euro_gdp(self, NOMINAL_OR_REAL):
        '''
            Description:
            This function takes output (GDP) data from FRED for the Euroz zone. To do so, I use the FRED API by means of a function
            called "fetch_fred_data" saved in the Aux class. 

            Source: FRED.

            Returns: 
            It saves a file called "euro_gdp.csv". This output contains the following columns: 
                – year: The year in wich the value is measured.
                – country: The country the value is corresponding to.
                - freq: The frequency at which the data is calculated.
                - unit: The unit of measure (meur = Million Euro)
                – var: The variable the value is measuring (gdp).
                - value: The value.
                - base: it contains the base with respect to which real gdp is calculated. In the case of nominal
                gdp I just add a nan.
        '''

        gdp = {}
        # country,value,freq,unit,var,year,quarter,month
        if NOMINAL_OR_REAL.lower() == "real":
            gdp_unit_code = "CLV_I10"
            gdp_unit = "bclv"
            gdp_base = 2010
        elif NOMINAL_OR_REAL.lower() == "nominal":
            gdp_unit_code = "CP_MEUR"
            gdp_unit = "beur" # I will divide the number by 1000, because Eurostad gives the datsa in million euros
            gdp_base = np.nan
        else:
            raise("We only account for real or nominal GDP.")
        
        # Load the codes for the FRED database
        codes = pd.read_csv("data/fred_gdp_codes.csv")
        codes = codes[codes.country=="EA19"]
        # Take the gdp dataset
        macro_var = codes[codes["var"]==NOMINAL_OR_REAL.lower() + "_gdp"]["code"].values[0]
        gdp = self.aux.fetch_fred_data(macro_var).div(1e3)
        gdp.index = [pd.Period(date,freq="Q") for date in gdp.index]
        gdp.index.name = "date"
        # Add info vars
        gdp["freq"] = "q"
        gdp["unit"] = gdp_unit
        gdp["var"] = NOMINAL_OR_REAL + "_gdp"
        gdp["base"] = gdp_base
        gdp["year"] = gdp.index.year
        gdp["quarter"] = gdp.index.quarter
        gdp["month"] = gdp.quarter*3
        gdp["country"] = "EA19"

        gdp.to_csv("data/euro/euro_" + NOMINAL_OR_REAL  + "_gdp_base" + str(gdp_base) + ".csv")
        return gdp

    def us_gdp(self, NOMINAL_OR_REAL):
        '''
            Description:
            This function takes output (GDP) data from FRED for the US. To do so, I use the FRED API by means of a function
            called "fetch_fred_data" saved in the Aux class. 

            Source: FRED.

            Returns: 
            It saves two files called "us_gdp.csv". This output contains the following columns: 
                – year: The year in wich the value is measured.
                – country: The country the value is corresponding to.
                - freq: The frequency at which the data is calculated.
                - unit: The unit of measure (beur = Billions of Euros in the case of nominal GDP and bclv = Billions of chained
                X Dollars, where X is the base)
                – var: The variable the value is measuring (gdp).
                - value: The value.
                - base: it contains the base with respect to which real gdp is calculated. In the case of nominal
                gdp I just add a nan.

        '''
        # country,value,freq,unit,var,year,quarter,month
        if NOMINAL_OR_REAL.lower() == "real":
            gdp_unit_code = "CLV_I12"
            gdp_unit = "bclv"
            gdp_base = 2012
        elif NOMINAL_OR_REAL.lower() == "nominal":
            gdp_unit_code = "CP_BUSD"
            gdp_unit = "beur"
            gdp_base = np.nan
        else:
            raise("We only account for real or nominal GDP.")
        
        # Load the codes for the FRED database
        codes = pd.read_csv("data/fred_gdp_codes.csv")
        codes = codes[codes.country=="US"]
        # Take the gdp dataset
        macro_var = codes[codes["var"]==NOMINAL_OR_REAL.lower() + "_gdp"]["code"].values[0]
        gdp = self.aux.fetch_fred_data(macro_var)
        gdp.index = [pd.Period(date,freq="Q") for date in gdp.index]
        gdp.index.name = "date"
        # Add info vars
        gdp["freq"] = "q"
        gdp["unit"] = gdp_unit
        gdp["var"] = NOMINAL_OR_REAL + "_gdp"
        gdp["base"] = gdp_base
        gdp["year"] = gdp.index.year
        gdp["quarter"] = gdp.index.quarter
        gdp["month"] = gdp.quarter*3
        gdp["country"] = "US"

        # Save them:
        gdp.to_csv("data/us/us_" + NOMINAL_OR_REAL + "_gdp.csv")
        return gdp

    def euro_output_gap(self):
        '''
            Description:
            This function constructs a dataset for the Output gaps, i.e., deviations of actual GDP from potential GDP as % of potential GDP.

            Source: Manual computation using GDP and GDPPOT from the FRED

            Parameters: None

            Returns: 
 
        '''
        # LOAD GDP
        if self.aux.file_exists(self.aux.euro_folder, "euro_real_gdp"):
            gdp = pd.read_csv(self.aux.euro_folder + "euro_real_gdp.csv", index_col="date")
            gdp.index = [pd.Period(date,freq="Q") for date in gdp.index]
        else:
            gdp = self.us_gdp()
        # LOAD GDPPOT
        if self.aux.file_exists(self.aux.euro_folder, "euro_gdppot"):
            gdppot = pd.read_csv(self.aux.euro_folder + "euro_gdppot.csv", index_col="date")
            gdppot.index = [pd.Period(date,freq="Q") for date in gdppot.index]
        else:
            gdppot = self.us_gdppot()

        output_gap = (gdp.value).apply(np.log)
        output_gap -= (gdppot.value).apply(np.log)
        output_gap *=100 #( (df.GDPC1 - df.GDPPOT) / df.GDPPOT ) * 100
        output_gap = output_gap.to_frame()
        output_gap.columns = ["value"]
        #year,country,value,var,full_name,freq,unit
        output_gap["year"] = output_gap.index.year
        output_gap["country"] = "EA19"
        output_gap["var"] = "GAP"
        output_gap["full_name"] = "Output gap as a percentage of potential GDP"
        output_gap["freq"] = "q"
        output_gap["unit"] = "percentage"
        output_gap["base"] = self.base_year
        output_gap["year"] = gdp.index.year
        output_gap["quarter"] = gdp.index.quarter
        output_gap["month"] = gdp.quarter*3
        output_gap.to_csv("data/euro/euro_output_gap.csv")
        return output_gap

    def us_output_gap(self):
        # LOAD GDP
        if self.aux.file_exists(self.aux.us_folder, "us_real_gdp"):
            gdp = pd.read_csv(self.aux.us_folder + "us_real_gdp.csv", index_col="date")
            gdp.index = [pd.Period(date,freq="Q") for date in gdp.index]
        else:
            gdp = self.us_gdp()
        # LOAD GDPPOT
        if self.aux.file_exists(self.aux.us_folder, "us_gdppot"):
            gdppot = pd.read_csv(self.aux.us_folder + "us_gdppot.csv", index_col="date")
            gdppot.index = [pd.Period(date,freq="Q") for date in gdppot.index]
        else:
            gdppot = self.us_gdppot()

        output_gap = (gdp.value).apply(np.log)
        output_gap -= (gdppot.value).apply(np.log)
        output_gap *=100 #( (df.GDPC1 - df.GDPPOT) / df.GDPPOT ) * 100
        output_gap = output_gap.to_frame()
        output_gap.columns = ["value"]
        #year,country,value,var,full_name,freq,unit
        output_gap["year"] = output_gap.index.year
        output_gap["country"] = "US"
        output_gap["var"] = "GAP"
        output_gap["full_name"] = "Output gap as a percentage of potential GDP"
        output_gap["freq"] = "q"
        output_gap["unit"] = "percentage"
        output_gap["base"] = 2010
        output_gap["year"] = gdp.index.year
        output_gap["quarter"] = gdp.index.quarter
        output_gap["month"] = gdp.quarter*3
        output_gap.to_csv("data/us/us_output_gap.csv")
        return output_gap

    def euro_gdppot(self):
        df = pd.read_csv("data/euro/raw/AMECO6.TXT", sep=";")
        df = df[df["SUB-CHAPTER"]=="05 Potential gross domestic product at constant prices"]
        df = df[df["COUNTRY"]=="Euro area (19 countries)"]
        df = df[df["TITLE"] == "Potential gross domestic product at 2015 reference levels "]
        df = df.drop(columns=["CODE", "COUNTRY", "SUB-CHAPTER", "TITLE", "UNIT"])

        df.index = ["value"]
        df = df.astype("float")
        df = df.T.iloc[:-1]
        df.index = [pd.Period(date,freq="Y") for date in df.index]
        df.index.name = "date"
        df = df.dropna()
        # GDPPOT:
        gdppot = (df.resample("Q").interpolate()).div(4)
        gdppot["country"] = "EA19"
        gdppot["freq"] = "q"
        gdppot["unit"] = "meur"
        gdppot["var"]  = "gdppot"
        gdppot["base"]  = 2015
        gdppot["year"] = gdppot.index.year
        gdppot["month"] = gdppot.index.month
        gdppot["quarter"] = gdppot.index.quarter
        gdppot.to_csv("data/euro/euro_gdppot.csv")
        return gdppot
    
    def us_gdppot(self):

        # Load the codes for the FRED database
        codes = pd.read_csv("data/fred_gdp_codes.csv")
        codes = codes[codes.country=="US"]
        # Take the gdp dataset
        macro_var = codes[codes["var"]=="gdppot"]["code"].values[0]
        gdppot = self.aux.fetch_fred_data(macro_var)
        gdppot.index = [pd.Period(date,freq="Q") for date in gdppot.index]
        gdppot.index.name = "date"
        # Add info vars
        gdppot["freq"] = "q"
        gdppot["unit"] = "bclv"
        gdppot["var"] = "gdppot"
        gdppot["base"] = 2012
        gdppot["year"] = gdppot.index.year
        gdppot["quarter"] = gdppot.index.quarter
        gdppot["month"] = gdppot.quarter*3
        gdppot["country"] = "US"
        # Save them:
        gdppot.to_csv("data/us/us_gdppot.csv")
        return gdppot

    def gdp(self, country):
        if country.lower() == 'us': 
            self.us_gdp("nominal")
            self.us_gdp("real")
        elif ('eu' in country.lower()) | ('ea' in country.lower()): 
            nominal_gdp = self.euro_gdp("nominal")
            real_gdp = self.euro_gdp("real")
            df = self.change_base(nominal_gdp, real_gdp, self.base_year)
            real_gdp["value"] = df["new_real"]
            real_gdp["base"] = self.base_year
            real_gdp.to_csv("data/euro/euro_real_gdp.csv")
        else: raise ValueError("Invalid country")

    def gdppot(self, country):
        #print(50*"-")
        #tic = self.aux.initiate_timer("Building potential output.csv\n")
        if country.lower() == 'us': self.us_gdppot()
        elif ('eu' in country.lower()) | ('ea' in country.lower()): self.euro_gdppot()
        else: raise ValueError("Invalid country")
        #print("\n")
        #toc = self.aux.end_timer(tic)
        #print(50*"-")

    def output_gap(self, country):
        if country.lower() == 'us': self.us_output_gap()
        elif ('eu' in country.lower()) | ('ea' in country.lower()): self.euro_output_gap()
        else: raise ValueError("Invalid country")
    
    def macro_code(self, _freq):
        if (_freq.lower() == "a") or (_freq.lower() == "annual"):
            _macro_code = 'NAMA_10_GDP'
        elif (_freq.lower() == "q") or (_freq.lower() == "quarterly"):
            _macro_code = 'NAMQ_10_GDP'
        return _macro_code.lower()
        
    @property
    def freq(self):
        if (self._freq.lower() == "a") or (self._freq.lower() == "annual"):
            _freq = 'a'
        elif (self._freq.lower() == "q") or (self._freq.lower() == "quarterly"):
            _freq = 'q'
        return _freq
    
    @property
    def transf(self):
        return ["level", "log"]
    
    @property
    def aux(self):

        return self._aux
    
    @property
    def countries(self):
        ''' I provide here a (sub)list of (the top 4) country codes (EUROSTAT) plus the US'''
        _countries = [
            'ES',   # Spain
            'FR',   # France  
            'DE',   # Germany
            'IT',   # Italy
            'EA19',  # Euro Zone
            'EA20']

        return _countries + ["US"]
    
    @property
    def base_year(self):
        return self._base_year

