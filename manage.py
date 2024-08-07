import click
import subprocess

@click.group()
def cli():
    pass

@click.command()
def setup_db():
    """Set up the database and populate initial data."""
    subprocess.run(["python", "app/data_processing.py"])
    click.echo("Database setup and initial data populated.")
# Register the setup_db command  
cli.add_command(setup_db)

if __name__ == "__main__":
    cli()
    
    
    
