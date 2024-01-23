{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "NjOZYpPavkrx"
      },
      "source": [
        "# Lecture 05 notebook\n",
        "\n",
        "**Date:** Jan 23, 2024\n",
        "\n",
        "## Learning objectives\n",
        "\n",
        "What you should be able to do after today's lecture.\n",
        "\n",
        "1.  🧮 Define linear regression, its limitations, and objective function.\n",
        "2.  🧮 Describe the purpose of loss functions in regression.\n",
        "3.  🐍 Understand the conversion of data from a DataFrame to NumPy arrays.\n",
        "4.  🐍 Develop hands-on programming skills for implementing regression in Python.\n",
        "5.  🧮 Interpret the coefficients obtained through optimization and evaluate the model's performance.\n",
        "6.  🐍 Visualize linear regression models and their fit to data.\n",
        "7.  🧮 Discuss practical considerations for model interpretation, assumptions, and limitations.\n",
        "\n",
        "## Readings\n",
        "\n",
        "Relevant content for today's lecture.\n",
        "\n",
        "-   [Plotting](../../../modules/intro/plotting/)\n",
        "-   [Regression](../../../modules/intro/regression/)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "pqIP8S9gvkrz"
      },
      "source": [
        "## Imports\n",
        "\n",
        "First, let's get all of our imports out of the way."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "VVvlXpjmvkrz"
      },
      "outputs": [],
      "source": [
        "import sys\n",
        "\n",
        "IN_COLAB = \"google.colab\" in sys.modules\n",
        "if IN_COLAB:\n",
        "    !pip install rdkit-pypi\n",
        "    !pip install py3dmol\n",
        "\n",
        "import numpy as np\n",
        "import pandas as pd\n",
        "import matplotlib.pyplot as plt\n",
        "from rdkit import Chem\n",
        "from rdkit.Chem import AllChem\n",
        "from rdkit.Chem import Draw\n",
        "from sklearn.linear_model import LinearRegression\n",
        "\n",
        "\n",
        "np.set_printoptions(precision=6, suppress=True)\n",
        "\n",
        "\n",
        "def show_mol(smi, style=\"stick\"):\n",
        "    \"\"\"Renders a visualization of a smiles string\"\"\"\n",
        "    mol = Chem.MolFromSmiles(smi)\n",
        "    mol = Chem.AddHs(mol)\n",
        "    AllChem.EmbedMolecule(mol)\n",
        "    AllChem.MMFFOptimizeMolecule(mol, maxIters=200)\n",
        "    mblock = Chem.MolToMolBlock(mol)\n",
        "\n",
        "    view = py3Dmol.view(width=500, height=500)\n",
        "    view.addModel(mblock, \"mol\")\n",
        "    view.setStyle({style: {}})\n",
        "    view.zoomTo()\n",
        "    view.show()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "5PG21f55vkrz"
      },
      "source": [
        "## Muddy points\n",
        "\n",
        "The cell block below is for clarifying any muddy points we have today."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "11Lt35Wlvkrz"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "1A6YB_l9vkr0"
      },
      "source": [
        "## Motivation\n",
        "\n",
        "Today, we delve into the application of regression analysis in chemistry and data science.\n",
        "Our dataset comprises pKa values and corresponding molecular descriptors, offering a quantitative approach to understanding molecular properties.\n"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "Vm-DjuFyvkr0"
      },
      "source": [
        "## pKa\n",
        "\n",
        "The pKa measures a substance's acidity or basicity, particularly in chemistry.\n",
        "It is the negative logarithm (base 10) of the acid dissociation constant (Ka) of a solution.\n",
        "The pKa value helps quantify the strength of an acid in a solution.\n",
        "\n",
        "The expression for the acid dissociation constant (Ka), from which pKa is derived, is given by the following chemical equilibrium equation for a generic acid (HA) in water:\n",
        "\n",
        "$$\n",
        "\\text{HA} \\rightleftharpoons \\text{H}^+ + \\text{A}^-\n",
        "$$\n",
        "\n",
        "The equilibrium constant (Ka) for this reaction is defined as the ratio of the concentrations of the dissociated ions ($\\text{H}^+$ and $\\text{A}^-$) to the undissociated acid ($\\text{HA}$):\n",
        "\n",
        "$$\n",
        "\\text{Ka} = \\frac{[\\text{H}^+][\\text{A}^-]}{[\\text{HA}]}\n",
        "$$\n",
        "\n",
        "Taking the negative logarithm (base 10) of both sides of the equation gives the expression for pKa:\n",
        "\n",
        "$$\n",
        "\\text{pKa} = -\\log_{10}(\\text{Ka})\n",
        "$$\n",
        "\n",
        "So, in summary, the pKa is calculated by taking the negative logarithm of the acid dissociation constant (Ka) for a given acid. A lower pKa indicates a stronger acid.\n",
        "\n",
        "In simpler terms:\n",
        "\n",
        "-   A lower pKa indicates a stronger acid because it means the acid is more likely to donate a proton (H+) in a chemical reaction.\n",
        "-   A higher pKa indicates a weaker acid as it is less likely to donate a proton.\n",
        "\n",
        "The pKa is a crucial parameter in understanding the behavior of acids and bases in various chemical reactions.\n",
        "It is commonly used in fields such as medicinal chemistry, biochemistry, and environmental science to describe and predict the behavior of molecules in solution."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "y9rz8UITvkr0"
      },
      "source": [
        "## Molecular descriptors\n",
        "\n",
        "Molecular descriptors are quantitative representations of chemical compounds that capture various structural, electronic, and physicochemical properties.\n",
        "These descriptors are numerical values or sets of values that encode information about the characteristics of a molecule.\n",
        "Molecular descriptors provide a structured and standardized way to quantify molecular features, facilitating the analysis and comparison of different molecules in chemical and computational studies.\n",
        "\n",
        "Molecular descriptors can include a wide range of information, such as:\n",
        "\n",
        "-   Structural Descriptors: These describe the geometry and connectivity of atoms within a molecule. Examples include molecular weight, size, and shape descriptors.\n",
        "-   Topological Descriptors: These capture information about the connectivity of atoms in a molecular structure, often expressed as graphs or matrices.\n",
        "-   Electronic Descriptors: These reflect the electronic properties of a molecule, including features related to electron distribution, charge, and orbital energies.\n",
        "-   Physicochemical Descriptors: These encompass properties such as solubility, partition coefficients, and melting points, providing insights into the physical behavior of the molecule.\n",
        "-   Quantum Chemical Descriptors: These are derived from quantum mechanical calculations and provide detailed information about a molecule's electronic structure and energetics.\n",
        "\n",
        "Molecular descriptors are crucial in quantitative structure-activity relationship (QSAR) studies, computational chemistry, and drug design.\n",
        "By converting complex molecular structures into numerical values, researchers can apply statistical and computational techniques to analyze and model the relationships between molecular features and various properties or activities.\n"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "WTM3fti7vkr0"
      },
      "source": [
        "## Exploring the dataset\n",
        "\n",
        "Now, let's shift our focus to a practical application of our theoretical knowledge.\n",
        "\n",
        "I found [this dataset](https://github.com/IUPAC/Dissociation-Constants) that contains a bunch of high-quality experimental measurements of pKas.\n",
        "It contains a bunch of information and other aspects that makes regression a bit of a nightmare; thus, I did some cleaning of the data and computed some molecular features (i.e., descriptors) that we can use.\n",
        "Before delving into regression analysis, it is essential to conduct a systematic review of the dataset.\n",
        "This preliminary examination will provide us with the necessary foundation to understand the quantitative relationships between molecular features and acidity.\n",
        "Let's now proceed with a methodical investigation of the empirical data, setting the stage for our subsequent analytical endeavors."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "NcI5uycQvkr0"
      },
      "source": [
        "### Loading\n",
        "\n",
        "Using the Pandas library, read the CSV file into a DataFrame.\n",
        "Use the variable you defined in the previous step."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "MP9kKuiavkr0"
      },
      "outputs": [],
      "source": [
        "CSV_PATH = \"https://gitlab.com/oasci/courses/pitt/biosc1540-2024s/-/raw/main/biosc1540/files/csv/pka/pka_desc_selected.csv\""
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "2i-Cyq3Jvkr1"
      },
      "source": [
        "### Take a look\n",
        "\n",
        "Print the first few rows of the DataFrame to check if the data has been successfully loaded."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "4I-2VDGNvkr1"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "gE1xhzeBvkr1"
      },
      "source": [
        "### Histograms\n",
        "\n",
        "Use Matplotlib's `plt.subplots() `function to create a single subplot.\n",
        "Assign the returned figure and axis objects to variables (`fig` and `ax`, respectively).\n",
        "\n",
        "Utilize the `ax.hist()` function to plot a histogram.\n",
        "Use the `\"pka_value\"` column from the DataFrame (`df`) as the data, and set the number of bins to `100`.\n",
        "Choose a `color` for the bars.\n",
        "\n",
        "Set labels for the x-axis and y-axis using `ax.set_xlabel()` and `ax.set_ylabel()` functions.\n",
        "\n",
        "Finally, use `plt.show()` to display the histogram."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "y_uJkn2Rvkr1"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "nT9C_8iKvkr1"
      },
      "source": [
        "### Scatter\n",
        "\n",
        "Use Matplotlib's `plt.subplots()` function to create a single subplot.\n",
        "Assign the returned figure and axis objects to variables (`fig` and `ax`, respectively).\n",
        "Utilize the `ax.scatter()` function to plot a scatter plot.\n",
        "Specify the x-axis data as `\"MaxEStateIndex\"` and the y-axis data as `\"pka_value\"` from your DataFrame (`df`).\n",
        "Choose a color for the scatter points."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "dyz0eG8jvkr1"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "jEoA6qcyvkr1"
      },
      "source": [
        "The method assigns numerical values (E-state indices) to each atom in a molecule, representing the atom's electronic state.\n",
        "The E-state indices are calculated based on the atom's atomic number, hybridization, and the types of neighboring atoms.\n",
        "The `MaxEStateIndex` is then derived by finding the maximum E-state index among all atoms in the molecule."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "aB-uwT7Pvkr1"
      },
      "source": [
        "Use Matplotlib's `plt.subplots()` function to create a single subplot.\n",
        "Assign the returned figure and axis objects to variables (`fig` and `ax`, respectively).\n",
        "Utilize the `ax.scatter()` function to plot a scatter plot.\n",
        "Specify the x-axis data as `\"SPS\"` and the y-axis data as `\"pka_value\"` from your DataFrame (`df`).\n",
        "Choose a color for the scatter points."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "di7vhJmIvkr1"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "HtNcyVrXvkr1"
      },
      "source": [
        "Use the `ax.scatter()` function to create a scatter plot.\n",
        "Specify the x-axis data as \"SPS\" and the y-axis data as `\"MaxEStateIndex\"` from your DataFrame (`df`)."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "7-ZfP3XQvkr1"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "HsVlOkKnvkr1"
      },
      "source": [
        "Spacial score (SPS) is an empirical scoring system to express the spacial complexity of a compound in an uniform manner and on a highly granular scale for ranking and comparison between molecules."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "3Q_aYu0Evkr1"
      },
      "source": [
        "## Prediction\n",
        "\n",
        "Our objective is to predict pKa values using a machine learning model.\n",
        "In order to do this, we need to prepare our data for training and testing.\n",
        "Identify the features and target variable.\n",
        "In this case, the features are the molecular descriptors, and the target variable is the pKa value.\n",
        "Create separate dataframes for `df_features` and `df_targets`."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "jRE7shBPvkr1"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "8j9pHOmevkr1"
      },
      "source": [
        "The target variable (`df_targets`) and features (`df_features`) need to be converted into NumPy arrays for compatibility with machine learning models."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "RbauN7fovkr1"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "28TgCAhpvkr1"
      },
      "source": [
        "### Linear model\n",
        "\n",
        "Create an instance of the `LinearRegression` model from scikit-learn.\n",
        "Use the `fit` method to train the linear regression model with your features and target variable."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "1awgI5R0vkr1"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "r-L9735Nvkr1"
      },
      "source": [
        "Use the score method to calculate and print the coefficient of determination ($R^2$) of the linear regression model."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "CtbGUvz3vkr1"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "CMNFRPT3vkr1"
      },
      "source": [
        "Use the predict method to generate predictions (predictions) based on the trained linear regression model and the input `features`.\n",
        "Create a scatter plot where the x-axis represents the actual pKa values (`targets`), the y-axis represents the predicted pKa values (`predictions`)."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "EWmV61ATvkr1"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "pDDFax05vkr1"
      },
      "source": [
        "Points close to the diagonal line indicate accurate predictions, while deviations suggest discrepancies between actual and predicted values."
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "eHkq_sOcvkr2"
      },
      "source": [
        "#### Sanity check\n",
        "\n",
        "Let's take a look at the coefficients and probe our model.\n",
        "\n",
        "Extracted from the columns of `df_features`, representing the names of the features.\n",
        "Obtain the coefficients obtained from the trained linear regression model.\n",
        "\n",
        "Use `ax.barh()` to create a horizontal bar graph. Feature names are on the y-axis, and corresponding coefficients are on the x-axis.\n",
        "Add a vertical dashed line (`ax.axvline()`) at zero for reference."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "FEQSrFkJvkr2"
      },
      "outputs": [],
      "source": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "QiVg4APNvkr2"
      },
      "source": [
        "Do these coefficients make sense?"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "0U-36SUmvkr2"
      },
      "outputs": [],
      "source": []
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
      "provenance": []
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}