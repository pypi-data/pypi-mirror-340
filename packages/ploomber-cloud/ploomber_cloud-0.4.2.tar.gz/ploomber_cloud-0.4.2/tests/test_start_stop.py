import sys
import pytest
from unittest.mock import Mock, call

from ploomber_cloud.cli import cli

CMD_NAME = "ploomber-cloud"


@pytest.mark.parametrize(
    "endpoint, job_details_response, is_eks",
    [
        (
            "jobs/job-id/service_start",
            {"status": "started", "projectId": "someid"},
            False,
        ),
        (
            "v2/jobs/job-id/service_start",
            {"status": "started", "projectId": "someid"},
            True,
        ),
    ],
    ids=["default", "eks"],
)
def test_start_command(monkeypatch, set_key, endpoint, job_details_response, is_eks):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "start", "--project-id", "someid"])
    mock_requests = Mock(name="requests")

    def mock_get(*args, **kwargs):
        if "/projects/someid" in args[0]:
            return Mock(
                ok=True,
                json=Mock(return_value={"jobs": [{"id": "job-id"}], "is_eks": is_eks}),
            )
        return Mock(ok=True, json=Mock(return_value=job_details_response))

    def mock_patch(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value=job_details_response))

    mock_requests.get.side_effect = mock_get
    mock_requests.patch.side_effect = mock_patch

    monkeypatch.setattr("ploomber_cloud.api.requests", mock_requests)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    assert (
        call(
            "https://cloud-prod.ploomber.io/projects/someid",
            headers={"accept": "application/json", "api_key": "somekey"},
        )
        in mock_requests.get.call_args_list
    )
    assert (
        call(
            "https://cloud-prod.ploomber.io/jobs/job-id",
            headers={"accept": "application/json", "api_key": "somekey"},
        )
        in mock_requests.get.call_args_list
    )

    mock_requests.patch.assert_called_with(
        f"https://cloud-prod.ploomber.io/{endpoint}",
        headers={"accept": "application/json", "api_key": "somekey"},
    )


@pytest.mark.parametrize(
    "endpoint, job_details_response, is_eks",
    [
        (
            "jobs/job-id/service_stop",
            {"status": "stopped", "projectId": "someid"},
            False,
        ),
        (
            "v2/jobs/job-id/service_stop",
            {"status": "stopped", "projectId": "someid"},
            True,
        ),
    ],
    ids=["default", "eks"],
)
def test_stop_command(monkeypatch, set_key, endpoint, job_details_response, is_eks):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "stop", "--project-id", "someid"])
    mock_requests = Mock(name="requests")

    def mock_get(*args, **kwargs):
        if "/projects/someid" in args[0]:
            return Mock(
                ok=True,
                json=Mock(return_value={"jobs": [{"id": "job-id"}], "is_eks": is_eks}),
            )
        return Mock(ok=True, json=Mock(return_value=job_details_response))

    def mock_patch(*args, **kwargs):
        return Mock(ok=True, json=Mock(return_value=job_details_response))

    mock_requests.get.side_effect = mock_get
    mock_requests.patch.side_effect = mock_patch

    monkeypatch.setattr("ploomber_cloud.api.requests", mock_requests)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    assert (
        call(
            "https://cloud-prod.ploomber.io/projects/someid",
            headers={"accept": "application/json", "api_key": "somekey"},
        )
        in mock_requests.get.call_args_list
    )
    assert (
        call(
            "https://cloud-prod.ploomber.io/jobs/job-id",
            headers={"accept": "application/json", "api_key": "somekey"},
        )
        in mock_requests.get.call_args_list
    )

    mock_requests.patch.assert_called_with(
        f"https://cloud-prod.ploomber.io/{endpoint}",
        headers={"accept": "application/json", "api_key": "somekey"},
    )


def test_start_command_server_error(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "start", "--project-id", "someid"])
    mock_requests = Mock(name="requests")

    def mock_get(*args, **kwargs):
        if "/projects/someid" in args[0]:
            return Mock(
                ok=True,
                json=Mock(return_value={"jobs": [{"id": "job-id"}], "is_eks": False}),
            )
        if "/jobs/job-id" in args[0]:
            return Mock(ok=True, json=Mock(return_value={"projectId": "someid"}))
        return Mock(ok=False, json=Mock(return_value={"detail": "some error"}))

    def mock_patch(*args, **kwargs):
        return Mock(ok=False, json=Mock(return_value={"detail": "some error"}))

    mock_requests.get.side_effect = mock_get
    mock_requests.patch.side_effect = mock_patch

    monkeypatch.setattr("ploomber_cloud.api.requests", mock_requests)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 1
    mock_requests.get.assert_called_with(
        "https://cloud-prod.ploomber.io/projects/someid",
        headers={"accept": "application/json", "api_key": "somekey"},
    )
    mock_requests.patch.assert_called_with(
        "https://cloud-prod.ploomber.io/jobs/job-id/service_start",
        headers={"accept": "application/json", "api_key": "somekey"},
    )
    assert "Error: An error occurred: some error" in capsys.readouterr().err


def test_stop_command_server_error(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "stop", "--project-id", "someid"])
    mock_requests = Mock(name="requests")

    def mock_get(*args, **kwargs):
        if "/projects/someid" in args[0]:
            return Mock(
                ok=True,
                json=Mock(return_value={"jobs": [{"id": "job-id"}], "is_eks": False}),
            )
        if "/jobs/job-id" in args[0]:
            return Mock(ok=True, json=Mock(return_value={"projectId": "someid"}))
        return Mock(ok=False, json=Mock(return_value={"detail": "some error"}))

    def mock_patch(*args, **kwargs):
        return Mock(ok=False, json=Mock(return_value={"detail": "some error"}))

    mock_requests.get.side_effect = mock_get
    mock_requests.patch.side_effect = mock_patch

    monkeypatch.setattr("ploomber_cloud.api.requests", mock_requests)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 1
    mock_requests.get.assert_called_with(
        "https://cloud-prod.ploomber.io/projects/someid",
        headers={"accept": "application/json", "api_key": "somekey"},
    )
    mock_requests.patch.assert_called_with(
        "https://cloud-prod.ploomber.io/jobs/job-id/service_stop",
        headers={"accept": "application/json", "api_key": "somekey"},
    )
    assert "Error: An error occurred: some error" in capsys.readouterr().err
