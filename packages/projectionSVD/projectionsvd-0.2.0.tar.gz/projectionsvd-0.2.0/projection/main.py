"""
projectionSVD.
Main caller.
"""

__author__ = "Jonas Meisner"

# Libraries
import argparse
import os
import sys

### Argparse
parser = argparse.ArgumentParser(prog="projectionSVD")
parser.add_argument("--version", action="version",
	version="%(prog)s v0.2.0")
parser.add_argument("-b", "--bfile", metavar="PLINK",
	help="Prefix for target PLINK files (.bed, .bim, .fam)")
parser.add_argument("-s", "--eigvals", metavar="FILE",
	help="File path to eigenvalues")
parser.add_argument("-v", "--loadings", metavar="FILE",
	help="File path to SNP loadings")
parser.add_argument("-f", "--freqs", metavar="FILE",
	help="File path to discovery allele frequencies from PLINK")
parser.add_argument("-t", "--threads", metavar="INT", type=int, default=1,
	help="Number of threads (1)")
parser.add_argument("-o", "--out", metavar="OUTPUT", default="projection",
	help="Prefix output name")
parser.add_argument("--batch", metavar="INT", type=int, default=8192,
	help="Mini-batch size for projection (8192)")
parser.add_argument("--freqs-col", metavar="INT", type=int, default=6,
	help="Column number for frequencies (.afreq)")
parser.add_argument("--raw", action="store_true",
	help="Only output projections without FID/IID")



##### projectionSVD #####
def main():
	args = parser.parse_args()
	if len(sys.argv) < 2:
		parser.print_help()
		sys.exit()
	print("-----------------------")
	print(f"projectionSVD v0.2.0")
	print("by J. Meisner")
	print("-----------------------\n")

	# Check input
	assert args.bfile is not None, "No input data (--bfile)!"
	assert args.eigvals is not None, "No eigenvalues provided (--eigvals)!"
	assert args.loadings is not None, "No SNP loadings provided (--loadings)!"
	assert args.freqs is not None, "No allele frequencies provided (--freqs)!"
	assert args.threads > 0, "Please select a valid number of threads!"
	assert args.batch > 0, "Please select a valid value for batch size!"
	assert args.freqs_col >= 0, "Please select a valid value for freq column!"

	# Control threads of external numerical libraries
	os.environ["MKL_NUM_THREADS"] = str(args.threads)
	os.environ["MKL_MAX_THREADS"] = str(args.threads)
	os.environ["OMP_NUM_THREADS"] = str(args.threads)
	os.environ["OMP_MAX_THREADS"] = str(args.threads)
	os.environ["NUMEXPR_NUM_THREADS"] = str(args.threads)
	os.environ["NUMEXPR_MAX_THREADS"] = str(args.threads)
	os.environ["OPENBLAS_NUM_THREADS"] = str(args.threads)
	os.environ["OPENBLAS_MAX_THREADS"] = str(args.threads)

	# Load numerical libraries
	import numpy as np
	from math import ceil
	from projection import functions
	from projection import shared

	### Read and prepare data
	# Reading PLINK files
	assert os.path.isfile(f"{args.bfile}.bed"), "bed file doesn't exist!"
	assert os.path.isfile(f"{args.bfile}.bim"), "bim file doesn't exist!"
	assert os.path.isfile(f"{args.bfile}.fam"), "fam file doesn't exist!"
	assert os.path.isfile(f"{args.eigvals}"), "eigvals file doesn't exist!"
	assert os.path.isfile(f"{args.loadings}"), "loadings file doesn't exist!"
	assert os.path.isfile(f"{args.freqs}"), "freqs file doesn't exist!"
	print("Reading data...", end="", flush=True)
	G, M, N = functions.readPlink(args.bfile)
	print(f"\rLoaded {N} samples and {M} SNPs.\n")

	# Load smaller inputs
	S = np.genfromtxt(args.eigvals, dtype=float)
	V = np.genfromtxt(args.loadings, dtype=float)
	f = np.genfromtxt(args.freqs, dtype=float, usecols=(args.freqs_col-1))
	assert S.shape[0] == V.shape[1], "Files doesn't match!"
	assert V.shape[0] == M, "Number of sites doesn't match (--loadings)!"
	assert f.shape[0] == M, "Number of sites doesn't match (--freqs)!"
	K = S.shape[0]

	# Transform eigenvalues to singular values and multiply on V
	S = np.sqrt(S*M)
	V *= (1.0/S)
	del S

	# Specify denominator
	d = 1.0/np.sqrt(2*f*(1-f))

	### Perform projection
	print(f"Performing projection in batches of {args.batch} SNPs.")
	U = np.zeros((N, K))
	E = np.zeros((args.batch, N))

	# Standardize and project in batches
	L = ceil(M/args.batch)
	m = 0
	for l in range(L):
		print(f"\rBatch {l+1}/{L}", end="", flush=True)
		if l == (L-1): # Last batch
			E = np.zeros((M - m, N))
		shared.standardizeE(E, G, f, d, m)
		U += np.dot(E.T, V[m:(m + E.shape[0]),:])
		m += E.shape[0]
	print("")
	del G, E, V, f, d
	
	### Save projections to file
	if args.raw:
		np.savetxt(f"{args.out}.eigvecs", U, fmt="%.7f", delimiter="\t")
		print(f"\nSaved projected eigenvectors as {args.out}.eigvecs")
	else:
		F = np.loadtxt(f"{args.bfile}.fam", dtype=np.str_, usecols=[0,1])
		h = ["#FID", "IID"] + [f"PC{k}" for k in range(1, K+1)]
		U = np.hstack((F, np.round(U, 7)))
		np.savetxt(f"{args.out}.eigvecs", U, fmt="%s", delimiter="\t", header="\t".join(h), comments="")
		print(f"\nSaved projected eigenvectors as {args.out}.eigvecs")



##### Main exception #####
assert __name__ != "__main__", "Please use the 'projectionSVD' command!"
