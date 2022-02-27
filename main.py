import requests
import typer
import json
import pprint
from distutils.version import StrictVersion

BASE_URL = "https://pypi.org/pypi"

app = typer.Typer()

def _get_versions(pkg: str, uri: str = BASE_URL):
    data = f"{uri}/{pkg}/json"
    res = requests.get(data, timeout=10)
    try:
        #raise requests.exceptions.Timeout
        res.raise_for_status()
        releases = res.json()["releases"].keys()
        return (sorted(releases, key=StrictVersion), 0)
    except requests.exceptions.HTTPError:
        return (f"The package {pkg} was not found in Pypy. Please check your package name.", 1)

    except requests.exceptions.Timeout:
        return ("The connection timed out, maybe try another uri.", 1, "TimeoutError")

@app.command()
def get_versions(pkg: str, uri: str = BASE_URL):
    data = f"{uri}/{pkg}/json"
    res = requests.get(data, timeout=10)
    try:
        #raise requests.exceptions.Timeout
        res.raise_for_status()
        releases = res.json()["releases"].keys()
        typer.echo("\n".join(sorted(releases, key=StrictVersion)))
    except requests.exceptions.HTTPError:
        typer.echo(f"The package {pkg} was not found in Pypy. Please check your package name.")
        raise typer.Exit(code=1)
    except requests.exceptions.Timeout:
        typer.echo("The connection timed out, maybe try another uri.")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    #get_versions("a12dsdasbafds")
    get_versions("typer")
    #app()