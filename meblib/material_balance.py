import pandas as pd
import numpy as np
from sympy.solvers import solve
from sympy import Symbol


# TODO: Rectify logic for nan_method
class MaterialBalance:

    def __init__(self):
        self.output1_flowrate = None
        self.output2_flowrate = None
        self.output1_components_compositions = None
        self.output2_components_compositions = None

    @staticmethod
    def row_filled_method(comps_df, row_index_filled, input_flow_rate):
        n1 = Symbol('n1')
        n2 = Symbol('n2')
        n3 = Symbol('n3')
        stream_flows_dict = {n1: input_flow_rate}
        expression1 = n2 + n3 + - input_flow_rate
        expression2 = input_flow_rate - n2
        expression3 = comps_df.iloc[row_index_filled][2] * n2 + comps_df.iloc[row_index_filled][3] * expression2 - \
            comps_df.iloc[row_index_filled][1] * input_flow_rate
        stream_flows_dict.update(solve([expression3, expression1], (n2, n3)))
        # molar_flow_rates_df = pd.DataFrame(index=range(len(comps_df.index)), columns=range(len(comps_df.columns) - 1))
        for row_index in range(len(comps_df)):
            stream1_value = comps_df.loc[row_index, 'InputStream']
            stream2_value = comps_df.loc[row_index, 'OutputStream1']
            stream3_value = comps_df.loc[row_index, 'OutputStream2']
            # using relation: n1*x1 = n2*x2 + n3*x3
            if pd.isnull(stream1_value):
                comps_df.loc[row_index, 'InputStream'] = (stream2_value * stream_flows_dict[n2] + stream3_value *
                                                          stream_flows_dict[n3]) / input_flow_rate

            elif pd.isnull(stream2_value):
                comps_df.loc[row_index, 'OutputStream1'] = (stream1_value * input_flow_rate - stream3_value *
                                                            stream_flows_dict[n3]) / stream2_value

            elif pd.isnull(stream2_value):
                comps_df.loc[row_index, 'OutputStream2'] = (stream1_value * input_flow_rate - stream2_value *
                                                            stream_flows_dict[n2]) / stream3_value

        return comps_df, stream_flows_dict

    @staticmethod
    def row_check_method(comps_streams_df):
        row_index_of_full_vals = None

        for index in range(len(comps_streams_df)):
            is_col1_non_nan = pd.isnull(comps_streams_df.loc[index, "InputStream"])
            is_col2_non_nan = pd.isnull(comps_streams_df.loc[index, "OutputStream1"])
            is_col3_non_nan = pd.isnull(comps_streams_df.loc[index, "OutputStream2"])

            if not (is_col1_non_nan or is_col2_non_nan or is_col3_non_nan):
                row_index_of_full_vals = index

        return row_index_of_full_vals

    @staticmethod
    def nan_method(stream_comps, input_flow_rate):
        for column_value in ['InputStream', 'OutputStream1', 'OutputStream2']:
            column_ser = stream_comps[column_value]

        if column_ser.isnull().sum() == 2:
            input_value = 1 - stream_comps[column_value].sum()
            null_rows = column_ser[column_ser.isnull()]

            if column_value == 'InputStream' or column_value == 'OutputStream1' or 'OutputStream2':
                stream_comps.loc[null_rows.index[0], column_value + '_1'] = -input_flow_rate
                stream_comps.loc[null_rows.index[1], column_value + '_1'] = input_flow_rate
                stream_comps[column_value + '_1'] = stream_comps[column_value + '_1'].fillna(0)

            stream_comps.loc[null_rows.index[0], column_value] = stream_comps.loc[null_rows.index[0], 'Components'] + \
                column_value
            stream_comps.loc[null_rows.index[1], column_value] = '-' + stream_comps.loc[
                null_rows.index[0], 'Components'] + column_value + ' ' + '+' + ' ' + str(input_value)
            stream_comps[column_value] = stream_comps[column_value].astype(str).str.replace(
                stream_comps.loc[null_rows.index[0], 'Components'] + column_value, '0', regex=False)

        streams_df = stream_comps.drop('Components', axis=1)
        streams_df = streams_df.astype(str).replace('nan', np.nan)

        for column_name in streams_df.columns.to_list():
            streams_df[column_name] = streams_df[column_name].apply(lambda x: pd.eval(x) if type(x) == str else x)
        df_array = streams_df.to_numpy()
        const_array = df_array[:, 0] * 100
        output_stream_1_array = df_array[:, 1:]
        return const_array, output_stream_1_array
