from RPA.Database import Database
from pydoc import locate


class OracleExtendedDatabase(Database):
    """This library extends keywords of the parent `RPA.Database` library.
    
    New keyword provided: Oracle Call Procedure
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def oracle_call_procedure(
        self, procedure_name: str, input_parameters: list, result_type: str = "str"
    ):
        """Keyword for calling a stored procedure in the Oracle Database.

        :param procedure_name: name of the stored procedure
        :param input_parameters: all procedure parameters in a list
        :param result_type: type of the return value (default 'str')
        :return: returnable value of the stored procedure result

        Example:

        .. code-block:: robotframework

            @{params}     Create List   FirstParam   SecondParam   ThirdParam
            ${result}     Call Stored Procedure   mystpr  ${params}
        """
        cursor = self._dbconnection.cursor()
        result_object = cursor.var(locate(result_type))
        input_parameters.append(result_object)
        cursor.callproc(procedure_name, input_parameters)
        return result_object.getvalue()
