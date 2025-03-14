import pandas as pd
from .models import Participant, CompetitiveHouse, AgeGroup

def get_student_info_from_csv(file_path):
    return pd.read_csv(file_path)

def initialize_data():

    age_groups = [
        {
            'title': 'Under 14',
            'earliest_dob': '2012-01-01',
        },
        {
            'title': 'Under 15',
            'earliest_dob': '2011-01-01',

        },
        {
            'title': 'Under 16',
            'earliest_dob': '2010-01-01',
        },
        {
            'title': 'Under 17',
            'earliest_dob': '2009-01-01',
        },
        {
            'title': 'Under 18',
            'earliest_dob': '2008-01-01',
        },
        {
            'title': 'OPEN',
            'earliest_dob': '2007-01-01',
        },
    ]




    df = pd.DataFrame(get_student_info_from_csv('data/students.csv'))

    for index, row in df.iterrows():
        # determine empty 
        first_name = row['First name']
        last_name = row['Surname']
        date_of_birth = str(row['Birth date'])
        gender = row['Gender']

        house = row['Competitive hosue']

        house, created = CompetitiveHouse.objects.get_or_create(name=house)

        participant, created = Participant.objects.get_or_create(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            competitive_house=house
        )

    genders = ['M', 'F']

    for gender in genders:
        for age_group in age_groups:
            title = age_group['title']
            earliest_dob = age_group['earliest_dob']

            AgeGroup.objects.get_or_create(
                title=title,
                earliest_dob=earliest_dob,
                gender=gender)

    print('Data has been successfully imported')