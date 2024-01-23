{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/jmd290/biosc1540/blob/a02/a02.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "4ZMUY2AJv1OC"
      },
      "source": [
        "# Assignment 02\n",
        "\n",
        "**Due**: Jan 25 at 11:59 pm\n",
        "\n",
        "**Points**: 10\n",
        "\n",
        "In this assignment, we will explore a [real dataset](https://www.kaggle.com/competitions/lish-moa/overview) involving gene expression data and its change when cells are exposed to different drugs.\n",
        "This type of data is used to elucidate the drug's mechanism of action (MoA).\n",
        "\n",
        "You can find the documentation for the relevant pages:\n",
        "\n",
        "-   [numpy](https://numpy.org/doc/stable/)\n",
        "-   [pandas](https://pandas.pydata.org/docs/index.html)\n",
        "-   [matplotlib](https://matplotlib.org/)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "2wKi-zm5v1OE"
      },
      "source": [
        "## Setup\n",
        "\n",
        "The following cell is needed to setup your Jupyter Notebook.\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 4,
      "metadata": {
        "id": "jg6dFJIwv1OE"
      },
      "outputs": [],
      "source": [
        "import numpy as np\n",
        "import pandas as pd\n",
        "import matplotlib.pyplot as plt"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "VkBRSL-0v1OF"
      },
      "source": [
        "## Problem 1\n",
        "\n",
        "Below, we have a URL stored in `CSV_PATH_FEATURES` that direct to a comma separated value (CSV) file.\n",
        "Use pandas to load the CSV file located at `CSV_PATH_FEATURES` into a DataFrame, and store the DataFrame in a variable named `df_feat`."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 5,
      "metadata": {
        "id": "M4KFvQMhv1OF"
      },
      "outputs": [],
      "source": [
        "CSV_PATH_FEATURES = \"https://gitlab.com/oasci/courses/pitt/biosc1540-2024s/-/raw/main/biosc1540/files/csv/moa_cancer/train_features.csv\""
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 6,
      "metadata": {
        "id": "RGKJAP1Fv1OF"
      },
      "outputs": [],
      "source": [
        "df_feat = pd.read_csv(CSV_PATH_FEATURES)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "W-yi7Y2sv1OG"
      },
      "source": [
        "We have the following information in our CSV file: features `g-` signify gene expression data, and `c-` signify cell viability data.\n",
        "`cp_type` indicates samples treated with a compound (`cp_vehicle`) or with a control perturbation (`ctrl_vehicle`); control perturbations have no MoAs; `cp_time` and `cp_dose` indicate treatment duration (24, 48, 72 hours) and dose (high or low)."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "zi_NxZfGv1OG"
      },
      "source": [
        "## Problem 2\n",
        "\n",
        "Drop the column `sig_id` from `df_feat` and store the resulting DataFrame in a variable called `df_feat_cleaned`.\n",
        "Be sure to not overwrite your `df_feat` variable."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 7,
      "metadata": {
        "id": "N0QvlVsCv1OG"
      },
      "outputs": [],
      "source": [
        "df_feat_cleaned = df_feat.drop(labels=[\"sig_id\"], axis=1)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "DvuXPVt1v1OG"
      },
      "source": [
        "## Problem 3\n",
        "\n",
        "Slice `df_feat_cleaned` using a boolean mask where `cp_time` is equal to `24` and store it in a new variable called `df_feat_sliced`."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 8,
      "metadata": {
        "id": "rjkLeIJ9v1OG"
      },
      "outputs": [],
      "source": [
        "mask = df_feat_cleaned[\"cp_time\"] == 24\n",
        "df_feat_sliced = df_feat_cleaned[mask]"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "yvzdFlQQv1OG"
      },
      "source": [
        "## Problem 4\n",
        "\n",
        "Using `df_feat_sliced`, create a variable named `cp_type_list` and assign it a list containing each unique value of `cp_type`.\n",
        "Hint: The length of your `cp_type_list` should be equal to `2`."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 9,
      "metadata": {
        "id": "w_5h_IRxv1OG"
      },
      "outputs": [],
      "source": [
        "cp_type_list = df_feat_sliced[\"cp_type\"].unique()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "LXHgWDA4v1OG"
      },
      "source": [
        "## Problem 5\n",
        "\n",
        "Using `df_feat_sliced`, store the data under column `g-0` in a NumPy array called `g_0_expression` and `g-1` in `g_1_expression`."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 10,
      "metadata": {
        "id": "7Ji3nnmDv1OH"
      },
      "outputs": [],
      "source": [
        "g_0_expression = df_feat_sliced['g-0'].to_numpy()\n",
        "g_1_expression = df_feat_sliced['g-1'].to_numpy()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "Oe45vxhev1OH"
      },
      "source": [
        "## Problem 6\n",
        "\n",
        "Create a dictionary named `g_stats` with keys `g-0` and `g-1`.\n",
        "Set the values for these keys to be empty dictionaries `{}`."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 11,
      "metadata": {
        "id": "v0R78W2Pv1OH"
      },
      "outputs": [],
      "source": [
        "g_stats = dict.fromkeys('g-0', 'g-1')"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "cxoAFO-dv1OH"
      },
      "source": [
        "Now, compute the following statistics and store them under their respective key.\n",
        "\n",
        "-   `mean` the mean\n",
        "-   `std`: standard deviation\n",
        "\n",
        "For example, compute the mean of `g_0_expression` and store it in `g-0`."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 12,
      "metadata": {
        "id": "nUuCLtfWv1OH"
      },
      "outputs": [],
      "source": [
        "g_stats['g-0'] = (g_0_expression.mean, g_0_expression.std)\n",
        "g_stats['g-1'] = (g_1_expression.mean, g_1_expression.std)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "ssTYGNYev1OH"
      },
      "source": [
        "## Problem 7\n",
        "\n",
        "Create a scatter plot with `g_0_expression` on the x-axis and `g_1_expression` on the y-axis."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 13,
      "metadata": {
        "id": "ypZBpMpKv1OH",
        "outputId": "074e4191-def3-4eeb-d5a4-187bf3c195d4",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 450
        }
      },
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 640x480 with 1 Axes>"
            ],
            "image/png": "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\n"
          },
          "metadata": {}
        }
      ],
      "source": [
        "fig, ax = plt.subplots(ncols=1, nrows=1)\n",
        "label_1 = \"g_0_expression\"\n",
        "label_2 = \"g_1_expression\"\n",
        "plt.scatter(\n",
        "    g_0_expression,\n",
        "    g_1_expression,\n",
        "    alpha=0.75,\n",
        "    color = 'green',\n",
        ")\n",
        "plt.xlabel(label_1)\n",
        "plt.ylabel(label_2)\n",
        "plt.show()"
      ]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "biosc1540-2024s-dev",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.11.7"
    },
    "colab": {
      "provenance": [],
      "include_colab_link": true
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}