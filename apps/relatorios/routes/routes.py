from flask import Blueprint, request, current_app, jsonify
from apps.usuarios.users_utils.jwt.validate import jwt_required
from apps.relatorios.utils_relatorios.handle_pdf.pdf import create_pdf
from flask import send_file
import base64
from io import BytesIO

relatorio_blueprint = Blueprint("relatorio", __name__)


@relatorio_blueprint.route("/relatorio/pdf/", methods=["POST"])
@jwt_required
def gerar_pdf():
    data_list = []
    data = request.json

    data_to_use = data if isinstance(data, dict) else data[0]

    headers = [
        key for key in data_to_use.keys() if key != "mercadoria" and key != "entrega"
    ]
    for item in data:
        row = [item[header] for header in headers]
        data_list.append(row)

    data = [headers] + data_list

    pdf_output = BytesIO()
    create_pdf(data, pdf_output)
    pdf_output.seek(0)

    base64.b64encode(pdf_output.getvalue()).decode("utf-8")

    return send_file(
        pdf_output,
        as_attachment=True,
        download_name="relatorio.pdf",
        mimetype="application/pdf",
    )
