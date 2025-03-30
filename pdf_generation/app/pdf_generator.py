# app/pdf_generator.py

import subprocess
import logging
import os

logger = logging.getLogger(__name__)

def generate_pdf(user_data: dict, template_path: str, output_pdf: str) -> None:
    """
    Generate a PDF using Typst given user_data and a Typst template.
    
    :param user_data: Dictionary containing user info & stocks.
    :param template_path: Path to the Typst template file (e.g. 'report.ttyp').
    :param output_pdf: The desired output PDF file path.
    """
    # Read the template
    with open(template_path, "r") as f:
        template = f.read()

    # Format the "stocks" data for insertion
    stocks_list = user_data.get("stocks", [])
    # Convert each stock to Typst-friendly text
    stocks_formatted = ",\n  ".join(
        [
            f'("{stock["stockName"]}", {stock["qty"]}, "{stock["type"]}", {float(stock["value"]):.2f})'
            for stock in stocks_list
        ]
    )

    # You can add more fields if needed
    replacements = {
        "[NAME]": user_data.get("name", "N/A"),
        "[EMAIL]": user_data.get("email", "N/A"),
        "[STOCKS]": stocks_formatted
    }

    # Do the replacements
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)

    # Write a temporary Typst file
    generated_typ_path = "generated_report.ttyp"
    with open(generated_typ_path, "w") as f:
        f.write(template)

    try:
        # Execute Typst
        result = subprocess.run(
            ["typst", "compile", generated_typ_path, output_pdf],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.info("PDF successfully generated: %s", output_pdf)
    except subprocess.CalledProcessError as e:
        logger.error("PDF generation failed. Stderr:\n%s", e.stderr.decode())
    except FileNotFoundError:
        logger.error("Error: Typst compiler not found. Install from https://typst.app")
    finally:
        # Clean up generated .ttyp if you don't need to keep it:
        if os.path.exists(generated_typ_path):
            os.remove(generated_typ_path)
