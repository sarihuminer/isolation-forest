# נסיר פיצרים שקשורים לשייכות העובד למחלקה וכן מאפיינים סטטיים, היות ובמודל הנוכחי אנחנו מעוניינים ללמוד חריגות בהתנהגות העובד כלפי עצמו לאורך זמן
exclude_keywords = [
    'employee_department',
    'employee_position',
    'employee_classification_freq',
    'employee_campus_cat',
    'has_criminal_record',
    'has_medical_history',
    'has_foreign_citizenship',
    'is_contractor',
    'is_employee_in_origin_country',
    'employee_seniority',
    'is_new_employee',
    'is_veteran_employee'
    ]

# הגדרת שמות הפיצרים הרלוונטיים למודל
include_also = [
    'print_vs_department_avg',
    'print_per_minute',
    'prints_percentile',
    'burns_percentile',
    'total_printed_pages_zscore_global',
    'num_print_commands_zscore_global',
    'total_burn_volume_mb_zscore_global'
]

# בניית רשימת הפיצ'רים - כולל גם פרמטרים מהמחסנית השניה
feature_cols = [
    col for col in df.columns
    if (
        (col.endswith('_zscore') or 
         col.endswith('_percentile') or 
         col.endswith('_per_minute') or 
         col.endswith('_vs_department_avg') or
         col.endswith('_quartile') or
         col.endswith('_freq_quartile')) and
        not any(key in col for key in exclude_keywords)
    ) or (col in include_also and col in df.columns)
]

print(len(feature_cols))