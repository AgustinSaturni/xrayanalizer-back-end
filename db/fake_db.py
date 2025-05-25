from models.project import Project
from models.report import Report, Angle

# Simulación de una base de datos en memoria
projects = [
    Project(
        id="1",
        name="Paciente A - Evaluación Inicial",
        patientId="PAC-001",
        date="15/04/2025",
        description="Evaluación inicial del paciente A",
        imageCount=0,
        reportCount=0
    ),
    Project(
        id="2",
        name="Paciente B - Seguimiento",
        patientId="PAC-002",
        date="10/04/2025",
        description="Seguimiento del paciente B",
        imageCount=0,
        reportCount=0
    ),
    Project(
        id="3",
        name="Paciente C - Post-operatorio",
        patientId="PAC-003",
        date="05/04/2025",
        description="Evaluación post-operatoria del paciente C",
        imageCount=0,
        reportCount=0
    ),
]

# Simulación de base de datos de reportes
reports = [
    Report(
        id=1,
        name= "nombre prueba 1",
        projectName="Paciente A - Evaluación Inicial",
        patientId="PAC-001",
        date="15/04/2025",
        imageCount=3,
        projectId="1",
        angles=[
            Angle(name="Ángulo de Hallux Valgus", value="23°"),
            Angle(name="Ángulo Intermetatarsiano", value="12°"),
            Angle(name="Ángulo PASA", value="8°"),
            Angle(name="Ángulo DASA", value="6°"),
        ],
        notes="El paciente presenta un hallux valgus moderado en el pie derecho.",
    ),
    Report(
        id=2,
        name="nombre prueba 2",
        projectName="Paciente A - Evaluación Inicial",
        patientId="PAC-001",
        date="15/04/2025",
        imageCount=1,
        projectId="1",
        angles=[
            Angle(name="Ángulo de Hallux Valgus", value="18°"),
            Angle(name="Ángulo Intermetatarsiano", value="10°"),
            Angle(name="Ángulo PASA", value="7°"),
            Angle(name="Ángulo DASA", value="5°"),
        ],
        notes="Seguimiento del paciente A, se observa mejoría.",
    ),
    Report(
        id=3,
        name= "nombre prueba 3",
        projectName="Paciente B - Seguimiento",
        patientId="PAC-002",
        date="10/04/2025",
        imageCount=2,
        projectId="2",
        angles=[
            Angle(name="Ángulo de Hallux Valgus", value="15°"),
            Angle(name="Ángulo Intermetatarsiano", value="9°"),
            Angle(name="Ángulo PASA", value="6°"),
            Angle(name="Ángulo DASA", value="4°"),
        ],
        notes="Evaluación de seguimiento del paciente B.",
    ),
    Report(
        id=4,
        name= "nombre prueba 4",
        projectName="Paciente C - Post-operatorio",
        patientId="PAC-003",
        date="05/04/2025",
        imageCount=4,
        projectId="3",
        angles=[
            Angle(name="Ángulo de Hallux Valgus", value="8°"),
            Angle(name="Ángulo Intermetatarsiano", value="7°"),
            Angle(name="Ángulo PASA", value="5°"),
            Angle(name="Ángulo DASA", value="3°"),
        ],
        notes="Evaluación post-operatoria, resultados satisfactorios.",
    ),
    Report(
        id=5,
        name= "nombre prueba 5",
        projectName="Paciente D - Evaluación Pre-quirúrgica",
        patientId="PAC-004",
        date="01/04/2025",
        imageCount=2,
        projectId="4",
        angles=[
            Angle(name="Ángulo de Hallux Valgus", value="28°"),
            Angle(name="Ángulo Intermetatarsiano", value="15°"),
            Angle(name="Ángulo PASA", value="10°"),
            Angle(name="Ángulo DASA", value="8°"),
        ],
        notes="Evaluación pre-quirúrgica, se recomienda intervención.",
    ),
]
