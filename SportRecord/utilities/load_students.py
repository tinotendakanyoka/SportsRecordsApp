import csv
from datetime import datetime
from core.models import GENDER_CHOICES, Student, House

def convert_date(date_str):
  """Converts date string in DD/MM/YY format to a datetime object."""
  return datetime.strptime(date_str, "%d/%m/%y")

def convert_gender(gender):
  """Converts single letter gender (M/F) to model's choice value (MALE/FEMALE)."""
  return GENDER_CHOICES[0][0] if gender.upper() == "M" else GENDER_CHOICES[1][0]


def create_students_from_csv(csv_filename):
  """Reads a CSV file and creates Student objects for each entry."""
  with open(csv_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      # Extract data from each row (assuming header matches your CSV)
      surname = row['Surname']
      first_name = row['First name']
      birth_date = convert_date(row['Birth date'])
      gender = convert_gender(row['Gender'])
      house_name = row['Competitive house']  # Assuming house is identified by name

      # Find the house object (replace with your logic to find the house)
      house = House.objects.get(name=house_name)

      # Create and save the Student object
      student = Student(
          full_name=f"{first_name} {surname}",
          date_of_birth=birth_date,
          gender=gender,
          points=0,  # Assuming default points is 0
          house=house,
      )
      student.save()

  print(f"Successfully created student objects from {csv_filename}.")


