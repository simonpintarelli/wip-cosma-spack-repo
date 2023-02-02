# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TiledMm(CMakePackage, CudaPackage, ROCmPackage):
    """Matrix multiplication on GPUs for matrices stored on a CPU. Similar to cublasXt, but ported to both NVIDIA and AMD GPUs."""

    homepage =  "https://github.com/eth-cscs/Tiled-MM/"
    url = "https://github.com/eth-cscs/Tiled-MM/archive/refs/tags/v2.0.tar.gz"
    git = "https://github.com/eth-cscs/Tiled-MM.git"

    version("master", branch="master")
    version("2.0", sha256="ea554aea8c53d7c8e40044e6d478c0e8137d7e8b09d7cb9650703430d92cf32e")

    variant("shared", default=True)
    variant("examples", default=False)

    depends_on('rocblas', when='+rocm')

    conflicts('~cuda~rocm')

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("TIELDMM_WITH_EXAMPLES", "examples"),
        ]

        if "+rocm" in self.spec:
            args.extend([self.define("TILED_MM_GPU_BACKEND", "ROCM")])

        if "+cuda" in self.spec:
            args.extend([self.define("TILED_MM_GPU_BACKEND", "CUDA")])

        return args