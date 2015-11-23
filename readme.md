#### django.contrib.postgres: ArrayField, HStoreField, and RangeField.    

### 0.  General Question     

Please provide a brief overview of the new field types, described here: ArrayField, HStoreField, and RangeField.     
How are these field classes constructed?     
How are they different from other Django model field definitions?     
How does the Django ORM construct valid postgres SQL queries for these fields?     

### 1.  Context    

Field is an abstract class that represents a database table column. This is defined in django.db.models.fields     



What is a Field to Django and how are these field classes constructed?    

Field is an abstract class that represents a database table column.     
This is defined in django.db.models.fields    

    
    >>> from django.db.models import Field
    >>> len(dir(Field))
    97
    

Let’s pick out some truly intrinsic methods, and then very briefly walk through how a basic built-in Field is defiend    

1. contribute_to_class - How the Field class gets bound to the Model class we have defined, if this isn’t defined then the setattr() just gets called for the new Field class to the Model class    
2. db_type() - Perform preliminary non-db specific value checks and conversions. This just returns a string e.g. 'int8range' for BigIntegerRangeField. When addressing just PG this is easy because we are writing for exactly one database, Postgres, and therefore know exactly what the Column type is  we return     
3. get_internal_type() is a 'cheat' to convert to python type directly    
4. get_db_prep_value()  Returns field's value prepared for interacting with the database backend.    
5. get_prep_lookup() Perform preliminary non-db specific lookup checks and conversions.    
6. get_db_prep_lookup()Returns field's value prepared for database lookup.    
7. deconstruct() essentially for adding any kwargs that are custom for this Field type, the deconstruct method will be used for serialization and migrations    


### 2.  The Real Question and Challenge    

That was a nice example of how to write a Field but it was very easy since Decimal is fairly standard   

One of the best paradigms in which to approach this is to present ourselves with the problem of writing the custom Postgres Field.    
 
### 3.  Array Type    

from the Postgres Docs:    

1. Array Type    
PostgreSQL allows columns of a table to be defined as variable-length multidimensional arrays. Arrays of any built-in or user-defined base type, enum type, or composite type can be created. (The type of the array needs to be specified.)     
 
    
    CREATE TABLE sal_emp (
    name            text,
    pay_by_quarter  integer[],
    schedule        text[][]
    );
 
2. What python type does this most closely map to?     
3. Even though we haven’t looked thoroughly at all the attributes of class Field, what additional attributes might we need to add to our subclass’ initializer.    
I’m very tempted to show the entire file but I will truncate to make best brief example    

4. We want to do our logic in the database whenever possible.     

5. We get into Transforms the ArrayLenTransform is the easiest example to look over.    
6. Our ultimate goal again is to return a string that will compile into the SQL that we pass to our Postgres connection    

    @ArrayField.register_lookup
    class ArrayLenTransform(Transform):
        lookup_name = 'len'
        output_field = IntegerField()
        def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)

        return 'array_length(%s, 1)' % lhs, params


### 4.  Range Type

1. Range types are data types representing a range of values of some element type (called the range's subtype).    

    CREATE TYPE floatrange AS RANGE ( 
        subtype = float8, 
        subtype_diff = float8mi 
    ); 
    SELECT '[1.234, 5.678]'::floatrange;

2. Let's not forget about checking the work that psycopg2 does here    
    class psycopg2.extras.Range(lower=None, upper=None, bounds='[)', empty=False)


3. This is similar in that we need a base_field type, but we’re going to find out the psycopg2 has done a lot of this mapping for us and the ore interesting part is actually in the queries

4. We’ll use the Lookup API here:      
    PostgresSimpleLookup(Lookup):
    lhs, lhs_params=self.process_lhs(qn, connection)

### 5.  HStore Type

1. This module implements the hstore data type for storing sets of key/value pairs within a single PostgreSQL value.     

    k => v foo => bar, 
    baz => whatever 
    "1-a" => "anything at all"


### 6. Including Fields in Models

1. We never create a Field in isolation. Each Field is bound to a Model which gets constructed by a giant Meta Class, the BaseModel    


    class SolarPanel(models.Model):
     
        square_feet_access = IntegerRangeField()
        avail_team_period = DateRangeField()  
        types_of_surface = ArrayField( models.CharField(max_length=100, blank=True ),
                           blank = True,
                           null = True,
                         )
        unique_install_parameters = HStoreField()
