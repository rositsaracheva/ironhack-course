
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select customer
from "warehouse"."main"."stg_sales"
where customer is null



  
  
      
    ) dbt_internal_test