from click.testing import CliRunner

from dnscontroller.main import main, parse_ttl


def test_parse_ttl():
    assert parse_ttl("auto") == 1
    assert parse_ttl("5min") == 300
    assert parse_ttl("1h") == 3600
    assert parse_ttl("1d") == 86400
    assert parse_ttl("300") == 300


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "DNS Controller - Manage DNS records via Cloudflare" in result.output

    result = runner.invoke(main, ["ls", "--help"])
    assert result.exit_code == 0
    assert "List DNS records" in result.output

    result = runner.invoke(main, ["set", "--help"])
    assert result.exit_code == 0
    assert "Set a DNS record" in result.output

    result = runner.invoke(main, ["rm", "--help"])
    assert result.exit_code == 0
    assert "Remove a DNS record" in result.output
