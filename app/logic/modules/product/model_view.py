from flask_admin.model import BaseModelView


class ProductModelView(BaseModelView):
    def get_pk_value(self, model):
        return self.model.id
