# Example on Oracle operations

## Workaround for calling stored procedure in Oracle database

Due to the issue in the `RPA.Database` library in `rpaframework` **15.9.0** (and earlier) this example provides an workaround
solution.

Example contains an extended  library `OracleExtendedDatabase.py`, which will add keyword `Oracle Call Procedure`. This extended 
library contains all the keywords from `RPA.Database` plus this new keyword.

## Example procedure used in the Oracle database

```sql
CREATE OR REPLACE PROCEDURE PROCEDURE1 
(
  PARAM1 IN VARCHAR2,
  PARAM2 OUT VARCHAR2
) AS 
BEGIN
  PARAM2 :=  ('Welcome '|| PARAM1);
END PROCEDURE1;
```

The procedure is given an input parameter as string and it will return output as string, for example. with input `Robot` the output
will be `Welcome Robot`.

## Calling above procedure in Robot Framework syntax

```robotframework
  @{params}=    Create List    Robot
  ${result}=    Oracle Call Procedure    PROCEDURE1    ${params}
  IF  "${result}" == "Welcome Robot"
      Log To Console   We are welcome
  ELSE
      Log To Console   They do not welcome robots
  END
```
