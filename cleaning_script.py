import pandas as pd

def filter_top_5_countries(file_path):
    """
    Filters the top 5 countries by CO2 emissions from the given CSV file and saves the result to a new CSV file.

    Parameters:
    - file_path: str, path to the input CSV file.
    """
    df = pd.read_csv(file_path)
    
    df_filtered = df[(df['Year'] >= 2000) & (df['Year'] <= 2019)]  # 2020 data is not complete
    
    country_emissions = df_filtered.groupby('Entity')['Value_co2_emissions_kt_by_country'].sum()
    top_5_countries = country_emissions.nlargest(5).index
    
    df_top_5 = df_filtered[df_filtered['Entity'].isin(top_5_countries)]
    
    df_top_5 = df_top_5.drop(columns=['Financial flows to developing countries (US $)', 'Renewable-electricity-generating-capacity-per-capita'])
    
#    df_top_5.reset_index(inplace=True)
    
    df_top_5.to_csv('data/top_5_countries.csv', index=False)
    
    print(f'Top 5 countries data saved to data/top_5_countries.csv')

# Example usage:
# filter_top_5_countries('data/global-data-on-sustainable-energy.csv')

filter_top_5_countries('data/global-data-on-sustainable-energy.csv')