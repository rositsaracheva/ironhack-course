
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  SELECT *
FROM "warehouse"."main"."example_model"
WHERE total_with_tax <= 0
  
  
      
    ) dbt_internal_test