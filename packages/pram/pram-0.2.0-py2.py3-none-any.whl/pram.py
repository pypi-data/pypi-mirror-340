# SPDX-License-Identifier: MIT
import pandas as pd
import numpy as np
import argparse
import os
import logging


class Pram:

    @staticmethod
    def __get_transition_matrix__(values):
        """
        Create a standard transition matrix
        :param values:
        :return:
        """
        # Create a transition matrix using the counts of A:B
        counts = pd.Series(values).value_counts(sort=False)
        v = counts.values
        matrix_values = v * v[:, None]
        matrix = pd.DataFrame(matrix_values)
        matrix.columns = counts.index
        matrix.index = counts.index

        # Normalize the columns to sum to 1
        matrix = matrix.divide(matrix.sum(axis=0), axis=1)
        return matrix

    @staticmethod
    def __get_weighted_transition_matrix__(values, m, alpha):
        """
        Create a transition matrix weighted by alpha
        :param values: the set of values to create a transition matrix for
        :param alpha: alpha - degree of change
        :param m: minimum diagonal
        :return:
        """
        tm = Pram.__get_transition_matrix__(values)

        # Apply minimum value to diagonal using m
        diag = np.diag(tm)
        diag = [m if a_ < m else a_ for a_ in diag]
        diag = pd.Series(diag, index=tm.columns)
        np.fill_diagonal(tm.values, diag)

        # normalise so cols add up to 1
        tm = tm.div(tm.sum(axis=0), axis=1)

        # identity matrix of diagonal
        ei = tm.copy()
        for col in ei.columns:
            ei[col].values[:] = 0
        np.fill_diagonal(ei.values, 1)

        # apply alpha
        wm = alpha * tm + (1 - alpha) * ei

        # normalise so cols add up to 1
        wm = wm.div(wm.sum(axis=0), axis=1)

        return wm

    @staticmethod
    def __pram_replace__(tm, current_value):
        """
        Randomly changes values using the supplied transition matrix
        :param tm:
        :param current_value:
        :return:
        """
        column = tm[current_value]
        return np.random.choice(column.index, p=column.values)

    @staticmethod
    def pram(data, m=0.8, alpha=0.5, columns=None, strata=None):
        """
        Uses PRAM to add perturbation to the supplied dataset
        :param data: a dataframe
        :param m: min diagonal value (defaults to 0.8)
        :param alpha: the degree of change, from 0 (no changes) to 1 (max changes). Defaults to 0.5
        :param columns: a list of the names of the columns to apply PRAM to. Defaults to None, applying to all columns.
        :return:
        """
        logger = logging.getLogger('pram')

        # Convert everything in the dataframe into a string - we can only
        # work with factors/tokens using PRAM
        data = data.applymap(str)

        if columns is None:
            columns = data.columns

        if strata and strata in columns:

            logger.warning("Columns used for stratification cannot also be modified; " + strata +
                            " will be removed from the set of columns")
            columns = columns[columns != strata]

        # Create the weighted transition matrix for each column
        transition_matrices = {}

        if strata is not None:
            strata_levels = list(set(data[strata].values))
            strata_levels.append('all')
        else:
            strata_levels = ['all']

        for level in strata_levels:
            for column in columns:
                if level == 'all':
                    values = data[column].values
                else:
                    values = data[data[strata] == level][column].values
                transition_matrices[level, column] = Pram.__get_weighted_transition_matrix__(values, m, alpha)

        logger.debug("Completed building transition matrices - processing data")

        # For each row apply PRAM
        for index, row in data.iterrows():
            for column in columns:
                if strata is not None and strata != column:
                    strata_value = row[strata]
                else:
                    strata_value = 'all'
                row[column] = Pram.__pram_replace__(transition_matrices[strata_value, column], row[column])

        return data

    @staticmethod
    def __print_frequencies__(input_df, output_df):
        """
        Prints a table of the frequencies of values for the input and the output,
        enabling the user to determine whether the PRAM algorithm has substantially
        altered the 'shape' of the data and needs to modify the threshold and/or
        alpha.
        :param input_df: the original dataframe
        :param output_df: the modified dataframe
        :return: None. Outputs the table to STDOUT
        """
        input_df = input_df.applymap(str)
        freq = None
        for column in input_df.columns:
            i = input_df[column]
            o = output_df[column]
            ip = i.value_counts(normalize=True).round(2)
            op = o.value_counts(normalize=True).round(2)
            p = pd.DataFrame({'Column': column, 'Original': ip, "Output": op}).fillna(0)
            if freq is None:
                freq = p
            else:
                freq = pd.concat([freq, p])
        print(freq)


def pram(data, m=0.8, alpha=0.5, columns=None, strata=None):
    """
    Uses PRAM to add perturbation to the supplied dataset
    :param data: a dataframe
    :param m: minimum diagonal value (defaults to 0.8)
    :param alpha: the degree of change, from 0 (no changes) to 1 (max changes). Defaults to 0.5
    :param columns: a list of the names of the columns to apply PRAM to. Defaults to None, applying to all columns.
    :return: a dataset modified using the PRAM algorithm
    """
    return Pram.pram(data, m=m, alpha=alpha, columns=columns, strata=strata)


def main():
    argparser = argparse.ArgumentParser(description='Post-randomisation method (PRAM) for Python.')
    argparser.add_argument('input_path', metavar='<input>', type=str, nargs=1, default='input.csv',
                           help='The name of the CSV data file to process')
    argparser.add_argument('output_path', metavar='<output>', type=str, nargs='?', default='output.csv',
                           help='The output file name')
    argparser.add_argument('m', metavar='<m>', type=float, nargs='?', default=0.8,
                           help='The minimum diagonal value')
    argparser.add_argument('a', metavar='<a>', type=float, nargs='?', default=0.5,
                           help='The alpha value')
    argparser.add_argument('strata', metavar='<strata>', type=str, nargs='?', default=None,
                           help='The column to stratify by')
    argparser.add_argument('columns', metavar='<columns>', type=str, nargs='*', default=None, action='append',
                           help='The columns to include')
    argparser.add_argument('-f', action='store_true',
                           help='Print a frequency table showing original vs changed frequencies.')
    argparser.add_argument('-debug', action='store_true',
                           help='Enable debugging mode.')

    args = argparser.parse_args()

    # Defaults
    input_path = vars(args)['input_path'][0]
    output_path = vars(args)['output_path']
    columns = vars(args)['columns'][0]
    strata = vars(args)['strata']
    param_minimum = vars(args)['m']
    param_alpha = vars(args)['a']
    print_frequencies = vars(args)['f']
    debug = vars(args)['debug']

    logger = logging.getLogger('pram')
    logging.basicConfig()

    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debugging enabled")

    if len(columns) == 0:
        columns = None

    if isinstance(columns, str):
        columns = [columns]

    if not os.path.exists(input_path):
        logger.error('Input data file does not exist')
        exit()
    else:
        logger.info("Input data file: " + input_path)

    logger.info("Output file: " + output_path)

    # Load the dataset
    logger.debug("Loading dataset")
    input_data = pd.read_csv(input_path)
    logger.debug("Dataset loaded")

    # Apply the perturbation
    output_data = pram(input_data, m=param_minimum, alpha=param_alpha, columns=columns, strata=strata)

    # Print frequency table
    if print_frequencies:
        Pram.__print_frequencies__(input_data, output_data)

    # Write the output
    output_data.to_csv(output_path, encoding='UTF-8', index=False)


if __name__ == "__main__":
    main()
