from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import (
    letter
)

from reportlab.platypus.flowables import HRFlowable

from datetime import datetime


# =========================================================
# GENERATE PROFESSIONAL AGRICULTURE REPORT
# =========================================================
def generate_agriculture_report(

    question,

    response,

    prediction,

    forecast_weather
):

    # =====================================================
    # FILE PATH
    # =====================================================
    file_path = (
        "KrishiMitra_Report.pdf"
    )

    # =====================================================
    # PDF DOCUMENT
    # =====================================================
    doc = SimpleDocTemplate(

        file_path,

        pagesize=letter,

        rightMargin=40,

        leftMargin=40,

        topMargin=40,

        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    story = []

    # =====================================================
    # TITLE
    # =====================================================
    title = Paragraph(

        """
        <font size=20>
        <b>KrishiMitra AI</b>
        </font>
        <br/>
        <font size=12>
        Intelligent Agricultural Advisory Report
        </font>
        """,

        styles["Title"]
    )

    story.append(title)

    story.append(
        Spacer(1, 15)
    )

    # =====================================================
    # TIMESTAMP
    # =====================================================
    timestamp = datetime.now().strftime(
        "%d-%m-%Y %H:%M"
    )

    report_time = Paragraph(

        f"""
        <b>Generated On:</b>
        {timestamp}
        """,

        styles["BodyText"]
    )

    story.append(report_time)

    story.append(
        Spacer(1, 10)
    )

    story.append(
        HRFlowable(
            width="100%"
        )
    )

    story.append(
        Spacer(1, 15)
    )

    # =====================================================
    # USER QUESTION
    # =====================================================
    question_section = Paragraph(

        f"""
        <font size=14>
        <b>Farmer Query</b>
        </font>
        <br/><br/>
        {question}
        """,

        styles["BodyText"]
    )

    story.append(question_section)

    story.append(
        Spacer(1, 20)
    )

    # =====================================================
    # WEATHER RISKS
    # =====================================================
    heat_risk = forecast_weather.get(
        "heat_risk",
        "Unknown"
    )

    rainfall_risk = forecast_weather.get(
        "rainfall_risk",
        "Unknown"
    )

    humidity_risk = forecast_weather.get(
        "humidity_risk",
        "Unknown"
    )

    # =====================================================
    # CROP HEALTH SCORE
    # =====================================================
    crop_health_score = 85

    if heat_risk == "High":

        crop_health_score -= 20

    if rainfall_risk == "High":

        crop_health_score -= 15

    if humidity_risk == "High":

        crop_health_score -= 10

    # =====================================================
    # SUMMARY TABLE
    # =====================================================
    summary_data = [

        [
            "Predicted Yield",
            str(prediction)
        ],

        [
            "Crop Health Score",
            f"{crop_health_score}%"
        ],

        [
            "Heat Risk",
            heat_risk
        ],

        [
            "Rainfall Risk",
            rainfall_risk
        ],

        [
            "Humidity Risk",
            humidity_risk
        ]
    ]

    table = Table(

        summary_data,

        colWidths=[220, 220]
    )

    table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgreen
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, -1),
                colors.black
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.grey
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "Helvetica-Bold"
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                10
            ),

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.beige
            )
        ])
    )

    summary_title = Paragraph(

        """
        <font size=14>
        <b>Agricultural Intelligence Summary</b>
        </font>
        """,

        styles["BodyText"]
    )

    story.append(summary_title)

    story.append(
        Spacer(1, 10)
    )

    story.append(table)

    story.append(
        Spacer(1, 25)
    )

    # =====================================================
    # AI ADVISORY
    # =====================================================
    advisory_title = Paragraph(

        """
        <font size=14>
        <b>AI Agricultural Advisory</b>
        </font>
        """,

        styles["BodyText"]
    )

    story.append(advisory_title)

    story.append(
        Spacer(1, 10)
    )

    short_response = response[:2500]

    advisory = Paragraph(

        short_response.replace(
            "\n",
            "<br/>"
        ),

        styles["BodyText"]
    )

    story.append(advisory)

    story.append(
        Spacer(1, 25)
    )

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================
    recommendation_title = Paragraph(

        """
        <font size=14>
        <b>Key Recommendations</b>
        </font>
        """,

        styles["BodyText"]
    )

    story.append(recommendation_title)

    story.append(
        Spacer(1, 10)
    )

    recommendations = []

    if rainfall_risk == "High":

        recommendations.append(
            "Ensure proper field drainage management."
        )

    if heat_risk == "High":

        recommendations.append(
            "Increase irrigation during extreme heat."
        )

    if humidity_risk == "High":

        recommendations.append(
            "Monitor fungal disease outbreaks carefully."
        )

    if not recommendations:

        recommendations.append(
            "Current agricultural conditions look stable."
        )

    for rec in recommendations:

        rec_para = Paragraph(

            f"• {rec}",

            styles["BodyText"]
        )

        story.append(rec_para)

        story.append(
            Spacer(1, 6)
        )

    story.append(
        Spacer(1, 25)
    )

    # =====================================================
    # FOOTER
    # =====================================================
    footer = Paragraph(

        """
        <font size=10>
        Generated by KrishiMitra AI
        <br/>
        Intelligent Agricultural Decision Support System
        </font>
        """,

        styles["Italic"]
    )

    story.append(footer)

    # =====================================================
    # BUILD PDF
    # =====================================================
    doc.build(story)

    return file_path