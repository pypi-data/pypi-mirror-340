import numpy as np
from scipy.integrate import solve_ivp
import re

class SurfaceKineticsPuretzky2005:
    def __init__(self, carb_strc_surface=False, carb_deactiv=False, 
                 plot_request=True, initial_conditions=None, 
                 dp=10e-9, P_FEEDSTOCK=266.645, feedstock_gas_name="C2H2",
                 main_product_species=["C2H4", "C4H4"], reactor_volume=5.5e-3,
                 n0=2.2775521143014057e+22, np1=1e4, np2=1e4,
                 surface_coverage_gp=1, gas_NP_time_considered=True,
                 current_H2_flux=1, H2_STICKING_PROBABILITY=0.2):
        
        self.surface_coverage_gp = surface_coverage_gp
        self.P_FEEDSTOCK = P_FEEDSTOCK
        self.initial_conditions = initial_conditions or [0, 0, 0, 0, 0]
        self.dp = dp
        self.n0 = n0
        self.np1 = np1
        self.np2 = np2
        self.reactor_volume = reactor_volume
        self.gas_NP_time_considered = gas_NP_time_considered
        self.current_H2_flux = current_H2_flux
        self.H2_STICKING_PROBABILITY = H2_STICKING_PROBABILITY
        self.carb_strc_surface = carb_strc_surface
        self.carb_deactiv = carb_deactiv
        self.plot_request = plot_request
        self.feedstock_gas_name = feedstock_gas_name
        self.main_product_species = main_product_species

        self.species_weight = self.mass_calculator(self.feedstock_gas_name)
        mass_1 = self.mass_calculator(main_product_species[0])
        mass_2 = self.mass_calculator(main_product_species[1])
        self.average_species_weight_product = (mass_1 * np1 + mass_2 * np2) / (np1 + np2)

        self.NAVA = 6.022e23  # Avogadro's number
        self.kb = 1.38065e-23  # Boltzmann constant, J/K

        self.S_0 = surface_coverage_gp * np.pi * (dp)**2  # Catalyst surface area (m²)
        self.n_m = 1e19  # Surface carbon monolayer density
        self.alpha = 1  # Monolayer count

        # Activation energies (eV)
        self.E_a1 = 0.41
        self.E_sb = 2.2
        self.E_b = 1.5
        self.E_p = 2.60
        self.E_rl = 2.4

        # Kinetic parameters
        self.k_sb_known = 17
        self.T_known = 575 + 273.15
        self.k_c1 = 3e-3
        self.k_d1 = 1
        self.k_d2 = 1
        self.B = self.k_sb_known / np.exp(-self.E_sb / (8.617e-5 * self.T_known))

    @staticmethod
    def mass_calculator(species):
        atomic_masses = {'H': 1.00784, 'C': 12.0107, 'O': 15.999, 'N': 14.0067}
        tokens = re.findall(r'([A-Z][a-z]*)(\d*)', species)
        molar_mass = sum(atomic_masses[el] * (int(count) if count else 1) for el, count in tokens)
        return (molar_mass / 1000) / 6.02214076e23

    def calculate_k_sb(self, T_K):
        return self.B * np.exp(-self.E_sb / (8.617e-5 * T_K))

    def calculate_n0(self, temp_C):
        return self.n0

    def calculate_n(self, temp_C, t, y=None):
        T_K = temp_C + 273.15
        n0 = self.n0

        if y is not None:
            carbon_consumed = (y[0] + y[3] + y[4]) * self.reactor_volume
            molecules_consumed = carbon_consumed / 2
            return max(0, n0 - molecules_consumed)
        else:
            g_t = 1 if self.gas_NP_time_considered else 1 - np.exp(-0.02 * t)
            n = g_t * n0 - 2 * (self.np1 + self.np2)
            return max(n, 0)

    def ode_system(self, t, y, temp_C):
        T_K = temp_C + 273.15
        n0 = self.n0
        carbon_consumed = y[0] + y[3] + y[4]
        molecules_consumed = carbon_consumed / 2
        n = max(0, n0 - molecules_consumed / self.reactor_volume)
        g_t = 1 if self.gas_NP_time_considered else 1 - np.exp(-0.02 * t)
        n_p = self.np1 + self.np2

        F_b1 = 0.25 * self.S_0 * n * (self.kb * T_K / (2 * np.pi * self.species_weight)) ** 0.5
        F_c1 = F_b1 * np.exp(-self.E_a1 / (8.617e-5 * T_K))

        F_b2 = 0.25 * self.S_0 * n_p * (self.kb * T_K / (2 * np.pi * self.average_species_weight_product)) ** 0.5
        F_c2 = F_b2 * np.exp(-self.E_a1 / (8.617e-5 * T_K))

        k_sb = self.calculate_k_sb(T_K)
        k_t = (4e-5 / self.dp**2) * np.exp(-self.E_b / (8.617e-5 * T_K))
        k_r = self.current_H2_flux * self.H2_STICKING_PROBABILITY

        N_c, N_L1, N_L2, N_b, N_t = y
        N_L = N_L1 + N_L2

        dN_c_dt = F_c1 * (1 - N_L / (self.alpha * self.S_0 * self.n_m)) - (k_sb + self.k_c1) * N_c
        dN_L1_dt = (F_c2 * (1 - N_L / (self.alpha * self.S_0 * self.n_m)) + self.k_c1 * N_c - self.k_d1 * N_L2) if self.carb_strc_surface else 0
        dN_L2_dt = (k_r * (1 - N_L / (self.alpha * self.S_0 * self.n_m)) - self.k_d2 * N_L2) if self.carb_deactiv else 0
        dN_b_dt = k_sb * N_c - k_t * N_b + self.k_d1 * N_L1
        dN_t_dt = k_t * N_b

        return [dN_c_dt, dN_L1_dt, dN_L2_dt, dN_b_dt, dN_t_dt]

    def calculate_length(self, N_t):
        atoms_per_micron = ((self.dp * 1e9) / 10) * 7e6
        return N_t / atoms_per_micron

    def run_surface_kinetics_simulation(self, temperatures, time_span):
        results = {}
        for temp_C in temperatures:
            try:
                sol = solve_ivp(lambda t, y: self.ode_system(t, y, temp_C),
                                time_span, self.initial_conditions, method='BDF',
                                rtol=1e-6, atol=1e-10, dense_output=True,
                                max_step=(time_span[1] - time_span[0]) / 100)
                if sol.success:
                    results[temp_C] = sol
                else:
                    print(f"Warning: {temp_C}°C did not converge: {sol.message}")
            except Exception as e:
                print(f"Error at {temp_C}°C: {e}")
        if not results:
            raise RuntimeError("No simulations completed.")
        return results

    def get_final_values(self, results):
        temp_C = list(results.keys())[0]
        sol = results[temp_C]
        final_state = sol.y[:, -1]
        final_n = self.calculate_n(temp_C, sol.t[-1], final_state)
        
        return np.array([final_n, *final_state])
print("True")

