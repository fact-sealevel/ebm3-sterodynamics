# Thermal expansion projections for PROTECT
# Victor Malagon Santos, 17.06.2024

# import os
import numpy as np

# import netCDF4 as nc
import pandas as pd
import time
import xarray as xr
# from netCDF4 import Dataset
# import pickle
# import sys
# import re
# import argparse


class ProjectionError(Exception):
    pass


def ebm3_thermalexpansion_project(
    scenario,
    climate_data_file,
    params_file,
    coef_file,
    pyear_start,
    pyear_end,
    pyear_step,
    nsamps,
    pipeline_id,
    seed,
    baseyear,
    global_sl_out_file,
):
    # constants
    a = 6.37 * 1e6
    earth_area = 4 * np.pi * a**2

    # path = os.path.dirname(__file__)

    # heat capacity of each layer from fair2. Needed to compute OHC
    fparam = pd.read_csv(params_file)
    c1 = fparam["clim_c1"]
    c2 = fparam["clim_c2"]
    c3 = fparam["clim_c3"]
    nsims = 1001

    rng = np.random.default_rng(seed)
    if nsamps > nsims:
        run_idx = np.arange(nsims)
        sample_idx = rng.choice(nsims, nsamps, nsamps > nsims)
    else:
        run_idx = rng.choice(nsims, nsamps, nsamps > nsims)
        sample_idx = np.arange(nsamps)

    c1 = c1[sample_idx]
    c2 = c2[sample_idx]
    c3 = c3[sample_idx]
    # create target years array
    targyears = np.arange(pyear_start, pyear_end + 1, pyear_step)

    # temperature output from fair2. Needed t compute OHC
    climate_ds = xr.open_dataset(climate_data_file, group=scenario)
    print("climate ds coords: ", climate_ds.coords)
    gsat = climate_ds["surface_temperature"].data
    deepoceant = climate_ds["deep_ocean_temperature"].data
    years = climate_ds["years"].data

    #   Expansion coefficients. Needed to to convert OCH to global thermal expansion (GTE)
    # ds = Dataset(coef_file)
    expansion_coef_ds = xr.open_dataset(coef_file)
    include_models = expansion_coef_ds["model"].data
    eeh3 = expansion_coef_ds["expcoefs"].data  # [:]
    # include_models = ds['model'][:]
    # eeh3 = ds['expcoefs'][:]

    # estimate OHC
    up = gsat * np.array(c1)
    mid = deepoceant[:, :, 0] * np.array(c2)
    low = deepoceant[:, :, 1] * np.array(c3)
    n = np.zeros((len(years), nsamps))
    n[1:, :] = (
        up[1:, :] - up[:-1, :] + mid[1:, :] - mid[:-1, :] + low[1:, :] - low[:-1, :]
    )
    ohc_samps = np.cumsum(n * earth_area, 0) * 365 * 24 * 3.6 * 1e3 * 1e-24

    # Generate samples assuming normal distribution
    rng = np.random.default_rng(seed)
    expcoef_samps = rng.normal(loc=np.mean(eeh3), scale=np.std(eeh3), size=(nsamps, 1))

    # Produce the projection samples
    gte_samps = ohc_samps * expcoef_samps.flatten()

    # Center these samples on the baseyear
    baseyear_idx = np.flatnonzero(years == baseyear)
    gte_samps = gte_samps - gte_samps[baseyear_idx, :]

    # Subset the samples for the projection years
    targyear_idx = np.isin(years, targyears)
    gte_samps = gte_samps[targyear_idx, :]

    # Invert the dimensions of the variable and convert from m to mm
    gte_samps *= 1000.0
    gte_samps = gte_samps.T

    # Save the projections to a pickle
    # output = {"thermsamps": gte_samps, "targyears": targyears, "baseyear": baseyear, \
    # "include_models": include_models, "scenario": scenario}
    # outfile = open(os.path.join(os.path.dirname(__file__), "{}_projections.pkl".format(pipeline_id)), 'wb')
    # pickle.dump(output, outfile)
    # outfile.close()
    # Write the total global projections to a netcdf file
    ds_out = xr.Dataset(
        {
            "sea_level_change": xr.DataArray(
                gte_samps[:, :, np.newaxis].astype("f4"),
                dims=["samples", "years", "locations"],
                attrs={"units": "mm"},
            )
        },
        coords={
            "years": ("years", targyears.astype("i4")),
            "samples": ("samples", np.arange(nsamps, dtype="i8")),
            "locations": ("locations", np.array([-1], dtype="i8")),
            #"lat": ("locations", np.array([np.inf], dtype="f4")),
            #"lon": ("locations", np.array([np.inf], dtype="f4")),
        },
        attrs={
            "description": "Global SLR contribution from Thermal Expansion according to Three-Layer Model workflow",
            "history": "Created " + time.ctime(time.time()),
            "source": "FACTS: {0}".format(pipeline_id),
            "scenario": scenario,
            "baseyear": baseyear,
            "comment": "Included Models: " + ",".join([str(x) for x in include_models]),
        },
    )
    ds_out.to_netcdf(
        global_sl_out_file,
        encoding={"sea_level_change": {"zlib": True, "complevel": 4}},
    )
    # return(0)


def ebm3_thermalexpansion_project_fn(
    scenario,
    climate_data_file,
    params_file,
    coef_file,
    nsamps,
    pyear_start,
    pyear_end,
    pyear_step,
    baseyear,
    seed,
    pipeline_id,
    global_sl_out_file,
):
    ebm3_thermalexpansion_project(
        scenario=scenario,
        climate_data_file=climate_data_file,
        coef_file=coef_file,
        params_file=params_file,
        nsamps=nsamps,
        pyear_start=pyear_start,
        pyear_end=pyear_end,
        pyear_step=pyear_step,
        baseyear=baseyear,
        seed=seed,
        pipeline_id=pipeline_id,
        global_sl_out_file=global_sl_out_file,
    )
