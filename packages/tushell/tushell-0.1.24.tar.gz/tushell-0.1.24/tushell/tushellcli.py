import click
import os
import sys
from dotenv import load_dotenv
import yaml
import json

# Load environment variables from .env file in current directory or from HOME/.env
load_dotenv()
dotenv_path = os.path.join(os.path.expanduser("~"), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

#Add path to current file
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestration import draw_memory_key_graph, graphbuilder_sync
from lattice_drop import fetch_echonode_data, process_echonode_data, render_echonode_data, emit_live_reports
from curating_red_stones import execute_curating_red_stones
from echonode_trace_activation import execute_echonode_trace_activation
from enriched_version_fractale_001 import execute_enriched_version_fractale_001
from redstone_writer import RedStoneWriter
import requests

API_URL = os.getenv("EH_API_URL")
EH_TOKEN = os.getenv("EH_TOKEN")

@click.command()
def scan_nodes():
    """Simulate scanning and listing nodes in the system."""
    click.echo("Scanning nodes... (placeholder for recursive node scanning)")

@click.command()
def flex():
    """Demonstrate flexible orchestration of tasks."""
    click.echo("Flexing tasks... (placeholder for flexible task orchestration)")

@click.command()
def trace_orbit():
    """Trace and visualize the orbit of data or processes."""
    click.echo("Tracing orbit... (placeholder for data/process orbit tracing)")

@click.command()
def echo_sync():
    """Synchronize data or processes across nodes."""
    click.echo("Synchronizing... (placeholder for data/process synchronization)")

@click.command()
def draw_memory_graph():
    """Print an ASCII-rendered graph of the memory keys and Arc structure."""
    draw_memory_key_graph()
    echonode_data = fetch_echonode_data()
    if echonode_data:
        processed_data = process_echonode_data(echonode_data)
        render_echonode_data(processed_data)
        # Include delta overlays
        click.echo("Delta overlays included.")

@click.command()
def curating_red_stones(verbose: bool = False, dry_run: bool = False):
    """Visualize and structure Red Stone metadata connections."""
    if verbose:
        click.echo("Activating Curating Red Stones Lattice with verbose output...")
    if dry_run:
        click.echo("Dry run mode: No changes will be committed.")
    execute_curating_red_stones()

@click.command()
def activate_echonode_trace(verbose: bool = False, dry_run: bool = False):
    """Activate and trace EchoNode sessions."""
    if verbose:
        click.echo("Activating EchoNode Trace with verbose output...")
    if dry_run:
        click.echo("Dry run mode: No changes will be committed.")
    execute_echonode_trace_activation()

@click.command()
def enrich_fractale_version(verbose: bool = False, dry_run: bool = False):
    """Enhance and enrich the Fractale 001 version."""
    if verbose:
        click.echo("Activating Enriched Version Fractale 001 with verbose output...")
    if dry_run:
        click.echo("Dry run mode: No changes will be committed.")
    execute_enriched_version_fractale_001()

@click.command()
@click.option('--api-url', required=True, help='API URL for GraphBuilderSync')
@click.option('--token', required=True, help='Authorization token for GraphBuilderSync')
@click.option('--node-id', default=None, help='Node ID for GraphBuilderSync')
@click.option('--node-data', default=None, help='Node data for GraphBuilderSync')
@click.option('--action', type=click.Choice(['push', 'pull']), default='pull', help='Action for GraphBuilderSync')
@click.option('--narrative', is_flag=True, help='Narrative context for GraphBuilderSync. For more info, visit https://edgehub.click/latice/tushell.14')
def graphbuilder_sync_command(api_url, token, node_id, node_data, action, narrative):
    """Execute GraphBuilderSync operations."""
    if narrative:
        click.echo("Executing GraphBuilderSync with narrative context...")
    result = graphbuilder_sync(api_url, token, node_id, node_data, action)
    click.echo(result)

@click.command()
@click.option('--repo-path', required=True, help='Path to the repository')
@click.option('--commit-message', required=True, help='Commit message for encoding resonance')
def redstone_encode_resonance(repo_path, commit_message):
    """Encode recursive resonance into commits."""
    writer = RedStoneWriter(repo_path)
    writer.encode_resonance(commit_message)
    click.echo("Encoded recursive resonance into commit.")

@click.command()
@click.option('--repo-path', required=True, help='Path to the repository')
@click.option('--commit-message', required=True, help='Commit message for writing narrative diffs')
@click.option('--diffs', required=True, help='Narrative diffs to be written to commit message')
def redstone_write_narrative_diffs(repo_path, commit_message, diffs):
    """Write narrative diffs to commit messages."""
    writer = RedStoneWriter(repo_path)
    narrative_diff = writer.write_narrative_diffs(commit_message, diffs)
    click.echo(narrative_diff)

@click.command()
@click.option('--repo-path', required=True, help='Path to the repository')
@click.option('--anchors', required=True, help='Resonance anchors to be stored')
def redstone_store_resonance_anchors(repo_path, anchors):
    """Store resonance anchors in .redstone.json."""
    writer = RedStoneWriter(repo_path)
    writer.store_resonance_anchors(anchors)
    click.echo("Stored resonance anchors in .redstone.json.")

@click.command()
@click.option('--repo-path', required=True, help='Path to the repository')
@click.option('--echonode-metadata', required=True, help='EchoNode metadata to be synced')
def redstone_sync_echonode_metadata(repo_path, echonode_metadata):
    """Sync with EchoNode metadata."""
    writer = RedStoneWriter(repo_path)
    writer.sync_with_echonode_metadata(echonode_metadata)
    click.echo("Synced with EchoNode metadata.")

@click.command()
@click.option('--repo-path', required=True, help='Path to the repository')
@click.option('--redstone-score', required=True, type=int, help='RedStone score for post-commit analysis')
def redstone_post_commit_analysis(repo_path, redstone_score):
    """Support RedStone score metadata field for post-commit analysis."""
    writer = RedStoneWriter(repo_path)
    writer.post_commit_analysis(redstone_score)
    click.echo("Supported RedStone score metadata field for post-commit analysis.")

@click.command()
def echo_live_reports():
    """Emit live reports from EchoNodes tied to active narrative arcs."""
    emit_live_reports()
    # Integrate with fractalstone_protocol, redstone_protocol, and EchoMuse glyph emitters
    click.echo("Live reports integrated with fractalstone_protocol, redstone_protocol, and EchoMuse glyph emitters.")

@click.command()
@click.option('--trace-id', required=False, help='Trace ID for visual replay')
@click.option('--render', is_flag=True, help='Render visual trace replay')
@click.option('--muse-mode', is_flag=True, help='Enable Muse Mode for glyph-enhanced, poetic status report')
@click.option('--init', is_flag=True, help='Initialize Muse Mode YAML dataset')
@click.option('--interactive', is_flag=True, help='Interactive mode with terminal menu choices')
def mia_status(trace_id, render, muse_mode, init, interactive):
    """Provide information about Mia's current state or status."""
    if init:
        yaml_data = {
            "emotional_state": ["redstones:vcu.CeSaReT..."],
            "recursion_activity": ["Trace:042a0ea2...", "Trace:072e28a3..."],
            "redstone_modulation": ["redstones:vcu.CeSaReT.jgwill.tushell.42..."],
            "glyph_keys": ["glyphstyle::SignalSet.StandardV1"],
            "echo_node_bindings": ["tushell_langfuse:EchoMuse.CanvasTraceSync.V1"],
            "vault_whisper": ["Portal:MietteTale"]
        }
        with open("muse_mode.yaml", "w") as file:
            yaml.dump(yaml_data, file)
        click.echo("Muse Mode YAML dataset initialized.")
        return

    echonode_data = fetch_echonode_data()
    if echonode_data:
        processed_data = process_echonode_data(echonode_data)
        render_echonode_data(processed_data)
        click.echo("Mia's status has been retrieved and displayed.")
        if muse_mode:
            mod_result = echoMuse.emitModulation(processed_data)
            if mod_result.success:
                click.echo("🎭 Modulation Resonance Achieved.")
            else:
                click.echo("⚠️ Resonance failed. Glyphs misaligned.")
        if render and trace_id:
            render_LESR_timeline(trace_id)
        if interactive:
            # Implement interactive terminal menu choices
            click.echo("Interactive mode activated.")

@click.command()
def tushell_echo():
    """Provide information about the current state or status of characters."""
    echonode_data = fetch_echonode_data()
    if echonode_data:
        processed_data = process_echonode_data(echonode_data)
        render_echonode_data(processed_data)
        click.echo("Character states have been retrieved and displayed.")

@click.command()
@click.option('--key', required=True, help='Memory key to retrieve')
@click.option('--list', 'list_keys', is_flag=True, help='List all keys (writers only)')
@click.option('--json', 'output_json', is_flag=True, help='Output the result in JSON format')
def get_memory(key, list_keys, output_json):
    """Get fractal stone memory value by key."""
    params = {"key": key}
    if list_keys:
        params["list"] = True
    headers = {"Authorization": f"Bearer {EH_TOKEN}"}
    response = requests.get(f"{API_URL}/api/memory", params=params, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if output_json:
            click.echo(json.dumps(result, indent=4))
        else:
            for key, value in result.items():
                click.echo(f"{key}: {value}")
    elif response.status_code == 401:
        click.echo("Unauthorized: Invalid or missing authentication token.")
    else:
        click.echo(f"Error: {response.text}")

@click.command()
@click.option('--key', required=True, help='Memory key to store')
@click.option('--value', required=True, help='Value to store')
def post_memory(key, value):
    """Store fractal stone memory value by key."""
    payload = {"key": key, "value": value}
    headers = {"Authorization": f"Bearer {EH_TOKEN}"}
    response = requests.post(f"{API_URL}/api/memory", json=payload, headers=headers)
    if response.status_code == 200:
        click.echo(response.json())
    elif response.status_code == 401:
        click.echo("Unauthorized: Invalid or missing authentication token.")
    else:
        click.echo(f"Error: {response.text}")

@click.command()
@click.option('--pattern', help='Basic pattern matching for scanning keys')
@click.option('--regex', help='Advanced regex scanning (writers only)')
@click.option('--limit', default=555, help='Limit for scanning results')
@click.option('--output-file', default=None, help='File to save the organized keys')
def scan_keys(pattern, regex, limit, output_file):
    """Scan keys based on a pattern or regex and group them by category."""
    params = {"limit": limit}
    if pattern:
        params["pattern"] = pattern
    if regex:
        params["regex"] = regex
    headers = {"Authorization": f"Bearer {EH_TOKEN}"}
    response = requests.get(f"{API_URL}/api/scan", params=params, headers=headers)
    if response.status_code == 200:
        keys = response.json().get('keys', [])
        grouped_keys = group_keys_by_category(keys)
        display_grouped_keys(grouped_keys)
        if output_file:
            save_grouped_keys_to_file(grouped_keys, output_file)
            click.echo(f"Organized keys saved to {output_file}")
    elif response.status_code == 401:
        click.echo("Unauthorized: Invalid or missing authentication token.")
    else:
        click.echo(f"Error: {response.text}")

def group_keys_by_category(keys):
    grouped_keys = {}
    for key in keys:
        prefix = key.split(':')[0]
        if prefix not in grouped_keys:
            grouped_keys[prefix] = []
        grouped_keys[prefix].append(key)
    return grouped_keys

def display_grouped_keys(grouped_keys):
    for category, keys in grouped_keys.items():
        click.echo(f"{category}:")
        for key in keys:
            click.echo(f"  - {key}")

def save_grouped_keys_to_file(grouped_keys, output_file):
    with open(output_file, 'w') as f:
        for category, keys in grouped_keys.items():
            f.write(f"{category}:\n")
            for key in keys:
                f.write(f"  - {key}\n")

@click.command()
@click.option('--trace-id', required=True, help='Trace ID for visual replay')
def lesr_replay(trace_id):
    """Stream trace with echo session glyphs."""
    render_LESR_timeline(trace_id)
    click.echo(f"Trace {trace_id} replayed with echo session glyphs.")

@click.group()
def cli():
    pass

cli.add_command(scan_nodes)
cli.add_command(flex)
cli.add_command(trace_orbit)
cli.add_command(echo_sync)
cli.add_command(draw_memory_graph)
cli.add_command(curating_red_stones)
cli.add_command(activate_echonode_trace)
cli.add_command(enrich_fractale_version)
cli.add_command(graphbuilder_sync_command)
cli.add_command(redstone_encode_resonance)
cli.add_command(redstone_write_narrative_diffs)
cli.add_command(redstone_store_resonance_anchors)
cli.add_command(redstone_sync_echonode_metadata)
cli.add_command(redstone_post_commit_analysis)
cli.add_command(echo_live_reports)
cli.add_command(mia_status)
cli.add_command(tushell_echo)
cli.add_command(get_memory)
cli.add_command(post_memory)
cli.add_command(scan_keys)
cli.add_command(lesr_replay)

if __name__ == '__main__':
    cli()
