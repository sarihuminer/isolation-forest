def add_features(df):
    # Z-scores גלובליים
    for col in ['total_printed_pages', 'num_print_commands', 'total_burn_volume_mb']:
        df[f'{col}_zscore_global'] = (df[col] - df[col].mean()) / df[col].std()
    
    # אחוזונים
    df['prints_percentile'] = df['total_printed_pages'].rank(pct=True)
    df['burns_percentile'] = df['total_burn_volume_mb'].rank(pct=True)
    
    # יחס למחלקה
    df['department_avg_print'] = df.groupby('employee_department_freq')['total_printed_pages'].transform('mean')
    df['print_vs_department_avg'] = df['total_printed_pages'] / df['department_avg_print']
    
    # יחס לנוכחות
    df['print_per_minute'] = df['total_printed_pages'] / df['total_presence_minutes']
    
    return df