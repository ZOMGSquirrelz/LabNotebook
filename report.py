from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import config
import database
import functions


# Generates a PDF report for the specified project_id
def generate_report(project_id):
    logo_path = "images/NotebookLogo.jpg"
    final_results = functions.generate_report_results(project_id)
    project_create_date = database.get_project_details(project_id)[2]
    filename = f'Reports/{project_create_date}-ProjectID-{project_id}.pdf'

    # Create a canvas
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Add logo to the top-left corner
    c.drawImage(logo_path, 20, 675, width=60, height=100)

    # Add title
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 50, "Final Results Report")

    # Add project number and creation date
    c.setFont("Helvetica", 16)
    c.drawCentredString(width / 2, height - 70, f"Project Number: {project_id}")
    c.drawCentredString(width / 2, height - 90, f"Creation Date: {project_create_date}")

    # Move down to start adding sample/test results
    y_position = height - 150

    sql_test_list = database.get_test_list()

    # Iterate through final results and add to the PDF
    for sample_num, sample_value in final_results.items():
        # Sample Header
        c.setFont("Helvetica-Bold", 14)
        c.drawString(20, y_position, f"Sample Number: {sample_num}")
        y_position -= 20  # Move down

        # Add test results for this sample
        for test_id, result in sample_value:
            test_name = next((key for key, value in sql_test_list.items() if value == test_id), "Unknown Test")
            unit = config.result_units.get(test_name, "")
            c.setFont("Helvetica", 12)
            c.drawString(40, y_position, f"{test_name}: {result} {unit}")
            y_position -= 15  # Move down

        y_position -= 10  # Add space before the next sample

    # Save the PDF
    c.save()
