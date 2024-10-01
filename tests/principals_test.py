from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']      
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED.value, AssignmentStateEnum.GRADED.value]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    Failure case: If an assignment is in Draft state, it cannot be graded by principal.
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,  # Assuming this ID corresponds to a draft assignment
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json['error'] == "Assignment not found or cannot be graded."


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,  # Assuming this ID corresponds to a valid submitted assignment
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C.value


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,  # Re-grading the same assignment
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200
    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B.value
