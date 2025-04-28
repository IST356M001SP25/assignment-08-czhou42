import pandas as pd
import streamlit as st 

def top_locations(violations_df: pd.DataFrame, threshold=1000):
    top_locs = violations_df.groupby('location')['violation_amount'].sum()
    top_locs = top_locs[top_locs >= threshold].reset_index()
    top_locs = top_locs.rename(columns={'violation_amount': 'amount'})
    return top_locs

def top_locations_mappable(violations_df: pd.DataFrame, threshold=1000):
    top_locs = top_locations(violations_df, threshold)
    top_locs_latlon = violations_df[['location', 'lat', 'lon']].drop_duplicates()
    top_locs = pd.merge(top_locs, top_locs_latlon, on='location', how='left')
    return top_locs[['location', 'lat', 'lon', 'amount']]

def tickets_in_top_locations(violations_df: pd.DataFrame, threshold=1000):
    top_locs = top_locations(violations_df, threshold)
    tickets_top = violations_df[violations_df['location'].isin(top_locs['location'])]
    return tickets_top

if __name__ == '__main__':
    violations_df = pd.read_csv('./cache/final_cuse_parking_violations.csv')

    top_locs_df = top_locations(violations_df)
    top_locs_df.to_csv('./cache/top_locations.csv', index=False)

    top_locs_map_df = top_locations_mappable(violations_df)
    top_locs_map_df.to_csv('./cache/top_locations_mappable.csv', index=False)

    tickets_top_df = tickets_in_top_locations(violations_df)
    tickets_top_df.to_csv('./cache/tickets_in_top_locations.csv', index=False)