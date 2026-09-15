from pathlib import Path
from src.validators import validate_script

def test_fixture_scripts():
    for p in Path('data/scripts').glob('fixture_ad_*.json'):
        assert validate_script(p)
