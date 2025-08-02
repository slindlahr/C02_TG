import pandas as pd

class AnalyseC02Data:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.tables = {}  # Speicherung der dfs

        # Data Cleaning
        self.df['andere'] = self.df['andere'].fillna(0)
        #Renaming
        self.df = self.df.rename(columns={"total": "c02_emissions"})

        # Analysen
        self._prepare_kpis_pro_jahr()
        self._prepare_lookerstudio_table()
        self._prepare_energiemix()
        self._prepare_gemeindeentwicklung()
        self._prepare_entwicklung_einwohner_vs_C02()

    def _prepare_kpis_pro_jahr(self):
        df = self.df.groupby('jahr').agg({
            'c02_emissions': 'sum',
            'einwohner': 'sum'
        }).reset_index()

        df['energy_per_inhabitant'] = df['c02_emissions'] / df['einwohner']
        df['growth_total_energy_pct'] = df['c02_emissions'].pct_change() * 100
        df['growth_energy_per_inhabitant_pct'] = df['energy_per_inhabitant'].pct_change() * 100

        # Cast datatypes
        df["jahr"] = pd.to_datetime(df["jahr"].astype(str) + "-01-01")

        self.tables['kpi_pro_jahr'] = df

    def _prepare_lookerstudio_table(self):
        df = self.df.copy()

        # Optional: Datum im Format "jahr" als echtes Datum (z. B. 01.01.2023)
        df["jahr"] = pd.to_datetime(df["jahr"].astype(str) + "-01-01")

        # Kein groupby — keine Aggregation!
        df = df[["jahr", "gemeinde_name", "einwohner", "c02_emissions", "energiebezugsflaeche", "loaded_at"]].copy()

        self.tables["lookerstudio_base"] = df


    def _prepare_energiemix(self):
        df = self.df.copy()
        # Summieren der Energiearten pro jahr
        df_grouped = df.groupby("jahr")[["erdoelbrennstoffe", "erdgas", "andere"]].sum().reset_index()

        # Umwandeln in Long-Format
        df = df_grouped.melt(
            id_vars="jahr",
            value_vars=["erdoelbrennstoffe", "erdgas", "andere"],
            var_name="energietraeger",
            value_name="menge"
        )

        df["anteil_prozent"] = df.groupby("jahr")["menge"].transform(lambda x: round(x / x.sum() * 100, 2))

        # Cast datatypes
        df["jahr"] = pd.to_datetime(df["jahr"].astype(str) + "-01-01")

        self.tables['energiemix_pro_jahr'] = df


    def _prepare_gemeindeentwicklung(self):
        df = self.df.copy()
        df['energy_per_inhabitant'] = df['c02_emissions'] / df['einwohner']

        df = df[['bfs_nr_gemeinde', 'gemeinde_name', 'jahr', 'c02_emissions', 'energy_per_inhabitant']]

        # Cast datatypes
        df["jahr"] = pd.to_datetime(df["jahr"].astype(str) + "-01-01")

        self.tables['gemeindeentwicklung'] = df


    def _prepare_entwicklung_einwohner_vs_C02(self):
        df = self.df.copy()
        df = df[["jahr", "gemeinde_name", "einwohner", "c02_emissions", "energiebezugsflaeche"]].copy()

        df["C02_pro_qm"] = df["c02_emissions"] / df["energiebezugsflaeche"] * 1000
        df["C02_pro_einwohner"] = df["c02_emissions"] / df["einwohner"] * 1000

        # Cast datatypes
        df["jahr"] = pd.to_datetime(df["jahr"].astype(str) + "-01-01")

        self.tables["einwohner_vs_c02"] = df

    def get_table(self, name: str) -> pd.DataFrame:
        return self.tables.get(name)

    def get_all_tables(self) -> dict:
        return self.tables