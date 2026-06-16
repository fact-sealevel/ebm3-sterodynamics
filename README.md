# ebm3-sterodynamics

This module is based on the [ebm3/sterodynamics](https://github.com/radical-collaboration/facts/tree/development/modules/ebm3/sterodynamics) module of [FACTS1](https://github.com/radical-collaboration/facts/tree/development/modules/ebm3/sterodynamics). 

## Example

This application can run on emissions-projected climate data generated from the [fair2-climate](https://github.com/fact-sealevel/fair2-climate) module in the FACTS2 framework which is based on the Finite Amplitude Impulse Response (FaIR) v2 [model](https://docs.fairmodel.net/en/stable/intro.html). 

### Setup

From your project root, create directories to hold input and output data and download the input data required to run this module. 

```shell
mkdir -p ./data/input
# download data
curl -sL https://zenodo.org/records/16024082/files/tlm_sterodynamics_cmip6_ebm3_data.tgz | tar -zx -C ./data/input
curl -sL https://zenodo.org/records/11506798/files/ebm3_thermal_expansion_data.tgz | tar -zx -C ./data/input

#make dir for output data
mkdir -p ./data/output
```

>[!IMPORTANT]
> This module **requires** a `climate.nc` file that is the output of the FACTS2 [fair2-climate](https://github.com/fact-sealevel/fair2-climate) module, which is created outside of this prototype. See the example in this repository's README to run the module and create the output file. Before running this example, manually move the file into `./data/input` and ensure that the filename matches that passed to `climate-file`. The number of samples (`--nsamps`) drawn in the FAIR run must pass the number of samples specified in this run. 

Run the application in a container based on the image published in the container registry. Note that the number of samples in the FAIR `climate.nc` file passed must match the `--nsamps` argument.
```shell
docker run --rm \
-v ./data/input:/mnt/data_in:ro \
-v ./data/output_for_ebm:/mnt/data_out \
ebm3-sterodynamics:package \
--scenario 'ssp585' \
--nsamps 1000 \
--seed 1234 \
--pyear-start 2020 \
--pyear-end 2150 \
--pyear-step 10 \
--baseyear 2005 \
--location-file /mnt/data_in/location.lst \
--pipeline-id aaa \
--climate-data-file /mnt/data_in/climate_1000.nc \
--rfmip /mnt/data_in/ebm3_project_data/rfmip-radiative-forcing-annual-means-v4-0-0.csv \
--oceandynamics-params-file /mnt/data_in/ebm3_project_data/4xCO2_cummins_ebm3_cmip6.csv \
--zosdir /mnt/data_in/cmip6/zos/ \
--coef-file /mnt/data_in/ebm3_project_data/scmpy3LM_RCMIP_CMIP6calpm_n18_expcoefs.nc \
--thermal-expansion-params-file /mnt/data_in/ebm3_project_data/calibrated_constrained_parameters.csv \
--output-gslr-file /mnt/data_out/gslr.nc \
--output-lslr-file /mnt/data_out/lslr.nc \
--output-lslr-quantile-file /mnt/data_out/lslr_quantile.nc
```

## Features
```shell
Usage: ebm3-sterodynamics [OPTIONS]

Options:
  --scenario TEXT                 SSP scenario (ie. 'ssp585')  [default:
                                  ssp585]
  --nsamps INTEGER                Number of samples to generate  [default:
                                  20000]
  --seed INTEGER                  Seed value for random number generator
                                  [default: 1234]
  --pyear-start INTEGER RANGE     Projection year start  [default: 2020;
                                  x>=2020]
  --pyear-end INTEGER RANGE       Projection year end  [default: 2100;
                                  x<=2300]
  --pyear-step INTEGER RANGE      Projection year step  [default: 10; x>=1]
  --baseyear INTEGER              Year to which projections are referenced
                                  [default: 2000]
  --location-file TEXT            Path to file that contains name, id, lat,
                                  and lon of points for localization
                                  [required]
  --pipeline-id TEXT              Unique identifier for this instance of the
                                  module.
  --climate-data-file TEXT        NetCDF4/HDF5 file containing surface
                                  temperature data
  --rfmip TEXT                    rfmip file  [default:
                                  ebm3_project_data/rfmip-radiative-forcing-
                                  annual-means-v4-0-0.csv]
  --oceandynamics-params-file TEXT
                                  CMIP6 params csv  [default: ebm3_project_dat
                                  a/4xCO2_cummins_ebm3_cmip6.csv]
  --zosdir TEXT                   Path to CMIP6 ZOS directory  [default:
                                  cmip6/zos/]
  --init-local-out-file TEXT      Path to the initial local output file
  --init-local-quantile-file TEXT
                                  Path to the initial local quantile file
  --thermal-expansion-params-file TEXT
                                  Full path to the calibrated constrains
                                  params file  [default:
                                  calibrated_constraints_paramters.csv]
  --coef-file TEXT                Full path to expansion coefficient file
                                  [default:
                                  scmpy3LM_RCMIP_CMIP6calpm_n18_expcoefs.nc]
  --output-gslr-file TEXT         Path to the output file for global sea-level
                                  rise
  --help                          Show this message and exit.
```

See this help documentation by passing the --help flag when running the application, for example:
```shell
docker run --rm ebm3-sterodynamics --help
```

## Build the container locally
You can build the container with Docker by running the following command from the repository root:

```shell
docker build -t ebm3-sterodynamics .
```

## Results
This module writes a global SLR contribution projection NetCDF file. Optionally, it also writes projections of contribution to local relative sea level.

## Support 
Source code is available online at https://github.com/fact-sealevel/ebm3-sterodynamics. This software is open source, available under the MIT license.

Please file issues in the issue tracker at https://github.com/fact-sealevel/ebm3-sterodynamics/issues.
