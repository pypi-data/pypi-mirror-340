from click.testing import CliRunner
from sofaman.sofamangen import generate, export

def test_generate_xmi(tmp_path):
    runner = CliRunner()
    input_file = tmp_path / "input.sofa"
    output_file = tmp_path / "output.xmi"
    input_file.write_text("class A")

    result = runner.invoke(generate, [str(input_file), str(output_file), '--type', 'xmi'])

    assert result.exit_code == 0
    assert output_file.exists()

def test_generate_puml(tmp_path):
    runner = CliRunner()
    input_file = tmp_path / "input.sofa"
    output_file = tmp_path / "output.puml"
    input_file.write_text("class B")

    result = runner.invoke(generate, [str(input_file), str(output_file), '--type', 'puml'])

    assert result.exit_code == 0
    assert output_file.exists()

def test_generate_invalid_type(tmp_path):
    runner = CliRunner()
    input_file = tmp_path / "input.sofa"
    output_file = tmp_path / "output.invalid"
    input_file.write_text("class A")

    result = runner.invoke(generate, [str(input_file), str(output_file), '--type', 'invalid'])

    assert result.exit_code != 0
    assert "Unknown type invalid" in result.output

def test_generate_missing_input():
    runner = CliRunner()
    result = runner.invoke(generate, ['missing_input.sofa', 'output.xmi', '--type', 'xmi'])

    assert result.exit_code != 0
    assert "Error: Invalid value for 'INPUT'" in result.output

def test_export_id(tmp_path):
    runner = CliRunner()
    input_file = tmp_path / "input.xmi"
    output_file = tmp_path / "output.json"
    input_file.write_text("<xmi:XMI xmlns:xmi='http://schema.omg.org/spec/XMI/2.1'></xmi:XMI>")

    result = runner.invoke(export, [str(input_file), str(output_file)])

    assert result.exit_code == 0
    assert output_file.exists()

def test_ids_file(tmp_path):
    runner = CliRunner()
    input_file = tmp_path / "input.xmi"
    output_file = tmp_path / "output.json"
    ids_file = tmp_path / "ids.json"
    input_file.write_text("class A")
    ids_file.write_text('{"A": "1"}')
    result = runner.invoke(generate, [str(input_file), str(output_file), '--ids_file', str(ids_file)])

    assert result.exit_code == 0
    assert output_file.exists()

