import subprocess
import json
import time

import os
print os.getcwd()
print __file__

def test_output_strips_email_spaces():
    command = ["python", "adp_parser.py", "FullExport_servicesOnly_newest.txt"]
    subprocess.Popen(command)
    time.sleep(1)

    with open('open_ref.json') as data_file:
        data = json.load(data_file)
        offensive_field = data[70]["locations"][0]["emails"]
        expected = [
                "ronald.sanders@sfdph.org",
                "juanita.alvarado@sfdph.org",
                "joseph.calderon@sfdph.org",
                ]

        assert offensive_field == expected
