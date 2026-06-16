import click
from ebm3_sterodynamics.ebm3_oceandynamics_project import (
    ebm3_oceandynamics_project_fn,
)
from ebm3_sterodynamics.ebm3_thermalexpansion_project import (
    ebm3_thermalexpansion_project_fn
)

@click.command()
@click.option("--scenario", 
              help="SSP scenario (ie. 'ssp585')",
              default='ssp585',
              show_default=True,
              type=str)
@click.option("--nsamps",
              help = "Number of samples to generate",
              default=20000,
              show_default=True,
              type=int)
@click.option("--seed",
              help="Seed value for random number generator",
              type=int,
              default=1234,
              show_default=True)
@click.option(
    "--pyear-start",
    envvar="BAMBER19_ICESHEETS_PYEAR_START",
    help="Projection year start",
    default=2020,
    type=click.IntRange(min=2020),
    show_default=True,
)
@click.option(
    "--pyear-end",
    help="Projection year end",
    default=2100,
    type=click.IntRange(max=2300),
    show_default=True,
)
@click.option(
    "--pyear-step",
    help="Projection year step",
    default=10,
    show_default=True,
    type=click.IntRange(min=1),
)
@click.option(
    "--baseyear",
    help="Year to which projections are referenced",
    default=2000,
    show_default=True,
    type=int,
)
@click.option(
    "--location-file",
    help="Path to file that contains name, id, lat, and lon of points for localization",
    required=True,
    type=str,
)
@click.option(
    "--pipeline-id",
    help="Unique identifier for this instance of the module.",
    required=False,
    type=str,
)
@click.option(
    "--climate-data-file",
    default=None,
    help="NetCDF4/HDF5 file containing surface temperature data",
)
@click.option(
    "--rfmip",
    help="rfmip file",
    default = "ebm3_project_data/rfmip-radiative-forcing-annual-means-v4-0-0.csv",
    show_default=True,
    type=str,
)
@click.option(
    "--oceandynamics-params-file",
    help = "CMIP6 params csv",
    default= "ebm3_project_data/4xCO2_cummins_ebm3_cmip6.csv",
    type=str,
    show_default=True
)
@click.option(
    "--zosdir",
    help="Path to CMIP6 ZOS directory",
    default="cmip6/zos/",
    type=str,
    show_default=True  
)
@click.option(
    "--output-lslr-file",
    help="Path to the initial local output file",
    default=None,
    type=str,
)
@click.option(
   "--output-lslr-quantile-file",
    help="Path to the initial local quantile file",
    default=None,
    type=str,
)
@click.option(
    "--thermal-expansion-params-file",
    help="Full path to the calibrated constrains params file",
    default = "calibrated_constraints_paramters.csv",
    show_default=True,
    type=str,
)
@click.option(
    "--coef-file",
    help= "Full path to expansion coefficient file",
    default = "scmpy3LM_RCMIP_CMIP6calpm_n18_expcoefs.nc",
    show_default=True,
    type=str,
)
@click.option(
    "--output-gslr-file",
    help="Path to the output file for global sea-level rise",
    default=None,
    type=str,
)
def main(
    scenario,
    nsamps,
    seed,
    pyear_start,
    pyear_end,
    pyear_step,
    baseyear,
    location_file,
    pipeline_id,
    climate_data_file,
    rfmip,
    oceandynamics_params_file,
    coef_file,
    thermal_expansion_params_file,
    zosdir,
    output_lslr_file,
    output_lslr_quantile_file,
    output_gslr_file
):
    ebm3_thermalexpansion_project_fn(
        scenario=scenario,
        climate_data_file=climate_data_file,
        params_file=thermal_expansion_params_file,
        coef_file=coef_file,
        nsamps = nsamps,
        pyear_start = pyear_start,
        pyear_end = pyear_end,
        pyear_step = pyear_step,
        baseyear=baseyear,
        seed=seed,
        pipeline_id=pipeline_id,
        global_sl_out_file=output_gslr_file
    )
    click.echo("Thermal expansion projections completed.")

    #writes initial local output and local quantile output files
    ebm3_oceandynamics_project_fn(
        scenario = scenario,
        nsamps = nsamps,
        seed = seed,
        pyear_start = pyear_start,
        pyear_end = pyear_end,
        pyear_step = pyear_step,
        baseyear = baseyear,
        location_file = location_file,
        pipeline_id = pipeline_id,
        climate_data_file = climate_data_file,
        rfmip = rfmip,
        params = oceandynamics_params_file,
        zosdir = zosdir,
        global_sl_out_file=output_gslr_file,
        lslr_out_file=output_lslr_file,
        lslr_quantile_out_file=output_lslr_quantile_file
    )
    click.echo("Oceandynamics projections completed.")
    


