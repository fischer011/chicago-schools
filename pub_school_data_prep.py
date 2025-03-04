"""vh.pub_school_data_prep

Loads Chicago Public Schools dataset and creates pandas DataFrame.  
Data preparation including cleaning, handling missing data, data
formatting, creation of new data columns. Data filtering for 
calculations. Creates a file and saves output results to file in same 
directory as code and dataset.
"""

import sys
import os
import pandas as pd

def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    output_dir = base_dir+'\\data_prep_pd.txt'
    
    # Read in csv file of Chicago Public Schools data.
    cps = pd.read_csv('cps.csv'
                      , usecols= ['School_ID'
                                  , 'Short_Name'
                                  , 'Is_High_School'
                                  , 'Zip'
                                  , 'Student_Count_Total'
                                  , 'College_Enrollment_Rate_School'
                                  , 'Grades_Offered_All'
                                  , 'School_Hours'
                                  ]
                      )

    # Creating DataFrame object with needed original columns. 
    cps_df = pd.DataFrame(cps)

    # Need to split list inside each 'cell' into separate 
    # objects to pull by index.
    grades_split = cps_df.Grades_Offered_All.str.split(pat=",")

    # Need highest and lowest grade offered.  Making into lists 
    # which will populate respective columns being created.
    lowest_grade = []
    highest_grade = []
    for row in grades_split:
        l_grade = row[0]
        h_grade = row[-1]
        lowest_grade.append(l_grade)
        highest_grade.append(h_grade)
    cps_df['Lowest_Grade'] = pd.DataFrame(lowest_grade)
    cps_df['Highest_Grade'] = pd.DataFrame(highest_grade)

    # Using school hours to create school_start_hour column in cps_df. 
    # Some entries have leading zeros and letter char.  If statement is 
    # to account for lack of uniformity.
    start_hour = []
    hours = pd.Series(cps_df.School_Hours, dtype=str)
    for row in hours:
            for x in row:
                if x == '7':
                    start_hour.append(x)
                    break
                elif x == '8':
                    start_hour.append(x)
                    break
                elif x == '9':
                    start_hour.append(x)
                    break

    cps_df['School_Start_Hour'] = pd.DataFrame(start_hour) 

    # Replacing missing values with mean for respective 
    # columns before calculations.
    cps_df['College_Enrollment_Rate_School'] = (
        cps_df['College_Enrollment_Rate_School'].fillna(
            cps_df['College_Enrollment_Rate_School'].mean()))
    
    # Task specifies 'in high school' and 'non high school' 
    # for some calculations.
    col_rate_hs = cps_df.query('Is_High_School == True')
    col_rate_hs_mu = col_rate_hs['College_Enrollment_Rate_School'].mean()
    col_rate_hs_sd = col_rate_hs['College_Enrollment_Rate_School'].std()
    
    studcnt_nonhs = cps_df.query('Is_High_School == False')
    studcnt_nonhs_mu = studcnt_nonhs['Student_Count_Total'].mean()
    studcnt_sd = studcnt_nonhs['Student_Count_Total'].std()

    # Getting start hour distribution.
    start_hr_dist = cps_df['School_Start_Hour'].value_counts()    

    # Need number of schools outside the loop. Creating list of 
    # zip codes inside loop to check cps_df['Zip'] against.
    # Filtering and creating outside_loop_df.
    loop_neighborhood = ['60601', '60602', '60603', '60604'
                         , '60605', '60606', '60607', '60616']
    
    cps_df['Zip'] = (cps_df['Zip'].astype(str))
    outside_loop_df = cps_df[~(cps_df['Zip'].isin(loop_neighborhood))] 
    
    # Creating df with desired columns for output.
    df_to_print = pd.DataFrame(cps_df
                               , columns= ['School_ID'
                                           , 'Short_Name'
                                           , 'Is_High_School'
                                           , 'Zip'
                                           , 'Student_Count_Total'
                                           , 'College_Enrollment_Rate_School'
                                           , 'Lowest_Grade'
                                           , 'Highest_Grade'
                                           , 'School_Start_Hour'
                                           ]
                               )
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 1000)
    with open(output_dir, 'w') as f:
        original_stdout = sys.stdout
        sys.stdout = f
        print(df_to_print.head(10))
        st_col_rt = '\nCollege Enrollment Rate for High Schools = '
        template_col_rt = '{0:.2f} (sd= {1:.2f}) \n'
        print(st_col_rt + template_col_rt.format(col_rate_hs_mu, col_rate_hs_sd))
        st_stud_ct = 'Total Student Count for non-High Schools = '
        template_stud_ct = '{0:.2f} (sd= {1:.2f}) \n'
        print(st_stud_ct + template_stud_ct.format(studcnt_nonhs_mu, studcnt_sd))
        st_dist = 'Distribution of Starting Hours:'
        template_st_dist = '  {0}am: {1}'
        print(st_dist)
        print(template_st_dist.format('8', start_hr_dist[0]))
        print(template_st_dist.format('7', start_hr_dist[1]))
        print(template_st_dist.format('9', start_hr_dist[2])) 
        print('\nNumber of schools outside Loop: ' + str(len(outside_loop_df)))
        sys.stdout = original_stdout
        
if __name__ == "__main__":
    main() 



