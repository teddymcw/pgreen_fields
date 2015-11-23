#### django.contrib.postgres: ArrayField, HStoreField, and RangeField.    

0. #### General Question     

Please provide a brief overview of the new field types, described here: ArrayField, HStoreField, and RangeField.     
How are these field classes constructed?     
How are they different from other Django model field definitions?     
How does the Django ORM construct valid postgres SQL queries for these fields?     

1. #### Context    

Field is an abstract class that represents a database table column. This is defined in django.db.models.fields     



What is a Field to Django and how are these field classes constructed?    

Field is an abstract class that represents a database table column.     
This is defined in django.db.models.fields    

    ```python
    >>> from django.db.models import Field
    >>> len(dir(Field))
    97
    ```

Let’s pick out some truly intrinsic methods, and then very briefly walk through how a basic built-in Field is defiend    

1. contribute_to_class - How the Field class gets bound to the Model class we have defined, if this isn’t defined then the setattr() just gets called for the new Field class to the Model class    
2. db_type() - Perform preliminary non-db specific value checks and conversions. This just returns a string e.g. 'int8range' for BigIntegerRangeField. When addressing just PG this is easy because we are writing for exactly one database, Postgres, and therefore know exactly what the Column type is  we return     
3. get_internal_type() is a 'cheat' to convert to python type directly    
4. get_db_prep_value()  Returns field's value prepared for interacting with the database backend.    
5. get_prep_lookup() Perform preliminary non-db specific lookup checks and conversions.    
6. get_db_prep_lookup()Returns field's value prepared for database lookup.    
7. deconstruct() essentially for adding any kwargs that are custom for this Field type, the deconstruct method will be used for serialization and migrations    


2. #### The Real Question and Challenge    

That was a nice example of how to write a Field but it was very easy since Decimal is fairly standard   


One of the best paradigms in which to approach this is to present ourselves with the problem of writing the custom Postgres Field.    
 
from the Postgres Docs:    
1. Array Type
PostgreSQL allows columns of a table to be defined as variable-length multidimensional arrays. Arrays of any built-in or user-defined base type, enum type, or composite type can be created. (The type of the array needs to be specified.) 
 
```SQL
CREATE TABLE sal_emp (
    name            text,
    pay_by_quarter  integer[],
    schedule        text[][]
);
```