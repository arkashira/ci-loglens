import pytest
from ci_loglens import LogLens, LogLensConfig, CITool

def test_connect_azure_devops_ci_tool():
    config = LogLensConfig(ci_tool=CITool.AZURE_DEVOPS, ci_tool_config={})
    log_lens = LogLens(config)
    result = log_lens.connect_ci_tool()
    assert result["connected"] == True
    assert result["ci_tool"] == CITool.AZURE_DEVOPS.value

def test_connect_github_actions_ci_tool():
    config = LogLensConfig(ci_tool=CITool.GITHUB_ACTIONS, ci_tool_config={})
    log_lens = LogLens(config)
    result = log_lens.connect_ci_tool()
    assert result["connected"] == True
    assert result["ci_tool"] == CITool.GITHUB_ACTIONS.value

def test_connect_jenkins_ci_tool():
    config = LogLensConfig(ci_tool=CITool.JENKINS, ci_tool_config={})
    log_lens = LogLens(config)
    result = log_lens.connect_ci_tool()
    assert result["connected"] == True
    assert result["ci_tool"] == CITool.JENKINS.value

def test_analyze_ci_logs():
    config = LogLensConfig(ci_tool=CITool.AZURE_DEVOPS, ci_tool_config={})
    log_lens = LogLens(config)
    result = log_lens.analyze_ci_logs()
    assert result["logs_analyzed"] == True

def test_connect_unsupported_ci_tool():
    config = LogLensConfig(ci_tool="unsupported_tool", ci_tool_config={})
    log_lens = LogLens(config)
    with pytest.raises(ValueError):
        log_lens.connect_ci_tool()
