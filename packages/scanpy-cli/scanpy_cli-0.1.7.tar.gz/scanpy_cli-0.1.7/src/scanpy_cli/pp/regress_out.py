import rich_click as click
import scanpy as sc
import sys


@click.command()
@click.argument("keys", required=True)
@click.option(
    "--layer", "-l", help="If provided, which element of layers to regress on."
)
@click.option(
    "--n-jobs", "-j", type=int, help="Number of jobs for parallel computation."
)
@click.option(
    "--input-file",
    "-i",
    required=True,
    help="Input h5ad file containing AnnData object.",
)
@click.option(
    "--output-file",
    "-o",
    required=True,
    help="Output h5ad file to save the processed AnnData object.",
)
def regress_out(keys, layer, n_jobs, input_file, output_file):
    """Regress out (mostly) unwanted sources of variation.

    Uses simple linear regression. This is inspired by Seurat's regressOut function in R.
    Note that this function tends to overcorrect in certain circumstances.

    KEYS: Keys for observation annotation on which to regress. Can be a comma-separated list.
    """
    try:
        # Parse comma-separated keys if provided
        keys_list = keys.split(",")

        # Load the AnnData object
        adata = sc.read_h5ad(input_file)

        # Call scanpy's regress_out function
        sc.pp.regress_out(adata, keys=keys_list, layer=layer, n_jobs=n_jobs)

        # Save the result
        adata.write(output_file)

        click.echo(
            f"Successfully regressed out {keys} from data and saved to {output_file}"
        )
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
