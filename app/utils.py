def generic_model_mutation_process(model, data, id=None, commit=True):
    """ funcion para crear, recuperar o editar la instancia de un modelo

        :author: Desconocido

        :param model(django.db.models.Model): instancia del modelo
        :param data(dict): diccionario con los valores de los atributos
            del modelo
        :param id(str): id de la instancia
        :param commit(bool): indica si los cambios se deben almacenar
            en la base de datos

        :return: instancia del modelo
        :rtype: django.db.models.Model
    """

    if id:
        item = model.objects.get(id=id)
        try:
            del data['id']
        except KeyError:
            pass

        for field, value in data.items():
            setattr(item, field, value)
    else:
        item = model(**data)

    if commit:
        item.save()

    return item
