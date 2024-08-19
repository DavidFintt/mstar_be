from flask import current_app
from apps.mercadoria.models import EstoqueMercadoria


def gerenciar_estoque(mercadoria, quantidade, type):
    try:
        db_session = current_app.config["SESSION"]()
        estoque = (
            db_session.query(EstoqueMercadoria)
            .filter(EstoqueMercadoria.mercadoria == mercadoria)
            .first()
        )
        if estoque:
            estoque.quantidade += quantidade if type == "entrada" else -quantidade
            db_session.commit()
            db_session.close()
            return True
        estoque = EstoqueMercadoria(mercadoria=mercadoria, quantidade=quantidade)
        db_session.add(estoque)
        db_session.commit()
        db_session.close()
        return True
    except Exception as e:
        raise Exception(str(e))
