from app import create_app, db
from app.models import Grant, Application, Feedback
from datetime import datetime, timedelta

app = create_app()

try:
    with app.app_context():
        # Create grants
        grant1 = Grant(
            title='Community Green Fund',
            description='Funding for environmental projects',
            eligibility='Non-profits, community groups',
            deadline=datetime.now() + timedelta(days=30),
            category='Environment'
        )
        grant2 = Grant(
            title='Cultural Heritage Grant',
            description='Support for cultural events',
            eligibility='Cultural organizations',
            deadline=datetime.now() + timedelta(days=60),
            category='Culture'
        )
        db.session.add_all([grant1, grant2])
        db.session.commit()

        # Create applications
        app1 = Application(
            grant_id=grant1.id,
            applicant_name='Oscar Maingi',
            applicant_email='oscar@example.com',
            proposal='Green park initiative',
            status='pending'
        )
        app2 = Application(
            grant_id=grant2.id,
            applicant_name='Anne Yula',
            applicant_email='anne@example.com',
            proposal='Art festival',
            status='approved'
        )
        db.session.add_all([app1, app2])
        db.session.commit()

        # Create feedback
        feedback1 = Feedback(
            grant_id=grant1.id,
            commenter_name='Oscar Maingi',
            commenter_email='oscar@example.com',
            comment='Great initiative!',
            rating=5
        )
        feedback2 = Feedback(
            grant_id=grant1.id,
            commenter_name='Anne Yula',
            commenter_email='anne@example.com',
            comment='Needs clearer guidelines',
            rating=3
        )
        db.session.add_all([feedback1, feedback2])
        db.session.commit()

        print('Database seeded successfully!')
except Exception as e:
    print(f'Error seeding database: {str(e)}')