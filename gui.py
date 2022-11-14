import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from meblib import material_balance
import pandas as pd
from omlib import minerals
from omlib import oils
import error_handling


class RootWindow:
    def __init__(self, master=None):
        # build ui
        self.root_toplevel = tk.Tk() if master is None else tk.Toplevel(master)
        self.root_toplevel.configure(
            background="#80ffff",
            height=200,
            highlightbackground="#c0c0c0",
            width=200)
        self.root_toplevel.resizable(False, False)
        self.root_toplevel.title("SELECT A COURSE")
        self.meb_course_button = ttk.Button(self.root_toplevel)
        self.meb_course_button.configure(text='Mass and Energy balances')
        self.meb_course_button.pack(padx=50, pady=80, side="top")
        self.meb_course_button.configure(command=self.goto_meb_page)
        self.om_course_button = ttk.Button(self.root_toplevel)
        self.om_course_button.configure(text='Oils and Minerals Processing')
        self.om_course_button.pack(padx=100, pady=100, side="top")
        self.om_course_button.configure(command=self.goto_om_page)

        # Main widget
        self.main_window = self.root_toplevel

        # Declare root window GUI attributes for model lists
        self.om_equations_list_window = None
        self.meb_equations_list_window = None

    def run(self):
        self.main_window.mainloop()

    def goto_meb_page(self):
        self.main_window.destroy()
        self.meb_equations_list_window = MebEquationsListUI()
        self.meb_equations_list_window.run()

    def goto_om_page(self):
        self.main_window.destroy()
        self.om_equations_list_window = OmEquationsListUI()
        self.om_equations_list_window.run()


class MebEquationsListUI:
    def __init__(self, master=None):
        # build ui
        self.meb_equations_toplevel = tk.Tk() if master is None else tk.Toplevel(master)
        self.meb_equations_toplevel.configure(
            height=200, takefocus=True, width=200)
        self.meb_equations_toplevel.resizable(False, False)
        self.meb_equations_toplevel.title("MEB Equations")
        self.meb_equations_frame = tk.Frame(self.meb_equations_toplevel)
        self.meb_equations_frame.configure(
            background="#1a99d7", height=600, width=600)
        self.separator_button = tk.Button(self.meb_equations_frame)
        self.separator_button.configure(
            background="#ffffff",
            foreground="#000000",
            highlightbackground="#fb466a",
            highlightcolor="#f487f8",
            justify="center",
            text='SEPARATOR',
            width=15)
        self.separator_button.grid(column=1, padx=150, pady=50, row=5)
        self.separator_button.configure(command=self.go_to_separator_window)
        self.meb_equations_frame.pack(side="top")

        # Main widget
        self.main_window = self.meb_equations_toplevel
        # Declare GUI attributes for models of MEB library
        self.separator_window = None

    def run(self):
        self.main_window.mainloop()

    def go_to_separator_window(self):
        self.main_window.destroy()
        self.separator_window = SeparatorUI()
        self.separator_window.run()


class OmEquationsListUI:
    def __init__(self, master=None):
        # build ui
        self.om_equations_toplevel = tk.Tk() if master is None else tk.Toplevel(master)
        self.om_equations_toplevel.configure(
            height=200,
            takefocus=True,
            width=200)
        self.om_equations_toplevel.resizable(False, False)
        self.om_equations_toplevel.title("OM Equations")
        self.om_equations_frame = tk.Frame(self.om_equations_toplevel)
        self.om_equations_frame.configure(height=300,
                                          background="#1a99d7",
                                          width=300)
        self.gys_method = ttk.Button(self.om_equations_frame)
        self.gys_method.configure(
            text="Use Gy's method for obtaining \n    the minimum sample mass")
        self.gys_method.grid(column=0, padx=10, pady=10, row=0)
        self.gys_method.configure(command=self.go_to_gys_method)
        self.sample_diff_densities_button = ttk.Button(self.om_equations_frame)
        self.sample_diff_densities_button.configure(
            text='Get sample mass for \nSampling particles of\n different densities')
        self.sample_diff_densities_button.grid(
            column=0, padx=10, pady=10, row=1)
        self.sample_diff_densities_button.configure(
            command=self.go_to_samp_diff_densities)
        self.rr_size_dist_button = ttk.Button(self.om_equations_frame)
        self.rr_size_dist_button.configure(
            text='Visualise size distribution using\nRosin-Rammler size distribution')
        self.rr_size_dist_button.grid(column=0, padx=10, pady=10, row=2)
        self.rr_size_dist_button.configure(
            command=self.go_to_rosin_rammler_dist)
        self.gs_size_dist_button = ttk.Button(self.om_equations_frame)
        self.gs_size_dist_button.configure(
            text='    Visualise size distribution using\nGaudin-Schuhmann size distribution')
        self.gs_size_dist_button.grid(column=0, padx=20, pady=10, row=3)
        self.gs_size_dist_button.configure(
            command=self.go_to_gaudin_schuhmann_dist)
        self.get_mill_power_button = ttk.Button(self.om_equations_frame)
        self.get_mill_power_button.configure(text='Get required mill power')
        self.get_mill_power_button.grid(column=3, padx=10, pady=10, row=3)
        self.get_mill_power_button.configure(
            command=self.go_to_required_mill_power)
        self.get_critical_mill_speed_button = ttk.Button(self.om_equations_frame)
        self.get_critical_mill_speed_button.configure(
            text='Get critical speed of mill')
        self.get_critical_mill_speed_button.grid(
            column=0, padx=10, pady=10, row=4)
        self.get_critical_mill_speed_button.configure(
            command=self.go_to_critical_mill_speed)
        self.get_perc_solids_button = ttk.Button(self.om_equations_frame)
        self.get_perc_solids_button.configure(
            text='Get percentage solids\n     in slurry stream')
        self.get_perc_solids_button.grid(column=3, padx=10, pady=10, row=1)
        self.get_perc_solids_button.configure(command=self.go_to_perc_solids)
        self.get_dry_solids_mass_flowrate_button = ttk.Button(self.om_equations_frame)
        self.get_dry_solids_mass_flowrate_button.configure(
            text='    Get dry solids mass \nflowrate in slurry stream')
        self.get_dry_solids_mass_flowrate_button.grid(
            column=3, ipadx=10, pady=10, row=2)
        self.get_dry_solids_mass_flowrate_button.configure(
            command=self.go_to_dry_solids_mass_flowrate)
        self.pop_balancing_button = ttk.Button(self.om_equations_frame)
        self.pop_balancing_button.configure(
            text='     Population balancing \nusing breakage predictions')
        self.pop_balancing_button.grid(column=3, padx=10, row=0)
        self.pop_balancing_button.configure(command=self.go_to_pop_balancing)
        self.specific_gravity_button = ttk.Button(self.om_equations_frame)
        self.specific_gravity_button.configure(text='Get specific gravity')
        self.specific_gravity_button.grid(column=3, row=4)
        self.pop_balancing_button.configure(command=self.go_to_specific_gravity)
        self.om_equations_frame.pack(side="top")

        # Main widget
        self.main_window = self.om_equations_toplevel

        # Declare GUI attributes for models of OM library
        self.diff_densities_window = None
        self.gys_method_window = None
        self.rosin_rammler_window = None
        self.gaudinn_schuchmann_window = None
        self.mill_power_window = None
        self.critical_mill_speed_window = None
        self.perc_solids_window = None
        self.dry_solids_mass_flowrate_window = None
        self.pop_balancing_window = None

    def run(self):
        self.main_window.mainloop()

    def go_to_specific_gravity(self):
        pass

    def go_to_gys_method(self):
        self.main_window.destroy()
        self.gys_method_window = GysUI()
        self.gys_method_window.run()

    def go_to_samp_diff_densities(self):
        self.main_window.destroy()
        self.diff_densities_window = DifferentdensitiesUI()
        self.diff_densities_window.run()

    def go_to_rosin_rammler_dist(self):
        self.main_window.destroy()
        self.rosin_rammler_window = RosinRammlerUI()
        self.rosin_rammler_window.run()

    def go_to_gaudin_schuhmann_dist(self):
        self.main_window.destroy()
        self.gaudinn_schuchmann_window = GaudinSchuhmannUI()
        self.gaudinn_schuchmann_window.run()

    def go_to_required_mill_power(self):
        self.main_window.destroy()
        self.mill_power_window = MillPowerUI()
        self.mill_power_window.run()

    def go_to_critical_mill_speed(self):
        self.main_window.destroy()
        self.mill_power_window = MillSpeedUI()
        self.mill_power_window.run()

    def go_to_perc_solids(self):
        self.main_window.destroy()
        self.perc_solids_window = PercentageSolidsUI()
        self.perc_solids_window.run()

    def go_to_dry_solids_mass_flowrate(self):
        self.main_window.destroy()
        self.dry_solids_mass_flowrate_window = DryMassFlowrateUI()
        self.dry_solids_mass_flowrate_window.run()

    def go_to_pop_balancing(self):
        self.main_window.destroy()
        self.pop_balancing_window = PopuationBalanceUI()
        self.pop_balancing_window.run()


class GysUI:
    def __init__(self, master=None):
        # build ui
        self.gys_method_toplevel = tk.Tk() if master is None else tk.Toplevel(master)
        self.gys_method_toplevel.configure(
            height=200, takefocus=True, width=200)
        self.gys_method_toplevel.resizable(False, False)
        self.gys_method_toplevel.title("Gy's Method")
        self.gys_method_frame = tk.Frame(self.gys_method_toplevel)
        self.gys_method_frame.configure(
            background="#80ffff", height=600, width=600)
        self.largest_particle_dim_label = tk.Label(self.gys_method_frame)
        self.largest_particle_dim_label.configure(
            anchor="center", text='LARGEST PARTICLE DIMENSION [microns]')
        self.largest_particle_dim_label.grid(column=1, row=1)
        self.largest_particle_dim_entry = tk.Entry(self.gys_method_frame)
        self.largest_particle_dim_entry.configure(validate="focusin")
        self.largest_particle_dim_entry.grid(
            column=2, padx="30 30", pady=20, row=1)
        self.sampling_var_lbl = tk.Label(self.gys_method_frame)
        self.sampling_var_lbl.configure(text='SAMPLING ERROR VARIANCE')
        self.sampling_var_lbl.grid(column=1, pady=50, row=2)
        self.sampling_constant_lbl = tk.Label(self.gys_method_frame)
        self.sampling_constant_lbl.configure(text='SAMPLING CONSTANT')
        self.sampling_constant_lbl.grid(column=1, pady="30 50", row=3)
        self.submit_button = tk.Button(self.gys_method_frame)
        self.submit_button.configure(
            background="#ffff80",
            foreground="#000000",
            highlightbackground="#fb466a",
            highlightcolor="#f487f8",
            justify="center",
            text='SUBMIT DATA',
            width=15)
        self.submit_button.grid(column=2, pady="10 20", row=4)
        self.submit_button.configure(command=self.get_input_data)
        self.sampling_error_variance_entry = tk.Entry(self.gys_method_frame)
        self.sampling_error_variance_entry.configure(validate="focusin")
        self.sampling_error_variance_entry.grid(column=2, padx="30 30", row=2)
        self.sampling_constant_entry = tk.Entry(self.gys_method_frame)
        self.sampling_constant_entry.configure(validate="focusin")
        self.sampling_constant_entry.grid(column=2, pady="30 50", row=3)
        self.back_button = ttk.Button(self.gys_method_frame)
        self.back_button.configure(text='BACK')
        self.back_button.grid(column=0, padx=10, pady=10, row=6)
        self.back_button.configure(command=self.go_back)
        self.gys_method_frame.pack(side="top")

        # Main widget
        self.main_window = self.gys_method_toplevel

    def run(self):
        self.main_window.mainloop()

    def go_back(self):
        self.main_window.destroy()
        om_window = OmEquationsListUI()
        om_window.run()

    def get_input_data(self):
        largest_particle_dimension = self.largest_particle_dim_entry.get()
        sampling_error_variance = self.sampling_error_variance_entry.get()
        sampling_constant = self.sampling_constant_entry.get()
        try:
            largest_particle_dimension = float(largest_particle_dimension)
            sampling_error_variance = float(sampling_error_variance)
            sampling_constant = float(sampling_constant)
            has_negative = error_handling.check_for_negative(sampling_error_variance, sampling_constant,
                                                             largest_particle_dimension)
            if has_negative:
                messagebox.showerror('INVALID INPUT', 'Please ensure that all values entered are positive real numbers')
            else:
                sampling_object = minerals.Sampling()
                sampling_object.gys_method(largest_particle_dimension, sampling_error_variance, sampling_constant)
                messagebox.showinfo('OUTPUT',
                                    f'MINIMUM SAMPLING MASS  = {sampling_object.minimum_sample_mass: .2f} grams')

        except ValueError:
            messagebox.showerror('INVALID INPUT', 'Please ensure that all values entered are real numbers')


class DifferentdensitiesUI:
    def __init__(self, master=None):
        # build ui
        self.samp_diff_densities_toplevel = tk.Tk(
        ) if master is None else tk.Toplevel(master)
        self.samp_diff_densities_toplevel.configure(
            height=200, takefocus=True, width=200)
        self.samp_diff_densities_toplevel.resizable(False, False)
        self.samp_diff_densities_toplevel.title(
            "SAMPLING DIFFERENT DENISITY PARTICLES")
        self.sampling_diff_densities_frame = tk.Frame(
            self.samp_diff_densities_toplevel)
        self.sampling_diff_densities_frame.configure(
            background="#80ffff", height=600, width=600)
        self.assay_probability_lbl = tk.Label(
            self.sampling_diff_densities_frame)
        self.assay_probability_lbl.configure(
            anchor="center", text='ASSAY PROBABILITY')
        self.assay_probability_lbl.grid(column=1, pady="10 0", row=1)
        self.assay_probability_entry = tk.Entry(
            self.sampling_diff_densities_frame)
        self.assay_probability_entry.configure(validate="focusin")
        self.assay_probability_entry.grid(column=2, padx=30, pady=20, row=1)
        self.assay_error_perc_lbl = tk.Label(
            self.sampling_diff_densities_frame)
        self.assay_error_perc_lbl.configure(text='ASSAY ERROR %')
        self.assay_error_perc_lbl.grid(column=1, padx=10, pady=30, row=2)
        self.average_particle_size_lbl = tk.Label(
            self.sampling_diff_densities_frame)
        self.average_particle_size_lbl.configure(
            text='AVERAGE PARTICLE SIZE [mm]')
        self.average_particle_size_lbl.grid(column=1, padx=10, pady=30, row=3)
        self.submit_button = tk.Button(self.sampling_diff_densities_frame)
        self.submit_button.configure(
            background="#ffff80",
            foreground="#000000",
            highlightbackground="#fb466a",
            highlightcolor="#f487f8",
            justify="center",
            text='SUBMIT DATA',
            width=15)
        self.submit_button.grid(column=2, pady=20, row=5)
        self.submit_button.configure(command=self.get_input_data)
        self.upload_props_button = tk.Button(
            self.sampling_diff_densities_frame)
        self.upload_props_button.configure(
            background="#ff8000",
            default="normal",
            font="TkDefaultFont",
            justify="left",
            takefocus=False,
            text='UPLOAD PROPORTIONS\n            EXCEL FILE ')
        self.upload_props_button.grid(column=1, padx=10, row=5)
        self.upload_props_button.configure(command=self.get_file)
        self.assay_error_perc_entry = tk.Entry(
            self.sampling_diff_densities_frame)
        self.assay_error_perc_entry.configure(validate="focusin")
        self.assay_error_perc_entry.grid(column=2, padx=30, row=2)
        self.average_particle_size_entry = tk.Entry(
            self.sampling_diff_densities_frame)
        self.average_particle_size_entry.configure(validate="focusin")
        self.average_particle_size_entry.grid(column=2, padx="30 30", row=3)
        self.average_particle_mass_entry = tk.Entry(
            self.sampling_diff_densities_frame)
        self.average_particle_mass_entry.configure(validate="focusin")
        self.average_particle_mass_entry.grid(column=2, padx="30 30", row=4)
        self.average_particle_mass_lbl = tk.Label(
            self.sampling_diff_densities_frame)
        self.average_particle_mass_lbl.configure(
            text='AVERAGE PARTICLE MASS [grams]')
        self.average_particle_mass_lbl.grid(column=1, padx=10, pady=30, row=4)
        self.back_button = ttk.Button(self.sampling_diff_densities_frame)
        self.back_button.configure(text='BACK')
        self.back_button.grid(column=0, padx=10, pady=10, row=6)
        self.back_button.configure(command=self.go_back)
        self.sampling_diff_densities_frame.pack(side="top")

        # Main widget
        self.main_window = self.samp_diff_densities_toplevel

        self.COLUMNS = ['Fraction', 'Mass%', 'Assay%', 'Density']
        self.proportions_file_path = ''

    def run(self):
        self.main_window.mainloop()

    def go_back(self):
        self.main_window.destroy()
        om_window = OmEquationsListUI()
        om_window.run()

    def get_input_data(self):

        if self.proportions_file_path is None or self.proportions_file_path == '':
            messagebox.showerror('No proportions file selected', 'Please select a Proportions_variables.xlsx file')
        else:
            assay_probability = self.assay_probability_entry.get()
            average_particle_size = self.average_particle_size_entry.get()
            average_particle_mass = self.average_particle_mass_entry.get()
            assay_error_perc = self.assay_error_perc_entry.get()

            try:
                assay_probability = float(assay_probability)
                average_particle_size = float(average_particle_size)
                average_particle_mass = float(average_particle_mass)
                assay_error_perc = float(assay_error_perc)
                has_negative = error_handling.check_for_negative(assay_probability, average_particle_size,
                                                                 average_particle_mass, assay_error_perc)
                if has_negative:
                    messagebox.showerror('INVALID INPUT',
                                         'Please ensure that all values entered are positive real numbers')
                elif assay_probability < 0.9 or assay_probability >= 1:
                    messagebox.showerror('Invalid assay probability', 'Assay probability value must be between'
                                                                      ' 0.9(included) and 1(excluded)')
                elif assay_error_perc >= 100:
                    messagebox.showerror('Invalid assay error %', 'Assay error % must be less than 1')

                else:
                    sampling_object = minerals.Sampling()
                    df_proportions = pd.read_excel(self.proportions_file_path)
                    if not error_handling.check_for_nulls(df_proportions):
                        # Remove whitespaces that user might mistakenly enter
                        df_proportions.columns = df_proportions.columns.str.replace(' ', '')
                        if not error_handling.check_df_dtypes(df_proportions):
                            messagebox.showerror('INVALID EXCEL FILE',
                                                 'Please ensure that all entries in excel file are numerical values')
                        else:
                            if error_handling.check_columns(df_proportions, self.COLUMNS):
                                df_diff_density_masses_output = sampling_object.get_sample_diff_densities(
                                    assay_probability,
                                    assay_error_perc,
                                    average_particle_size,
                                    average_particle_mass,
                                    df_proportions)
                                Output.df_to_excel_output(df_diff_density_masses_output)
                            else:
                                messagebox.showerror('COLUMN NAMES INVALID',
                                                     'Please ensure that all column names are'
                                                     ' correct in Proportions_variables.xlsx')
                    else:
                        messagebox.showerror('MISSING VALUES IN FILE',
                                             'Please ensure that all there are no '
                                             'missing values in the Proportions_variables.xlsx file')
            except ValueError:
                messagebox.showerror('INVALID INPUT', 'Please ensure that all values entered are real numbers')

    def get_file(self):
        # Only allows submission of one file type with a set file name
        self.proportions_file_path = filedialog.askopenfilename(title="Proportions spreadsheet",
                                                                filetypes=(("excel files",
                                                                            "Proportions_variables.xlsx"),))


class SeparatorUI:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=200, takefocus=True, width=200)
        toplevel1.resizable(False, False)
        toplevel1.title(
            "SEPARATOR")
        self.separator_frame = tk.Frame(toplevel1)
        self.separator_frame.configure(
            background="#80ffff", height=600, width=600)
        self.input_stream_label = tk.Label(self.separator_frame)
        self.input_stream_label.configure(
            anchor="center", text='INPUT STREAM COMPONENTS')
        self.input_stream_label.grid(column=1, row=1)
        self.input_from_options = tk.StringVar(value='A')
        __values = ['A']
        self.optionmenu_input_from = tk.OptionMenu(
            self.separator_frame, self.input_from_options, *__values, command=None)
        self.optionmenu_input_from.grid(column=3, padx=5, row=1)
        self.from1_label = tk.Label(self.separator_frame)
        self.from1_label.configure(text='FROM:')
        self.from1_label.grid(column=2, padx="50 0", row=1)
        self.to1_label = tk.Label(self.separator_frame)
        self.to1_label.configure(text='TO:')
        self.to1_label.grid(column=4, padx="50 10", row=1)
        self.input_to_options = tk.StringVar(value='J')
        __values = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.optionmenu_input_to = tk.OptionMenu(
            self.separator_frame, self.input_to_options, *__values, command=None)
        self.optionmenu_input_to.grid(column=5, row=1)
        self.input_stream_flowrate_label = tk.Label(self.separator_frame)
        self.input_stream_flowrate_label.configure(
            text='INPUT STREAM FLOW RATE:')
        self.input_stream_flowrate_label.grid(column=6, padx="50 10", row=1)
        self.input_flowrate_entry = tk.Entry(self.separator_frame)
        self.input_flowrate_entry.configure(validate="focusin")
        self.input_flowrate_entry.grid(column=7, padx="30 30", row=1)
        self.output1_stream_label = tk.Label(self.separator_frame)
        self.output1_stream_label.configure(
            text='1ST OUTPUT STREAM COMPONENTS')
        self.output1_stream_label.grid(column=1, pady=100, row=2)
        label6 = tk.Label(self.separator_frame)
        label6.configure(text='2ND OUTPUT STREAM COMPONENTS')
        label6.grid(column=1, pady="0 50", row=3)
        self.from2_label = tk.Label(self.separator_frame)
        self.from2_label.configure(text='FROM:')
        self.from2_label.grid(column=2, padx="50 0", row=2)
        self.output1_from_options = tk.StringVar(value='A')
        __values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        self.optionmenu_output1_from = tk.OptionMenu(
            self.separator_frame, self.output1_from_options, *__values, command=None)
        self.optionmenu_output1_from.grid(column=3, padx=5, row=2)
        self.to2_label = tk.Label(self.separator_frame)
        self.to2_label.configure(text='TO:')
        self.to2_label.grid(column=4, padx="50 0", row=2)
        self.output1_to_options = tk.StringVar(value='J')
        __values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.optionmenu_output1_to = tk.OptionMenu(
            self.separator_frame, self.output1_to_options, *__values, command=None)
        self.optionmenu_output1_to.grid(column=5, row=2)
        self.from3_label = tk.Label(self.separator_frame)
        self.from3_label.configure(text='FROM:')
        self.from3_label.grid(column=2, padx="50 0", pady="0 50", row=3)
        self.output2_from_options = tk.StringVar(value='A')
        __values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        self.optionmenu_output2_from = tk.OptionMenu(
            self.separator_frame, self.output2_from_options, *__values, command=None)
        self.optionmenu_output2_from.grid(column=3, pady="0 50", row=3)
        self.to3_label = tk.Label(self.separator_frame)
        self.to3_label.configure(text='TO:')
        self.to3_label.grid(column=4, padx="50 0", pady="0 50", row=3)
        self.output2_to_options = tk.StringVar(value='J')
        __values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.optionmenu_output2_to = tk.OptionMenu(
            self.separator_frame, self.output2_to_options, *__values, command=None)
        self.optionmenu_output2_to.grid(column=5, pady="0 50", row=3)
        self.comp_info_label = tk.Label(self.separator_frame)
        self.comp_info_label.configure(
            text='COMPONENTS START FROM\nA TO J. THE MAXIMUM \nNUMBER OF COMPONENTS \nTHAT CAN BE IN ANY \nSTREAM = 10')
        self.comp_info_label.grid(column=6, padx="40 0", row=2)
        self.submit_button = tk.Button(self.separator_frame)
        self.submit_button.configure(
            background="#ffff80",
            foreground="#000000",
            highlightbackground="#fb466a",
            highlightcolor="#f487f8",
            justify="center",
            text='SUBMIT DATA',
            width=15)
        self.submit_button.grid(column=7, row=3)
        self.submit_button.configure(command=self.get_input_data)
        self.upload_comps_button = tk.Button(self.separator_frame)
        self.upload_comps_button.configure(
            background="#ff8000",
            default="normal",
            font="TkDefaultFont",
            justify="left",
            takefocus=False,
            text='UPLOAD COMPOSITIONS \n            EXCEL FILE ')
        self.upload_comps_button.grid(column=7, padx=10, row=2)
        self.upload_comps_button.configure(command=self.read_file)
        self.separator_frame.pack(side="top")
        self.composition_file_path = ''

        # Main widget
        self.main_window = toplevel1

    def run(self):
        self.main_window.mainloop()

    def get_input_data(self):
        # TODO: add checks for negatives on each dataframe column
        input_to_option = self.input_to_options.get()

        output1_from_option = self.output1_from_options.get()
        output1_to_option = self.output1_to_options.get()

        output2_from_option = self.output2_from_options.get()
        output2_to_option = self.output2_to_options.get()

        if self.composition_file_path is None or self.composition_file_path == '':
            messagebox.showerror('No composition file selected', 'Please select a composition Excel file')
        elif (output1_from_option > output1_to_option) or (output2_from_option > output2_to_option):
            messagebox.showerror('Invalid range',
                                 'The FROM components must take alphabetical precedence over the TO components')
        elif (input_to_option < output1_to_option) or (input_to_option < output2_to_option):
            messagebox.showerror('Invalid output components',
                                 'Components in output streams must also be present in the input stream')
        else:
            input_flow_rate = self.input_flowrate_entry.get()
            try:
                input_flow_rate = float(input_flow_rate)
                stream_comps_dict = pd.read_excel(self.composition_file_path).to_dict()
                # Using ASCII A till J for loop bounds
                for i in range(ord(input_to_option) - 65 + 1, 10):
                    del stream_comps_dict['Components'][i]
                    del stream_comps_dict['InputStream'][i]
                    del stream_comps_dict['OutputStream1'][i]
                    del stream_comps_dict['OutputStream2'][i]

                stream_comps_df = pd.DataFrame(stream_comps_dict)
                print(stream_comps_df)
                if not error_handling.check_df_dtypes(stream_comps_df.drop(columns=stream_comps_df.columns[0], axis=1)):
                    messagebox.showerror('INVALID EXCEL FILE',
                                         'Please ensure that all entries in excel file are numerical values')
                else:
                    # condition A
                    independent_vars = 0
                    # Condition B
                    max_comps = 0
                    # Condition C
                    count_non_zeros_non_nan = 0

                    for column_name in stream_comps_df.drop("Components", axis=1).columns:
                        column = stream_comps_df[column_name]
                        count_of_non_zeros = (column != 0).sum()
                        count_non_zeros_non_nan += column[column != 0].count()
                        independent_vars += count_of_non_zeros
                        if count_of_non_zeros > max_comps:
                            max_comps = count_of_non_zeros

                    for column_value in ['InputStream', 'OutputStream1', 'OutputStream2']:
                        column_ser = stream_comps_df[column_value]

                        if column_ser.isnull().sum() == 1:
                            fill_value = 1 - column_ser.sum()
                            stream_comps_df[column_value] = stream_comps_df[column_value].fillna(fill_value)

                    column = stream_comps_df['InputStream']
                    if column[column != 0].count() == 0:
                        messagebox.showerror('INVALID INPUT',
                                             'Please supply at least one mole fraction in the input stream')
                    elif ~(independent_vars - max_comps - 1 <= count_non_zeros_non_nan):
                        # Checking DOF
                        messagebox.showerror('Unsolvable', 'Please supply more data in the input file')
                    else:
                        messagebox.showinfo('Data submission', 'Data submitted successfully!')

                    stream_comps = stream_comps_df.copy()
                    separator = material_balance.MaterialBalance()
                    row_index_filled = separator.row_check_method(stream_comps)
                    print(stream_comps)
                    if row_index_filled is None:
                        separator.nan_method(stream_comps, input_flow_rate=input_flow_rate)
                    else:
                        solved_comps_df, stream_flow_rates_dict = separator.row_filled_method(stream_comps,
                                                                                              row_index_filled,
                                                                                              input_flow_rate)
                        for column_value in ['InputStream', 'OutputStream1', 'OutputStream2']:
                            solved_comps_df[column_value] = solved_comps_df[column_value].astype(float).round(2)
                        print(f'solved_comps_df = {solved_comps_df}')
                        print(f'stream_flow_rates_dict = {stream_flow_rates_dict}')
            except ValueError:
                messagebox.showerror('INVALID INPUT', 'Please enter a valid flow rate value')

    def read_file(self):
        self.composition_file_path = filedialog.askopenfilename(title="Composition spreadsheet",
                                                                filetypes=(("excel files", "*.xlsx"),))


class RosinRammlerUI:
    def __init__(self, master=None):
        # build ui
        self.rosin_rammler_toplevel = tk.Tk(
        ) if master is None else tk.Toplevel(master)
        self.rosin_rammler_toplevel.configure(
            height=300, takefocus=True, width=600)
        self.rosin_rammler_toplevel.resizable(True, False)
        self.rosin_rammler_toplevel.title(
            "ROSIN-RAMMLER")
        self.rosin_rammler_frame = tk.Frame(
            self.rosin_rammler_toplevel)
        self.rosin_rammler_frame.configure(
            background="#80ffff", height=300, width=600)
        self.input_size_fraction_lbl = tk.Label(
            self.rosin_rammler_frame)
        self.input_size_fraction_lbl.configure(
            anchor="center", text='INPUT SIZE FRACTION [microns]')
        self.input_size_fraction_lbl.grid(column=1, padx=10, pady=10, row=1)
        self.input_size_fraction_entry = tk.Entry(
            self.rosin_rammler_frame)
        self.input_size_fraction_entry.configure(validate="focusin")
        self.input_size_fraction_entry.grid(column=2, padx=30, pady=20, row=1)
        self.submit_button = tk.Button(self.rosin_rammler_frame)
        self.submit_button.configure(
            background="#ffff80",
            foreground="#000000",
            highlightbackground="#fb466a",
            highlightcolor="#f487f8",
            justify="center",
            text='SUBMIT DATA',
            width=15)
        self.submit_button.grid(column=2, pady=20, row=5)
        self.submit_button.configure(command=self.get_input_data)
        self.upload_sieve_data_button = tk.Button(
            self.rosin_rammler_frame)
        self.upload_sieve_data_button.configure(
            background="#ff8000",
            cursor="arrow",
            default="normal",
            font="TkTextFont",
            justify="left",
            takefocus=False,
            text='UPLOAD SIEVE DATA\n         EXCEL FILE ')
        self.upload_sieve_data_button.grid(column=1, padx=10, row=5)
        self.upload_sieve_data_button.configure(command=self.get_file)
        self.back_button = ttk.Button(self.rosin_rammler_frame)
        self.back_button.configure(text='BACK')
        self.back_button.grid(column=0, padx=10, pady=10, row=6)
        self.back_button.configure(command=self.go_back)
        self.rosin_rammler_frame.pack(side="top")

        # Main widget
        self.main_window = self.rosin_rammler_toplevel
        self.COLUMNS = ['Aperture', 'Mass%', 'Cumulative_Mass%_Passing']
        self.sieve_data_file_path = None
        self.rr_perc_retained_lbl = None  # Hidden output label

    def run(self):
        self.main_window.mainloop()

    def go_back(self):
        self.main_window.destroy()
        om_window = OmEquationsListUI()
        om_window.run()

    def get_input_data(self):
        if self.sieve_data_file_path is None or self.sieve_data_file_path == '':
            messagebox.showerror('No sieve data file selected', 'Please select a sieve_data.xlsx file')
        else:
            input_size_fraction = self.input_size_fraction_entry.get()

            try:
                input_size_fraction = float(input_size_fraction)

                if error_handling.check_for_negative(input_size_fraction):
                    messagebox.showerror('INVALID INPUT',
                                         'Please ensure that all values entered are positive real numbers')
                else:
                    sampling_object = minerals.Sampling()
                    df_sieve_data = pd.read_excel(self.sieve_data_file_path)
                    if not error_handling.check_df_dtypes(
                            df_sieve_data.drop(columns=df_sieve_data.columns[0], axis=1)):
                        messagebox.showerror('INVALID EXCEL FILE',
                                             'Please ensure that all entries in excel file are numerical values')
                    else:
                        if (df_sieve_data.values < 0).any():
                            messagebox.showerror('INVALID DATA IN FILE',
                                                 'Please ensure that all values in the file submitted'
                                                 ' are positive real numbers')
                        else:
                            # Remove whitespaces that user might mistakenly enter
                            df_sieve_data.columns = df_sieve_data.columns.str.replace(' ', '')
                            if error_handling.check_columns(df_sieve_data, self.COLUMNS):
                                if not error_handling.check_for_nulls(df_sieve_data):
                                    rosin_rammler_cumulative_perc_retained = sampling_object.rosin_rammler(
                                        input_size_fraction=input_size_fraction,
                                        df_sieve_analysis_data=df_sieve_data)
                                    self.rr_perc_retained_lbl = ttk.Label(
                                        self.rosin_rammler_frame)
                                    self.rr_perc_retained_lbl.configure(text='CUMULATIVE % RETAINED = ' +
                                                                             str(rosin_rammler_cumulative_perc_retained)
                                                                             + '%')
                                    self.rr_perc_retained_lbl.grid(column=2, row=6, pady=10, padx=10)
                                else:
                                    messagebox.showerror('MISSING VALUES IN FILE',
                                                         'Please ensure that all there are no '
                                                         'missing values in the sieve_data.xlsx file')
                            else:
                                messagebox.showerror('COLUMN NAMES INVALID',
                                                     'Please ensure that all column names are'
                                                     ' correct in Proportions_variables.xlsx')
            except ValueError:
                messagebox.showerror('INVALID INPUT', 'Please ensure that all values entered are real numbers')

    def get_file(self):
        # Only allows submission of one file type with a set file name
        self.sieve_data_file_path = filedialog.askopenfilename(title="Sieve data spreadsheet",
                                                               filetypes=(("excel files",
                                                                           "sieve_data.xlsx"),))


class GaudinSchuhmannUI:
    def __init__(self, master=None):
        # build ui
        self.gaudinn_schuhmann_toplevel = tk.Tk(
        ) if master is None else tk.Toplevel(master)
        self.gaudinn_schuhmann_toplevel.configure(
            height=200, takefocus=True, width=200)
        self.gaudinn_schuhmann_toplevel.resizable(False, False)
        self.gaudinn_schuhmann_toplevel.title(
            "GAUDINN-SCHUHMANN")
        self.gaudin_schuhmann_frame = tk.Frame(
            self.gaudinn_schuhmann_toplevel)
        self.gaudin_schuhmann_frame.configure(
            background="#80ffff", height=600, width=600)
        self.input_size_fraction_lbl = tk.Label(
            self.gaudin_schuhmann_frame)
        self.input_size_fraction_lbl.configure(
            anchor="center", text='INPUT SIZE FRACTION [microns]')
        self.input_size_fraction_lbl.grid(column=1, padx=10, pady=10, row=1)
        self.input_size_fraction_entry = tk.Entry(
            self.gaudin_schuhmann_frame)
        self.input_size_fraction_entry.configure(validate="focusin")
        self.input_size_fraction_entry.grid(column=2, padx=30, pady=20, row=1)
        self.submit_button = tk.Button(self.gaudin_schuhmann_frame)
        self.submit_button.configure(
            background="#ffff80",
            foreground="#000000",
            highlightbackground="#fb466a",
            highlightcolor="#f487f8",
            justify="center",
            text='SUBMIT DATA',
            width=15)
        self.submit_button.grid(column=2, pady=20, row=5)
        self.submit_button.configure(command=self.get_input_data)
        self.upload_sieve_data_button = tk.Button(
            self.gaudin_schuhmann_frame)
        self.upload_sieve_data_button.configure(
            background="#ff8000",
            cursor="arrow",
            default="normal",
            font="TkTextFont",
            justify="left",
            takefocus=False,
            text='UPLOAD SIEVE DATA\n         EXCEL FILE ')
        self.upload_sieve_data_button.grid(column=1, padx=10, row=5)
        self.upload_sieve_data_button.configure(command=self.get_file)
        self.back_button = ttk.Button(self.gaudin_schuhmann_frame)
        self.back_button.configure(text='BACK')
        self.back_button.grid(column=0, padx=10, pady=10, row=6)
        self.back_button.configure(command=self.go_back)
        self.gaudin_schuhmann_frame.pack(side="top")

        # Main widget
        self.main_window = self.gaudinn_schuhmann_toplevel
        self.COLUMNS = ['Aperture', 'Mass%', 'Cumulative_Mass%_Passing']
        self.sieve_data_file_path = None
        self.gs_perc_retained_lbl = None  # Hidden output label

    def run(self):
        self.main_window.mainloop()

    def go_back(self):
        self.main_window.destroy()
        om_window = OmEquationsListUI()
        om_window.run()

    def get_input_data(self):
        if self.sieve_data_file_path is None or self.sieve_data_file_path == '':
            messagebox.showerror('No sieve data file selected', 'Please select a sieve_data.xlsx file')
        else:
            input_size_fraction = self.input_size_fraction_entry.get()

            try:
                input_size_fraction = float(input_size_fraction)

                if input_size_fraction == 1:
                    messagebox.showerror('INVALID INPUT',
                                         'Please ensure that all values entered are positive real numbers')
                else:
                    sampling_object = minerals.Sampling()
                    df_sieve_data = pd.read_excel(self.sieve_data_file_path)
                    if not error_handling.check_df_dtypes(
                            df_sieve_data.drop(columns=df_sieve_data.columns[0], axis=1)):
                        messagebox.showerror('INVALID EXCEL FILE',
                                             'Please ensure that all entries in excel file are numerical values')
                    else:
                        if (df_sieve_data.values < 0).any():
                            messagebox.showerror('INVALID DATA IN FILE',
                                                 'Please ensure that all values in the file submitted'
                                                 ' are positive real numbers')
                        else:
                            # Remove whitespaces that user might mistakenly enter
                            df_sieve_data.columns = df_sieve_data.columns.str.replace(' ', '')
                            if error_handling.check_columns(df_sieve_data, self.COLUMNS):
                                if not error_handling.check_for_nulls(df_sieve_data):
                                    gaudin_schuhmann_cumulative_perc_retained = sampling_object.gaudin_schuhmann(
                                        input_size_fraction=input_size_fraction,
                                        df_sieve_analysis_data=df_sieve_data)
                                    self.gs_perc_retained_lbl = ttk.Label(self.gaudin_schuhmann_frame)
                                    self.gs_perc_retained_lbl.configure(text='CUMULATIVE % RETAINED = ' +
                                                                        str(gaudin_schuhmann_cumulative_perc_retained)
                                                                        + '%')
                                    self.gs_perc_retained_lbl.grid(column=2, row=6, pady=10, padx=10)
                                else:
                                    messagebox.showerror('MISSING VALUES IN FILE',
                                                         'Please ensure that all there are no '
                                                         'missing values in the sieve_data.xlsx file')
                            else:
                                messagebox.showerror('COLUMN NAMES INVALID',
                                                     'Please ensure that all column names are'
                                                     ' correct in Proportions_variables.xlsx')
            except ValueError:
                messagebox.showerror('INVALID INPUT', 'Please ensure that all values entered are real numbers')

    def get_file(self):
        # Only allows submission of one file type with a set file name
        self.sieve_data_file_path = filedialog.askopenfilename(title="Sieve data spreadsheet",
                                                               filetypes=(("excel files",
                                                                           "sieve_data.xlsx"),))


class MillSpeedUI:
    def __init__(self, master=None):
        # build ui
        self.mill_speed_toplevel = tk.Tk() if master is None else tk.Toplevel(master)
        self.mill_speed_toplevel.configure(
            height=200, takefocus=True, width=200)
        self.mill_speed_toplevel.resizable(False, False)
        self.mill_speed_toplevel.title("CRITICAL MILL SPEED")
        self.mill_speed_frame = tk.Frame(self.mill_speed_toplevel)
        self.mill_speed_frame.configure(
            background="#80ffff", height=600, width=600)
        self.mill_diameter_lbl = tk.Label(self.mill_speed_frame)
        self.mill_diameter_lbl.configure(anchor="center", text='MILL DIAMETER [m]')
        self.mill_diameter_lbl.grid(column=1, row=1)
        self.mill_diameter_entry = tk.Entry(self.mill_speed_frame)
        self.mill_diameter_entry.configure(validate="focusin")
        self.mill_diameter_entry.grid(column=2, padx="30 30", pady=20, row=1)
        self.ball_diameter_lbl = tk.Label(self.mill_speed_frame)
        self.ball_diameter_lbl.configure(text='BALL DIAMETER [m]')
        self.ball_diameter_lbl.grid(column=1, padx=20, pady=50, row=2)
        self.calculate_mill_power_button = tk.Button(self.mill_speed_frame)
        self.calculate_mill_power_button.configure(
            background="#ffff80",
            foreground="#000000",
            highlightbackground="#fb466a",
            highlightcolor="#f487f8",
            justify="center",
            text='CALCULATE MILL SPEED',
            width=20)
        self.calculate_mill_power_button.grid(column=1, padx=10, pady="10 20", row=4)
        self.calculate_mill_power_button.configure(command=self.calculate_mill_speed)
        self.ball_diameter_entry = tk.Entry(self.mill_speed_frame)
        self.ball_diameter_entry.configure(validate="focusin")
        self.ball_diameter_entry.grid(column=2, padx="30 30", row=2)
        self.back_button = ttk.Button(self.mill_speed_frame)
        self.back_button.configure(text='BACK')
        self.back_button.grid(column=0, padx=10, pady=10, row=6)
        self.back_button.configure(command=self.go_back)
        self.mill_speed_frame.pack(side="top")

        # Main widget
        self.main_window = self.mill_speed_toplevel
        self.mill_speed_lbl = None  # Hidden label, displays output

    def run(self):
        self.main_window.mainloop()

    def go_back(self):
        self.main_window.destroy()
        om_window = OmEquationsListUI()
        om_window.run()

    def calculate_mill_speed(self):
        ball_diameter = self.ball_diameter_entry.get()
        mill_diameter = self.mill_diameter_entry.get()
        try:
            ball_diameter = float(ball_diameter)
            mill_diameter = float(mill_diameter)
            milling_obj = minerals.Milling()
            if error_handling.check_for_negative(mill_diameter, mill_diameter):
                messagebox.showerror('INVALID INPUT', 'Please ensure that all values entered are positive real numbers')
            if not mill_diameter <= ball_diameter:
                mill_critical_speed = round(milling_obj.get_mill_critical_speed(ball_diameter=ball_diameter,
                                                                                mill_diameter=mill_diameter), 2)
                self.mill_speed_lbl = ttk.Label(self.mill_speed_frame)
                self.mill_speed_lbl.configure(text='MILL CRITICAL SPEED = ' + str(mill_critical_speed))
                self.mill_speed_lbl.grid(column=2, row=6, pady=10, padx=10)
            else:
                messagebox.showerror('INVALID INPUT', 'Ball diameter cannot be greater than '
                                                      'or equal to mill diameter')
        except ValueError:
            messagebox.showerror('INVALID INPUT', 'Please ensure that all values entered are real numbers')
        except ZeroDivisionError:
            messagebox.showerror('DIVISION BY ZERO', 'Please ensure that the values for ball diameter '
                                                     'and mill diameter are not equal')


class MillPowerUI:
    def __init__(self, master=None):
        # build ui
        self.mill_power_toplevel = tk.Tk() if master is None else tk.Toplevel(master)
        self.mill_power_toplevel.configure(
            height=200, takefocus=True, width=200)
        self.mill_power_toplevel.resizable(False, False)
        self.mill_power_toplevel.title("REQUIRED MILL POWER [kW]")
        self.mill_power_frame = tk.Frame(self.mill_power_toplevel)
        self.mill_power_frame.configure(
            background="#80ffff", height=600, width=600)
        self.work_index_lbl = tk.Label(self.mill_power_frame)
        self.work_index_lbl.configure(anchor="center", text='WORK INDEX')
        self.work_index_lbl.grid(column=1, pady="10 0", row=1)
        self.work_index_entry = tk.Entry(self.mill_power_frame)
        self.work_index_entry.configure(validate="focusin")
        self.work_index_entry.grid(column=2, padx=30, pady=20, row=1)
        self.product_size_lbl = tk.Label(self.mill_power_frame)
        self.product_size_lbl.configure(text='PRODUCT SIZE [microns]')
        self.product_size_lbl.grid(column=1, padx=10, pady=30, row=2)
        self.feed_size_lbl = tk.Label(self.mill_power_frame)
        self.feed_size_lbl.configure(text='FEED SIZE [microns]')
        self.feed_size_lbl.grid(column=1, padx=10, pady=30, row=3)
        self.calculate_mill_power_button = tk.Button(self.mill_power_frame)
        self.calculate_mill_power_button.configure(
            background="#ffff80",
            foreground="#000000",
            highlightbackground="#fb466a",
            highlightcolor="#f487f8",
            justify="center",
            text='CALCULATE MILL POWER',
            width=20)
        self.calculate_mill_power_button.grid(column=1, padx='180 0', pady=20, row=5)
        self.calculate_mill_power_button.configure(command=self.calculate_mill_power)
        self.product_size_entry = tk.Entry(self.mill_power_frame)
        self.product_size_entry.configure(validate="focusin")
        self.product_size_entry.grid(column=2, padx=30, row=2)
        self.feed_size_entry = tk.Entry(self.mill_power_frame)
        self.feed_size_entry.configure(validate="focusin")
        self.feed_size_entry.grid(column=2, padx="30 30", row=3)
        self.dry_solid_mass_flowrate_entry = tk.Entry(self.mill_power_frame)
        self.dry_solid_mass_flowrate_entry.configure(validate="focusin")
        self.dry_solid_mass_flowrate_entry.grid(column=2, padx="30 30", row=4)
        self.dry_solid_mass_flowrate_lbl = tk.Label(self.mill_power_frame)
        self.dry_solid_mass_flowrate_lbl.configure(
            text='DRY SOLID MASS FLOWRATE [t/h]')
        self.dry_solid_mass_flowrate_lbl.grid(
            column=1, padx=10, pady=30, row=4)
        self.back_button = ttk.Button(self.mill_power_frame)
        self.back_button.configure(text='BACK')
        self.back_button.grid(column=0, padx=10, pady=10, row=6)
        self.back_button.configure(command=self.go_back)
        self.mill_power_frame.pack(side="top")

        # Main widget
        self.main_window = self.mill_power_toplevel

    def run(self):
        self.main_window.mainloop()

    def go_back(self):
        self.main_window.destroy()
        om_window = OmEquationsListUI()
        om_window.run()

    def calculate_mill_power(self):
        work_index = self.work_index_entry.get()
        product_size = self.product_size_entry.get()
        feed_size = self.feed_size_entry.get()
        dry_solid_mass_flowrate = self.dry_solid_mass_flowrate_entry.get()
        try:
            work_index = float(work_index)
            product_size = float(product_size)
            feed_size = float(feed_size)
            dry_solid_mass_flowrate = float(dry_solid_mass_flowrate)

            milling_obj = minerals.Milling()
            if error_handling.check_for_non_positive(work_index, product_size, feed_size, dry_solid_mass_flowrate):
                messagebox.showerror('INVALID INPUT', 'Please ensure that all values entered are positive real numbers')
            elif product_size > feed_size:
                messagebox.showerror('INVALID INPUT', 'Product size cannot be greater than feed size')
            else:
                mill_power = round(milling_obj.get_mill_power(work_index, product_size, feed_size,
                                                              dry_solid_mass_flowrate), 2)
                messagebox.showinfo('OUTPUT', f'Required mill power = {mill_power}')
        except ValueError:
            messagebox.showerror('INVALID INPUT', 'Please ensure that all values entered are real numbers')


class PercentageSolidsUI:
    def __init__(self, master=None):
        # build ui
        self.percentage_solids_toplevel = tk.Tk() if master is None else tk.Toplevel(master)
        self.percentage_solids_toplevel.configure(
            height=200, takefocus=True, width=200)
        self.percentage_solids_toplevel.resizable(False, False)
        self.percentage_solids_toplevel.title("PERCENTAGE SOLIDS [%]")
        self.percentage_solids_frame = tk.Frame(
            self.percentage_solids_toplevel)
        self.percentage_solids_frame.configure(
            background="#80ffff", height=600, width=600)
        self.slurry_density_lbl = tk.Label(self.percentage_solids_frame)
        self.slurry_density_lbl.configure(
            anchor="center", text='SLURRY DENSITY [kg/m3]')
        self.slurry_density_lbl.grid(column=1, pady="10 0", row=1)
        self.slurry_density_entry = tk.Entry(self.percentage_solids_frame)
        self.slurry_density_entry.configure(validate="focusin")
        self.slurry_density_entry.grid(column=2, padx=30, pady=20, row=1)
        self.dry_solid_density_lbl = tk.Label(self.percentage_solids_frame)
        self.dry_solid_density_lbl.configure(text='DRY SOLID DENSITY [kg/m3]')
        self.dry_solid_density_lbl.grid(column=1, padx=10, pady=30, row=2)
        self.submit_button = tk.Button(self.percentage_solids_frame)
        self.submit_button.configure(
            background="#ffff80",
            foreground="#000000",
            highlightbackground="#fb466a",
            highlightcolor="#f487f8",
            justify="center",
            text='CALCULATE % SOLIDS',
            width=20)
        self.submit_button.grid(column=1, padx="180 0", pady=20, row=5)
        self.submit_button.configure(command=self.calculate_percentage_solids)
        self.dry_solid_density_entry = tk.Entry(self.percentage_solids_frame)
        self.dry_solid_density_entry.configure(validate="focusin")
        self.dry_solid_density_entry.grid(column=2, padx=30, row=2)
        self.back_button = ttk.Button(self.percentage_solids_frame)
        self.back_button.configure(text='BACK')
        self.back_button.grid(column=0, padx=10, pady=10, row=6)
        self.back_button.configure(command=self.go_back)
        self.percentage_solids_frame.pack(side="top")

        # Main widget
        self.main_window = self.percentage_solids_toplevel

    def run(self):
        self.main_window.mainloop()

    def go_back(self):
        self.main_window.destroy()
        om_window = OmEquationsListUI()
        om_window.run()

    def calculate_percentage_solids(self):
        slurry_density = self.slurry_density_entry.get()
        dry_solid_density = self.dry_solid_density_entry.get()
        try:
            slurry_density = float(slurry_density)
            dry_solid_density = float(dry_solid_density)

            milling_obj = minerals.Milling()
            if error_handling.check_for_non_positive(slurry_density, dry_solid_density):
                messagebox.showerror('INVALID INPUT', 'Please ensure that all values entered are positive real numbers')
            else:
                percentage_solids = round(milling_obj.get_percentage_solids(slurry_density, dry_solid_density), 2)
                if percentage_solids > 100:
                    messagebox.showerror('INVALID INPUT', 'Input values result in a percentage > 100')
                else:
                    messagebox.showinfo('OUTPUT', f'Percentage solids = {percentage_solids} %')
        except ValueError:
            messagebox.showerror('INVALID INPUT', 'Please ensure that all values entered are real numbers')
        except ZeroDivisionError:
            messagebox.showerror('INVALID INPUTS', 'Input values result in division by zero, please try again')


class DryMassFlowrateUI:
    def __init__(self, master=None):
        self.combo_box_options = ["DRY SOLID DENSITY [kg/m3]", "PERCENTAGE SOLIDS [%]"]
        # build ui
        self.dry_solid_mass_flowrate_toplevel = tk.Tk(
        ) if master is None else tk.Toplevel(master)
        self.dry_solid_mass_flowrate_toplevel.configure(
            height=200, takefocus=True, width=200)
        self.dry_solid_mass_flowrate_toplevel.resizable(False, False)
        self.dry_solid_mass_flowrate_toplevel.title("DRY MASS FLOWRATE [kg/h]")
        self.dry_solid_mass_flowrate_frame = tk.Frame(
            self.dry_solid_mass_flowrate_toplevel)
        self.dry_solid_mass_flowrate_frame.configure(
            background="#80ffff", height=600, width=600)
        self.slurry_vol_flowrate_lbl = tk.Label(
            self.dry_solid_mass_flowrate_frame)
        self.slurry_vol_flowrate_lbl.configure(
            anchor="center", text='SLURRY VOLUMETRIC FLOWRATE [m3/h]')
        self.slurry_vol_flowrate_lbl.grid(column=1, padx=20, row=1)
        self.slurry_vol_flowrate_entry = tk.Entry(
            self.dry_solid_mass_flowrate_frame)
        self.slurry_vol_flowrate_entry.configure(validate="focusin")
        self.slurry_vol_flowrate_entry.grid(
            column=2, padx="30 30", pady=20, row=1)
        self.slurry_density_lbl = tk.Label(self.dry_solid_mass_flowrate_frame)
        self.slurry_density_lbl.configure(text='SLURRY DENSITY [kg/m3]')
        self.slurry_density_lbl.grid(column=1, pady=50, row=2)
        self.calculate_dry_mass_flowrate_button = tk.Button(
            self.dry_solid_mass_flowrate_frame)
        self.calculate_dry_mass_flowrate_button.configure(
            background="#ffff80",
            foreground="#000000",
            highlightbackground="#fb466a",
            highlightcolor="#f487f8",
            justify="center",
            text='CALCULATE DRY MASS FLOWRATE',
            width=30)
        self.calculate_dry_mass_flowrate_button.grid(
            column=2, padx=20, pady=20, row=4)
        self.calculate_dry_mass_flowrate_button.configure(
            command=self.calculate_dry_mass_flowrate)
        self.slurry_density_entry = tk.Entry(
            self.dry_solid_mass_flowrate_frame)
        self.slurry_density_entry.configure(validate="focusin")
        self.slurry_density_entry.grid(column=2, padx="30 30", row=2)
        self.perc_density_solids_entry = ttk.Entry(
            self.dry_solid_mass_flowrate_frame)
        self.perc_density_solids_entry.grid(column=2, row=3)
        self.perc_density_cmbox = ttk.Combobox(
            self.dry_solid_mass_flowrate_frame)
        self.perc_density_cmbox.configure(
            state="readonly",
            values=self.combo_box_options)
        self.perc_density_cmbox.grid(column=1, padx=20, row=3)
        self.perc_density_cmbox.current(0)
        self.back_button = ttk.Button(self.dry_solid_mass_flowrate_frame)
        self.back_button.configure(text='BACK')
        self.back_button.grid(column=0, padx=10, pady=10, row=6)
        self.back_button.configure(command=self.go_back)
        self.dry_solid_mass_flowrate_frame.pack(side="top")

        # Main widget
        self.main_window = self.dry_solid_mass_flowrate_toplevel

    def run(self):
        self.main_window.mainloop()

    def go_back(self):
        self.main_window.destroy()
        om_window = OmEquationsListUI()
        om_window.run()

    def calculate_dry_mass_flowrate(self):
        slurry_density = self.slurry_density_entry.get()
        slurry_vol_flowrate = self.slurry_vol_flowrate_entry.get()
        if str(self.perc_density_cmbox.get()) == self.combo_box_options[0]:
            dry_solid_density = self.perc_density_solids_entry.get()
            try:
                slurry_density = float(slurry_density)
                slurry_vol_flowrate = float(slurry_vol_flowrate)
                dry_solid_density = float(dry_solid_density)
                milling_obj = minerals.Milling()
                if error_handling.check_for_non_positive(slurry_density, dry_solid_density, slurry_vol_flowrate):
                    messagebox.showerror('INVALID INPUT',
                                         'Please ensure that all values entered are positive real numbers')
                else:
                    milling_obj.get_dry_solid_mass_flowrate(
                        slurry_vol_flowrate=slurry_vol_flowrate,
                        slurry_density=slurry_density,
                        dry_solid_density=dry_solid_density)
                    messagebox.showinfo('OUTPUT', f'Dry mass flowrate = {milling_obj.dry_solid_mass_flowrate} kg/h')
            except ValueError:
                messagebox.showerror('INVALID INPUT', 'Please ensure that all values entered are real numbers')
            except ZeroDivisionError:
                messagebox.showerror('INVALID INPUTS', 'Input values result in division by zero, please try again')
        else:
            percentage_solids = self.perc_density_solids_entry.get()
            try:
                slurry_density = float(slurry_density)
                slurry_vol_flowrate = float(slurry_vol_flowrate)
                percentage_solids = float(percentage_solids)
                milling_obj = minerals.Milling()
                if error_handling.check_for_non_positive(slurry_density, percentage_solids, slurry_vol_flowrate):
                    messagebox.showerror('INVALID INPUT',
                                         'Please ensure that all values entered are positive real numbers')
                elif percentage_solids > 100:
                    messagebox.showerror('INVALID INPUT', 'Percentage solids input cannot be > 100')
                else:
                    milling_obj.get_dry_solid_mass_flowrate(
                        slurry_vol_flowrate=slurry_vol_flowrate,
                        slurry_density=slurry_density,
                        percentage_solids=percentage_solids)
                    messagebox.showinfo('OUTPUT', f'Dry mass flowrate = {milling_obj.dry_solid_mass_flowrate} kg/h')
            except ValueError:
                messagebox.showerror('INVALID INPUT', 'Please ensure that all values entered are real numbers')
            except ZeroDivisionError:
                messagebox.showerror('INVALID INPUTS', 'Input values result in division by zero, please try again')


class PopuationBalanceUI:
    def __init__(self, master=None):
        # build ui
        self.population_balance_toplevel = tk.Tk(
        ) if master is None else tk.Toplevel(master)
        self.population_balance_toplevel.configure(
            height=200, takefocus=True, width=200)
        self.population_balance_toplevel.resizable(False, False)
        self.population_balance_toplevel.title("POPULATION BALANCE")
        self.population_balance_frame = tk.Frame(
            self.population_balance_toplevel)
        self.population_balance_frame.configure(
            background="#80ffff", height=600, width=600)
        self.residence_time_lbl = tk.Label(self.population_balance_frame)
        self.residence_time_lbl.configure(
            anchor="center", text='RESIDENCE TIME')
        self.residence_time_lbl.grid(column=1, padx=5, pady=10, row=1)
        self.residence_time_entry = tk.Entry(self.population_balance_frame)
        self.residence_time_entry.configure(validate="focusin")
        self.residence_time_entry.grid(column=2, padx=0, pady=20, row=1)
        self.submit_button = tk.Button(self.population_balance_frame)
        self.submit_button.configure(
            background="#ffff80",
            foreground="#000000",
            highlightbackground="#fb466a",
            highlightcolor="#f487f8",
            justify="center",
            text='SUBMIT DATA',
            width=15)
        self.submit_button.grid(column=1, pady=20, row=3)
        self.submit_button.configure(command=self.get_input_data)
        self.population_data_button = tk.Button(self.population_balance_frame)
        self.population_data_button.configure(
            background="#ff8000",
            cursor="arrow",
            default="normal",
            font="TkTextFont",
            justify="left",
            takefocus=False,
            text='UPLOAD POPULATION BALANCE DATA\n           \t        EXCEL FILE ')
        self.population_data_button.grid(column=1, padx=10, pady=20, row=2)
        self.population_data_button.configure(command=self.get_population_file)
        self.breakage_data_button = tk.Button(self.population_balance_frame)
        self.breakage_data_button.configure(
            background="#ff8000",
            cursor="arrow",
            default="normal",
            font="TkTextFont",
            justify="left",
            takefocus=False,
            text='UPLOAD BREAKAGE\n   DATA EXCEL FILE ')
        self.breakage_data_button.grid(column=2, padx="20 10", pady=20, row=2)
        self.breakage_data_button.configure(command=self.get_breakage_file)
        self.back_button = ttk.Button(self.population_balance_frame)
        self.back_button.configure(text='BACK')
        self.back_button.grid(column=0, padx=10, pady=10, row=6)
        self.back_button.configure(command=self.go_back)
        self.population_balance_frame.pack(side="top")

        # Main widget
        self.main_window = self.population_balance_toplevel

        self.population_balance_data_path = None
        self.breakage_data_path = None
        self.breakage_columns = []
        self.POPULATION_COLUMNS = ['Interval_number', 'Selection_function', 'Mass_fraction']

    def run(self):
        self.main_window.mainloop()

    def go_back(self):
        self.main_window.destroy()
        om_window = OmEquationsListUI()
        om_window.run()

    def get_input_data(self):
        if self.breakage_data_path is None or self.breakage_data_path == '':
            messagebox.showerror('No breakage data file selected',
                                 'Please select a breakage_data.xlsx file')
        if self.population_balance_data_path is None or self.population_balance_data_path == '':
            messagebox.showerror('No population balance file selected',
                                 'Please select a population_balance_data.xlsx file')
        else:
            residence_time = self.residence_time_entry.get()
            try:
                residence_time = float(residence_time)
                error_handling.check_for_negative(residence_time)
                if error_handling.check_for_non_positive(residence_time):
                    messagebox.showerror('INVALID INPUT',
                                         'Please ensure that the residence time is a positive real number')
                else:
                    milling_object = minerals.Milling()
                    df_breakage_matrix = pd.read_excel(self.breakage_data_path)
                    df_pop_balance_data = pd.read_excel(self.population_balance_data_path)
                    if error_handling.check_for_nulls(df_breakage_matrix) and error_handling.check_for_nulls(
                            df_pop_balance_data):
                        messagebox.showerror('MISSING VALUES IN FILES',
                                             'Please ensure that all there are no '
                                             'missing values in the uploaded excel files')
                    else:
                        if not error_handling.check_df_dtypes(df_pop_balance_data.drop(
                                columns=df_pop_balance_data.columns[0], axis=1)) or \
                                error_handling.check_df_dtypes(df_breakage_matrix.drop(
                                columns=df_breakage_matrix.columns[0], axis=1)):
                            messagebox.showerror('INVALID EXCEL FILE',
                                                 'Please ensure that all entries in excel files are numerical values')
                        else:
                            # Remove whitespaces that user might mistakenly enter
                            df_breakage_matrix.columns = df_breakage_matrix.columns.str.replace(' ', '')
                            df_pop_balance_data.columns = df_pop_balance_data.columns.str.replace(' ', '')
                            if error_handling.check_columns(df_pop_balance_data, self.POPULATION_COLUMNS):
                                df_product_mass_fractions = milling_object.breakage_prediction(df_breakage_matrix,
                                                                                               df_pop_balance_data,
                                                                                               residence_time)
                                Output.df_to_excel_output(df_product_mass_fractions)
                            else:
                                messagebox.showerror('COLUMN NAMES INVALID',
                                                     'Please ensure that all column names are'
                                                     ' correct in Proportions_variables.xlsx')
            except ValueError:
                messagebox.showerror('INVALID INPUT', 'Please ensure that all values entered are real numbers')

    def get_breakage_file(self):
        self.breakage_data_path = filedialog.askopenfilename(title="Breakage data spreadsheet",
                                                             filetypes=(("excel files",
                                                                         "breakage_data.xlsx"),))

    def get_population_file(self):
        self.population_balance_data_path = filedialog.askopenfilename(title="Populatin balance data spreadsheet",
                                                                       filetypes=(("excel files",
                                                                                   "population_balance_data.xlsx"),))


class ApiGravityUI:
    def __init__(self, master=None):
        # build ui
        self.specific_gravity_toplevel = tk.Tk() if master is None else tk.Toplevel(master)
        self.specific_gravity_toplevel.configure(
            height=200, takefocus=True, width=200)
        self.specific_gravity_toplevel.resizable(False, False)
        self.specific_gravity_toplevel.title("PERCENTAGE SOLIDS")
        self.specific_gravity_frame = tk.Frame(self.specific_gravity_toplevel)
        self.specific_gravity_frame.configure(
            background="#80ffff", height=600, width=600)
        self.specific_gravity_lbl = tk.Label(self.specific_gravity_frame)
        self.specific_gravity_lbl.configure(
            anchor="center", text='SPECIFIC  GRAVITY')
        self.specific_gravity_lbl.grid(column=1, pady="10 0", row=1)
        self.specific_gravity_entry = tk.Entry(self.specific_gravity_frame)
        self.specific_gravity_entry.configure(validate="focusin")
        self.specific_gravity_entry.grid(column=2, padx=30, pady=20, row=1)
        self.calc_api_gravity_button = tk.Button(self.specific_gravity_frame)
        self.calc_api_gravity_button.configure(
            background="#ffff80",
            foreground="#000000",
            highlightbackground="#fb466a",
            highlightcolor="#f487f8",
            justify="center",
            text='CALCULATE API GRAVITY',
            width=20)
        self.calc_api_gravity_button.grid(
            column=1, padx="180 0", pady=20, row=5)
        self.calc_api_gravity_button.configure(command=self.calculate_api_gravity)
        self.back_button = ttk.Button(self.specific_gravity_frame)
        self.back_button.configure(text='BACK')
        self.back_button.grid(column=0, padx=10, pady=10, row=6)
        self.back_button.configure(command=self.go_back)
        self.specific_gravity_frame.pack(side="top")

        # Main widget
        self.main_window = self.specific_gravity_toplevel

    def run(self):
        self.main_window.mainloop()

    def go_back(self):
        self.main_window.destroy()
        om_window = OmEquationsListUI()
        om_window.run()

    def calculate_api_gravity(self):
        specific_gravity = self.specific_gravity_entry.get()
        try:
            specific_gravity = float(specific_gravity)

            if error_handling.check_for_non_positive(specific_gravity):
                messagebox.showerror('INVALID INPUT', 'Please ensure that all values entered are positive real numbers')
            else:
                crude_oil_object = oils.CrudeOil()
                crude_oil_object.api_gravity(specific_gravity)
                messagebox.showinfo('OUTPUT',
                                    f'API GRAVITY = {crude_oil_object.api_gravity: .2f} ')

        except ValueError:
            messagebox.showerror('INVALID INPUT', 'Please ensure that all values entered are real numbers')


class Output:
    @staticmethod
    def df_to_excel_output(df_output):
        messagebox.showinfo('DATA SUBMISSION', 'Data submitted successfully!')
        output_file_directory = filedialog.askdirectory(title='Select folder for output file')
        df_output.to_excel(output_file_directory + '/output.xlsx',
                           sheet_name='Output')
        messagebox.showinfo('FILE DOWNLOAD', 'Output file named output.xlsx successfully downloaded')
