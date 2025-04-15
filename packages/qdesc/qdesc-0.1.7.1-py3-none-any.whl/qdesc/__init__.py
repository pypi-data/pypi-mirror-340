

def desc(df):
    import pandas as pd
    import numpy as np
    from scipy.stats import anderson
    x = np.round(df.describe().T,2)
    x = x.iloc[:, [0,1,2,5,3,7]]
    x.rename(columns={'50%': 'median'}, inplace=True)
    mad_values = {}
    # computes the manual mad which is more robust to outliers and non-normal distributions
    for column in df.select_dtypes(include=[np.number]):
        median = np.median(df[column])
        abs_deviation = np.abs(df[column] - median)
        mad = np.median(abs_deviation)
        mad_values[column] = mad
    mad_df = pd.DataFrame(list(mad_values.items()), columns=['Variable', 'MAD'])
    mad_df.set_index('Variable', inplace=True)
    results = {}
    # Loop through each column to test only continuous variables (numeric columns)
    for column in df.select_dtypes(include=[np.number]):  # Only continuous variables
        result = anderson(df[column])
        statistic = result.statistic
        critical_values = result.critical_values
        # Only select the 5% and 1% significance levels
        selected_critical_values = {
            '5% crit_value': critical_values[2],  # 5% critical value
            '1% crit_value': critical_values[4]   # 1% critical value
        }
        # Store the results in a dictionary
        results[column] = {
            'AD_stat': statistic,
            **selected_critical_values  # Add critical values for 5% and 1% levels
        }
    # Convert the results dictionary into a DataFrame
    anderson_df = pd.DataFrame.from_dict(results, orient='index')
    
    xl = x.iloc[:, :4]
    xr = x.iloc[:, 4:]
    x_df = np.round(pd.concat([xl, mad_df, xr, anderson_df], axis=1),2)
    return x_df

def freqdist(df, column_name):
    import pandas as pd
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    
    if df[column_name].dtype not in ['object', 'category']:
        raise ValueError(f"Column '{column_name}' is not a categorical column.")
    
    freq_dist = df[column_name].value_counts().reset_index()
    freq_dist.columns = [column_name, 'Count']
    freq_dist['Percentage'] = (freq_dist['Count'] / len(df)) * 100
    return freq_dist


def freqdist_a(df, ascending=False):
    results = []  
    for column in df.select_dtypes(include=['object', 'category']).columns:
        frequency_table = df[column].value_counts()
        percentage_table = df[column].value_counts(normalize=True) * 100

        distribution = pd.DataFrame({
            'Column': column,
            'Value': frequency_table.index,
            'Count': frequency_table.values,
            'Percentage': percentage_table.values
        })
        distribution = distribution.sort_values(by='Percentage', ascending=ascending)
        results.append(distribution)
    final_df = pd.concat(results, ignore_index=True)
    return final_df

def clean_sheet_name(name):
    import re
    # Remove invalid characters
    name = re.sub(r'[:\\/?*\[\]]', '', name)
    # Limit to 31 characters
    name = name.strip()[:31]
    return name

def freqdist_to_excel(df, output_path, sort_by='Percentage', ascending=False, top_n=None):
    import pandas as pd
    import numpy as np
    used_names = set()
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        for column in df.select_dtypes(include=['object', 'category']).columns:
            frequency_table = df[column].value_counts()
            percentage_table = df[column].value_counts(normalize=True) * 100

            distribution = pd.DataFrame({
                'Value': frequency_table.index,
                'Count': frequency_table.values,
                'Percentage': percentage_table.values
            })
            distribution = distribution.sort_values(by=sort_by, ascending=ascending)
            if top_n is not None:
                distribution = distribution.head(top_n)
            # Generate safe sheet name
            base_name = clean_sheet_name(column)
            sheet_name = base_name
            count = 1
            while sheet_name.lower() in used_names:
                sheet_name = f"{base_name[:28]}_{count}"  # stay within 31 char limit
                count += 1
            used_names.add(sheet_name.lower())
            distribution.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"Frequency distributions written to {output_path}")
