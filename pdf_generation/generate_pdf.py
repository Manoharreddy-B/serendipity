import subprocess
import os
import random
from datetime import datetime

def generate_pdf(user_data):
    with open("report.ttyp", "r") as f:
        template = f.read()

    # Format stocks as a Typst array of tuples (each row on its own line)
    stocks_formatted = ",\n  ".join(
        [f'("{symbol}", {qty}, "{typ}", {value:.2f})'
        for symbol, qty, typ, value in user_data["stocks"]]
    )

    replacements = {
        "[NAME]": user_data["name"],
        "[EMAIL]": user_data["email"],
        # "[PHONE]": user_data["phone"],
        "[STOCKS]": stocks_formatted
    }

    for old, new in replacements.items():
        template = template.replace(old, new)

    with open("generated_report.ttyp", "w") as f:
        f.write(template)

    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    # Generate the filename
    date_str = datetime.now().strftime("%d%m%y")
    random_number = random.randint(1, 10000)
    filename = f"reports/{date_str}_{user_data["name"]}_{random_number}.pdf"
    try:
        subprocess.run(
            ["typst", "compile", "generated_report.ttyp", filename],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"PDF successfully generated: {filename}")
    except subprocess.CalledProcessError as e:
        print(f"PDF generation failed: {e.stderr.decode()}")
    except FileNotFoundError:
        print("Error: Typst compiler not found. Install from https://typst.app")


