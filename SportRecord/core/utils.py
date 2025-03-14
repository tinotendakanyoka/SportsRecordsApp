import pandas as pd
from .models import Participant, CompetitiveHouse, AgeGroup
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from django.http import HttpResponse
from django.utils import timezone
from .models import EventParticipation, AthleticEvent, Record, Participant, CompetitiveHouse

def bulk_upd(event):
    all_event_participants = list(EventParticipation.objects.filter(event=event).order_by('-best_attempt'))
        
        # Assign rankings
    for index, event_participant in enumerate(all_event_participants):
        event_participant.athlete_position = index + 1

        # **Bulk update to save all rankings in a single query**
    EventParticipation.objects.bulk_update(all_event_participants, ['athlete_position'])

        # **Update points for top 8 positions**
    points_map = {1: 9, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
    participants_to_update = []

    for event_participant in all_event_participants:
        position = event_participant.athlete_position
        points = points_map.get(position, 0)  # Default to 0 if out of top 8

        # Update individual and house points
        event_participant.participant.individual_points += points
        event_participant.participant.competitive_house.points += points

        participants_to_update.append(event_participant.participant)
        participants_to_update.append(event_participant.participant.competitive_house)

        # **Check for new event record**
        if position == 1 and event_participant.best_attempt > event_participant.event.current_record:
            record, created = Record.objects.get_or_create(
                event=event_participant.event,
                participant=event_participant.participant,
                record=event_participant.best_attempt,
                record_date=timezone.now()
            )
            event_participant.event.current_record_holder_name = (
                f'{event_participant.participant.first_name} {event_participant.participant.last_name}'
            )
            event_participant.event.current_record = event_participant.best_attempt
            event_participant.event.record_date = timezone.now()
            event_participant.event.save()

        # **Bulk update participant and house points in a single query**
    Participant.objects.bulk_update(
        [p for p in participants_to_update if isinstance(p, Participant)], 
        ['individual_points']
    )
    CompetitiveHouse.objects.bulk_update(
        [p for p in participants_to_update if isinstance(p, CompetitiveHouse)], 
        ['points']
    )

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

def generate_report(event):
    response = HttpResponse(content_type='applicaiton/pdf')
    response['Content-Disposition'] = f'attachment; filename="{event}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(A5))

    elements = []

    styles = getSampleStyleSheet()

    doc.leftMargin = 50
    doc.topMargin = 3

    logo = 'data/logo.png'
    img = Image(logo, width=30*mm, height=30*mm)
    title_style = styles['Heading1']
    title_style.alignment = 1
    info_row = Paragraph("Hellenic Academy Official Results Sheet", title_style)
            
    elements.append(img)
    elements.append(Spacer(1, 2))
    elements.append(info_row)
    elements.append(Spacer(1, 2))

    event_info = Paragraph(f'Event: {event}', styles['Heading3'])
    elements.append(event_info)
    elements.append(Spacer(1, 2))
    results_table_skel = [
        ['Position', 'Participant Name', 'House', 'Distance/Laptime'],

    ]
    
    participations = EventParticipation.objects.filter(event=event).order_by('athlete_position')

    for participation in participations:
        results_table_skel.append([f'{participation.athlete_position}', f'{participation.participant.first_name} {participation.participant.last_name}', f'{participation.participant.competitive_house.name}', f'{participation.best_attempt} {"s" if event.is_track_event else "m"}'])

    table_styling = TableStyle([
        ('BACKGROUND', (0,0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0,0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 11.5),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('GRID', (0,0), (-1,-1), 1, colors.black),

    ])

    results_table = Table(results_table_skel)
    results_table.setStyle(table_styling)
    elements.append(results_table)

    doc.build(elements)

    return response