"""
Flask web interface for the Stage 1 order price calculator.

Wraps price_calculator.process_4_priced_order() with a simple HTML form:
enter number_of_items / unit_price / country_code / order_date, get back
the same priced-order breakdown as the CLI --interactive mode.
"""

from flask import Flask, render_template, request

from price_calculator import COUNTRY_VAT, process_4_priced_order

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    errors = []
    # Keep whatever the user typed so the form doesn't clear on error.
    form_values = {
        "number_of_items": "",
        "unit_price": "",
        "country_code": "DK",
        "order_date": "",
    }

    if request.method == "POST":
        form_values["number_of_items"] = request.form.get("number_of_items", "").strip()
        form_values["unit_price"] = request.form.get("unit_price", "").strip()
        form_values["country_code"] = request.form.get("country_code", "").strip()
        form_values["order_date"] = request.form.get("order_date", "").strip()

        number_of_items = None
        unit_price = None

        try:
            number_of_items = int(form_values["number_of_items"])
        except ValueError:
            errors.append("Number of items must be a whole number.")

        try:
            unit_price = float(form_values["unit_price"])
        except ValueError:
            errors.append("Unit price must be a number.")

        if not form_values["country_code"]:
            errors.append("Country code is required.")

        if not errors:
            try:
                result = process_4_priced_order(
                    number_of_items,
                    unit_price,
                    form_values["country_code"],
                    form_values["order_date"],
                )
            except ValueError as exc:
                errors.append(str(exc))

    return render_template(
        "index.html",
        result=result,
        errors=errors,
        form_values=form_values,
        countries=COUNTRY_VAT,
    )


if __name__ == "__main__":
    # debug=True is for local development only - turn off before deploying.
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
