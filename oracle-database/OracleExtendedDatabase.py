from RPA.Database import Database
from pydoc import locate


class OracleExtendedDatabase(Database):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def oracle_call_procedure(
        self, procedure_name: str, input_parameters: list, result_type: str = "str"
    ):
        """_summary_

        :param procedure_name: _description_
        :param input_parameters: _description_
        :param result_type: _description_
        :return: _description_
        """
        cursor = self._dbconnection.cursor()
        result_object = cursor.var(locate(result_type))
        input_parameters.append(result_object)
        cursor.callproc(procedure_name, input_parameters)
        return result_object.getvalue()
