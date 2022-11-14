import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# TODO: - Check column names, throw exceptions if cols not found in dataframes
# TODO: -> Make changes in report Addendum for modifications of return values


class Sampling:
    def __init__(self):
        self.minimum_sample_mass = None
        self.diff_density_masses = None
        # Gaudin-Schuhmann cumulative % mass retained
        self.gs_cumulative_perc_retained = None
        # Rosin-Rammler cumulative % mass retained
        self.rr_cumulative_perc_retained = None

    """
    Gy's method for obtaining minimum sample mass
    for particle size distribution representation
    """

    def gys_method(self, largest_particle_dimension, sampling_error_variance, sampling_constant):
        self.minimum_sample_mass = sampling_constant * (largest_particle_dimension ** 3) / sampling_error_variance ** 2
        return

    def get_sample_diff_densities(self, assay_probability, assay_error_perc, average_particle_size,
                                  average_particle_mass, df_proportions):
        # Only for 2 components - mineral(any mineral) and gangue(any commercially valueless material)
        df_prob_deviation = pd.read_excel("mineral_sampling_deviation.xlsx")
        std_dev_index = df_prob_deviation[df_prob_deviation['Probability'] == assay_probability].index
        std_deviation = assay_error_perc / df_prob_deviation.loc[std_dev_index]['Deviation'].values[0]
        variance = std_deviation ** 2

        # Get numerator of expression
        sum_prop_numerator = 0
        for i in df_proportions.index:
            sum_prop_numerator += df_proportions['Mass%'][i] / \
                                  (df_proportions['Density'][i] * average_particle_size ** 3)

        # Solve for proportions
        proportions_list = []
        for i in df_proportions.index:
            proportions_numerator = df_proportions['Mass%'][i] / \
                                    (df_proportions['Density'][i] * average_particle_size ** 3)
            proportions_list.append(round(proportions_numerator / sum_prop_numerator, 3))

        df_proportions['Proportions'] = proportions_list  # Create new column named proportions in dataframe

        number_of_particles_list = []  # Column required for the calculation of sample mass
        for i in df_proportions.index:
            number_of_particles_list.append(df_proportions['Proportions'][i] * (1 - df_proportions['Proportions'][i]) /
                                            variance)

        df_proportions['Number_of_particles'] = proportions_list  # Create new column for No. of particles in dataframe

        sample_masses_list = []  # final list for output values
        for i in df_proportions.index:
            sample_masses_list.append(round(df_proportions['Number_of_particles'][i] * average_particle_mass, 3))

        df_proportions['Sample_masses'] = sample_masses_list  # Create new column named Sample_masses
        print(df_proportions)
        self.diff_density_masses = sample_masses_list  # assign object member to sample masses
        return df_proportions

    def get_minimum_sample_mass(self):
        return self.minimum_sample_mass

    # Rosin-Rammler distribution
    def rosin_rammler(self, input_size_fraction, df_sieve_analysis_data):
        # %passing = (100 - %retained) and %retained = (100 - %passing)
        # TODO: Ensure only one row where cumulative%passing=0

        # Add columns for log(aperture) and log(Cumulative % passing) as log_x and log_y respectively
        df_sieve_analysis_data['log_aperture'] = np.log10(df_sieve_analysis_data['Aperture'])
        df_sieve_analysis_data['log_y'] = np.log10(df_sieve_analysis_data['Cumulative_Mass%_Passing'])
        df_sieve_analysis_data['Cumulative_Mass%_Retained'] = [100 - row for row in
                                                               df_sieve_analysis_data['Cumulative_Mass%_Passing']]
        # Drop rows with Cumulative_Mass%_Retained = 0
        df_sieve_analysis_data.drop(
            df_sieve_analysis_data[df_sieve_analysis_data['Cumulative_Mass%_Retained'] <= 0].index, inplace=True)

        # Adding columns to dataframe for easier computation
        df_sieve_analysis_data['log100_div_R'] = [round(math.log10(100 / row), 3) for row in
                                                  df_sieve_analysis_data['Cumulative_Mass%_Retained']]
        df_sieve_analysis_data['loglog100_div_R'] = [round(math.log10(math.log10(100 / row)), 3) for row in
                                                     df_sieve_analysis_data['Cumulative_Mass%_Retained']]
        # For plotting polynomial best fit straight line
        x_max = math.ceil(df_sieve_analysis_data['log_aperture'].max())
        x_min = math.floor(df_sieve_analysis_data['log_aperture'].min())

        # Get slope and y-intercept of polynomial fit line
        slope, intercept = np.polyfit(df_sieve_analysis_data['log_aperture'],
                                      df_sieve_analysis_data['loglog100_div_R'], 1)

        # Plot polynomial best fit line for Rosin-Rammler
        x = np.linspace(x_min, x_max, 100)
        y = slope * x + intercept
        plt.plot(x, y, '-r', label='Rosin-Rammler')
        plt.plot(x, y)

        # Plot desired point and get cumulative mass retained
        log_log_cumulative_mass = slope * math.log10(input_size_fraction) + intercept
        log_cumulative_mass = 10 ** log_log_cumulative_mass
        cumulative_mass_perc_retained = 100 / 10 ** log_cumulative_mass
        x1 = [math.log10(input_size_fraction)]
        y1 = [log_log_cumulative_mass]

        plt.plot(x1, y1, marker="o", markersize=10, markerfacecolor="green")
        plt.text(math.log10(input_size_fraction), log_log_cumulative_mass,
                 f'   {math.log10(input_size_fraction): .2f},   {log_log_cumulative_mass: .2f}')
        self.rr_cumulative_perc_retained = round(cumulative_mass_perc_retained, 2)
        # Display graph
        plt.title('Rosin-Rammler distribution (log scale)')
        plt.ylabel('log(log(100/R))  (R = mass % retained)')
        plt.xlabel('Logarithm of Particle size (microns)')
        plt.grid()
        plt.show()
        return self.rr_cumulative_perc_retained

    # Gaudin-Schuhmann distribution
    def gaudin_schuhmann(self, input_size_fraction, df_sieve_analysis_data):
        # %passing and %retained=(100-%passing)
        # TODO: Ensure only one row where cumulative%passing=0 if the row has a 0

        # Drop rows with Cumulative_Mass%_Passing = 0
        df_sieve_analysis_data.drop(
            df_sieve_analysis_data[df_sieve_analysis_data['Cumulative_Mass%_Passing'] <= 0].index, inplace=True)

        # Add columns for log(aperture value) and log(Cumulative % passing)
        # as log_x and log_y respectively
        df_sieve_analysis_data['log_x'] = np.log10(df_sieve_analysis_data['Aperture'])
        df_sieve_analysis_data['log_y'] = np.log10(df_sieve_analysis_data['Cumulative_Mass%_Passing'])

        # For plotting polynomial best fit straight line
        x_max = math.ceil(df_sieve_analysis_data['log_x'].max())
        x_min = math.floor(df_sieve_analysis_data['log_x'].min())

        # Get slope and y-intercept of polynomial fit line
        slope, intercept = np.polyfit(df_sieve_analysis_data['log_x'], df_sieve_analysis_data['log_y'], 1)

        # Plot polynomial best fit line for Gaudin-Schuhmann
        x = np.linspace(x_min, x_max, 100)
        y = slope * x + intercept
        plt.plot(x, y, '-r', label='Gaudin-Schuhmann')

        # plot log(Cumulative % passing) vs log(aperture)
        plt.plot(df_sieve_analysis_data['log_x'], df_sieve_analysis_data['log_y'],
                 linestyle='--', marker='o', color='b', label='linear')

        # Plot desired point
        output_cumulative_mass_fraction = slope * math.log10(input_size_fraction) + intercept
        x1 = [math.log10(input_size_fraction)]
        y1 = [output_cumulative_mass_fraction]

        plt.plot(x1, y1, marker="o", markersize=10, markerfacecolor="green")
        plt.text(math.log10(input_size_fraction), output_cumulative_mass_fraction,
                 f'   {math.log10(input_size_fraction): .2f},   {output_cumulative_mass_fraction: .2f}')

        self.gs_cumulative_perc_retained = round(100 - (10 ** output_cumulative_mass_fraction), 2)
        print(self.gs_cumulative_perc_retained)
        # Display graph
        plt.title('Gaudin-Schuhmann distribution (log scale)')
        plt.ylabel('Logarithm of Cumulative mass % passing')
        plt.xlabel('Logarithm of Particle size (microns)')
        plt.ylim(0, 2)  # log(100) can never be exceeded because a % can never be > 100%
        plt.grid()
        plt.show()

        return self.gs_cumulative_perc_retained


class Milling:
    # All densities in kg/m3
    WATER_DENSITY = 997

    def __init__(self):
        self.mill_critical_speed = None
        self.percentage_solids = None
        self.dry_solid_mass_flowrate = None
        self.energy_required = None  # used in get_bond_energy
        self.mill_power = None  # used in get_mill_power
        self.product_mass_fractions = None

    #   Uses Bond's law to obtain power
    def get_mill_power(self, work_index, product_size, feed_size, dry_solid_mass_flowrate):
        # Bond's law
        self.energy_required = 10 * work_index * (1 / math.sqrt(product_size) - 1 / math.sqrt(feed_size))
        # Mill power needed for required energy
        self.mill_power = self.energy_required * dry_solid_mass_flowrate
        return self.mill_power

    def get_mill_critical_speed(self, mill_diameter, ball_diameter):
        # Mill critical speed for optimum crushing
        self.mill_critical_speed = 42.3 / math.sqrt(mill_diameter - ball_diameter)
        return self.mill_critical_speed

    def get_percentage_solids(self, slurry_density, dry_solid_density):
        # Percentage solids in a mixture
        self.percentage_solids = 100 * dry_solid_density * (slurry_density - self.WATER_DENSITY) / (slurry_density * (
                dry_solid_density - self.WATER_DENSITY))
        return self.percentage_solids

    def get_dry_solid_mass_flowrate(self, slurry_vol_flowrate, slurry_density, percentage_solids=None,
                                    dry_solid_density=None):
        # 2 different equations for obtaining self.dry_solid_mass_flowrate
        # Use equation implemented below if only percentage_solids is non-Null
        if dry_solid_density is None and percentage_solids is not None:
            self.dry_solid_mass_flowrate = slurry_vol_flowrate * slurry_density * percentage_solids / 100

        # Use equation implemented below if only dry_solid_density is non-Null
        elif percentage_solids is None and dry_solid_density is not None:
            self.dry_solid_mass_flowrate = slurry_vol_flowrate * dry_solid_density * (
                    slurry_density - self.WATER_DENSITY) / (
                                                   dry_solid_density - self.WATER_DENSITY)
            self.dry_solid_mass_flowrate = round(self.dry_solid_mass_flowrate, 2)
        return

    # Private static method for breakage prediction calculation
    @staticmethod
    def __interval_i_summation(residence_time, selection_functions, breakage_functions, products, index):
        summation_term = 0
        for i in range(index + 1):
            summation_term += selection_functions[i] * breakage_functions[i] * products[i]

        return residence_time * summation_term

    def breakage_prediction(self, df_breakage_matrix, df_pop_balance_data, residence_time):
        """
        TODO: Check sum of Mass_fraction column = 1
        TODO: Check if values in Selection_function column < 1 and >= 0
        TODO: sum(column_values(breakage_data)) = 1
        TODO: columns of breakage_data must have Nans in each column equal to the column index+1
        """
        df_breakage_matrix_transpose = df_breakage_matrix.T.fillna(0)
        products = [0]
        selection_functions = df_pop_balance_data['Selection_function'].tolist()
        for index in range(df_pop_balance_data.shape[0]):
            breakage_functions = df_breakage_matrix_transpose[index].tolist()
            breakage_functions.append(0)
            if index == 1:
                products.reverse()  # reverse list to send element = 0 to end of list
            products_mass_fractions_numerator = df_pop_balance_data['Mass_fraction'][index] \
                + self.__interval_i_summation(residence_time, selection_functions, breakage_functions, products, index)
            products_mass_fractions_denominator = 1 + residence_time * df_pop_balance_data['Selection_function'][index]
            if index < 1:
                # Append at end if first element
                products.append(round(products_mass_fractions_numerator / products_mass_fractions_denominator, 3))
            else:
                # Insert in second last position if index at 1 or higher (from second value)
                products.insert(-1, round(products_mass_fractions_numerator / products_mass_fractions_denominator, 3))
            print(products)
        products.pop()  # remove last zero that list was initialised with
        self.product_mass_fractions = pd.DataFrame({'Interval_number': list(df_pop_balance_data['Interval_number']),
                                                    'Product Mass Fractions': products})
        return self.product_mass_fractions  # TODO: CHANGE RETURN VALUE
