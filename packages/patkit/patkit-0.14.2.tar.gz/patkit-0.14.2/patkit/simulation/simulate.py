#!/usr/bin/env python3
#
# Copyright (c) 2019-2025
# Pertti Palo, Scott Moisik, Matthew Faytak, and Motoki Saito.
#
# This file is part of the Phonetic Analysis ToolKIT
# (see https://github.com/giuthas/patkit/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# The example data packaged with this program is licensed under the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License. You should have received a
# copy of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License along with the data. If not,
# see <https://creativecommons.org/licenses/by-nc-sa/4.0/> for details.
#
# When using the toolkit for scientific publications, please cite the
# articles listed in README.md. They can also be found in
# citations.bib in BibTeX format.
#
"""
Simulate data and run metrics on it with plotting.

Original version was published for Ultrafest 2024.
"""

from functools import partial
from pathlib import Path

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from patkit.constants import SplineNNDsEnum, SplineShapesEnum
from patkit.metrics.calculate_spline_metric import (
    # spline_diff_metric,
    spline_nnd_metric, spline_shape_metric
)

from .contour_tools import generate_contour
from .metric_calculations import (
    Comparison, ComparisonSoundPair,
    calculate_metric_series_for_comparisons,
    calculate_metric_series_for_contours,
    get_distance_metric_baselines,
    get_shape_metric_baselines,
)
from .rays_on_contours import (
    distance_metric_rays_on_contours,
    shape_metric_rays_on_contours,
)
from .perturbation_series_plots import mci_perturbation_series_plot


def run_simulations(
    comparisons, contours, perturbations, save_path, sound_pairs
) -> None:
    """
    Main to create plots for the Ultrafest 2024 paper.
    """
    # TODO 0.15: these should run based on config
    annd_baselines, annd_results = simulate_dyadic_metrics(
        comparisons, contours, perturbations)
    mci_baselines, mci_results = simulate_single_contour_metrics(
        contours, perturbations)

    # TODO 0.15: RESULTS
    save_result_figures(annd_baselines, annd_results, contours, mci_baselines,
                        mci_results, perturbations, save_path, sound_pairs)


def save_result_figures(
        annd_baselines, annd_results, contours, mci_baselines, mci_results,
        perturbations, save_path, sound_pairs
):
    with PdfPages(save_path / "annd_contours.pdf") as pdf:
        distance_metric_rays_on_contours(contours=contours,
                                         metrics=annd_results,
                                         metric_name="ANND",
                                         baselines=annd_baselines,
                                         number_of_perturbations=len(
                                             perturbations),
                                         figsize=(10.1, 4.72),
                                         columns=sound_pairs,
                                         scale=200,
                                         color_threshold=[.1, -.1])
        # plt.show()
        plt.tight_layout()
        pdf.savefig(plt.gcf())
    with PdfPages(save_path / "mci_contours.pdf") as pdf:
        shape_metric_rays_on_contours(contours=contours,
                                      metrics=mci_results,
                                      metric_name="MCI/Baseline MCI",
                                      baselines=mci_baselines,
                                      number_of_perturbations=len(
                                          perturbations),
                                      figsize=(7, 3.35),
                                      scale=20,
                                      color_threshold=np.log10([2, .5]))
        # plt.show()
        plt.tight_layout()
        pdf.savefig(plt.gcf())
    # with PdfPages(save_path/"annd_1.pdf") as pdf:
    #     make_annd_perturbation_series_plot(annd_dict=annd_results, pdf=pdf)
    # with PdfPages(save_path/"annd_2.pdf") as pdf:
    #     make_annd_perturbation_series_plot_2(annd_dict=annd_results,
    #                                          annd_baseline=annd_baseline,
    #                                          pdf=pdf)
    # make_mpbpd_perturbation_series_plot(contour_1=contours['æ'],
    #                                     contour_2=contours['i'],
    #                                     steps=[1, 2, 5, 10])
    with PdfPages(save_path / "mci_timeseries.pdf") as pdf:
        perturbations = [-2, -1, -.5, .5, 1, 2]
        mci_perturbation_series_plot(contours=contours,
                                     perturbations=perturbations,
                                     figsize=(12, 8))
        # plt.show()
        # plt.tight_layout()
        pdf.savefig(plt.gcf())
    # make_demonstration_contour_plot(
    #     contour_1=contours['æ'], contour_2=contours['i'])


def simulate_dyadic_metrics(
        comparisons: list[Comparison],
        contours: dict[str, np.ndarray],
        perturbations: list[float],
) -> tuple[dict[Comparison, float], dict[Comparison, dict[str, np.ndarray]]]:

    annd_call = partial(spline_nnd_metric,
                        metric=SplineNNDsEnum.ANND,
                        timestep=1,
                        notice_base="Ultrafest 2024 simulation: "
                        )
    annd_results = calculate_metric_series_for_comparisons(
        metric=annd_call,
        contours=contours,
        comparisons=comparisons,
        perturbations=perturbations,
        interleave=True
    )
    annd_baselines = get_distance_metric_baselines(
        metric=annd_call, contours=contours)
    return annd_baselines, annd_results


def simulate_single_contour_metrics(
        contours: dict[str, np.ndarray],
        perturbations: list[float] | tuple[float],
) -> tuple[dict[Comparison, float], dict[str, dict[str, np.ndarray]]]:
    mci_call = partial(spline_shape_metric,
                       metric=SplineShapesEnum.MODIFIED_CURVATURE,
                       notice_base="Ultrafest 2024 simulation: "
                       )
    mci_results = calculate_metric_series_for_contours(
        metric=mci_call,
        contours=contours,
        perturbations=perturbations
    )
    mci_baselines = get_shape_metric_baselines(
        metric=mci_call,
        contours=contours,
    )
    return mci_baselines, mci_results


def setup_simulation():
    save_path = Path("ultrafest2024/")
    if not save_path.exists():
        save_path.mkdir()
    sounds = ['æ', 'i']
    contours = {
        sound: generate_contour(sound) for sound in sounds
    }
    perturbations = [-2, -1, -.5, .5, 1, 2]

    comparisons = [
        Comparison(first='æ', second='æ', perturbed='second'),
        Comparison(first='æ', second='æ', perturbed='first'),
        Comparison(first='i', second='i', perturbed='second'),
        Comparison(first='i', second='i', perturbed='first'),
        Comparison(first='æ', second='i', perturbed='second'),
        Comparison(first='æ', second='i', perturbed='first'),
        Comparison(first='i', second='æ', perturbed='second'),
        Comparison(first='i', second='æ', perturbed='first'),
    ]
    sound_pairs = [
        ComparisonSoundPair(first='æ', second='æ'),
        ComparisonSoundPair(first='i', second='i'),
        ComparisonSoundPair(first='æ', second='i'),
        ComparisonSoundPair(first='i', second='æ'),
    ]
    return comparisons, contours, perturbations, save_path, sound_pairs


def generate_sound_pairs(
         sounds: list[str]
) -> list[ComparisonSoundPair] | list[Comparison]:
    sound_pairs = [
        ComparisonSoundPair(first='æ', second='æ'),
        ComparisonSoundPair(first='i', second='i'),
        ComparisonSoundPair(first='æ', second='i'),
        ComparisonSoundPair(first='i', second='æ'),
    ]
    return sound_pairs
